import time
import requests
import json
import pymysql
import paramiko
from sshtunnel import SSHTunnelForwarder
import pandas as pd

# contracts_url ="https://api.jcdecaux.com/vls/v1/contracts?apiKey=13886f5fd2c5c9276bf9e6960a74d4eb00e97cd8"
# contracts = requests.get(contracts_url)
# print("The contracts:")
# print(contracts.text,"\n")


def getStationlist(url):
    stationlist = requests.get(url)
    # return a lsit
    return stationlist.json()

def connectMysql(station_list,now):
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

    for i in station_list:
        # for j in i:
        #     print(j, ":", i[j], end=" ")
        # print("")

        station_number = i["number"]
        station_name = i["name"]
        address = i["address"]
        address.replace('\r','').replace('\n','').replace('\t','').replace('\ ','')
        position_lat = i["position"]["lat"]
        position_lng = i["position"]["lng"]
        banking = i["banking"]
        bonus = i["bonus"]
        bike_stands = i["bike_stands"]
        available_stands = i["available_bike_stands"]
        available_bikes = i["available_bikes"]
        status = i["status"]
        last_update = i["last_update"]
        #sql = 'insert into db1.bike_station (Update_time,Station_number, Station_name, Address, Latitude, Longitude, Banking, Bonus, Bike_stands, Available_bike_stands, Available_bikes, Station_status, Last_update) value ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (structure_time, station_number, station_name, address, position_lat, position_lng, banking, bonus, bike_stands,available_stands, available_bikes, status, last_update)
        sql = 'update db1.bike_station  set Update_time = "%s", Station_name = "%s", Address = "%s", Latitude = "%s", Longitude = "%s", Banking = "%s", Bonus = "%s", Bike_stands = "%s", Available_bike_stands = "%s", Available_bikes = "%s", Station_status = "%s", Last_update = "%s" where Station_number = "%s";' % (
        structure_time, station_name, address, position_lat, position_lng, banking, bonus, bike_stands,
        available_stands, available_bikes, status, last_update, station_number)

        # try:
        cursor.execute(sql)
        connection.commit()
        # except:
        #     connection.rollback()

    connection.close()

start = time.localtime(time.time())
while(True):
    now = time.localtime(time.time())
    structure_time = time.asctime(now)
    if now.tm_min-start.tm_min >= 5:
        start = now
        stationlist_url = "https://api.jcdecaux.com/vls/v1/stations?apiKey=13886f5fd2c5c9276bf9e6960a74d4eb00e97cd8&contract=dublin"
        station_list = getStationlist(stationlist_url)
        connectMysql(station_list, structure_time)


