import IP_setup
import visitors_counter
import ssl

from pymongo import MongoClient
from flask import Flask, render_template

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # 개인테스트용
db = client.dbsparta


@app.route('/')  # IP_setup.IP() = [coordinate, region_korean, city_korean]
def home():  # IP_setup.weather() = [temperature, description, humidity, image]
    ip_index = list()
    weather_index = list()

    for i in IP_setup.IP():
        ip_index.append(i)

    for j in IP_setup.weather(ip_index[0][0], ip_index[0][0]):  # ip_index[2][0], ip_index[2][1] = lat, lon
        weather_index.append(j)

    visitors_counter.visitors()
    print(ip_index)
    print(weather_index)

    return render_template('index.html', region=ip_index[1], city=ip_index[2],
                           temperature=weather_index[0], description=weather_index[1],
                           humidity=weather_index[2], image=weather_index[3],
                           visitors_today=list(db.todayCounter.find({}, {'_id': False})),
                           visitors_total=list(db.visitorCounter.find({}, {'_id': False})))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
