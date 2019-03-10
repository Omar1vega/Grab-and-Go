from Buttons import *
from Display import *
from Firebase import *
from RangeSensor import *


class Menu:
    def __init__(self):
        self.empty = 0
        self.display = Display()
        self.firebase = Firebase()
        self.buttons = Buttons()
        self.sensor = RangeSensor()
        self.items = self.firebase.get_items()

    def choose_item(self):
        position = 0
        while True:
            if position > len(self.items) - 1:
                position = 0
            if position < 0:
                position = len(self.items) - 1

            item = self.items[position]
            self.display.print("Choose Item: " + item["name"])
            button = self.buttons.get_button_pressed()
            if button == self.buttons.DOWN:
                position += 1
            elif button == self.buttons.UP:
                position -= 1
            elif button == self.buttons.A:
                self.display.print("Selected Item: " + item["name"])
                return item

    def calibrate_empty(self):
        self.display.print("Calibrate Empty Shelf", "", "Remove All Items", "", "Press A to proceed")
        button = self.buttons.get_button_pressed()
        if button == self.buttons.A:
            self.display.print("Calibrating...")
            empty_distance = self.sensor.calibrate()
            self.display.print("Calibration Done!", "Empty Distance: " + str(empty_distance))
            self.empty = empty_distance


def main():
    menu = Menu()
    menu.choose_item()


if __name__ == '__main__':
    main()
