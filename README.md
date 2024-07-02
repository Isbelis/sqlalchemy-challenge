# sqlalchemy-challenge -Climate Analysis and Flask API Design for Honolulu, Hawaii

## Overview
In this project, I conducted a comprehensive climate analysis of Honolulu, Hawaii using Python, SQLAlchemy, Pandas, and Matplotlib. The analysis provides insights and data that can aid in trip planning. Additionally, a Flask API was developed to allow easy access to the analyzed climate data.

## Project Structure

### Part 1: Analyze and Explore the Climate Data
Utilized climate_analysis.ipynb for data exploration and analysis.
Used hawaii.sqlite database with SQLAlchemy ORM queries.
Performed precipitation and station analysis.

### Part 2: Design Your Climate App
Implemented a Flask API (app.py) based on the analysis.
Provided routes for retrieving precipitation, station, and temperature data.

## Part 1: Analyze and Explore the Climate Data

### Precipitation Analysis

#### 1. Retrieve Data
- Found the most recent date in the dataset.
- Queried the previous 12 months of precipitation data.

#### 2. Data Preparation
- Selected date and prcp columns.
- Loaded query results into a Pandas DataFrame.
- Sorted DataFrame values by date.

#### 3. Visualization
- Plotted precipitation data using Matplotlib.

#### 4. Summary Statistics
- Calculated and printed summary statistics using Pandas.

### Station Analysis
#### 1. Total Stations
- Designed a query to calculate the total number of stations.

#### 2. Most Active Stations
- Identified stations with the most observations.
- Determined station with the highest number of observations.

#### 3. Temperature Analysis
- Calculated lowest, highest, and average temperatures for the most active station.

#### 4. Temperature Observation (tobs) Analysis
- Retrieved previous 12 months of tobs data.
- Plotted TOBS data as a histogram with bins=12.

### Part 2: Design Your Climate App
### Flask API Routes

#### 1. Homepage Route
 - Route: '/'
 - Functionality: Lists all available routes.

#### 2. Precipitation Route
- Route: '/api/v1.0/precipitation'
- Functionality: Returns last 12 months of precipitation data as JSON.

#### 3. Stations Route
- Route: '/api/v1.0/stations'
- Functionality: Returns JSON list of stations from the dataset.

#### 4. Temperature Observations Route
- Route: '/api/v1.0/tobs'
- Functionality: Returns temperature observations for the previous year from the most active station.

#### 5. Temperature Start Date Route
- Routes: '/api/v1.0/<start>'
- Functionality: Returns minimum, average, and maximum temperatures for specified start date.
#### 6. Temperature Start and End Date Route
- Routes: '/api/v1.0/<start>/<end>'
- Functionality: Returns minimum, average, and maximum temperatures for specified start-end range.

## Folder Structure
### SurfsUp/
#### files
1. 'climate_analysis.ipynb': Jupyter notebook for Part 1 analysis.
2. 'app.py': Flask application for Part 2 API.
#### folders
1. "Resources/"
    - hawaii.sqlite: SQLite database containing climate data.
    - CSV files or other resources used in analysis.
2. "Output/"
    - Contains images and graphs generated during analysis and API demonstration.


### Future Enhancements
- Expand API functionality with additional endpoints for more detailed climate data.
- Improve UI with interactive visualizations and user-friendly features.