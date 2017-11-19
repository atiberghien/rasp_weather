#! /usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from w1thermsensor import W1ThermSensor
import requests
import json

app = Flask(__name__)

@app.route("/")
def index():
    req = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Florac,fr&units=metric&appid=2249f831ffa31996fe0747849b7a8a21')
    data = json.loads(req.text)["main"]
    data["indoor_temp"] = W1ThermSensor().get_temperature()
    return render_template('index.html', data=data)

@app.route("/activate")
def activitate():
    return "Ventilateur activé"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
