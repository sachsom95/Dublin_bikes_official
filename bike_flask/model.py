from sqlalchemy import *
from flask import json

def get_conn():
    db_uri = "mysql://root:lhb280214@localhost:3306/dublin_bike"
    engine = create_engine(db_uri)
    conn = engine.connect()
    return conn

def update():
    conn = get_conn()
    sql = ""

def station_init():
    conn = get_conn()
    sql = "select number, name, address, latitude, longitude from position"
    result = conn.execute(sql)
    station_list = []
    for row in result:
        single_station = {}
        for each in row:
            single_station['number'] = row['number']
            single_station['name'] = row['name']
            single_station['address'] = row['address']
            single_station['latitude'] = float(row['latitude'])
            single_station['longitude'] = float(row['longitude'])
        station_list.append(single_station)
    return json.dumps(station_list)
# a = station_init()
# print(a)

def get_station_info(lat,lng):
    # db_uri = "mysql://root:dublinbikes@dublin.cwl57f78tvsl.us-east-1.rds.amazonaws.com:3306/bikes"
    db_uri = "mysql://root:lhb280214@localhost:3306/dublin_bike"
    engine = create_engine(db_uri)
    conn = engine.connect()
    sql = "select bike_stands, available_bike_stands, available_bikes, status " \
          "from status " \
          "join position " \
          "using (number) " \
          "where latitude = " + str(lat) + " and longitude = " + str(lng) + ";"
    result = conn.execute(sql)
    station_dict = {}
    for row in result:
        station_dict['bike_stands'] = row['bike_stands']
        station_dict['available_bike_stands'] = row['available_bike_stands']
        station_dict['available_bikes'] = row['available_bikes']
        station_dict['status'] = row['status']
    return json.dumps(station_dict)



# for r in result:
#   print(r)
#   print(type(r))

# result_list = result.fetchall()
# print("set is", result_list)
# print(type(result_list[0]))
