import time

from Camera import Camera
from Firebase import Firebase
from Rekognition import Rekognition

if __name__ == '__main__':
    firebase = Firebase()
    camera = Camera()
    rekognition = Rekognition(max_faces=9)

    while True:
        file_path = camera.take_picture()
        upload_path = rekognition.upload(file_path)

        users = rekognition.recognize_users(upload_path)

        if len(users) > 0:
            for user in users:
                firebase.archive_cart(user.UID)
        time.sleep(5)
