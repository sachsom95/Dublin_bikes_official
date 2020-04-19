from flask import Flask
from initial import init_bp
from ML.prediction import pred_bp

app = Flask(__name__)
app.register_blueprint(init_bp)
app.register_blueprint(pred_bp)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='ec2-3-80-6-206.compute-1.amazonaws.com',
        port=5000
    )
