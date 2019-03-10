import time

import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
from shelf import getDistance

RST = None  # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
display = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

display.begin()

# Clear display.
display.clear()
display.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = display.width
height = display.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

top = -2
x = 0
font = ImageFont.load_default()

try:
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Write two lines of text.

        draw.text((x, top), time.strftime("%H:%M:%S"), font=font, fill=255)
        draw.text((x, top + 8), "Distance: " + str(int(getDistance())) + "cm")

        # Display image.
        display.image(image)
        display.display()
        time.sleep(1)

except KeyboardInterrupt:
    display.clear()
    display.display()
    exit(0)
