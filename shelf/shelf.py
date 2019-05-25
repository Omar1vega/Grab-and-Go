#!/usr/bin/env python

import time

from FacialRecognition import takePicture, uploadToS3, recognize

itemPresent = True
itemAdded = False
itemRemoved = False


class Shelf:
    def __init__(self, item, sensor, camera, display):
        self.item = item
        self.sensor = sensor
        self.camera = camera
        self.display = display

    def set_item(self, item):
        self.item = item


def main():
    global itemPresent, itemAdded, itemRemoved
    while True:
        distance = getDistance()
        print("distance =", distance)

        if (37 - 4 < distance < 37 + 4):
            itemPresent = True

        if (distance > 54 - 4):
            itemPresent = False

        if (not itemPresent and not itemAdded):
            picture = takePicture()
            if picture:
                print(picture)
                s3Filepath = uploadToS3(picture)
                print(s3Filepath)
                id, name = recognize(s3Filepath)

                add_item(id)
            itemAdded = True

        if (itemPresent and not itemRemoved and itemAdded):
            removeItem()
            itemRemoved = True
            itemAdded = False

        time.sleep(0.5)


if __name__ == '__main__':
    print('Program is starting ... ')
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()
