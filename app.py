import IP_setup

from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def home():
    print(IP_setup.IP())
    return render_template('index.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
