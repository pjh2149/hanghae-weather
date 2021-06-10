import flask
import requests

from flask import Flask

app = Flask(__name__)

ip_address = "218.233.45.33"

def IP():
    # ip_address = flask.request.remote_addr
    r = requests.get(f"http://api.ipstack.com/{ip_address}?access_key=1a9cbe93c186352fe31f85507d226bb8&format=1", headers={'User-Agent': 'Mozilla/5.0'})
    result = r.json()
    region_name = result["region_name"]
    lat = round(result["latitude"], 6)
    lon = round(result["longitude"], 6)

    try:
        region = translator(region_name)
    except TypeError:
        try:
            region = translator2(region_name)
        except TypeError:
            region = translator3(region_name)
    return [[lat, lon], region]

def weather(lat, lon):
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=3d9290fe0f2425345dc583eb4d290e52&units=metric")
    result = r.json()
    temperature = round(float(result["main"]["temp"]), 1)
    description = result["weather"][0]["description"]
    wind_speed = result["wind"]["speed"]
    humidity = result["main"]["humidity"]
    image = result["weather"][0]["icon"]
    main = result["weather"][0]["main"]
    # background_image = ""
    # bad_weather = "https://i.pinimg.com/originals/0c/17/af/0c17afdc3841a2e112852745a8257983.jpg"
    # good_weather = "http://cdn6.dissolve.com/p/D1201_30_001/D1201_30_001_0004_600.jpg"
    # ok_weather = "https://thumbs.dreamstime.com/b/ship-white-sails-waves-sea-ocean-marine-background-illustration-discovery-america-columbus-121516839.jpg"
    if main == "Rain" or main == "Thunderstorm" or main == "Snow" or main == "Fog" or main == "Tornado":
        background_image = "https://i.pinimg.com/originals/0c/17/af/0c17afdc3841a2e112852745a8257983.jpg"
    elif main == "Clear" or main == "Clouds":
        background_image = "https://images.unsplash.com/photo-1593996663975-977407846c7d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80"
    else:
        background_image = "https://thumbs.dreamstime.com/b/ship-white-sails-waves-sea-ocean-marine-background-illustration-discovery-america-columbus-121516839.jpg"

    return [temperature, description, wind_speed, humidity, image, main, background_image]

def translator(text):
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {"X-Naver-Client-Id": "rcKyc1EaWsLVqa7_KMcV", "X-Naver-Client-Secret": "S0Xt7xUDbk"}
    params = {"source": "en", "target": "ko", "text": text}
    response = requests.post(request_url, headers=headers, data=params)
    return response.json()['message']['result']['translatedText']

def translator2(text):
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {"X-Naver-Client-Id": "vkiqbYUMOxV5kvNjSelf", "X-Naver-Client-Secret": "yTOQNBsIwq"}
    params = {"source": "en", "target": "ko", "text": text}
    response = requests.post(request_url, headers=headers, data=params)
    return response.json()['message']['result']['translatedText']

def translator3(text):
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {"X-Naver-Client-Id": "6uSpE4vIWa6ayIFlERQD", "X-Naver-Client-Secret": "8SqYAfF8W5"}
    params = {"source": "en", "target": "ko", "text": text}
    response = requests.post(request_url, headers=headers, data=params)
    return response.json()['message']['result']['translatedText']
