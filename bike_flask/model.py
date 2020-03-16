from sqlalchemy import *
from flask import json

def get_station_info(lat,lng):
    db_uri = "mysql://root:lhb280214@localhost:3306/dublin_bike"
    engine = create_engine(db_uri)
    conn = engine.connect()
# metadata = MetaData()
# inspector = inspect(engine)
# print(inspector.get_table_names()) # 获取数据库的所有table信息
# print(inspector.get_columns('position'))  #获取某个table的所有column
# print("*********")
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
