from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from dublin_bike import *
from sqlalchemy import *
from weather import weather
from datetime import timedelta
from bikes import bikes


# app = Flask(__name__,template_folder='user_manage/templates',
#     static_folder='user_manage/static')
app = Flask(__name__)
#在初始化flask时, 需要制定默认的模板文件夹, 否则就默认是root下的templates

# app.register_blueprint(weather.weather_bp)
app.register_blueprint(bikes.bike_bp)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT '] = timedelta(seconds=5)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lhb280214@localhost:3306/dublin_bike'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
#
# class Status(db.Model):
#     __tablename__ = 'status'
#
#     number = db.Column(db.Integer, primary_key=True)
#     bike_stands = db.Column(db.Integer)
#     available_bike_stands = db.Column(db.Integer)
#     available_bikes = db.Column(db.Integer)
#     status = db.Column(db.String(10))
#
#     postion = db.relationship('Position', backref='status')
#
#     def __init__(self, number, bike_stands, available_bike_stands, available_bikes, status):
#         self.number = number
#         self.bike_stands = bike_stands
#         self.available_bike_stands = available_bike_stands
#         self.available_bikes = available_bikes
#         self.status = status
#
#     def __repr__(self):
#         return '<Status status: %s, available_bike_stands: %d, available_bikes: %d>' % (self.status, self.available_bike_stands, self.available_bikes)
#
# class Position(db.Model):
#     __tablename__ = 'position'
#
#     number = db.Column(db.Integer, db.ForeignKey('status.number'), primary_key=True )
#     name = db.Column(db.String(50), nullable=False)
#     address = db.Column(db.String(50), nullable=False)
#     latitude = db.Column(db.DECIMAL(10,6), nullable=False)
#     longitude = db.Column(db.DECIMAL(10,6), nullable=False)
#     banking = db.Column(db.String(10), nullable=False)
#     bonus = db.Column(db.String(10), nullable=False)
#
#     def __init__(self, number, name, address, latitude, longitude, banking, bonus):
#         self.number = number
#         self.name = name
#         self. address = address
#         self.latitude = latitude
#         self.longitude = longitude
#         self.banking = banking
#         self.bonus = bonus
#
#     def __repr__(self):
#         return '<Position name: %s, address: %s>' % (self.name, self.address)
#
# def data_fill():
#     json_data = data_get()
#     for post in json_data:
#         p = Position(post['number'],post['name'],post['address'],post['position']['lat'],post['position']['lng'],post['banking'],post['bonus'])
#         db.session.add(p)
#         s = Status(post['number'], post['bike_stands'], post['available_bike_stands'], post['available_bikes'],post['status'])
#         db.session.add(s)
#     db.session.commit()

# @app.route('/')
# def index():
#     d = data_get()
#     message = "hello flask flask flask"
#
#     return render_template('index.html', ms = message, d = data_get())

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # data_fill()
    app.run()
