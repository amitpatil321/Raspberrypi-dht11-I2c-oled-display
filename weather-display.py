
import time
import sys
import board

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import adafruit_dht

import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# initialise 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# initialise dht sensor
dhtDevice = adafruit_dht.DHT11(board.D21) # Change board and pin number here

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# text_font_name = 'Roboto-Bold.ttf'
text_font_name = 'Poppins-Light.ttf'
text_font_bold = 'Poppins-Bold.ttf'
icon_font_name = 'fontawesome-webfont.ttf'
font_large = ImageFont.truetype(text_font_name, 16)
font_large_bold = ImageFont.truetype(text_font_bold, 16)
font_small = ImageFont.truetype(text_font_name, 10)
font_icon = ImageFont.truetype(icon_font_name, 20)

while True:
  try:
      # Print the values to the serial port
      temperature_c = dhtDevice.temperature
      temperature_f = temperature_c * (9 / 5) + 32
      humidity = dhtDevice.humidity

      # display temprature
      
      # print icon
      draw.text((5, 2), chr(62152), font=font_icon, fill=255)
    #   # print temrature string
      draw.text((20, 2), str("Temprature") , font=font_small, fill=255)
      draw.text((20, 14), str(temperature_c), font=font_large_bold, fill=255)
      draw.text((45, 14), str("°c"), font=font_large, fill=255)

      # display temprature
      
      # print icon
      draw.text((0, 36), chr(62172), font=font_icon, fill=255)
      # print humidity string
      draw.text((20, 36), str("Humidity"), font=font_small, fill=255)
      draw.text((20, 46), str(humidity), font=font_large_bold, fill=255)
      draw.text((40, 46), str("%"), font=font_large, fill=255)

      # Display image.
      disp.image(image)
      disp.display()

      # time.sleep(1)
      draw.rectangle((0,0,width,height), outline=0, fill=0)

  except RuntimeError as error:
      # Errors happen fairly often, DHT's are hard to read, just keep going
      # print(error.args[0])
      time.sleep(2.0)
      continue
  except Exception as error:
      dhtDevice.exit() 
      raise error

  time.sleep(2)
