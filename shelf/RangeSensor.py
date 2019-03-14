import atexit
import time
from collections import deque

import RPi.GPIO as GPIO

MAX_DISTANCE = 220  # define the maximum measured distance
timeOut = MAX_DISTANCE * 60  # calculate timeout according to the maximum measured distance


def pulse_in(pin, level, time_out):  # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while GPIO.input(pin) != level:
        if (time.time() - t0) > time_out * 0.000001:
            return 0
    t0 = time.time()
    while GPIO.input(pin) == level:
        if (time.time() - t0) > time_out * 0.000001:
            return 0
    return (time.time() - t0) * 1000000


def stable(dq):
    if len(dq) != dq.maxlen:
        return 0

    total = 0
    for num in dq:
        total += num
    average = total / len(dq)

    for num in dq:
        if num > (average + 1) or num < (average - 1):
            return 0

    return average


def cleanup():
    GPIO.cleanup()


class RangeSensor:
    def __init__(self, trigger_pin=24, echo_pin=25, display=None):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.display = display

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)

        atexit.register(cleanup)

    def __str__(self):
        return "(Trigger Pin: " + str(self.trigger_pin) + " Echo Pin: " + str(self.echo_pin) + ")"

    def get_distance(self):
        GPIO.output(self.trigger_pin, GPIO.HIGH)  # make trigPin send 10us high level
        time.sleep(0.00001)  # 10us
        GPIO.output(self.trigger_pin, GPIO.LOW)

        ping_time = pulse_in(self.echo_pin, GPIO.HIGH, timeOut)  # read plus time of echoPin
        distance = ping_time * 340.0 / 2.0 / 10000.0  # the sound speed is 340m/s, and calculate distance
        return distance

    def calibrate(self):
        d = deque(maxlen=10)
        while True:
            distance = self.get_distance()
            status = "Distance: " + str(distance)
            if self.display:
                self.display.print_lines(status)
            else:
                print(status)
            d.append(distance)
            stability = stable(d)
            if stability != 0:
                return stability
            time.sleep(0.5)


if __name__ == '__main__':
    range_sensor = RangeSensor()
    print(range_sensor)
    distance = range_sensor.get_distance()
    print("Distance: " + str(range_sensor.get_distance()) + "cm")
