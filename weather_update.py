import json
import requests
import mysql.connector
api_key = '79d3ddb4063b40e201255636111cc4f2'
api_base ='http://api.openweathermap.org/data/2.5/'
# API call for temperature in dublin
# http://api.openweathermap.org/data/2.5/weather?id=2964574&unit=metric&appid=79d3ddb4063b40e201255636111cc4f2
open_weather_dict={'dublin_temp':'weather?id=2964574&units=metric&appid='}
temp = 0
def get_weather():
    api_token = api_key
    request_string = api_base+open_weather_dict['dublin_temp']+api_token
    response =requests.get(request_string).text

    # return (response['main']['temp'])

temp = get_weather()
mydb = mysql.connector.connect(
  host="dublin.cwl57f78tvsl.us-east-1.rds.amazonaws.com",
  user="root",
  passwd="dublinbikes"
)




