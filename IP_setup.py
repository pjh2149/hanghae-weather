from urllib.request import Request, urlopen

import flask
from flask import Flask
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db = client.dbsparta

app = Flask(__name__)


# IP를 받아서, IP로 위치 찾고, 위치로 날씨 검색

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
    postcode_str = str(soup.select("#fl-post-1165 > div > div > div.fl-row.fl-row-fixed-width.fl-row-bg-none.fl-node-5d9c0c38837c0 > div > div.fl-row-content.fl-row-fixed-width.fl-node-content > div > div.fl-col.fl-node-5d9c0c3888731 > div > div.fl-module.fl-module-wipa-static-html.fl-node-5d9e84c8187fe > div > div > div > div > div.right > p:nth-child(4) > span:nth-child(2)")[0])

    region = region_str.replace('<span>', "").replace('</span>', "")
    city = city_str.replace('<span>', "").replace('</span>', "")
    coordinate = (coordinate_x_str.replace('<span>', "").replace('</span>', "").split(u'\xa0')[0], coordinate_y_str.replace('<span>', "").replace('</span>', "").split(u'\xa0')[0])
    postcode = postcode_str.replace('<span>', "").replace('</span>', "")

    print(region)
    print(city)
    print(coordinate)
    print(postcode)

    return [region, city, coordinate, postcode]
