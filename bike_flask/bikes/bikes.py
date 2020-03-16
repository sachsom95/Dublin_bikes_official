from flask import Blueprint, render_template, send_file, json
from dublin_bike import data_get


bike_bp = Blueprint('bike_bp', __name__,template_folder='templates', static_folder="static",
                    static_url_path="/bikes/static")

@bike_bp.route("/")
def bike():
    return render_template("index.html")


@bike_bp.route("/data")
def bike_data():
    json_data = data_get()
    return json.dumps(json_data)