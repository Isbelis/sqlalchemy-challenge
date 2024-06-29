# Import the dependencies.
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
import numpy as np

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/temp/<start>"
        f"/api/v1.0/stations"
        f"/api?v1.0/temp/<start>/<end>"
    )





@app.route(" /api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a
 ## dictionary using date as the key and prcp as the value
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(measurement.date,measurement.prcp).filter(measurement.date >=year_ago)

    session.close()


    return jsonify(results)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query all stations
    total_stations= session.query(func.count(station.station)).all()

    session.close()

    return jsonify(total_stations)

@app.route(" /api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)
# Query the dates and temperature observations of the most-active station for the previous year of data.
    Results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= year_ago).all()

    session.close()

    return jsonify(Results)


@app.route(" /api/v1.0/<start>") AND (/api/v1.0/<start>/<end>)
def summary_temperature():
lowest_temp, highest_temp, avg_temp = results[0]


# Create our session (link) from Python to the DB
session = Session(engine)

return jsonify(Results)

if __name__ == '__main__':
    app.run(debug=True)