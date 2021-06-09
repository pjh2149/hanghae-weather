import threading

import flask
import requests

from flask import Flask
from bs4 import BeautifulSoup
from selenium import webdriver

app = Flask(__name__)

def sel_IP():

    # ip_address = "218.233.45.33"
    ip_address = flask.request.remote_addr

    def sel():
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome('chromedriver', options=options)
        # driver = webdriver.Chrome('chromedriver')
        driver.get("https://mylocation.co.kr/")
        driver.implicitly_wait(0.3)

        element = driver.find_element_by_xpath('//*[@id="txtAddr"]')
        element.send_keys(ip_address)

        driver.implicitly_wait(0.3)

        try:
            search_button = driver.find_element_by_xpath('//*[@id="btnAddr2"]')
            search_button.click()
            driver.implicitly_wait(0.5)

        except:
            search_button = driver.find_element_by_xpath('// *[ @ id = "table2"] / tbody / tr[5] / td[2] / a')
            search_button.click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        address_split = soup.select_one('#lbAddr').text.split(" ")
        address_fullname = address_split[0] + " "+ address_split[1]

        driver.quit()

        return address_fullname

    def IP():
        r = requests.get(f"http://api.ipstack.com/{ip_address}?access_key=1a9cbe93c186352fe31f85507d226bb8&format=1",headers={'User-Agent': 'Mozilla/5.0'})
        result = r.json()
        lat = round(result["latitude"], 6)
        lon = round(result["longitude"], 6)

        return [lat, lon]

    coordinate = IP()
    address = sel()

    return [coordinate, address]

def weather(lat, lon):
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=3d9290fe0f2425345dc583eb4d290e52&units=metric&lang=kr")
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
        background_image = "http://cdn6.dissolve.com/p/D1201_30_001/D1201_30_001_0004_600.jpg"
    else:
        background_image = "https://thumbs.dreamstime.com/b/ship-white-sails-waves-sea-ocean-marine-background-illustration-discovery-america-columbus-121516839.jpg"

    return [temperature, description, wind_speed, humidity, image, main, background_image]
