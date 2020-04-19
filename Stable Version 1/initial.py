from flask import Blueprint, render_template, json, request
from db_connection import connectMysql, getForecast

# blueprint init_bp for first loading
init_bp = Blueprint("init_bp", __name__)


def load_static(file):
    '''load static file'''
    with open(file) as f:
        json_dict = json.load(f)
    return json_dict


json_dict = load_static('static/dublin.json')


@init_bp.route('/')
def hello_world():
    '''initialize the index page'''
    u = connectMysql()
    v = getForecast()

    dateArr = []
    for i in range(len(v)):
        date = (v[i][0].split(" "))[0]
        if date not in dateArr:
            dateArr.append(date)
    return render_template('index.html', stations=json.dumps(json_dict), realtime_data=u, date_array=dateArr)


@init_bp.route('/realtime', methods=['POST', 'GET'])
def fillFourBoxs():
    '''fill in real time value'''
    u = connectMysql()
    number = request.args.get("number")
    result = {}
    for i in u:
        if str(i[1]) == number:
            result = {"bike_available": i[10], "station": i[2], "status": i[11], "stands_available": i[9]}
            print(type(json.dumps(result)), result)
    return json.dumps(result)
