import requests
import json
from flask import json

url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=97743233cd4024c88f9531a52a74bbb4f67512a6"

def data_get(url="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=97743233cd4024c88f9531a52a74bbb4f67512a6"):
    object = requests.get(url)
    data = object.text
    return data

# print(data_get())
