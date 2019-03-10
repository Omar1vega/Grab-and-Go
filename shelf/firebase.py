import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class Firebase:
    def __init__(self):
        firebase_admin.initialize_app(credentials.Certificate('serviceAccountCredentials.json'),
                                      {'databaseURL': 'https://androidsample-225db.firebaseio.com/'})
        self.cache = {}

    def get_items(self):
        return list(db.reference('items').get().values())

    def add_item(self, item, user):
        new_item_key = db.reference("carts/" + user).child("items").push()
        new_item_key.set(item.get_value())

        self.cache[user] = new_item_key

    def remove_item(self, user):
        self.cache[user].delete()
        del self.cache[user]
