#!/usr/bin/env python
########################################################################
# Filename    : shelf.py
# Description : Detecting item pickup at shelf
# Author      : vegao1
# modification: 2018/11/07
########################################################################

import time

import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220  # define the maximum measured distance
timeOut = MAX_DISTANCE * 60  # calculate timeout according to the maximum measured distance


def updateDistance(distance):
    firebase_admin.initialize_app(credentials.Certificate('serviceAccountCredentials.json'),
                                  {'databaseURL': 'https://androidsample-225db.firebaseio.com/'})
    root = db.reference('distance')
    root.update({
        'distance': distance
    })


def pulseIn(pin, level, timeOut):  # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while GPIO.input(pin) != level:
        if (time.time() - t0) > timeOut * 0.000001:
            return 0
    t0 = time.time()
    while GPIO.input(pin) == level:
        if (time.time() - t0) > timeOut * 0.000001:
            return 0
    return (time.time() - t0) * 1000000


def getDistance():  # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin, GPIO.HIGH)  # make trigPin send 10us high level
    time.sleep(0.00001)  # 10us
    GPIO.output(trigPin, GPIO.LOW)
    pingTime = pulseIn(echoPin, GPIO.HIGH, timeOut)  # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0  # the sound speed is 340m/s, and calculate distance
    return distance


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(trigPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)


def checkDistance(distance):
    return 20 >= distance > 0


personAlerted = False
counter = 0


def awayMode():
    distance = getDistance()
    print("distance =", distance)

    updateDistance(int(distance))

    # if (checkDistance(distance)):
    # update firebase
    time.sleep(3)


def loop():
    while True:
        awayMode()


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    print('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
