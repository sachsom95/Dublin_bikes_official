from flask import Flask, render_template

import  json
# import requests
import mysql.connector

with open('static/dublin.json') as f:
    json_dict = json.load(f)


app = Flask(__name__)

@app.route("/")
def dublin_bike():
    def get_weather():
        mydb = mysql.connector.connect\
        (
            host="dublin.cwl57f78tvsl.us-east-1.rds.amazonaws.com",
            user="root",
            passwd="dublinbikes"
        )
        mycursor = mydb.cursor()
        query = "SELECT * from bikes.weather"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mydb.commit()

        mydb.close()

        return result

    u = get_weather()

    print((u))
    print((u[0]))
    print(len(u))

    return render_template('index.html', stations=json_dict,realtime_data = u[0])




if __name__ == '__main__':

    app.run(debug=True)

