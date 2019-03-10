from collections import deque
from random import randint

from RangeSensor import *


def calibrate(range_sensor):
    d = deque(maxlen=10)
    while True:
        distance = range_sensor.get_distance()
        print("Distance: " + str(distance))
        d.append(distance)
        stability = stable(d)
        if stability != 0:
            return stability


def main():
    d = deque(maxlen=10)

    start = 28
    end = 32

    for i in range(500):
        random_number = randint(start, end)
        d.append(random_number)

        stability = stable(d)
        if stability != 0:
            print("Data is stable with average: " + str(stability) + " after " + str(i) + " iterations")

            print("Final values:")
            for number in d:
                print(number)
            return


def stable(dq):
    if len(dq) != dq.maxlen:
        return 0

    total = 0
    for num in dq:
        total += num
    average = total // len(dq)

    for num in dq:
        if num > (average + 1) or num < (average - 1):
            return 0

    return average


if __name__ == '__main__':
    range_sensor = RangeSensor()
    stability = calibrate(range_sensor)
    print("Stable at " + str(stability))
