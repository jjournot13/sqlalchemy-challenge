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

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
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
def welcome();
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
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    query_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago)

    session.close()

    # Create dictionary to store results and return as JSON
    precipitation_data = []
    for data, prcp in query_results:
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
    stations = session.query(Measurement.station).distinct().all()

    session.close()

    # Create dictionary to store results and return as JSON
    return jsonify(stations)


if __name__ == "__main__":
    app.run(debug=True)