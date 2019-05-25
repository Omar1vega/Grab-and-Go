import subprocess
from datetime import datetime


class Camera:
    def __init__(self, resolution="1280x720"):
        self.resolution = resolution

    def take_picture(self):
        filename = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + ".jpg"
        subprocess.call("fswebcam -r " + self.resolution + " --no-banner " + filename, shell=True)
        return filename
