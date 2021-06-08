import IP_setup

from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
from flask import Flask, render_template
import requests

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)


@app.route('/')
def home():
    IP_setup.IP()
    lat = IP_setup.IP()[2][0]
    lon = IP_setup.IP()[2][1]
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=3d9290fe0f2425345dc583eb4d290e52&units=metric&lang=kr")
    result = r.json()
    temperature = result["main"]["temp"]
    description = result["weather"][0]["description"]
    humidity = result["main"]["humidity"]
    wind_speed = result["wind"]["speed"]
    image = result["weather"][0]["icon"]
    return render_template('index.html', result=result, temperature=temperature, description=description,
                           humidity=humidity, wind_speed=wind_speed, image=image)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
