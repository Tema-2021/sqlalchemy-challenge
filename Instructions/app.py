import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import Flask
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite") 

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Homepage():
    #"""List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#################################################
# Precipitation
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
#"""Return a list of all precipitation measurement"""
    # Convert the query results to a dictionary using date as the key and prcp as the value    
    # Return the JSON representation of your dictionary.
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        all()
    results

    session.close()
# Convert list of tuples into a dictionary
    all_ppt= []
    for date, prcp, in results:
        # date=each_row [1]
        # prcp=each_row[2]
        #all_ppt[date]=prcp
        ppt_dict = {}
        ppt_dict["date"] = prcp
        # ppt_dict["prcp"] = prcp
        all_ppt.append(ppt_dict)
        all_ppt = list(np.ravel(results))

    return jsonify(all_ppt)

#################################################
# Stations
#################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of stations from the dataset
    active_stations=session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).all()
    active_stations

    session.close()

    # Convert list of tuples into a normal list
    all_stations = list(np.ravel(active_stations))

    return jsonify(all_stations)

#################################################
# Tobs
#################################################
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_active=session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).first()
    most_active

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
    session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
       filter(Measurement.station=='USC00519281').all()

    station_results = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date >= last_year).all()
    station_results

    session.close()

    # Convert list of tuples into a normal list
    most_active_station = list(np.ravel(most_active))
    all_year = list(np.ravel(station_results))

    return jsonify(most_active_station, all_year)

#################################################
# Start
#################################################
@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)  

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    tobs_start = session.query(Measurement.date, func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
       filter(Measurement.date >= '2016, 8, 23').\
       group_by(Measurement.date).\
       order_by(Measurement.date).\
       all()
    tobs_start

    session.close()

    # Convert list of tuples into a normal list
    start_tobs = list(np.ravel(tobs_start))

    return jsonify(start_tobs)


if __name__ == '__main__':
    app.run(debug=True)

# Refer to HWapp.py for "api/v1.0/<start>/<end>" analysis