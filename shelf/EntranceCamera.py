import time

import firebase_admin
from firebase_admin import credentials, db

from FacialRecognition import takePicture, uploadToS3, recognize

firebase_admin.initialize_app(credentials.Certificate('serviceAccountCredentials.json'),
                              {'databaseURL': 'https://androidsample-225db.firebaseio.com/'})

root = db.reference('distance')
in_store = db.reference("store/users/in")
run = db.reference("devices/zero1")


def should_run():
    return run.get()


def init_user(id, name):
    in_store.child(str(id)).set({
        'name': name
    })


def remove_user(id):
    in_store.child(str(id)).delete()


def main():
    while True:
        shouldRun = str(should_run())
        if shouldRun == "False":
            print("firebase preventing execution")
            continue
        if shouldRun == "exit":
            exit(0)

        users_in_store()
        picture = takePicture()
        if picture:
            print(picture)
            s3Filepath = uploadToS3(picture)
            print(s3Filepath)
            id, name = recognize(s3Filepath)
            if id and name:
                init_user(id, name)

        time.sleep(1)


def users_in_store():
    users = in_store.get()
    if users:
        print(users)


if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
