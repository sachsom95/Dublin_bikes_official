
# # API call for temperature in dublin
# # http://api.openweathermap.org/data/2.5/weather?id=2964574&unit=metric&appid=79d3ddb4063b40e201255636111cc4f2
# open_weather_dict={'dublin_temp':'weather?id=2964574&units=metric&appid='}
# temp = 0
# def get_weather():
#     api_token = api_key
#     request_string = api_base+open_weather_dict['dublin_temp']+api_token
#     response =requests.get(request_string).text
#
#     # return (response['main']['temp'])
#
# temp = get_weather()
# mydb = mysql.connector.connect(
#   host="dublin.cwl57f78tvsl.us-east-1.rds.amazonaws.com",
#   user="root",
#   passwd="dublinbikes"
# )
#
import requests

api_key_open_weather = '79d3ddb4063b40e201255636111cc4f2'
api_open_weather_base = 'http://api.openweathermap.org/data/2.5/weather?'

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# By geographic coordinates
# API call:
# http://api.openweathermap.org/data/2.5/weather?lat=-6.26719&lon=53.34399&appid=79d3ddb4063b40e201255636111cc4f2
# Parameters:
# lat, lon coordinates of the location of your interest
# Examples of API calls:
# api.openweathermap.org/data/2.5/weather?lat=35&lon=139
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def get_weather_by_latitude(lat,lon):
    request_body = api_open_weather_base+'lat={}&lon={}&units=metric&appid={}'.format(lat,lon,api_key_open_weather)
    response = requests.get(request_body).json()

    if response['cod'] == 200:
        print(request_body)

        response = requests.get(request_body).json()
        print(response['weather'][0]['main'])
        weather = {'temp':response['weather'][0]['main']}

        print(response['weather'][0]['description'])
        weather = {'description': response['weather'][0]['description']}

        print(response['weather'][0]['icon'])
        weather = {'icon': response['weather'][0]['icon']}

        print(response['main']['feels_like'])
        weather = {'temp': response['weather'][0]['main']}
        print(response['main']['temp_min'])
        weather = {'temp': response['weather'][0]['main']}
        print(response['main']['temp_max'])
        weather = {'temp': response['weather'][0]['main']}
        print(response['wind']['speed'])
        weather = {'temp': response['weather'][0]['main']}
    else:
        print("Could not get information")

get_weather_by_latitude(53.34399,-6.26719)

# get_weather_by_latitude(53.34399,-6.26719)   <<<< dublin