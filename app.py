import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Station = Base.classes.stations

# Create our session (link) from Python to the DB
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
    """List of all returnable API routes."""
    return(
        f"Available Routes:<br/>"
        f"(Note: Most recent available date is 2017-08-23 while the latest is 2010-01-01).<br/>"

        f"/api/v1.0/precipitation<br/>"
        f"- Query dates and temperature from the last year. <br/>"

        f"/api/v1.0/stations<br/>"
        f"- Returns a json list of stations. <br/>"

        f"/api/v1.0/tobs<br/>"
        f"- Returns list of Temperature Observations(tobs) for previous year. <br/>"

        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"- Returns an Average, Max, and Min temperature for given date.<br/>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"- Returns an Average, Max, and Min temperature for given period.<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return Dates and Temp from the last year."""
    results = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.date <= "2016-01-01", Measurements.date >= "2016-01-01").\
        all()

    #create the JSON objects
    precipitation_list = [results]

    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(Station.name, Station.station, Station.elevation).all()

    #create dictionary for JSON
    station_list = []
    for result in results:
        row = {}
        row['name'] = result[0]
        row['station'] = result[1]
        row['elevation'] = result[2]
        station_list.append(row)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_obs():
    """Return a list of tobs for the previous year"""
    results = session.query(Station.name, Measurements.date, Measurements.tobs).\
        filter(Measurements.date >= "2016-01-01", Measurements.date <= "2017-01-01").\
        all()

    #create json, perhaps use dictionary
    tobs_list = []
    for result in results:
        row = {}
        row["Date"] = result[1]
        row["Station"] = result[0]
        row["Temperature"] = int(result[2])
        tobs_list.append(row)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<date>/')
def given_date(date):
    """Return the average temp, max temp, and min temp for the date"""
    results = session.query(Measurements.date, func.avg(Measurements.tobs), func.max(Measurements.tobs), func.min(Measurement.tobs)).\
        filter(Measurements.date == date).all()

#Create JSON
    data_list = []
    for result in results:
        row = {}
        row['Date'] = result[0]
        row['Average Temperature'] = float(result[1])
        row['Highest Temperature'] = float(result[2])
        row['Lowest Temperature'] = float(result[3])
        data_list.append(row)

    return jsonify(data_list)

@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    """Return the avg, max, min, temp over a specific time period"""
    results = session.query(func.avg(Measurements.tobs), func.max(Measurements.tobs), func.min(Measurements.tobs)).\
        filter(Measurements.date >= start_date, Measurements.date <= end_date).all()

    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Highest Temperature"] = float(result[1])
        row["Lowest Temperature"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)