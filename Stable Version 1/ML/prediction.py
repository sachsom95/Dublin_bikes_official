from flask import Blueprint, request, json
from db_connection import connectMysql, getForecast, getConnection
from ML import ML
import pandas as pd
import datetime
import pymysql
from sshtunnel import SSHTunnelForwarder

# blueprint for prediction part function
pred_bp = Blueprint("pred", __name__)


@pred_bp.route('/pred', methods=['POST', 'GET'])
def pred():
    '''get daily prediction data'''

    # connect database to access real-time data
    u = connectMysql()
    v = getForecast()

    # get data from frontend
    start_station = request.args.get("start_station")
    destination_station = request.args.get("destination_station")
    day_of_travel = request.args.get("day_of_travel")
    hour_of_travel = request.args.get("hour_of_travel")
    # print(start_station,destination_station,day_of_travel,hour_of_travel)

    # get backend data of the corresponding stations
    for i in range(len(u)):
        if start_station == u[i][2]:
            start_station_number = u[i][1]
            start_banking = u[i][6]
            start_bike_stands = u[i][8]
        if destination_station == u[i][2]:
            end_station_number = u[i][1]
            end_banking = u[i][6]
            end_bike_stands = u[i][8]

    # get weather forecast information according to the user's input
    day = pd.to_datetime(day_of_travel)
    day = day.weekday() + 1
    weather_info = []
    for i in range(len(v)):
        date = (v[i][0].split(" "))[0]
        hour = int(v[i][1])

        if int(hour_of_travel) == 23:
            if (str(pd.to_datetime(day_of_travel) + datetime.timedelta(days=1)).split(" ")[0] == str(
                    date)) and hour == 0:
                weather_info = v[i]
                break
        elif str(date) == str(day_of_travel):
            if abs(int(hour_of_travel) - hour) <= 1.5:
                weather_info = v[i]
                break
    if len(weather_info) == 0:
        weather_info = v[-1]

    temp = weather_info[2]
    feels_like = weather_info[3]
    temp_min = weather_info[4]
    temp_max = weather_info[5]
    pressure = weather_info[6]
    humidity = weather_info[7]
    wind_speed = weather_info[8]
    main_describe = weather_info[9]

    # encode categorical features
    if start_banking == 'False':
        start_banking = 0
    else:
        start_banking = 1

    if end_banking == 'False':
        end_banking = 0
    else:
        end_banking = 1

    if main_describe == "Clouds":
        main_describe = 0
    elif main_describe == "Drizzle":
        main_describe = 1
    elif main_describe == "Rain":
        main_describe = 2
    else:
        main_describe = 3

    # get historical data to print the first and second charts
    s, d = getHistoricalData(start_station_number, end_station_number, hour_of_travel)
    x_axis = []
    y_axis_bike = []
    y_axis_stands = []
    for i in range(7):
        x_axis.append(s[i][1].split(' ')[0])
        y_axis_bike.append(s[i][11])
        y_axis_stands.append(s[i][10])

    # invoke prediction program and feed all parameters
    start_arr = [float(day), float(hour_of_travel), float(start_station_number), float(start_bike_stands),
                 float(start_banking), float(main_describe), float(temp), float(feels_like), float(temp_min),
                 float(temp_max), float(wind_speed), float(pressure), float(humidity)]
    end_arr = [float(day), float(hour_of_travel), float(end_station_number), float(end_bike_stands), float(end_banking),
               float(main_describe), float(temp), float(feels_like), float(temp_min), float(temp_max),
               float(wind_speed), float(pressure), float(humidity)]

    result_1 = ML.predict_available_bike(start_arr)
    result_2 = ML.predict_available_stands(end_arr)
    final = {
        "bike_available": result_1
        , "stands_available": result_2
        , "x_axis": x_axis
        , "y_axis_bike": y_axis_bike
        , "y_axis_stands": y_axis_stands
        , "description": main_describe
    }
    return json.dumps(final)


def getHistoricalData(start_station_number, destination_station_number, hour):
    '''get historical data of the last seven days '''

    db_connect = getConnection()
    cur = db_connect.cursor()

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
    return s, d


@pred_bp.route('/predict_all', methods=['POST', 'GET'])
def predict_all():
    '''get hourly prediction data on the given date,
    basically just repeat the same prediction process 24 fimes'''

    u = connectMysql()
    v = getForecast()

    start_station = request.args.get("start_station")
    destination_station = request.args.get("destination_station")
    day_of_travel = request.args.get("day_of_travel")
    hour_of_travel = request.args.get("hour_of_travel")
    print(start_station, destination_station, day_of_travel, hour_of_travel)
    for i in range(len(u)):
        if start_station == u[i][2]:
            start_station_number = u[i][1]
            start_banking = u[i][6]
            start_bike_stands = u[i][8]
        if destination_station == u[i][2]:
            end_station_number = u[i][1]
            end_banking = u[i][6]
            end_bike_stands = u[i][8]

    day = pd.to_datetime(day_of_travel)
    day = day.weekday() + 1
    weather_info = []

    result_1 = {}
    result_2 = {}
    # hour changes from 0 to 23 and the else arguments are the same
    for clock in range(24):
        for i in range(len(v)):
            date = (v[i][0].split(" "))[0]
            hour = int(v[i][1])

            if int(hour_of_travel) == 23:
                if (str(pd.to_datetime(day_of_travel) + datetime.timedelta(days=1)).split(" ")[0] == str(
                        date)) and hour == 0:
                    weather_info = v[i]
                    break
            elif str(date) == str(day_of_travel):
                if abs(int(clock) - hour) <= 1.5:
                    weather_info = v[i]
                    break
        if len(weather_info) == 0:
            weather_info = v[i]

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
            start_banking = 1

        if end_banking == 'False':
            end_banking = 0
        else:
            end_banking = 1

        if main_describe == "Clouds":
            main_describe = 0
        elif main_describe == "Drizzle":
            main_describe = 1
        elif main_describe == "Rain":
            main_describe = 2
        else:
            main_describe = 3

        start_arr = [float(day), float(hour), float(start_station_number), float(start_bike_stands),
                     float(start_banking), float(main_describe), float(temp), float(feels_like), float(temp_min),
                     float(temp_max), float(wind_speed), float(pressure), float(humidity)]
        end_arr = [float(day), float(hour), float(end_station_number), float(end_bike_stands), float(end_banking),
                   float(main_describe), float(temp), float(feels_like), float(temp_min), float(temp_max),
                   float(wind_speed), float(pressure), float(humidity)]

        result_1[clock] = ML.predict_available_bike(start_arr)
        result_2[clock] = ML.predict_available_stands(end_arr)

    final = {
        "24hour_bikes": result_1
        , "24hour_stands": result_2
    }
    return json.dumps(final)
