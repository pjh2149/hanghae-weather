import flask

from pymongo import MongoClient
from datetime import datetime
from flask import Flask

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbsparta


def visitors():
    visitor_counts = db.visitorCounter.find_one({})['Counts']  # 총 방문자수
    today_visitor_counts = db.todayCounter.find_one({})['todayCounts']  # 일일 방문자수

    ip_address = flask.request.remote_addr

    today = str(datetime.now())
    today_date = today.split(' ')[0]

    if db.visitorsToday.find({'today date': today_date}).count() > 0:
        if db.visitorIP.find({'IP': ip_address}).count() > 0:
            pass
        else:
            updated_today_visitor_counts = today_visitor_counts + 1
            db.todayCounter.update_one({'todayCounts': today_visitor_counts},
                                       {'$set': {'todayCounts': updated_today_visitor_counts}})
    else:
        db.visitorsToday.insert_one({'today date': today_date})
        db.todayCounter.update_one({'todayCounts': today_visitor_counts},
                                   {'$set': {'todayCounts': 0}})
        if db.visitorIP.find({'IP': ip_address}).count() > 0:
            pass
        else:
            db.todayCounter.update_one({'todayCounts': 0},
                                       {'$set': {'todayCounts': 1}})
    if db.visitorIP.find({'IP': ip_address}).count() > 0:
        pass
    else:
        db.visitorIP.create_index("date", expireAfterSeconds=7200)
        db.visitorIP.insert_one({'IP': ip_address, "date": datetime.utcnow()})
        updated_visitor_counts = visitor_counts + 1
        db.visitorCounter.update_one({'Counts': visitor_counts}, {'$set': {'Counts': updated_visitor_counts}})