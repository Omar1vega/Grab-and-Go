import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class Firebase:
    def __init__(self):
        firebase_admin.initialize_app(credentials.Certificate('serviceAccountCredentials.json'),
                                      {'databaseURL': 'https://androidsample-225db.firebaseio.com/'})
        self.messages = db.reference('messages')

    def get_items(self):
        return list(db.reference('items').get().values())

    def add_item(self, item, user):
        new_item_key = db.reference("carts/" + user).child("items").push()
        new_item_key.set(item)

    def remove_item(self, item, user):
        item_reference = db.reference("carts/" + user).child("items")
        items = item_reference.get()
        for key in items:
            item_in_cart = items[key]
            if item_in_cart == item:
                item_reference.child(key).delete()
                return

    def log_message(self, message):
        self.messages.push().set(message)



if __name__ == "__main__":
    firebase = Firebase()

    firebase.remove_item(
        {'imageUrl': 'https://images-na.ssl-images-amazon.com/images/I/51ans2c7qUL.jpg', 'name': 'LaCroix'},
        "4ZSTy0yXTldWuzRKUqybjTajeno2")
