# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


from flask import Flask, jsonify
app = Flask(__name__)


# home
@app.route("/")
def home():
    home_string = '''
    Welcome to my API version 1.0 <br/>
    <br/>
    Available Routes: <br/>
    /api/v1.0/precipitation <br/>
    /api/v1.0/stations <br/>
    /api/v1.0/tobs <br/>
    /api/v1.0/[start_date format:yyyy-mm-dd] <br/>
    /api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]
    '''
    return home_string



# precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    
# create session from python to database    
    session = Session(engine)

# convert query results to a dictionary using `date` as key and `prcp` as value
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").all()

    total_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
               
        total_prcp.append(prcp_dict)

# end session
    session.close()

# return the json representation of dictionary
    return jsonify(total_prcp)



# stations
@app.route("/api/v1.0/stations")
def stations():

# create session from python to database    
    session = Session(engine)

    # query a list of all stations
    results = session.query(Station.station).all()

    # convert list of tuples into normal list
    total_stations = list(np.ravel(results))

# end session
    session.close()

# return the json representation of dictionary
    return jsonify(total_stations)



# tobs
@app.route("/api/v1.0/tobs")
def tobs():

# create session from python to database    
    session = Session(engine)

    # query dates and temps of the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= "2016-08-24").\
        filter(Measurement.date <= "2017-08-23").all()

# convert query results to a dictionary    
    station_tobs = []
    for date, tobs in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['tobs'] = tobs
               
        station_tobs.append(prcp_dict)

# end session
    session.close()

# return the json representation of dictionary
    return jsonify(station_tobs)


# start_date
@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    
    # create session from python to database    
    session = Session(engine)

    # query list of min, max, avg for a start date
    results = session.query(func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

# convert query results to a dictionary    
    start_date_tobs = []
    for min, max, avg in results:
        start_date_dict = {}
        start_date_dict['min'] = min
        start_date_dict['max'] = max
        start_date_dict['avg'] = avg
               
        start_date_tobs.append(start_date_dict)

# end session
    session.close()

# return the json representation of dictionary
    return jsonify(start_date_tobs)



# start_date, end_date
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    
    # create session from python to database    
    session = Session(engine)

    # query list of min, max, avg for a start date
    results = session.query(func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

# convert query results to a dictionary    
    start_end_tobs = []
    for min, max, avg in results:
        start_end_dict = {}
        start_end_dict['min'] = min
        start_end_dict['max'] = max
        start_end_dict['avg'] = avg
               
        start_end_tobs.append(start_end_dict)

# end session
    session.close()

# return the json representation of dictionary
    return jsonify(start_end_tobs)


if __name__ == "__main__":
    app.run(debug=True)