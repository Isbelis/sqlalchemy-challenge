# Import the dependencies.
# Data science
import numpy as np
import pandas as pd
import datetime as dt
#Python SQL toolkit and Ibject realtional mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, func


#Import dependedencies to create app
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################


# Define the database connection URL
# Adjust the path to match the actual location of your SQLite database file
DATABASE_URL = "sqlite:///C:/Users/Isbelis/Documents/Bootcamp/Homework/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite"
# create engine to hawaii.sqlite
engine = create_engine(DATABASE_URL)

# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():

    """List all available api routes."""
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/<start>'>/api/v1.0/&lt;start&gt;</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>/api/v1.0/&lt;start&gt;/&lt;end&gt;</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

# Create session (link) from Python to the DB
    session = Session(engine)

# Find the most recent date in the data set.
    recent_date = "SELECT max(date) FROM measurement"
    with engine.connect() as conn:
     print(conn.execute(text(recent_date)).fetchall())

# Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    precipitation_scores = session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date >=year_ago)

# Close the session
    session.close()
    
# Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {(date, station ): prcp for date, prcp, station in precipitation_scores}

 # Convert the precipitation_dict into a list of dictionaries
    precipitation_list = [{"Date": date,"Station":station, "Precipitation": prcp} for (date,station), prcp in precipitation_dict.items()]

# Print the resulting list of dictionaries
    print(precipitation_list)

# Return the JSON representation of the dictionary
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def station():
 
 # Create session (link) from Python to the DB
 session = Session(engine)

 # Return a JSON list of stations from the dataset
 # Query for all stations

 results = session.query(Station.station).all()

 # Close the session
 session.close()

 # Convert list of tuples into normal list
 station_list = list(np.ravel(results))

 # Convert list of tuple into a list of dictionaries
 station_dict_list = [{'station': station} for station in station_list]
 
 # Print the list of dictionaries
 print(station_dict_list)

 return jsonify(station_dict_list)
 
@app.route("/api/v1.0/tobs")
def temperature():
 # Create our session (link) from Python to the DB
 session = Session(engine)

 #Query the dates and temperature observations of the most-active station for the previous year of data.
 # Find the most recent date in the data set.
 recent_date = "SELECT max(date) FROM Measurement"
 with engine.connect() as conn:
    print(conn.execute(text(recent_date)).fetchall())

# Calculate the date one year from the last date in data set.
 year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
# declarate Most active station
 # Calculate the date 1 year ago from the last data point in the database
 year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query the most active station
  
 counts = session.query(Measurement.station, func.count(Measurement.station)).\
          group_by(Measurement.station).\
          order_by(func.count(Measurement.station).desc())
 counts_df = pd.read_sql(counts.statement, session.bind)  
 
 most_active_station = counts_df.iloc[0,0]

 results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                 filter(Measurement.station == most_active_station).\
                 all()

    # Query the temperature observations of the most active station for the last year
 Results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).\
           filter(Measurement.date >= year_ago).all()

 # Close the session
 session.close()

    # Convert list of tuples into normal list
 tobs_list = list(np.ravel(Results))

 # Convert list of tuple into a list of dictionaries
 keys = ['date', 'tobs']
 tobs_dict_list = [dict(zip(keys, result)) for result in Results]

# Print the list of dictionaries
 print(tobs_dict_list)

 return jsonify(tobs_dict_list)


@app.route("/api/v1.0/<start>")
def star_date_tobs (start):
     # Create our session (link) from Python to the DB
    session = Session(engine)

     # Convert start and end to datetime objects if they are provided
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    except ValueError:
        return jsonify({"error": "start date is required. Replace '<start>' with your preferred start date. The date format should be 'YYYY-MM-DD'."}), 400

    # Define the query to calculate TMIN, TAVG, and TMAX
    query = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*query).filter(Measurement.date >= start_date).all()


    # Close the session
    session.close()

    # Convert the results to a list of dictionaries
    temp_list = []
    for result in results:
        temp_dict = {
            "TMIN": result[0],
            "TAVG": result[1],
            "TMAX": result[2]
        }
        temp_list.append(temp_dict)

    return jsonify(temp_list)


@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):

     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert start and end to datetime objects if they are provided
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end, "%Y-%m-%d") if end else None
    except ValueError:
        return jsonify({"error": "Both start and end dates are required. Replace '<start>/<end>' with your preferred date range. The date format should be 'YYYY-MM-DD/YYYY-MM-DD'."}), 400

    # Define the query to calculate TMIN, TAVG, and TMAX
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if end_date:
        # If an end date is provided, calculate for the date range
        results = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    else:
        # If no end date is provided, calculate for dates greater than or equal to the start date
        results = session.query(*sel).filter(Measurement.date >= start_date).all()

    # Close the session
    session.close()

    # Convert the results to a list of dictionaries
    temp_list = []
    for result in results:
        temp_dict = {
            "TMIN": result[0],
            "TAVG": result[1],
            "TMAX": result[2]
        }
        temp_list.append(temp_dict)

    return jsonify(temp_list)

if __name__ == '__main__':
 app.run(debug=True)