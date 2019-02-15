from datetime import datetime

import cv2


def takePicture(camera):
    read, frame = camera.read()
    camera.release()

    if read:
        filename = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + ".png"
        cv2.imwrite(filename, frame)
        return filename
    return False


if __name__ == '__main__':
    while True:
        camera = cv2.VideoCapture(0)
        picture = takePicture(camera)
        if picture:
            print(picture)
        else:
            print("Failed to take picture")
