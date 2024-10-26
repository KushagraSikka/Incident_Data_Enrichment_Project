import streamlit as st
import pandas as pd
import altair as alt
import subprocess
import json
import os
from dotenv import load_dotenv  # to load environment variables from a .env file

# Load environment variables
load_dotenv()  # load from .env file
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

if GOOGLE_MAPS_API_KEY is None:
    st.error("Error: GOOGLE_MAPS_API_KEY not found in environment variables.")


def get_augmented_data(url_file_path):
    try:
        # Run your existing python script to generate data.  Error handling crucial here!
        process = subprocess.run(['pipenv', 'run', 'python', '../assignment2/assignment2.py',
                                 '--urls', url_file_path], capture_output=True, text=True, check=True)

        # Reads the file created by assignment2.py
        return pd.read_csv("augmented_data.csv")
    except subprocess.CalledProcessError as e:
        st.error(f"Error running data augmentation script: {e.stderr}")
        return None
    except FileNotFoundError:
        st.error(f"Error: Could not find the data augmentation script or the output file. Check paths and ensure the backend script ran successfully.")
        return None


st.title("Police Incident Data Augmentation & Visualization")

url_file_path = "files.csv"  # Path to your CSV of URLs

augmented_df = get_augmented_data(url_file_path)

if augmented_df is None:
    st.error("Failed to generate augmented data.")
else:
    st.subheader("Augmented Data (Sample)")
    st.dataframe(augmented_df.head(10))  # Show only the first 10 rows

    st.subheader("Filter Data")
    selected_day = st.selectbox(
        "Select Day of the Week (1-7)", augmented_df['Day of the Week'].unique())
    filtered_df = augmented_df[augmented_df['Day of the Week'] == selected_day]

    st.subheader("Visualizations")

    # Bar chart of incident types
    incident_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X('nature:N', title='Incident Nature'),
        y=alt.Y('count()', title='Number of Incidents')
    ).properties(
        title='Incident Nature Distribution'
    )
    st.altair_chart(incident_chart, use_container_width=True)

    # Scatter plot of Location Rank vs. Time of Day
    scatter_chart = alt.Chart(filtered_df).mark_circle().encode(
        x='Time of Day:Q',
        y='Location Rank:Q',
        tooltip=['nature', 'incident_location', 'Time of Day', 'Location Rank']
    ).properties(
        title="Location Rank vs Time of Day"
    )
    st.altair_chart(scatter_chart, use_container_width=True)
