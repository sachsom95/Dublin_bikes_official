import requests
import json
from flask import request,json,jsonify

url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=4c8b85c632a04f4b2778c719bb223cf6aea2d0a7"

def data_get(url="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=4c8b85c632a04f4b2778c719bb223cf6aea2d0a7"):
    object = requests.get(url)
    data = object.text
    return json.loads(data)

# print(data_get())
# print(json.dumps(data_get()))
