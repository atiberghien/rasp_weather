#! /usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, redirect
from w1thermsensor import W1ThermSensor
import requests
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
ACTUATOR_PIN = 8
GPIO.setup(ACTUATOR_PIN, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def index():
    req = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Florac,fr&units=metric&appid=2249f831ffa31996fe0747849b7a8a21')
    data = json.loads(req.text)["main"]
    data["indoor_temp"] = W1ThermSensor().get_temperature()
    data["actuator_state"] = GPIO.input(ACTUATOR_PIN)
    return render_template('index.html', data=data)

@app.route("/activate")
def activate():
    GPIO.output(ACTUATOR_PIN, True)
    return redirect("/")

@app.route("/deactivate")
def deactivate():
    GPIO.output(ACTUATOR_PIN, False)
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
