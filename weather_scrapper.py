# AUTHOR: SACHIN SOMAN

# >>>>>>>>>>>>>>LIBRARIES<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import requests
import mysql.connector
import time
#-----------------------------------------------------

# >>>>>>>>>>>>>SQL CONNECTION CONFIG<<<<<<<<<<<<<<<<<<
mydb = mysql.connector.connect(
  host="dublin.cwl57f78tvsl.us-east-1.rds.amazonaws.com",
  user="root",
  passwd="dublinbikes"
)
mycursor = mydb.cursor()

# -----------------------------------------------------

# >>>>>>>>>>>>>>>API KEYS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
api_key_open_weather = 'a3ab131d4929e85bbb554003ee79c398'
api_open_weather_base = 'http://api.openweathermap.org/data/2.5/weather?'

# -----------------------------------------------------

# >>>>>>>>>>>>>>>>>GLOBAL VARIABLES<<<<<<<<<<<<<<<<<<<<<
weather={}



# -------------------------------------------------------

# >>>>>>>>>>>>>>TIME<<<<<<<<<<<<<<<<<<<<<<
def time_stamp():
    """Return the current date time."""
    secondsSinceEpoch = time.time()
    timeObj = time.localtime(secondsSinceEpoch)
    time_str = '%d-%d-%d,%d-%d' % (
    timeObj.tm_mday, timeObj.tm_mon, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min)
    return time_str
#---------------------------------------------


def get_weather_by_latitude(lat = 53.34399,lon = -6.26719):
    """Return the weather dictionary based on lat and lon parameters default is dublin center."""
    global weather
    request_body = api_open_weather_base+'lat={}&lon={}&units=metric&appid={}'.format(lat,lon,api_key_open_weather)
    response = requests.get(request_body).json()
    if response['cod'] == 200:

        response = requests.get(request_body).json()
        tme = time_stamp()
        tme = tme.split(",")



        weather['date']=tme[0]
        weather['time']=tme[1]
        weather['temp'] = response['main']['temp']
        weather['description'] = response['weather'][0]['description']
        weather['icon'] = response['weather'][0]['icon']
        weather['feels_like'] = response['main']['feels_like']
        weather['temp_min'] = response['main']['temp_min']
        weather['temp_max'] = response['main']['temp_max']
        weather['wind_speed'] = response['wind']['speed']
    else:
        print("Could not get information")



def get_weather_by_city_id(id ='2964574' ):
    """Return the weather dictionary based city id default is dublin ID"""

    global weather
    request_body = api_open_weather_base+'id={}&units=metric&appid={}'.format(id,api_key_open_weather)
    response = requests.get(request_body).json()

    if response['cod'] == 200:
        print(request_body)

        response = requests.get(request_body).json()
        weather['time'] = time_stamp()
        weather['temp']= response['main']['temp']
        weather['description'] = response['weather'][0]['description']
        weather['icon'] = response['weather'][0]['icon']
        weather['feels_like'] = response['main']['feels_like']
        weather['temp_min'] = response['main']['temp_min']
        weather['temp_max'] = response['main']['temp_max']
        weather['wind_speed'] = response['wind']['speed']

    else:
        print("Could not get information")



latitude = 53.34399
longtitude =-6.26719
get_weather_by_latitude(lat=53.34399, lon=-6.26719)
query = "UPDATE bikes.weather SET date = '{}',time='{}', temp = {}, feels_like = {} ,temp_min = {}, temp_max = {}, wind_speed = {},icon = '{}', lat = {}, lon = {}, description = {} WHERE lat = {}".format(weather['date'],weather['time'],weather['temp'],weather['feels_like'],weather['temp_min'],weather['temp_max'],weather['wind_speed'],weather['icon'],latitude,longtitude,latitude,weather['description'])
print(query)

mycursor.execute(query)
mydb.commit()

print("Done executing query for --> {}".format(weather['time']))