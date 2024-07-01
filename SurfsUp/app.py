# Import the dependencies.
# Data science
import numpy as np
import pandas as pd
import datetime as dt
#Python SQL toolkit and Ibject realtional mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func
#Import dependedencies to create app
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
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
 precipitation_scores = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >=year_ago)

# Close the session
 session.close()
    
# Convert the query results to a dictionary using date as the key and prcp as the value
 precipitation_dict = {date: prcp for date, prcp in precipitation_scores}
    
# Return the JSON representation of the dictionary
 return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def station():
 
 # Create session (link) from Python to the DB
 session = Session(engine)
 # Return a JSON list of stations from the dataset
  # Query for all stations
 results = session.query(Station.station).all()
 session.close()
    # Convert list of tuples into normal list
 station_list = list(np.ravel(results))

 return jsonify(station_list)
 
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

    # Convert list of tuples into normal list
 tobs_list = list(np.ravel(Results))

 return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start=None, end=None):


    # Define the query to calculate TMIN, TAVG, and TMAX
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if end:
            # If an end date is provided, calculate for the date range
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        # If no end date is provided, calculate for dates greater than or equal to the start date
        results = session.query(*sel).filter(Measurement.date >= start).all()

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