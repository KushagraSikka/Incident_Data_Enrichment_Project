# CIS 6930, Spring 2024 Assignment 2: Augmenting Data

## Introduction

In Assignment 0, we wrote code to extract records from a public police department website. The code we created structures the data in a format helpful for analysis. For further data processing, we need to perform data augmentation on the extracted records, keeping fairness and bias issues in mind.

## Task Overview

This assignment performs data augmentation on records extracted from PDF files available on a public police department's website. The output, tab-separated content, should be printed to stdout. The augmented data will increase the data's usability in subsequent processing stages in the data pipeline.

## Project Overview

This project extracts data from PDF files provided by a public police department, augments it with additional information, and formats it into a structured dataset. The augmentation process involves adding day of the week, time of day, weather conditions, location rank, side of town, nature of the incident, and EMSSTAT status to each incident record. This document provides a detailed explanation of the functions used, the data augmentation process, and the test cases developed to ensure the reliability of the code.

## Detailed Function Descriptions

### `calculate_bearing(lat1, lon1, lat2, lon2)`

Calculates the bearing between two geographic points. Used to determine the "Side of Town" by calculating the direction from the city center to the incident location.

### `get_cardinal_direction(bearing)`

Converts a bearing in degrees to a cardinal direction (N, NE, E, SE, S, SW, W, NW). This helps in categorizing the "Side of Town".

### `get_side_of_town_and_coords(address, gmaps_client)`

Uses Google Maps API to geocode an address to latitude and longitude, then calculates the side of town based on the bearing from the city center.

### `augment_data_with_location_info(dataframe)`

Splits the 'incident_location' column into latitude, longitude, and "Side of Town" for each record in the dataframe.

### `fetch_data_from_db(db_path)`

Connects to a SQLite database to fetch stored incident records.

### `download_pdf(url, local_filename)`

Downloads a PDF from a given URL and saves it locally.

### `read_csv_and_download_pdfs(csv_file_path)`

Reads a CSV file containing URLs, downloads each PDF, and returns a list of local filenames.

### `extract_incidents(pdf_path)`

Extracts incident data from a PDF file and formats it into structured records.

### `createdb(db_filename, resources_dir)`

Creates a SQLite database for storing extracted incident records.

### `fetch_weather_code(latitude, longitude, incident_datetime)`

Fetches the weather condition (WMO code) for a given location and time using the Open-Meteo API.

### `populatedb(db, incidents)`

Inserts incident records into the SQLite database.

### `augment_and_rank_data(dataframe)`

Performs the data augmentation process on the extracted data, including adding weather conditions, calculating location and nature ranks, and determining the EMSSTAT status.

### `check_emsstat(row_index, dataframe)`

Checks if an incident should be marked with an EMSSTAT status based on specific conditions.

### `main(csv_file_path)`

The main function that orchestrates the entire process, from reading URLs, extracting and augmenting data, to exporting the final dataset.

## Test Cases

### `test_calculate_bearing()`

Tests the `calculate_bearing` function with known geographic points to ensure it calculates bearings accurately.

### `test_get_cardinal_direction()`

Ensures the `get_cardinal_direction` function correctly converts bearings to cardinal directions.

### `test_download_pdf()`

Verifies that the `download_pdf` function can successfully download and save PDF files from given URLs.

### `test_fetch_weather_code_success()`

Simulates a successful API call to fetch weather codes, ensuring the function returns the correct code.

### `test_fetch_weather_code_failure()`

Simulates an API call failure to ensure the function handles errors gracefully without crashing.

## Workflow Explanation

### Execution

The code is executable via the command line as follows:

pipenv run python assignment2.py --urls files.csv

`--urls <filename>` points to a file with a list of incident URLs. Each line contains only a URL.

## Data Augmentation Details

The augmented data includes the following columns, sorted by the order in which they appear in the `--urls` file:

- Day of the Week: Numeric value 1-7 (1 for Sunday to 7 for Saturday)
- Time of Day: Numeric code 0 to 24 describing the hour of the incident
- Weather: WMO CODE integer representing weather conditions at the incident location and time
- Location Rank: Integer ranking of the frequency of locations
- Side of Town: One of {N, S, E, W, NW, NE, SW, SE}, determined by orientation from the town's center (35.220833, -97.443611)
- Incident Rank: Integer ranking of the frequency of incident natures
- Nature: Direct text of the Nature from the source record
- EMSSTAT: Boolean indicating specific conditions related to EMS status

## Submission Components

This submission includes the following components:

- **DATASHEET.md**: Follows the template from datasheets for datasets, reviewing fairness and bias considerations.
- **README.md**: (This document) Contains execution instructions, an overview of the task, and additional information on the project setup.
- **COLLABORATORS**: Lists collaborations and contributions to this project.
- **tests/**: Contains pytest files for testing different components of the project.
- **setup.py**: For project setup and pytest integration.

## Known Issues and Assumptions

[NO known issues]

## External Resources

[Used Google GeoCoding API and openmeteo]

---

Developed by Kushagra Sikka - kushagrasikka@gmail.com

University of Florida | CIS 6930 Data Augmentation Project | Spring 2024
