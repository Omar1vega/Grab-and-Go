import subprocess
from datetime import datetime


def takePicture():
    filename = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + ".jpg"
    subprocess.call("fswebcam -r 1280x720 --no-banner " + filename, shell=True)
    return filename


if __name__ == '__main__':
    while True:
        picture = takePicture()
        if picture:
            print(picture)
        else:
            print("Failed to take picture")
