# Import the dependencies.
import numpy as np

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

Base.prepare(autoload_with = engine)
# Save references to each table
Station = Base.classes.station

Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        f"Available Routes: <br/> "
        f"/api/v1.0/precipitation <br/> "
        f"/api/v1.0/stations <br/> "
        f"/api/v1.0/tobs <br/> "
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
   
    prcp_q = session.query(Measurement.prcp,Measurement.date).all()
    session.close()
    
    prcp_values = []
    for prcp,date in prcp_q:
        prcp_dict = {}
        prcp_dict['Precipitation'] = prcp
        prcp_dict['Date'] = date
        prcp_values.append(prcp_dict)
    return jsonify(prcp_values)

@app.route("/api/v1.0/stations")
def station(): 
    session=Session(engine)
    station_q = session.query(Station.id,Station.station,Station.latitude,Station.longitude).all()
    session.close()

    station_values = []
    for id,station,latitude,longitude in station_q:
        station_dict = {}
        station_dict['id']=id
        station_dict['station']=station
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_values.append(station_dict)

    return jsonify(station_values)
    
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    tobs_q = session.query(Measurement.tobs,Measurement.date),all()
    session.close()

    tobs_value = []
    for tobs,date in tobs_q:
        tobs_dict = {}
        tobs_dict['tobs'] = tobs
        tobs_dict['date'] = date
        tobs_value.append(tobs_dict)

    return jsonify(tobs_values)

@app.route("/api/v1.0/<start>")
def trip1(start,end_date = '2017-08-23'):

    session=Session(engine)

    start_date_tobs_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()
    session.close()

    start_date_tobs_values = []
    for min, avg, max in start_date_tobs_results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min"] = min
        start_date_tobs_dict["average"] = avg
        start_date_tobs_dict["max"] = max
        start_date_tobs_values.append(start_date_tobs_dict)

    return jsonify(start_date_tobs_values)

@app.route("/api/v1.0/<start>/<end>")
def trip2(start_date, end_date='2017-08-23'):
   
    session = Session(engine)
    query_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    trip_value = []
    for min, avg, max in query_result:
        trip_dict = {}
        trip_dict["Min"] = min
        trip_dict["Average"] = avg
        trip_dict["Max"] = max
        trip_value.append(trip_dict)

    
    return jsonify(trip_value)


if __name__ == '__main__':
    app.run(debug=True)
