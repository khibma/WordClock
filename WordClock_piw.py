#quick, dirty port of https://github.com/jonnyarnold/wordclock/blob/master/inos/wordclock.ino

from Adafruit.Adafruit_I2C import Adafruit_I2C
import Adafruit.Adafruit_MCP230xx as ada
import time
import datetime
import RPi.GPIO as gpio
import os
gpio.setmode(gpio.BCM)

starttime=time.time()

# CONSTANTS

switch = 9
button = 24
#This constant is used as a 'null'
#The code will ignore this value when it is found
pinNoPin = {'z': 0}

#Pin numbers
pinMinFive = {'m': 3}
pinMinTen = {'m': 2}
pinMinutes = {'g': 17}
pinMinQuarter = {'g': 7}
pinMinTwenty = {'g': 22}
pinMinHalf = {'m': 1}
pinMinOClock = {'g': 23}

pinItIs = {'m': 0}
pinPast = {'m': 5}
pinTo = {'m': 4}

pinHourOne = {'m': 6}
pinHourTwo ={'m': 15}
pinHourThree = {'m': 7}
pinHourFour = {'m': 14}
pinHourFive = {'m': 11}
pinHourSix = {'m': 13}
pinHourSeven = {'m': 12}
pinHourEight = {'m': 10}
pinHourNine = {'g': 25}
pinHourTen = {'m': 8}
pinHourEleven = {'m': 9}
pinHourTwelve = {'g': 18}

#All pins
allPins = [pinItIs, pinMinFive, pinMinTen, pinMinQuarter, pinMinTwenty,
           pinMinHalf, pinMinOClock, pinPast, pinTo, pinHourOne, pinHourTwo,
           pinHourThree, pinHourFour, pinHourFive, pinHourSix, pinHourSeven,
           pinHourEight, pinHourNine, pinHourTen, pinHourEleven, pinHourTwelve]

#The hour pins array gives the order that the pins need to be lit up.
hourPins= [pinHourTwelve, pinHourOne, pinHourTwo, pinHourThree, pinHourFour, pinHourFive,
           pinHourSix, pinHourSeven, pinHourEight, pinHourNine, pinHourTen,
           pinHourEleven ]

#Minute pins are more tricky. The following array shows the sequence of minute pins
minuteSequence = [
        [ pinItIs, pinMinOClock ],
        [ pinMinFive, pinPast ],
        [ pinMinTen, pinPast ],
        [ pinMinQuarter, pinPast ],
        [ pinMinTwenty, pinPast ],
        [ pinMinTwenty, pinMinFive, pinPast ],
        [ pinMinHalf, pinPast ],
        [ pinMinTwenty, pinMinFive, pinTo ],
        [ pinMinTwenty, pinTo ],
        [ pinMinQuarter, pinTo ],
        [ pinMinTen, pinTo ],
        [ pinMinFive, pinTo ] ]


def setup(mcp, gpio, pins):
  ''' get pins setup and registered'''

  for pin in pins:
    for k, v in pin.items():
      if k == 'g':
        gpio.setup(v, gpio.OUT)
      else:
        mcp.config(v, mcp.OUTPUT)

def startUp(pins):
  ''' move through all the items and turn them on, turn them off'''

  for pin in pins:
    for k, v in pin.items():
      if k == 'g':
        gpio.output(v, True)
        time.sleep(0.2)
        gpio.output(v, False)
      elif k == 'm':
        mcp.output(v, True)
        time.sleep(0.2)
        mcp.output(v, False)

def turnOn(pins):
  if pins is not None:
    for p in pins:
      for k, v in p.items():
        if k == 'g':
          gpio.output(v, True)
        elif k == 'm':
          mcp.output(v, True)

def turnOff(pins):
  if pins is not None:
    for p in pins:
      for k, v in p.items():
        if k == 'g':
          gpio.output(v, False)
        elif k == 'm':
          mcp.output(v, False)
          
def SHUTDOWN():
  
  turnOff(allPins) 
  time.sleep(0.8)
  offSeq = [pinItIs, pinMinHalf, pinMinTen]
  for i in xrange(0, 2):
    turnOn(offSeq)
    time.sleep(0.5)
    turnOff(offSeq)
    time.sleep(0.5)
  print("shutting down...")
  os.system("sudo shutdown -h now")
  


class rtc(object):
  """ set time via RTC """
  
  def __init__(self):
    self.hour = datetime.datetime.now().hour
    self.minutes = datetime.datetime.now().minute
    self.hourOnIdx = None
    self.minuteOnIdx = None
    
  def loop(self): 

    if gpio.input(switch):
      SHUTDOWN()
    
    self.hour = datetime.datetime.now().hour
    self.minutes = datetime.datetime.now().minute    
    
    if self.minutes > 30:
      self.hour += 1    
    if self.hour > 12:
      self.hour = self.hour - 12
  
    if self.hour != self.hourOnIdx:
      turnOff(hourPins(self.hourOnIdx))
      self.hourOnIdx = self.hour
      turnOn(hourPins[self.hourOnIdx])
    
    if self.minutes/5 != self.minuteOnIdx: 
      turnOff(minuteSequence(self.minuteOnIdx))      
      self.minuteOnIdx = self.minutes / 5
      turnOn(minuteSequence[self.minuteOnIdx / 5])
      
    #http://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/25251804#25251804
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    #time.sleep(30) # check time every 30 seconds and increment if necessary

if __name__ == '__main__':

  # register MCP to use the 230xx chip (16 gpio expander)
  mcp = ada.Adafruit_MCP230XX(address = 0x20, num_gpios = 16)

  # initalize our GPIO/MCP-gpio LEDs
  setup(mcp, gpio, allPins)
  gpio.setup(switch, gpio.IN)
  
  clockRTC = rtc()
  
  #unused button.
  #gpio.setup(button, gpio.IN)  
  #gpio.add_event_detect(button, gpio.RISING, callback=clock.moveTime, bouncetime=200)

  # Sanity check at startup, turn all pins on and off 
  startUp(allPins)

  while True:
    clockRTC.loop()
  
