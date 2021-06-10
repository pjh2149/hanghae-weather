import threading

import flask
import requests

from flask import Flask
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def sel_IP():

    ip_address = "218.233.45.33"
    # ip_address = flask.request.remote_addr

    def sel():
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-dev-shm-usage")
        try:
            chrome_options.add_argument("disable-gpu")
        except:
            chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        driver.set_window_size(0, 0)
        driver.implicitly_wait(5)
        driver.get("https://www.iplocation.net/ip-lookup?query=" + ip_address)
        print(ip_address, "IP 받아오기 성공")
        print("사이트 입력 완료")
        driver.implicitly_wait(5)

        # element = driver.find_element_by_xpath('//*[@id="txtAddr"]')
        # element.send_keys(ip_address)
        # print("IP 입력 완료")
        # driver.implicitly_wait(1)
        #
        # search_button = driver.find_element_by_xpath('//*[@id="btnAddr2"]')
        # search_button.click()
        # print("검색 활성화")
        # driver.implicitly_wait(4)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        address_split1 = ""
        address_split2 = ""
        try:
            print("사이트 접속 완료")
            address_split1 = soup.select_one('body > section > div > div > div.col.col_8_of_12 > div:nth-child(4) > div > table > tbody:nth-child(2) > tr > td:nth-child(3)').text
            address_split2 = soup.select_one('body > section > div > div > div.col.col_8_of_12 > div:nth-child(4) > div > table > tbody:nth-child(2) > tr > td:nth-child(4)').text
            if address_split1 == address_split2:
                address_split1 = soup.select_one('body > section > div > div > div.col.col_8_of_12 > div:nth-child(5) > div > table > tbody:nth-child(2) > tr > td:nth-child(3)').text
                address_split2 = soup.select_one('body > section > div > div > div.col.col_8_of_12 > div:nth-child(4) > div > table > tbody:nth-child(2) > tr > td:nth-child(4)').text
        except:
            driver.implicitly_wait(5)
            print("사이트 접속 완료")
            address_split1 = soup.select_one(
                'body > section > div > div > div.col.col_8_of_12 > div:nth-child(4) > div > table > tbody:nth-child(2) > tr > td:nth-child(3)').text
            address_split2 = soup.select_one(
                'body > section > div > div > div.col.col_8_of_12 > div:nth-child(4) > div > table > tbody:nth-child(2) > tr > td:nth-child(4)').text
            if address_split1 == address_split2:
                address_split1 = soup.select_one(
                    'body > section > div > div > div.col.col_8_of_12 > div:nth-child(5) > div > table > tbody:nth-child(2) > tr > td:nth-child(3)').text
                address_split2 = soup.select_one(
                    'body > section > div > div > div.col.col_8_of_12 > div:nth-child(4) > div > table > tbody:nth-child(2) > tr > td:nth-child(4)').text

        try:
            address_split1 = translator(address_split1)
            address_split2 = translator(address_split2)
        except KeyError:
            try:
                address_split1 = translator(address_split1)
                address_split2 = translator(address_split2)
            except KeyError:
                try:
                    address_split1 = translator(address_split1)
                    address_split2 = translator(address_split2)
                except KeyError:
                    print("번역기 사용횟수 초과로 인해 주소 영어표기")
                    pass

        address_fullname = address_split1 + " " + address_split2
        driver.close()

        return address_fullname

    def IP():
        r = requests.get(f"http://api.ipstack.com/{ip_address}?access_key=1a9cbe93c186352fe31f85507d226bb8&format=1",headers={'User-Agent': 'Mozilla/5.0'})
        result = r.json()
        lat = round(result["latitude"], 6)
        lon = round(result["longitude"], 6)

        return [lat, lon]

    try:
        address = sel()
    except:
        print("오류가 발생하여 재실행합니다")
        address = sel()
    coordinate = IP()

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