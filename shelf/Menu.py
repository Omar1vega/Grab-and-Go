from Buttons import *
from Display import *
from Firebase import *
from RangeSensor import *


class Menu:
    def __init__(self):
        self.empty = 0
        self.item_size = 0
        self.margin = 0
        self.display = Display()
        self.firebase = Firebase()
        self.buttons = Buttons()
        self.sensor = RangeSensor(display=self.display)
        self.items = self.firebase.get_items()
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
                return item

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

            item_count = int((self.empty - full_distance) / self.item_size)

            self.display.print_lines("Calibration Done!", str(item_count) + " Items Detected!")
            time.sleep(3)

            for i in range(item_count):
                self.increments.append(self.empty - (i * self.item_size))

            self.display.print_lines(str(self.increments))
            time.sleep(3)


def main():
    menu = Menu()
    menu.choose_item()
    menu.calibrate_empty()
    menu.calibrate_item_size()
    menu.fill_shelf()


if __name__ == '__main__':
    main()
