## Datasheet for Dataset: Augmented Police Incident Reports

## Dataset Information Dataset Name:
#Augmented Police Incident Reports

# Description:
This dataset contains augmented data extracted from public police department PDF reports. The augmentation includes additional derived attributes like the day of the week, time of day, weather conditions, location rank, side of town, incident rank, nature of the incident, and EMS status.

# Version:
1.0
#Creation Date:
April 6, 2024

# Last Updated:

April 6, 2024
# Data Source:

Public police department PDF reports.
Data Augmentation Details:
The data augmentation process includes extracting URLs from PDF files, deriving additional attributes such as day of the week, time of day, weather conditions (using WMO CODE), location and incident frequency ranking, side of town (using geospatial analysis), nature of the incident, and EMS status. The weather data is fetched using the Open-Meteo API based on the incident's time and location.

## Introduction

In Assignment 0, we wrote code to extract records from a public police department website. The code we created structures the data in a format helpful for analysis. For further data processing, we need to perform data augmentation on the extracted records, keeping fairness and bias issues in mind.

## Task Overview

This assignment performs data augmentation on records extracted from PDF files available on a public police department's website. The output, tab-separated content, should be printed to stdout. The augmented data will increase the data's usability in subsequent processing stages in the data pipeline.

## Project Overview

This project extracts data from PDF files provided by a public police department, augments it with additional information, and formats it into a structured dataset. The augmentation process involves adding day of the week, time of day, weather conditions, location rank, side of town, nature of the incident, and EMSSTAT status to each incident record. This document provides a detailed explanation of the functions used, the data augmentation process, and the test cases developed to ensure the reliability of the code.


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

## Motivation

- **Purpose:** The dataset was created to enhance the usability of police incident data extracted from PDF reports by adding additional attributes such as day of the week, time of day, weather conditions, location rank, side of town, incident rank, nature of the incident, and EMS status.
- **Creators:** Kushagra Sikka.
- **Funding:** The dataset creation was not funded externally.
- **Comments:** No additional comments.

## Composition

- **Instances:** The dataset consists of structured records representing police incident reports.
- **Total Instances:** Variable based on the input CSV file.
- **Sample or Full Set:** The dataset is a sample extracted from a larger set of police incident reports available on public police department websites.
- **Data Fields:** Each instance includes attributes such as day of the week, time of day, weather, location rank, side of town, incident rank, nature of the incident, and EMS status.
- **Label or Target:** Not applicable.
- **Missing Information:** No information is intentionally missing from the instances.
- **Explicit Relationships:** Not applicable.
- **Data Splits:** Not applicable.
- **Errors or Noise:** No significant errors, noise, or redundancies in the dataset.

## Collection Process

- **Data Acquisition:** The dataset is collected from publicly available police department PDF reports using automated extraction methods.
- **Mechanisms:** Data extraction is performed using custom Python scripts.
- **Sampling Strategy:** Not applicable.
- **Participants:** The dataset creator, Kushagra Sikka, was involved in the data collection process.
- **Timeframe:** Data collection occurred during the extraction process.
- **Ethical Review:** No formal ethical review was conducted.

## Preprocessing/Cleaning/Labeling

- **Preprocessing:** Data cleaning involves extracting relevant information from PDF reports and structuring it into a tabular format.
- **Raw Data:** Only preprocessed data is included in the dataset.
- **Availability:** Preprocessing scripts are available upon request.

## Uses

- **Prior Usage:** The dataset has been used for data analysis and augmentation tasks.
- **Repository:** No specific repository links are provided.
- **Potential Uses:** The dataset can be used for further analysis, research, and application development in law enforcement and public safety domains.

## Distribution

- **Third-Party Distribution:** Distribution to third parties is not currently planned.
- **Distribution Method:** The dataset is distributed as CSV files.
- **DOI:** No DOI is assigned to the dataset.
- **Distribution Timing:** The dataset is available upon request.
- **Licensing:** The dataset is provided under a standard academic license.
- **External Restrictions:** No external restrictions are associated with the dataset.
- **Export Controls:** No export controls apply to the dataset.

## Maintenance

- **Support/Hosting:** The dataset is maintained by the dataset creator.
- **Contact Information:** Contact Kushagra Sikka for inquiries or support.
- **Erratum:** No errata exist for the dataset.
- **Updates:** Updates to the dataset will be communicated directly to users.

## Known Issues and Assumptions

[NO known issues]

## External Resources

[Used Google GeoCoding API and openmeteo]

---

Developed by Kushagra Sikka - kushagrasikka@gmail.com

University of Florida | CIS 6930 Data Augmentation Project | Spring 2024
