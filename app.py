from flask import Flask,render_template,request, json
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json
import ML
import pandas as pd
from sshtunnel import SSHTunnelForwarder
import datetime

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


def getForecast():
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

    sql = 'select * from db1.forecast'

    # try:
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    # except:
    # connection.rollback()

    connection.close()

    return result

def getHistoricalData(start_station_number,destination_station_number,hour):
    with SSHTunnelForwarder(
            ("ec2-3-80-6-206.compute-1.amazonaws.com",22),  # B机器的配置
            ssh_pkey="/Users/freddie/Downloads/asw-education-key.pem",
            ssh_username="ec2-user",
            remote_bind_address=("tutorial-db-instance.cf2q3iwaca38.us-east-1.rds.amazonaws.com", 3306)) as server:  # A机器的配置

        db_connect = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                     port=server.local_bind_port,
                                     user="tutorial_user",
                                     passwd="nyj19971023",
                                     db="Bike")

        cur = db_connect.cursor()

        # sql1 = '''SELECT *
        #         from Bike.bike_station
        #         where date_sub(curdate(),INTERVAL 7 DAY) <= DATE(STR_TO_DATE(Update_time, '%a %b %e %H:%i:%s %Y'))
        #         and Station_number = "%s"
        #         and Hour(STR_TO_DATE(Update_time, '%a %b %e %H:%i:%s %Y')) = "%s"
        #         and minute(STR_TO_DATE(Update_time, '%a %b %e %H:%i:%s %Y'))=0;
        # '''%(start_station_number,hour)
        forma = '%a %b %e %H:%i:%s %Y'

        sql1 = 'SELECT * from Bike.bike_station where date_sub(curdate(),INTERVAL 7 DAY) <= DATE(STR_TO_DATE(Update_time, "%s")) and Station_number = "%s" and Hour(STR_TO_DATE(Update_time, "%s")) = "%s"and minute(STR_TO_DATE(Update_time, "%s"))=0;' % (
        forma, start_station_number, forma, hour, forma)

        sql2 = 'SELECT * from Bike.bike_station where date_sub(curdate(),INTERVAL 7 DAY) <= DATE(STR_TO_DATE(Update_time, "%s")) and Station_number = "%s" and Hour(STR_TO_DATE(Update_time, "%s")) = "%s"and minute(STR_TO_DATE(Update_time, "%s"))=0;' % (
            forma, destination_station_number, forma, hour, forma)
        cur.execute(sql1)
        s = cur.fetchall()
        cur.execute(sql2)
        d = cur.fetchall()
        db_connect.commit()
        db_connect.close()
        return s,d

@app.route('/')
@app.route('/home')
def hello_world():
    u = connectMysql()
    v = getForecast()
    # s,d = getHistoricalData(4,6,3)
    # print(s)
    # print(d)

    dateArr = []
    for i in range(len(v)):
        date = (v[i][0].split(" "))[0]
        if date not in dateArr:
            dateArr.append(date)
    return render_template('index.html',stations = json.dumps(json_dict),realtime_data = u,date_array = dateArr)


@app.route('/ajax',methods=['POST','GET'])
def index():
    u = connectMysql()
    number = request.args.get("number")
    for i in u:
        if str(i[1])==number:
            result = {"bike_available":i[10],"station":i[2],"status":i[11],"stands_available":i[9]}
            print(type(result),result)
    return json.dumps(result)

@app.route('/pred',methods=['POST','GET'])
def pred():
    u = connectMysql()
    v = getForecast()

    start_station = request.args.get("start_station")
    destination_station = request.args.get("destination_station")
    day_of_travel = request.args.get("day_of_travel")
    hour_of_travel = request.args.get("hour_of_travel")
    print(start_station,destination_station,day_of_travel,hour_of_travel)
    for i in range(len(u)):
        if start_station == u[i][2]:
            start_station_number = u[i][1]
            start_banking = u[i][6]
            start_bonus = u[i][7]
            start_bike_stands = u[i][8]
            # print("start:",station_number,banking,bonus,bike_stands)
        if destination_station == u[i][2]:
            end_station_number = u[i][1]
            end_banking = u[i][6]
            end_bonus = u[i][7]
            end_bike_stands = u[i][8]
            # print("destination:",station_number,banking,bonus,bike_stands)


    day = pd.to_datetime(day_of_travel)
    day = day.weekday()+1
    weather_info = []
    for i in range(len(v)):
        date = (v[i][0].split(" "))[0]
        hour = int(v[i][1])

        if int(hour_of_travel) == 23:
            # print(date)
            # print(pd.to_datetime(day_of_travel)+datetime.timedelta(days=1))
            if(str(pd.to_datetime(day_of_travel)+datetime.timedelta(days=1)).split(" ")[0]==str(date)) and hour == 0:
                weather_info = v[i]
                print(weather_info)
                break
        elif str(date) == str(day_of_travel):
            if abs(int(hour_of_travel) - hour) <= 1.5:
                weather_info = v[i]
                break
    if len(weather_info)==0:
        weather_info = v[-1]
        print(weather_info)

    temp = weather_info[2]
    feels_like = weather_info[3]
    temp_min = weather_info[4]
    temp_max = weather_info[5]
    pressure = weather_info[6]
    humidity = weather_info[7]
    wind_speed = weather_info[8]
    main_describe = weather_info[9]

    if start_banking == 'False':
        start_banking = 0
    else:
        start_banking=1

    if end_banking == 'False':
        end_banking = 0
    else:
        end_banking=1

    if start_bonus == 'False':
        start_bonus = 0
    else:
        start_bonus = 1

    if end_bonus == 'False':
        end_bonus = 0
    else:
        end_bonus = 1

    if main_describe =="Clouds":
        main_describe = 0
    elif main_describe == "Drizzle":
        main_describe = 1
    elif main_describe == "Rain":
        main_describe = 2
    else:
        main_describe = 3

    # print("day, hour_of_travel, station_number, bike_stands, banking, bonus, main_describe, temp, feels_like, temp_min, temp_max, wind_speed, pressure, humidity")
    start_arr = [float(day), float(hour_of_travel), float(start_station_number), float(start_bike_stands), float(start_banking), float(start_bonus), float(main_describe), float(temp), float(feels_like), float(temp_min), float(temp_max), float(wind_speed), float(pressure), float(humidity)]
    end_arr = [float(day), float(hour_of_travel), float(end_station_number), float(end_bike_stands), float(end_banking), float(end_bonus), float(main_describe), float(temp), float(feels_like), float(temp_min), float(temp_max), float(wind_speed), float(pressure), float(humidity)]
    s,d = getHistoricalData(start_station_number,end_station_number,hour_of_travel)
    print("time     available bike      available stands")
    x_axis = []
    y_axis_bike = []
    y_axis_stands = []
    for i in range(7):
        print(s[i][1],'     ',s[i][11],"    ",d[i][10])
        x_axis.append(s[i][1].split(' ')[0])
        y_axis_bike.append(s[i][11])
        y_axis_stands.append(s[i][10])
    # print(start_arr)
    # print(end_arr)
    result_1 = ML.predict_available_bike(start_arr)
    result_2 = ML.predict_available_bike(end_arr)
    final = {
             "bike_available": result_1[0]
             ,"stands_available": result_2[1]
            ,"x_axis":x_axis
            ,"y_axis_bike":y_axis_bike
            ,"y_axis_stands":y_axis_stands
            ,"description": main_describe
    }
    #print(final)
    return json.dumps(final)

if __name__ == '__main__':
    app.run(
        debug=True
    )