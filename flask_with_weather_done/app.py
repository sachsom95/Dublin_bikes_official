from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json

with open('dublin.json') as f:
    json_dict = json.load(f)
    # for i in json_dict:
    #     print("lat :",i['latitude'],"lon : ",i['longitude'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''


def connectMysql():
    sql_hostname = 'localhost'
    sql_username = 'root'
    sql_password = 'nyj19971023'
    sql_main_database = 'db1'
    sql_port = 3306
    connection = pymysql.connect(host=sql_hostname,
                                 user=sql_username,
                                 passwd=sql_password,
                                 db=sql_main_database,
                                 port=sql_port)
    cursor = connection.cursor()

    # for i in station_list:
    # for j in i:
    #     print(j, ":", i[j], end=" ")
    # print("")

    # station_number = i["number"]
    # station_name = i["name"]
    # address = i["address"]
    # address.replace('\r', '').replace('\n', '').replace('\t', '').replace('\ ', '')
    # position_lat = i["position"]["lat"]
    # position_lng = i["position"]["lng"]
    # banking = i["banking"]
    # bonus = i["bonus"]
    # bike_stands = i["bike_stands"]
    # available_stands = i["available_bike_stands"]
    # available_bikes = i["available_bikes"]
    # status = i["status"]
    # last_update = i["last_update"]
    # sql = 'insert into Bike.realtime_data (Update_time,Station_number, Station_name, Address, Latitude, Longitude, Banking, Bonus, Bike_stands, Available_bike_stands, Available_bikes, Station_status, Last_update) value ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (structure_time, station_number, station_name, address, position_lat, position_lng, banking, bonus, bike_stands, available_stands, available_bikes, status, last_update)
    sql = 'select * from db1.bike_station'

    # try:
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    # except:
    # connection.rollback()

    connection.close()

    return result

@app.route('/')
@app.route('/home')
def hello_world():
    u = connectMysql()
    for i in u:
        print('Time : ',i)

    return render_template('index_w.html',stations = json_dict,realtime_data = u)

@app.route('/ajax',methods=['POST','GET'])
def index():
    u = connectMysql()
    number = request.args.get("number")
    for i in u:
        if str(i[1])==number:
            result = {"bike_available":i[10],"station":i[2],"status":i[11],"stands_available":i[9]}
            print(type(result),result)
    return json.dumps(result)

if __name__ == '__main__':
    app.run(
        debug=True
    )