from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pyodbc
import config


app = Flask(__name__)

def read_query_sql(script):
    '''Define function to read SQL query'''
    conn = pyodbc.connect('Driver={SQL Server};'
                        f'Server={config.database["server"]};'
                        f'Database={config.database["database"]};'
                        f'UID={config.database["username"]};'
                        f'PWD={config.database["password"]}'
                          )
    dfs = pd.read_sql_query(script, conn, index_col=None,parse_dates=None)
    conn.close()
    return dfs

def get_country(lat1,lon1):
    # import module
    from geopy.geocoders import Nominatim
    # initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((lat1,lon1))
    address = location.raw['address']

    # get country
    return address.get('country', '')

@app.route("/")
def index():
    return "<p>Welcome to weather checker</p>"


@app.route("/temperature")    
def get_temperature():
    
    with open('models\\temperature.sql','r') as f:
        script = f.read()
    if not request.args.get('pageNum'):
        offset = 0
    else:
        offset = int(request.args.get('pageNum'))*100    
    df  = read_query_sql(script.format(offset))
    
    if df.shape[0]==100:
        return jsonify({"status":"ok", "data": df.to_dict(orient='records'),
        "nextURL":request.base_url+"?pageNum="+str((offset//100)+1)})
    else:
        return jsonify({"status":"ok", "data": df.to_dict(orient='records')})        


@app.route("/stations")    
def get_stations():
    
    with open('models\\stations.sql','r') as f:
        script = f.read()
    if not request.args.get('pageNum'):
        offset = 0
    else:
        offset = int(request.args.get('pageNum'))*100    
    df  = read_query_sql(script.format(offset))
    
    if df.shape[0]==100:
        return jsonify({"status":"ok", "data": df.to_dict(orient='records'),
        "nextURL":request.base_url+"?pageNum="+str((offset//100)+1)})
    else:
        return jsonify({"status":"ok", "data": df.to_dict(orient='records')})   


@app.route("/getTempByLocation", methods=['POST'])    
def getTempByLocation():
    data = request.get_json()
    lat1 = data['lat1']
    lat2 = data['lat2']
    lon1 = data['lon1']
    lon2 = data['lon2']
    startYear = data['startYear']
    endYear = data['endYear']
    
    with open('models\\getTempByLocation.sql','r') as f:
        script = f.read()
    if not request.args.get('pageNum'):
        offset = 0
    else:
        offset = int(request.args.get('pageNum'))*100         
    df  = read_query_sql(script.format(lat1,lat2,lon1,lon2,startYear,endYear,offset))
    country = get_country(lat1,lon1)
    if df.shape[0]==100:
        return jsonify({"status":"ok", "data": df.to_dict(orient='records'),"country":country,
        "nextURL":request.base_url+"?pageNum="+str((offset//100)+1)})    
    else:
        return jsonify({"status":"ok", "data": df.to_dict(orient='records'),"country":country})    