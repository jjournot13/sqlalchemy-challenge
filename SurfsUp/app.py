# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Create homepage and list all available routes

@app.route('/')
def homepage():
    return(
        f"Climate Analysis for Hawaii<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query to pull the last 12 months of precipitation data
    query_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23')

    session.close()

    # Create dictionary to store results and return as JSON
    precipitation_data = []
    for date, prcp in query_results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_data.append(precipitation_dict)
    
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query to pull list of stations
    station_results = session.query(Station.station).all()

    session.close()

    # Convert results to list
    stations = list(np.ravel(station_results))

    # Return as JSON
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query to pull list of stations
    active_station_results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Convert results to list
    temperature_observations = list(np.ravel(active_station_results))

    # Return as JSON
    return jsonify(temperature_observations)

@app.route('/api/v1.0/<start>')
def start_date(start):
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query to pull the minimum, maximum and average temperature of precipitation data for range based on a specified start date
    start_date_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
            .filter(Measurement.date >= start).all()

    session.close()

    # Create dictionary to store results and return as JSON
    start_date_data = []
    for min, avg, max in start_date_results:
        start_date_dict = {}
        start_date_dict['Minimum Temperature'] = min
        start_date_dict['Maximum Temperature'] = max
        start_date_dict['Average Temperature'] = avg
        start_date_data.append(start_date_dict)
    
    return jsonify(start_date_data)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query to pull the minimum, maximum and average temperature of precipitation data for range based on a specified start and end dates
    start_end_date_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
            .filter(Measurement.date >= start).filter(Measurement.date >= end).all()

    session.close()

    # Create dictionary to store results and return as JSON
    start_end_date_data = []
    for min, avg, max in start_end_date_results:
        start_end_date_dict = {}
        start_end_date_dict['Minimum Temperature'] = min
        start_end_date_dict['Maximum Temperature'] = max
        start_end_date_dict['Average Temperature'] = avg
        start_end_date_data.append(start_end_date_dict)
    
    return jsonify(start_end_date_data)

if __name__ == "__main__":
    app.run(debug=True)