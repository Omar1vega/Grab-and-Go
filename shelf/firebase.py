import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

firebase_admin.initialize_app(credentials.Certificate('serviceAccountCredentials.json'),
                                  {'databaseURL': 'https://androidsample-225db.firebaseio.com/'})
root = db.reference('distance')

print(root.get())
 


def updateDistance(distance):
    firebase_admin.initialize_app(credentials.Certificate('serviceAccountCredentials.json'),
                                  {'databaseURL': 'https://androidsample-225db.firebaseio.com/'})
    root = db.reference('distance')
    root.update({
        'distance': distance
    })
