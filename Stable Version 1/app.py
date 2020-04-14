from flask import Flask
from initial import init_bp
from ML.prediction import pred_bp


app = Flask(__name__)
app.register_blueprint(init_bp)
app.register_blueprint(pred_bp)

if __name__ == '__main__':
    app.run(
        debug=True
    )