import atexit
import time

import RPi.GPIO as GPIO


class Buttons:
    UP, DOWN, LEFT, RIGHT, CENTER, A, B = range(7)

    def __init__(self, up_pin=17, down_pin=22, left_pin=27, right_pin=23, center_pin=4, a_pin=5, b_pin=6):
        self.up_pin = up_pin
        self.down_pin = down_pin
        self.left_pin = left_pin
        self.right_pin = right_pin
        self.center_pin = center_pin
        self.a_pin = a_pin
        self.b_pin = b_pin

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.up_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(self.down_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(self.left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(self.right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(self.center_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(self.a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(self.b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up

    atexit.register(GPIO.cleanup)

    def get_button_pressed(self):
        while 1:
            if not GPIO.input(self.up_pin):
                return self.UP
            if not GPIO.input(self.down_pin):
                return self.DOWN
            if not GPIO.input(self.left_pin):
                return self.LEFT
            if not GPIO.input(self.right_pin):
                return self.RIGHT
            if not GPIO.input(self.center_pin):
                return self.CENTER
            if not GPIO.input(self.a_pin):
                return self.A
            if not GPIO.input(self.b_pin):
                return self.B
            time.sleep(.01)
