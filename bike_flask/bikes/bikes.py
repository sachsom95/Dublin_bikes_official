from flask import Blueprint, render_template, send_file, json,request
from dublin_bike import data_get
from model import get_station_info


bike_bp = Blueprint('bike_bp', __name__,template_folder='templates', static_folder="static",
                    static_url_path="/bikes/static")

@bike_bp.route("/")
def bike():
    return render_template("index.html")


@bike_bp.route("/data")
def bike_data():
    json_data = data_get()
    return json.dumps(json_data)


@bike_bp.route("/station")
def station_info():
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    # print(lat, lng)

    station_info = get_station_info(lat,lng)
    print(type(station_info), station_info)
    return station_info


# select bike_stands, available_bike_stands, available_bikes, status
# from status
# join position
# using (number)
# where latitude = 53.349013 and longitude = -6.260311;