import numpy as np

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary with date keys and precipitation values"""
    # Query all dates and prcp values
    session = Session(engine)
    results = session.query(Measurement.date,func.sum(Measurement.prcp)).group_by(Measurement.date).all()

    # Create a dictionary with date as keys and prcp as values
    prcp_by_date = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_by_date.append(prcp_dict)

    return jsonify(prcp_by_date)


@app.route("/api/v1.0/passengers")
def precipitation2():
    """Return a dictionary with date keys and precipitation values"""
    # Query all dates and prcp values
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).group_by(Measurement.date).all()

    # Create a dictionary with date as keys and prcp as values
    prcp_by_date = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_by_date.append(prcp_dict)

    return jsonify(prcp_by_date)


if __name__ == '__main__':
    app.run(debug=True)
