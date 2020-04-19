import pymysql


def getConnection():
    '''get connection to db'''
    sql_hostname = 'tutorial-db-instance.cf2q3iwaca38.us-east-1.rds.amazonaws.com'
    sql_username = 'tutorial_user'
    sql_password = 'nyj19971023'
    sql_main_database = 'Bike'
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

    sql = 'select * from Bike.realtime_data'

    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def getForecast():
    '''request forecast data from db'''
    connection = getConnection()
    cursor = connection.cursor()

    sql = 'select * from Bike.forecast'

    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result
