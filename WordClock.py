#quick, dirty port of https://github.com/jonnyarnold/wordclock/blob/master/inos/wordclock.ino
#hopefully this will work instead of reinventing the wheel

from Adafruit.Adafruit_I2C import Adafruit_I2C
import Adafruit.Adafruit_MCP230xx as ada
#import subprocess
import time
import datetime
import RPi.GPIO as gpio
import os
gpio.setmode(gpio.BCM)

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
numberOfPins = 21

#The hour pins array gives the order that the pins need to be lit up.
hourPins= [pinHourOne, pinHourTwo, pinHourThree, pinHourFour, pinHourFive,
           pinHourSix, pinHourSeven, pinHourEight, pinHourNine, pinHourTen,
           pinHourEleven, pinHourTwelve]
numberOfHourPins = 12

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
        [ pinMinFive, pinTo ]  ]
numberOfMinuteSequences = 12

#Change the hour when the minute hits the following index
hourChangeIndex = 7

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
  for p in pins:
    for k, v in p.items():
      if k == 'g':
        gpio.output(v, True)
      elif k == 'm':
        mcp.output(v, True)

def turnOff(pins):
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
  

class wc(object):
  
  def __init__(self):
    # currentHourPinIndex keeps track of which hour pin (as defined in hourPins) is lit
    # 0 = "one", 1 = "two", etc.    
    self.currentHourPinIndex = 0
    # currentMinutePinsIndex does a similar job to currentHourPinsIndex.
    # 0 = "o'clock", 1 = "five past", ... ,
    # 5 = "twenty five past", 6 = "half past", 7 = "twenty five to", etc.
    self.currentMinuteSequenceIndex = -1
    self.lpTimer = 0
    self.loopMax = 150

  def loop(self):
    
    self.lpTimer = 0
    
    #Move the minutes onto the next step
    turnOff(minuteSequence[self.currentMinuteSequenceIndex])

    self.currentMinuteSequenceIndex +=1

    if self.currentMinuteSequenceIndex == 0:
      # must put this in a list as turnOn expects that
      turnOn([hourPins[self.currentHourPinIndex]])
  
    #If we hit the end of the minutePins array, add one to the hour index
    if(self.currentMinuteSequenceIndex >= numberOfMinuteSequences):
      self.currentMinuteSequenceIndex = 0
  
    turnOn(minuteSequence[self.currentMinuteSequenceIndex])
  
    #Check for hour change (this will change it after 'half past', thus 7 index)
    if(self.currentMinuteSequenceIndex == hourChangeIndex):
      turnOff([hourPins[self.currentHourPinIndex]])
      self.currentHourPinIndex += 1
  
      #If we hit the end of the hourPins array, go back to 0
      if(self.currentHourPinIndex >= numberOfHourPins):
          self.currentHourPinIndex = 0
  
      turnOn([hourPins[self.currentHourPinIndex]])
    
    # 150 * 2 seconds = 300seconds (5mins)
    # So loop every 5 minutes, but check every 2 seconds
    # if the switch has been turned off        
    while self.lpTimer < self.loopMax:  # 150 * 2 seconds
      if gpio.input(switch):
          SHUTDOWN()
      time.sleep(2)  
      self.lpTimer += 1
      
      
  def moveTime(self, pin):
    # INCREMENT THE TIME INDEX BY 1    
    print "moved the time"
    #self.currentMinuteSequenceIndex +=1
    self.lpTimer = self.loopMax


if __name__ == '__main__':

  # register MCP to use the 230xx chip (16 gpio expander)
  mcp = ada.Adafruit_MCP230XX(address = 0x20, num_gpios = 16)

  # initalize our GPIO/MCP-gpio LEDs
  setup(mcp, gpio, allPins)
  gpio.setup(switch, gpio.IN)
  gpio.setup(button, gpio.IN)
  clock = wc()
  
  #register the event detect for button
  gpio.add_event_detect(button, gpio.RISING, callback=clock.moveTime, bouncetime=200)

  # Sanity check at startup, turn all pins on and off 
  startUp(allPins)
  
  # start counting time
  while True:
    clock.loop()
