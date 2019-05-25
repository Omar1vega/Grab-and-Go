import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
from RangeSensor import *


class Display:
    def __init__(self):
        self.display = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        self.display.begin()
        self.display.clear()
        self.image = Image.new('1', (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
        self.font = ImageFont.load_default()
        atexit.register(self.clear)

    def clear(self):
        self.display.clear()
        self.display.display()

    def print_lines(self, *args):
        line = 0
        self.draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
        for string in args:
            self.draw.text((0, line), string, font=self.font, fill=255)
            line += 8
        self.display.image(self.image)
        self.display.display()


if __name__ == '__main__':
    range_sensor = RangeSensor()
    display = Display()
    while True:
        display.print_lines(time.strftime("%H:%M:%S"), "Distance: " + str(range_sensor.get_distance()) + "cm")
        time.sleep(1)
