import RPi.GPIO as gpio
import time

button = 24

gpio.setmode(gpio.BCM)
gpio.setup(button, gpio.IN)


def message(pin):
  print "you pressed the button!"
gpio.add_event_detect(button,gpio.RISING, callback=message, bouncetime=200)


while True:
  print "just hanging out"
  time.sleep(1)
