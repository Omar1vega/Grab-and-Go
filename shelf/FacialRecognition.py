from datetime import datetime

import cv2


def takePicture(camera):
    read, frame = camera.read()

    if read:
        filename = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + ".png"
        cv2.imwrite(filename, frame)
        return filename
    return False


if __name__ == '__main__':
    while True:
        camera = cv2.VideoCapture(0)
        try:
            picture = takePicture(camera)
            camera.release()
            if picture:
                print(picture)
            else:
                print("Failed to take picture")
        except KeyboardInterrupt:
            camera.release()
