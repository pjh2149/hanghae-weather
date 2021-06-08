import flask
import requests

from urllib.request import Request, urlopen
from flask import Flask
from bs4 import BeautifulSoup

def translator(text):
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {"X-Naver-Client-Id": "rcKyc1EaWsLVqa7_KMcV", "X-Naver-Client-Secret": "S0Xt7xUDbk"}
    params = {"source": "en", "target": "ko", "text": text}
    response = requests.post(request_url, headers=headers, data=params)
    return response.json()['message']['result']['translatedText']

app = Flask(__name__)

def IP():
    ip_address = flask.request.remote_addr
    req = Request("https://whatismyipaddress.com/ip/61.74.92.38", headers={'User-Agent': 'Mozilla/5.0'})  # IP 테스트 코드
    # req = Request("https://whatismyipaddress.com/ip/" + ip_address, headers={'User-Agent': 'Mozilla/5.0'})  # 실제 실행되어야하는 코드

    response = urlopen(req).read()
    soup = BeautifulSoup(response, 'html.parser')

    region_str = str(soup.select("#fl-post-1165 > div > div > div.fl-row.fl-row-fixed-width.fl-row-bg-none.fl-node-5d9c0c38837c0 > div > div.fl-row-content.fl-row-fixed-width.fl-node-content > div > div.fl-col.fl-node-5d9c0c3888731 > div > div.fl-module.fl-module-wipa-static-html.fl-node-5d9e84c8187fe > div > div > div > div > div.left > p:nth-child(11) > span:nth-child(2)")[0])
    city_str = str(soup.select("#fl-post-1165 > div > div > div.fl-row.fl-row-fixed-width.fl-row-bg-none.fl-node-5d9c0c38837c0 > div > div.fl-row-content.fl-row-fixed-width.fl-node-content > div > div.fl-col.fl-node-5d9c0c3888731 > div > div.fl-module.fl-module-wipa-static-html.fl-node-5d9e84c8187fe > div > div > div > div > div.left > p:nth-child(12) > span:nth-child(2)")[0])
    coordinate_x_str = str(soup.select("#fl-post-1165 > div > div > div.fl-row.fl-row-fixed-width.fl-row-bg-none.fl-node-5d9c0c38837c0 > div > div.fl-row-content.fl-row-fixed-width.fl-node-content > div > div.fl-col.fl-node-5d9c0c3888731 > div > div.fl-module.fl-module-wipa-static-html.fl-node-5d9e84c8187fe > div > div > div > div > div.right > p:nth-child(2) > span:nth-child(2)")[0])
    coordinate_y_str = str(soup.select("#fl-post-1165 > div > div > div.fl-row.fl-row-fixed-width.fl-row-bg-none.fl-node-5d9c0c38837c0 > div > div.fl-row-content.fl-row-fixed-width.fl-node-content > div > div.fl-col.fl-node-5d9c0c3888731 > div > div.fl-module.fl-module-wipa-static-html.fl-node-5d9e84c8187fe > div > div > div > div > div.right > p:nth-child(3) > span:nth-child(2)")[0])
    # postcode_str = str(soup.select("#fl-post-1165 > div > div > div.fl-row.fl-row-fixed-width.fl-row-bg-none.fl-node-5d9c0c38837c0 > div > div.fl-row-content.fl-row-fixed-width.fl-node-content > div > div.fl-col.fl-node-5d9c0c3888731 > div > div.fl-module.fl-module-wipa-static-html.fl-node-5d9e84c8187fe > div > div > div > div > div.right > p:nth-child(4) > span:nth-child(2)")[0])

    region = region_str.replace('<span>', "").replace('</span>', "")
    city = city_str.replace('<span>', "").replace('</span>', "")
    coordinate = (coordinate_x_str.replace('<span>', "").replace('</span>', "").split(u'\xa0')[0], coordinate_y_str.replace('<span>', "").replace('</span>', "").split(u'\xa0')[0])
    # postcode = postcode_str.replace('<span>', "").replace('</span>', "")

    region_korean = translator(region)
    city_korean = translator(city)

    return [coordinate, region_korean, city_korean]

def weather(lat, lon):
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=3d9290fe0f2425345dc583eb4d290e52&units=metric")
    result = r.json()
    temperature = round(float(result["main"]["temp"]),1)
    description = translator(result["weather"][0]["description"])
    humidity = result["main"]["humidity"]
    wind_speed = result["wind"]["speed"]
    main = result["weather"][0]["main"]
    # wind speed 단위 = meter / second
    image = result["weather"][0]["icon"]

    return [temperature, description, humidity, image, main]