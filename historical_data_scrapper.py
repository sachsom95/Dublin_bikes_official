
import  json
import requests
import time
import mysql.connector






mydb = mysql.connector.connect(
  host="dublin.cwl57f78tvsl.us-east-1.rds.amazonaws.com",
  user="root",
  passwd="dublinbikes"
)
mycursor = mydb.cursor()

key='https://api.jcdecaux.com/vls/v1/stations?apiKey=c1c3a7298b0e5f548ca9bedd48a3acd42dc8ae21&contract=dublin'


api_key_open_weather = '79d3ddb4063b40e201255636111cc4f2'
api_open_weather_base = 'http://api.openweathermap.org/data/2.5/weather?'
id ='2964574'
request_body = api_open_weather_base + 'id={}&units=metric&appid={}'.format(id, api_key_open_weather)
contract = "dublin"
overflow = 0
data={}



def getStationlist(url):
    stationlist = requests.get(url)
    return stationlist.json()
def getWeather(url):
    weatherdata=requests.get(url)
    return weatherdata.json()

def time_stamp():
    """Return the current date time."""
    secondsSinceEpoch = time.time()
    timeObj = time.localtime(secondsSinceEpoch)
    time_str = '%d:%d:%d' % (timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec)
    date_str = '%d-%d-%d' % ( timeObj.tm_year, timeObj.tm_mon,timeObj.tm_mday )
    return str(time_str) , str(date_str)


data['time'], data['date'] = (time_stamp())

station = getStationlist(key)
weather = getWeather(request_body)

data['main'] = weather['weather'][0]['main']
data['description'] = weather['weather'][0]['description']
data['temp'] = weather['main']['temp']
data['feels_like'] = weather['main']['feels_like']
data['temp_min'] = weather['main']['temp_min']
data['temp_max'] = weather['main']['temp_max']
data['wind_speed'] = weather['wind']['speed']
data['icon'] = weather['weather'][0]['icon']
data['pressure'] = weather['main']['pressure']
data['humidity'] = weather['main']['humidity']





for i in station:
    data["station_number"] = i["number"]
    data["station_name"] = i["name"]
    address = i["address"]
    address.replace('\r', '').replace('\n', '').replace('\t', '').replace('\ ', '')
    data["address"] = address
    data["position_lat"] = i["position"]["lat"]
    data["position_lng"] = i["position"]["lng"]
    data["banking"] = i["banking"]
    data["bonus"] = i["bonus"]
    data["bike_stands"] = i["bike_stands"]
    data["available_stands"] = i["available_bike_stands"]
    data["available_bikes"] = i["available_bikes"]
    data["status"] = i["status"]
    data["last_update"] = i["last_update"]


    query = 'insert into bikes.historic_data (time,date,address,banking,bike_stands,bonus,contract_name,name,number,overflow,' \
            'position_lat,position_lng,status,main,description,temp,feels_like,temp_min,temp_max,wind_speed,icon,' \
            'pressure,humidity) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");'%(data['time'], data['date'],data["address"], data["banking"], data["bike_stands"], data["bonus"], contract, data["station_name"], data["station_number"], overflow,data["position_lat"],data["position_lng"],data["status"],data['main'],data['description'],data['temp'],data['feels_like'],data['temp_min'],data['temp_max'],data['wind_speed'],data['icon'],data['pressure'],data['humidity'])



    mycursor.execute(query)
    mydb.commit()

print("Done executing query for --> {} on {}".format(data['time'], data['date']))
