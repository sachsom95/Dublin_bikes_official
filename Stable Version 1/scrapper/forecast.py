import requests
from flask import json
from db_connection import getConnection

url = "https://api.openweathermap.org/data/2.5/forecast?q=Dublin&units=metric&appid=334edd463962a36bb945255752407871"

def get_forecast(url="https://api.openweathermap.org/data/2.5/forecast?q=Dublin&units=metric&appid=334edd463962a36bb945255752407871"):
    object = requests.get(url)
    data = object.text
    return json.loads(data)

forecast_data = get_forecast()
forecast_list = forecast_data['list']

def clean_data():
    for i in range(len(forecast_list)):

        forecast_list[i].pop('dt')
        forecast_list[i].pop('clouds')
        forecast_list[i].pop('sys')

        forecast_list[i]['main'].pop('sea_level')
        forecast_list[i]['main'].pop('grnd_level')
        forecast_list[i]['main'].pop('temp_kf')
        forecast_list[i]['weather'][0].pop('id')
        forecast_list[i]['weather'][0].pop('description')
        forecast_list[i]['weather'][0].pop('icon')
        forecast_list[i]['wind'].pop('deg')

        forecast_list[i]['windSpeed'] =  forecast_list[i]['wind']['speed']
        forecast_list[i].pop('wind')

        forecast_list[i]['Desc'] = forecast_list[i]['weather'][0]['main']
        forecast_list[i].pop('weather')
        forecast_list[i]['Date'] = forecast_list[i].pop('dt_txt')
        forecast_list[i]['Hour'] = forecast_list[i]['Date'][11:13]
        if 'rain' in forecast_list[i]:
            forecast_list[i].pop('rain')
        forecast_list[i]['temp'] = forecast_list[i]['main']['temp']
        forecast_list[i]['feels_like'] = forecast_list[i]['main']['feels_like']
        forecast_list[i]['temp_min'] = forecast_list[i]['main']['temp_min']
        forecast_list[i]['temp_max'] = forecast_list[i]['main']['temp_max']
        forecast_list[i]['pressure'] = forecast_list[i]['main']['pressure']
        forecast_list[i]['humidity'] = forecast_list[i]['main']['humidity']
        forecast_list[i].pop('main')


def insert_date():

    connection = getConnection()
    cursor = connection.cursor()
    clean_data()

    # drop all the rows for next update
    sql_truncate = "truncate forecast;"
    cursor.execute(sql_truncate)

    for i in range(len(forecast_list)):
        date = forecast_list[i]['Date']
        hour = forecast_list[i]['Hour']
        temp = forecast_list[i]['temp']
        feels_like = forecast_list[i]['feels_like']
        temp_min = forecast_list[i]['temp_min']
        temp_max = forecast_list[i]['temp_max']
        pressure = forecast_list[i]['pressure']
        humidity = forecast_list[i]['humidity']
        wind_speed = forecast_list[i]['windSpeed']
        main = forecast_list[i]['Desc']

        sql = "insert into db1.forecast values ('%s','%s', '%s','%s','%s','%s', '%s', '%s', '%s', '%s');" % (date, hour, temp, feels_like, temp_min,temp_max, pressure, humidity, wind_speed, main)
        cursor.execute(sql)

    connection.commit()
    connection.close()

insert_date()