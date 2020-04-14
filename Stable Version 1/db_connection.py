import pymysql

def getConnection():
    '''get connection to db'''
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
    return connection


def connectMysql():
    '''request realtime bike station info from db'''
    connection = getConnection()
    cursor = connection.cursor()

    sql = 'select * from db1.bike_station'

    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result

def getForecast():
    '''request forecast data from db'''
    connection = getConnection()
    cursor = connection.cursor()

    sql = 'select * from db1.forecast'

    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result