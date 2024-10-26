from urllib.request import Request
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.point import Point
import argparse
import requests
import pandas as pd
import fitz  # PyMuPDF
import os
from datetime import datetime
import sqlite3
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import openmeteo_requests
import numpy as np
import requests_cache
from retry_requests import retry
import googlemaps
from math import radians, cos, sin, atan2, degrees

cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Initialize Google Maps client with your new API key from .env
APIKEY = os.getenv('GOOGLE_MAPS_API_KEY')

gmaps = googlemaps.Client(key=APIKEY)
openmeteo = openmeteo_requests.Client(session=retry_session)


def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Calculate the bearing between two points.
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dLon = lon2 - lon1
    x = cos(lat2) * sin(dLon)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)
    bearing = atan2(x, y)
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360  # Normalize to 0-360
    return bearing


def get_cardinal_direction(bearing):
    """
    Convert bearing to a cardinal direction.
    """
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    ix = round(bearing / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


def get_side_of_town_and_coords(address, gmaps_client):
    """
    Determine the side of town and return both the side and the coordinates.

    Parameters:
    - address (str): The address to geocode.
    - gmaps_client (googlemaps.Client): The Google Maps client instance.

    Returns:
    - tuple: (side_of_town, (latitude, longitude))
    """
    address_with_suffix = f"{address}, Norman, OK"
    geocode_result = gmaps_client.geocode(address_with_suffix)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        bearing = calculate_bearing(35.220833, -97.443611, lat, lng)
        side_of_town = get_cardinal_direction(bearing)
        return side_of_town, (lat, lng)
    else:
        return "Location not found", (None, None)


def augment_data_with_location_info(dataframe):
    # This function splits the Coords column and adds 'Latitude' and 'Longitude' columns
    result = dataframe['incident_location'].apply(
        lambda x: get_side_of_town_and_coords(x, gmaps)).apply(pd.Series)
    dataframe[['Side of Town', 'Coords']] = result
    dataframe[['Latitude', 'Longitude']] = pd.DataFrame(
        dataframe['Coords'].tolist(), index=dataframe.index)
    # Drop Coords column as it's no longer needed
    dataframe.drop(columns=['Coords'], inplace=True)
    return dataframe


def fetch_data_from_db(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Execute query to fetch relevant data
    query = "SELECT incident_time,incident_location,incident_ori,nature FROM incidents"
    dataframe = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    return dataframe


def download_pdf(url, local_filename):
    """Downloads a PDF from a specified URL."""
    # print(f"Attempting to download PDF from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_filename, 'wb') as file:
            file.write(response.content)
        # print(f"PDF saved as {local_filename}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
    return local_filename


def read_csv_and_download_pdfs(csv_file_path):
    """Reads a CSV file to get PDF URLs and downloads each PDF, returning a list of local filenames."""
    urls_df = pd.read_csv(
        csv_file_path, header=None)  # Assuming no header in the CSV
    downloaded_files = []

    for index, row in urls_df.iterrows():
        url = row[0]
        # Naming files as pdf_0.pdf, pdf_1.pdf, etc.
        local_filename = f"pdf_{index}.pdf"
        downloaded_files.append(download_pdf(url, local_filename))

    return downloaded_files


def extract_incidents(pdf_path):
    # Open the PDF file to read its contents
    with fitz.open(pdf_path) as doc:
        all_text = ''.join(page.get_text() for page in doc)

    # Split the combined text into individual lines
    lines = all_text.split('\n')

    incidents = []

    for i in range(len(lines)):
        if 'Date / Time' in lines[i]:
            continue  # Skip header line

        if i + 4 < len(lines) and '/' in lines[i] and ':' in lines[i]:
            edge_case_temp = lines[i + 3].strip()
            if edge_case_temp == "RAMP":
                edge_case_temp = lines[i + 4].strip()
            incident_data = {
                'Date/Time': lines[i].strip(),
                'Incident Number': lines[i + 1].strip(),
                'Location': lines[i + 2].strip(),
                'Nature': edge_case_temp if ':' not in lines[i + 3].strip() else "NULLVALUE",
                'Incident ORI': lines[i + 4].strip()
            }
            incidents.append(incident_data)

    return incidents


def createdb(db_filename="normanpd.db", resources_dir="resources"):
    """
    Create a SQLite database with the necessary table if it doesn't exist, in the parent directory's 'resources' folder.

    Parameters:
    - db_filename: Name of the SQLite database file.
    - resources_dir: Directory name to store the SQLite database file, relative to the parent directory of this script.

    Returns:
    - Connection object to the SQLite database.
    """
    # Calculate the parent directory of this script
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construct the full path to the resources directory in the parent directory
    resources_full_path = os.path.join(parent_dir, resources_dir)

    # Ensure the resources directory exists
    if not os.path.exists(resources_full_path):
        os.makedirs(resources_full_path)

    # Construct the full path to the database file
    db_path = os.path.join(resources_full_path, db_filename)

    # Connect to the SQLite database at the specified path
    try:
        conn = sqlite3.connect(db_path)
        # Create the incidents table if it doesn't exist
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS incidents (
                    incident_time TEXT,
                    incident_number TEXT UNIQUE,
                    incident_location TEXT,
                    nature TEXT,
                    incident_ori TEXT
                );
            ''')
        # print(f"Database created at: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def fetch_weather_code(latitude, longitude, incident_datetime):
    # Format date and hour as required by the API
    date = incident_datetime.strftime('%Y-%m-%d')
    hour = incident_datetime.strftime('%H:%M')

    # API parameters
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date,
        "end_date": date,
        "hourly": "weather_code"
    }

    url = "https://api.open-meteo.com/v1/forecast"

    # Make the API request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Assuming the API provides hourly data in this structure
        hours = data['hourly']['time']
        weather_codes = data['hourly']['weather_code']

        # Find closest hour index
        incident_hour = datetime.strptime(hour, '%H:%M').hour
        hour_indices = [datetime.strptime(
            h, '%Y-%m-%dT%H:%M').hour for h in hours]
        closest_hour_index = (
            np.abs(np.array(hour_indices) - incident_hour)).argmin()

        # Fetch the weather code for the closest hour
        weather_code = weather_codes[closest_hour_index]

        return weather_code
    else:
        print(
            f"Failed to fetch weather data for {latitude}, {longitude} on {date}")
        return None


def populatedb(db, incidents):
    c = db.cursor()
    for incident in incidents:
        # Check if the incident number already exists
        c.execute('SELECT incident_number FROM incidents WHERE incident_number = ?',
                  (incident['Incident Number'],))  # Use 'Incident Number' key
        if c.fetchone() is None:
            # Only insert if the incident does not exist
            c.execute('INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori) VALUES (?,?,?,?,?)',
                      (incident['Date/Time'], incident['Incident Number'], incident['Location'], incident['Nature'], incident['Incident ORI']))  # Use keys accordingly
    db.commit()


def augment_and_rank_data(dataframe):

    dataframe['incident_time'] = pd.to_datetime(dataframe['incident_time'])
    dataframe['Day of the Week'] = dataframe['incident_time'].dt.dayofweek+1
    dataframe['Time of Day'] = dataframe['incident_time'].dt.hour
    dataframe['EMSSTAT'] = [check_emsstat(
        i, dataframe) for i in range(len(dataframe))]
    dataframe['Weather Code'] = dataframe.apply(lambda row: fetch_weather_code(
        row['Latitude'], row['Longitude'], row['incident_time']), axis=1)

    dataframe[['Side of Town', 'Coords']] = dataframe['incident_location'].apply(
        lambda x: get_side_of_town_and_coords(x, gmaps)).apply(pd.Series)
    dataframe[['Latitude', 'Longitude']] = pd.DataFrame(
        dataframe['Coords'].tolist(), index=dataframe.index)
    dataframe.drop('Coords', axis=1, inplace=True)
    # Rank Location
    location_counts = dataframe['incident_location'].value_counts(
    ).reset_index()
    location_counts.columns = ['incident_location', 'Location Count']
    location_counts['Location Rank'] = location_counts['Location Count'].rank(
        method='min', ascending=False).astype(int)

    # Merge location counts and ranks
    dataframe = dataframe.merge(
        location_counts, on='incident_location', how='left')

    # Rank Nature
    nature_counts = dataframe['nature'].value_counts().reset_index()
    nature_counts.columns = ['nature', 'Nature Count']
    nature_counts['Nature Rank'] = nature_counts['Nature Count'].rank(
        method='min', ascending=False).astype(int)

    # Merge nature counts and ranks
    dataframe = dataframe.merge(nature_counts, on='nature', how='left')

    return dataframe


def check_emsstat(row_index, dataframe):
    current_row = dataframe.iloc[row_index]

    # First condition: Check if the current row's incident_ori is "EMSSTAT"
    if current_row['incident_ori'] == 'EMSSTAT':
        return True

    # Define the range for subsequent records to check (next one or two records)
    subsequent_indices = [i for i in range(
        row_index + 1, min(row_index + 3, len(dataframe)))]

    # Second condition: Check subsequent records for the same time and location with "EMSSTAT"
    for i in subsequent_indices:
        next_row = dataframe.iloc[i]
        if current_row['incident_time'] == next_row['incident_time'] and \
           current_row['incident_location'] == next_row['incident_location'] and \
           next_row['incident_ori'] == 'EMSSTAT':
            return True

    return False


def main(csv_file_path):
    db_path = '../resources/normanpd.db'
    # remove database if it exists
    if os.path.exists('../resources/normanpd.db',):
        os.remove('../resources/normanpd.db')
    # Setup the database connection
    db_conn = createdb()

    downloaded_files = read_csv_and_download_pdfs(csv_file_path)
    all_incidents = []
# pdf files are downloaded and incidents are extracted from them
    for pdf_file in downloaded_files:
        # Extract incidents from each PDF
        incidents = extract_incidents(pdf_file)
        all_incidents.extend(incidents)

        os.remove(pdf_file)  # Cleanup after processing
        # print(f"Removed {pdf_file}")
# populating the database with the extracted incidents
    populatedb(db_conn, all_incidents)
    location_df = fetch_data_from_db(db_path)
    dataframe = fetch_data_from_db(db_path)
    dataframe = augment_data_with_location_info(dataframe)

    augmented_ranked_data = augment_and_rank_data(dataframe)
    dataframe.sort_values(
        by=['incident_time', 'incident_location'], inplace=True)

    # Selecting the required columns
    final_data = augmented_ranked_data[[
        'Day of the Week', 'Time of Day', 'Weather Code', 'Location Rank', 'Side of Town', 'Nature Rank', 'nature', 'EMSSTAT'
    ]]

    # Sort by Day of the Week and Time of Day for readability
    final_data_sorted = final_data.sort_values(
        by=['Day of the Week', 'Time of Day'])
# printing the final data
    print(final_data_sorted)

    db_conn.close()  # Close the database connection
# exporting the final data to a csv file
    output_filename = "augmented_data.csv"
    final_data_sorted.to_csv("augmented_data.csv", index=False)
    print("Data successfully exported to augmented_data.csv")

    db_conn.close()  # Close the database connection


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process PDF URLs for incident data and store in database.')
    parser.add_argument('--urls', type=str, required=True,
                        help='CSV file containing the URLs.')
    args = parser.parse_args()
# taking arguments from the command line
    main(args.urls)
