from flask import Blueprint, render_template

weather_bp = Blueprint('weather_bp', __name__,template_folder='templates', static_folder="static",
                    static_url_path="/weather/static")

@weather_bp.route('/')
def weather1():
    return render_template('index.html')

@weather_bp.route('/weather_dublin')
def weather2():
    return render_template('dublin.html')