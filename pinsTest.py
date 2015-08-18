import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


T12 = 18 #YES
OCLOCK = 23 #YES
MINUTES = 17 #YES
QUARTER = 7
TWENTY = 22 #YES
NINE = 25 # YES

all = {"T12": 18, "OCLOCK": 23, "MINUTES": 17, "QUARTER": 7, "TWENTY": 22, "NINE": 25}

for k, v in all.items():
  print "whats on: {}, pin: {}".format(k, v)
  GPIO.setup(v, GPIO.OUT)
  GPIO.output(v, True)
  raw_input("next")
  #GPIO.output(v, False)

raw_input("off")
for k,v in all.items():
  print"pass"
  #GPIO.output(v, False)


GPIO.cleanup()
