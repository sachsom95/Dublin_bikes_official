import time
import requests
import pymysql


def getStationlist(url):
    stationlist = requests.get(url)
    # return a lsit
    return stationlist.json()


weather = {}
api_key_open_weather = 'a3ab131d4929e85bbb554003ee79c398'
api_open_weather_base = 'http://api.openweathermap.org/data/2.5/weather?'


def get_weather_by_city_id(id='2964574'):
    """Return the weather dictionary based city id default is dublin ID"""

    global weather
    request_body = api_open_weather_base + 'id={}&units=metric&appid={}'.format(id, api_key_open_weather)
    response = requests.get(request_body).json()

    if response['cod'] == 200:
        print(request_body)

        response = requests.get(request_body).json()
        # weather['time'] = time_stamp()
        weather['temp'] = response['main']['temp']
        weather['description'] = response['weather'][0]['description']
        weather['icon'] = response['weather'][0]['icon']
        weather['feels_like'] = response['main']['feels_like']
        weather['temp_min'] = response['main']['temp_min']
        weather['temp_max'] = response['main']['temp_max']
        weather['wind_speed'] = response['wind']['speed']

    else:
        print("Could not get information")


def connectMysql(station_list, now):
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
    get_weather_by_city_id()
    for i in station_list:
        # for j in i:
        #     print(j, ":", i[j], end=" ")
        # print("")

        station_number = i["number"]
        station_name = i["name"]
        address = i["address"]
        address.replace('\r', '').replace('\n', '').replace('\t', '').replace('\ ', '')
        position_lat = i["position"]["lat"]
        position_lng = i["position"]["lng"]
        banking = i["banking"]
        bonus = i["bonus"]
        bike_stands = i["bike_stands"]
        available_stands = i["available_bike_stands"]
        available_bikes = i["available_bikes"]
        status = i["status"]
        last_update = i["last_update"]
        sql = 'insert into db1.bike_station (Update_time,Station_number, Station_name, Address, Latitude, Longitude, Banking, Bonus, Bike_stands, Available_bike_stands, Available_bikes, Station_status, Last_update, Temperature,Feels_like, Temp_min, Temp_max, Wind_speed, Icon,Description) value ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (
            structure_time, station_number, station_name, address, position_lat, position_lng, banking, bonus,
            bike_stands, available_stands, available_bikes, status, last_update, weather['temp'], weather['feels_like'],
            weather['temp_min'], weather['temp_max'], weather['wind_speed'], weather['icon'], weather['description'])
        sql = 'update db1.bike_station  set Update_time = "%s", Station_name = "%s", Address = "%s", Latitude = "%s", Longitude = "%s", Banking = "%s", Bonus = "%s", Bike_stands = "%s", Available_bike_stands = "%s", Available_bikes = "%s", Station_status = "%s", Last_update = "%s",Temperature = "%s",Feels_like = "%s" ,Temp_min = "%s", Temp_max = "%s", Wind_speed = "%s",Icon = "%s",Description = "%s" where Station_number = "%s";' % (
            structure_time, station_name, address, position_lat, position_lng, banking, bonus, bike_stands,
            available_stands, available_bikes, status, last_update, weather['temp'], weather['feels_like'],
            weather['temp_min'],
            weather['temp_max'], weather['wind_speed'], weather['icon'], weather['description'], station_number)

        # get_weather_by_city_id()
        # query = "UPDATE bikes.weather SET date = '{}',time='{}', temp = {}, feels_like = {} ,temp_min = {}, temp_max = {}, wind_speed = {},icon = '{}', lat = {}, lon = {} WHERE lat = {}".format(
        #     weather['date'], weather['time'], weather['temp'], weather['feels_like'], weather['temp_min'],
        #     weather['temp_max'], weather['wind_speed'], weather['icon'], latitude, longtitude, latitude)
        # print(query)

        # try:
        cursor.execute(sql)
        connection.commit()
        # except:
        #     connection.rollback()

    connection.close()


# start = time.localtime(time.time())
# while(True):
now = time.localtime(time.time())
structure_time = time.asctime(now)
#     if now.tm_min-start.tm_min >= 5:
#         start = now
stationlist_url = "https://api.jcdecaux.com/vls/v1/stations?apiKey=13886f5fd2c5c9276bf9e6960a74d4eb00e97cd8&contract=dublin"
station_list = getStationlist(stationlist_url)
connectMysql(station_list, structure_time)
