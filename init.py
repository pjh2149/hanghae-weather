import warnings

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbsparta

warnings.filterwarnings("ignore", category=DeprecationWarning)

# DB 세팅을 위한 init.py

print("init.py\n\n...\ninitiate database setup\n")
db.visitorIP.insert_one({'IP': 0})
db.visitorsToday.insert_one({'today date': "2021-05-30"})
db.visitorCounter.remove()
db.visitorsToday.remove()
db.todayCounter.remove()
db.visitorIP.remove()
db.visitorCounter.insert_one({'Counts': 0})
db.todayCounter.insert_one({'todayCounts': 0})
print("...\ndatabase setup complete")