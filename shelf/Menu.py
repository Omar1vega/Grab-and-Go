import socket

from Buttons import *
from Camera import *
from Display import *
from Firebase import *
from RangeSensor import *
from Rekognition import *


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class Menu:
    def __init__(self):
        self.empty = 0
        self.item_size = 0
        self.margin = 0
        self.item = None
        self.display = Display()
        self.firebase = Firebase()
        self.buttons = Buttons()
        self.camera = Camera()
        self.rekognition = Rekognition()
        self.sensor = RangeSensor(display=self.display)
        self.items = self.firebase.get_items()
        self.item_count = 0
        self.current_item_count = 0
        self.increments = []

    def choose_item(self):
        position = 0
        while True:
            if position > len(self.items) - 1:
                position = 0
            if position < 0:
                position = len(self.items) - 1

            item = self.items[position]
            self.display.print_lines("Choose Item: " + item["name"])
            button = self.buttons.get_button_pressed()
            if button == self.buttons.DOWN:
                position += 1
            elif button == self.buttons.UP:
                position -= 1
            elif button == self.buttons.A:
                self.display.print_lines("Selected Item: " + item["name"])
                self.item = item
                return

    def calibrate_empty(self):
        self.display.print_lines("Calibrate Empty Shelf", "", "Remove All Items", "", "Press A to proceed")
        button = self.buttons.get_button_pressed()
        if button == self.buttons.A:
            self.display.print_lines("Calibrating...")
            empty_distance = self.sensor.calibrate()
            self.display.print_lines("Calibration Done!", "Empty Distance: " + str(empty_distance) + "cm")
            self.empty = empty_distance
            time.sleep(3)

    def calibrate_item_size(self):
        self.display.print_lines("Calibrate Item Size", "", "Place 1 Item", "", "Press A to proceed")
        button = self.buttons.get_button_pressed()
        if button == self.buttons.A:
            self.display.print_lines("Calibrating...")
            item_size = self.empty - self.sensor.calibrate()
            self.display.print_lines("Calibration Done!", "Item Size: " + str(item_size) + "cm")
            self.item_size = item_size
            time.sleep(3)

    def fill_shelf(self):
        self.display.print_lines("Fill Shelf With Items", "", "Press A When Finished")
        button = self.buttons.get_button_pressed()
        if button == self.buttons.A:
            self.display.print_lines("Calculating Item Quantity...")
            time.sleep(3)
            full_distance = self.sensor.calibrate()

            self.item_count = int((self.empty - full_distance) / self.item_size)
            self.current_item_count = self.item_count

            self.display.print_lines("Calibration Done!", str(self.item_count) + " Items Detected!")
            time.sleep(3)

            for i in range(self.item_count + 1):
                self.increments.append(self.empty - (i * self.item_size))

            self.display.print_lines(str(self.increments))
            print(self.increments)
            time.sleep(3)

    def run(self):
        while True:
            current_distance = self.sensor.get_distance()
            detected_item_count = self.increments.index(min(self.increments, key=lambda x: abs(x - current_distance)))
            self.display.print_lines("Current Distance: " + str(current_distance), "", "Detected Item Count:", "",
                                     str(detected_item_count))

            if detected_item_count == self.current_item_count:
                continue

            local_path = self.camera.take_picture()
            upload_path = self.rekognition.upload(local_path)
            users = self.rekognition.recognize_users(upload_path)
            if len(users) == 0:
                self.firebase.log_message("unrecognized user detected, at shelf with: " + self.item["name"])
                self.current_item_count = detected_item_count
                continue

            if detected_item_count < self.current_item_count:  # item picked up
                for i in range(detected_item_count, self.current_item_count):
                    self.firebase.add_item(self.item, users[0].UID)
            else:  # item put back
                for i in range(self.current_item_count, detected_item_count):
                    self.firebase.remove_item(self.item, users[0].UID)
            self.current_item_count = detected_item_count
            time.sleep(2)


def main():
    menu = Menu()
    try:
        menu.choose_item()
        menu.calibrate_empty()
        menu.calibrate_item_size()
        menu.fill_shelf()
        menu.run()
    except AssertionError:
        menu.display.print_lines(get_ip_address())
        time.sleep(2 * 60)


if __name__ == '__main__':
    main()
