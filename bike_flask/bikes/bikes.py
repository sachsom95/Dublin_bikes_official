from flask import Blueprint, render_template

bike_bp = Blueprint('bike_bp', __name__,template_folder='templates', static_folder="static",
                    static_url_path="/bikes/static")

@bike_bp.route("/")
def bike():
    return render_template("index.html")