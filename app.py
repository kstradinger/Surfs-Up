import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Station = Base.classes.station

app = Flask(__name__)



@app.route("/")
def welcome():
    """Welcome to Hawaii"""
    return (
        f"How can I help<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation Info"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Measurement.prcp, Measurement.date).\
filter(Measurement.date > '2016-08-22').all()

    
    precipitation = list(np.ravel(results))

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """ Weather Data Stations on Hawaii  """
    # Query all Stations
    session = Session(engine)
    results = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperatures():
    """ Temperature Data for most active station """
    # Query all Stations
    session = Session(engine)
    temp = session.query(Measurement.tobs).\
    filter(Measurement.station == max_station).\
    order_by(Measurement.tobs)

    temperaturess = list(np.ravel(temp))

    return jsonify(stations)


if __name__ == '__main__':
    app.run(debug=True)

