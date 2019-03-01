import time

import firebase_admin
from firebase_admin import credentials, db

from FacialRecognition import takePicture, uploadToS3, recognize

firebase_admin.initialize_app(credentials.Certificate('serviceAccountCredentials.json'),
                              {'databaseURL': 'https://androidsample-225db.firebaseio.com/'})

root = db.reference('distance')
in_store = db.reference("stores/users/in")


def init_user(id, name):
    in_store.child(str(id)).set({
        'name': name
    })


def remove_user(id):
    in_store.child(str(id)).delete()


def main():
    while True:
        picture = takePicture()
        if picture:
            print(picture)
            s3Filepath = uploadToS3(picture)
            print(s3Filepath)
            id, name = recognize(s3Filepath)
            if (id and name):
                init_user(id, name)

        time.sleep(1)


if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
