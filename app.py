import IP_setup
import visitors_counter
import ssl

from pymongo import MongoClient
from flask import Flask, render_template

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # 개인테스트용
db = client.dbsparta

@app.route('/')  # IP_setup.IP() = [region, city, coordinate, postcode, region_korean, city_korean]
def home():  # IP_setup.weather() = [temperature, description, humidity, wind_speed, image]
    visitors_counter.visitors()
    return render_template('index.html', region=IP_setup.IP()[4], city=IP_setup.IP()[5],
                           temperature=IP_setup.weather()[0], description=IP_setup.weather()[1],
                           humidity=IP_setup.weather()[2], wind_speed=IP_setup.weather()[3],
                           image=IP_setup.weather()[4], visitors_today=list(db.todayCounter.find({}, {'_id': False})),
                           visitors_total=list(db.visitorCounter.find({}, {'_id': False})))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
