import subprocess
from datetime import datetime

import boto3


def takePicture():
    filename = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + ".jpg"
    subprocess.call("fswebcam -r 1280x720 --no-banner " + filename, shell=True)
    return filename


def uploadToS3(filepath):
    s3 = boto3.resource('s3')
    uploadPath = "pickups" + filepath.split("/")[-1]
    s3.meta.client.upload_file(filepath, 'amazotgo', uploadPath)
    return uploadPath


if __name__ == '__main__':
    while True:
        picture = takePicture()
        if picture:
            print(picture)
            print(uploadToS3(picture))
        else:
            print("Failed to take picture")
