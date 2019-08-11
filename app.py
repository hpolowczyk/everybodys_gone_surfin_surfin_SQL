import numpy as np
import datetime as dt
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Reflect Database into ORM class
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Database into ORM class
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create references to the table
Measurement = Base.classes.measurement
Station = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Below are all the available api routes."""
    return (
        f"<strong>Available Routes:</strong><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"<u>Single Date Temperature Stats</u><br/>"
        f"Enter date in the following format YYYY-MM-DD<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"<u>Date Range Temperature Stats</u><br/>"
        f"Enter dates in the following format YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary with date keys and precipitation values"""
    # Query all dates and prcp values
    session = Session(engine)
    prcp_by_date = session.query(Measurement.date,func.sum(Measurement.prcp)).\
                group_by(Measurement.date).all()

    # Create a dictionary with date as keys and total precipitation on that date as values
    all_prcp = []
    for date,prcp in prcp_by_date:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the stations"""
    # Query all stations
    session = Session(engine)
    stations = session.query(Station.station).group_by(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations for the past year"""
    session = Session(engine)
    # Retrieve all date values from latest to earliest (descending order)
    dates = session.query(Measurement.date).order_by(Measurement.date.desc()).all()
    # Create reference variables for the earliest and latest dates
    latest_date = datetime.strptime(dates[0][0], '%Y-%m-%d')
    # Query date and tobs for the previous year
    tobs = session.query(Measurement.date,func.avg(Measurement.tobs)).\
        filter(Measurement.date >= latest_date - dt.timedelta(days=366)).\
        group_by(Measurement.date).order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(tobs))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def date(start):
    """Return list of minimum temp, average temp and max temp for a given start date"""
    session = Session(engine)
    # Query temperature stats (i.e. minimum, average, maximum) for all dates greater than and equal to the start date
    date_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    # Convert list of tuples into normal list
    date_lst = list(np.ravel(date_stats))

    # If the first element is null, then return an error statement
    if date_lst[0] is None:
        return jsonify({"error": f"Temperature stats for {start} was not found. Please choose an earlier date."}), 404
    return jsonify(date_lst)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):
    """Return list of minimum temp, average temp and max temp for a given start and end dates"""
    session = Session(engine)
    # Query temperature stats (i.e. minimum, average, maximum) for all dates between the start and end date (inclusive)
    range_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    range_lst = list(np.ravel(range_stats))

    # If the first element is null, then return an error statement
    if range_lst[0] is None:
        return jsonify({"error": f"Temperature stats for date range {start} to {end} was not found. Please choose another date range."}), 404
    return jsonify(range_lst) 
    
if __name__ == '__main__':
    app.run(debug=True)