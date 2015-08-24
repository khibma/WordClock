#quick, dirty port of https://github.com/jonnyarnold/wordclock/blob/master/inos/wordclock.ino
#hopefully this will work instead of reinventing the wheel

from Adafruit_I2C import Adafruit_I2C
import Adafruit_MCP230xx as ada
import subprocess
import time
import datetime
import RPi.GPIO as gpio
#import smbus

gpio.setmode(gpio.BCM)

# CONSTANTS

switch = 9
button = 24
#This constant is used as a 'null'
#The code will ignore this value when it is found
pinNoPin = -1

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
allPins = [pinMinFive, pinMinTen, pinMinQuarter, pinMinTwenty,
           pinMinHalf, pinMinOClock, pinPast, pinTo, pinHourOne, pinHourTwo,
           pinHourThree, pinHourFour, pinHourFive, pinHourSix, pinHourSeven,
           pinHourEight, pinHourNine, pinHourTen, pinHourEleven, pinHourTwelve]
numberOfPins = 21

#The hour pins array gives the order that the pins need to be lit up.
#(Length: 12)
hourPins= [pinHourOne, pinHourTwo, pinHourThree, pinHourFour, pinHourFive,
           pinHourSix, pinHourSeven, pinHourEight, pinHourNine, pinHourTen,
           pinHourEleven, pinHourTwelve]

numberOfHourPins = 12

#Minute pins are more tricky. The following array shows the sequence of minute pins
#to light up. pinNoPin is used to fill out the arrays, and should be ignored when
#looping over them.
minuteSequence = [
        [ pinMinOClock, pinNoPin, pinNoPin ],
        [ pinMinFive, pinPast, pinNoPin ],
        [ pinMinTen, pinPast, pinNoPin ],
        [ pinMinQuarter, pinPast, pinNoPin ],
        [ pinMinTwenty, pinPast, pinNoPin ],
        [ pinMinTwenty, pinMinFive, pinPast ],
        [ pinMinHalf, pinPast, pinNoPin ],
        [ pinMinTwenty, pinMinFive, pinTo ],
        [ pinMinTwenty, pinTo, pinNoPin ],
        [ pinMinQuarter, pinTo, pinNoPin ],
        [ pinMinTen, pinTo, pinNoPin ],
        [ pinMinFive, pinTo, pinNoPin ]  ]
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
        time.sleep(0.5)
        gpio.output(v, False)
      else:
        mcp.output(v, True)
        time.sleep(0.5)
        mcp.output(v, False)

def turnOn(pins):
  for p in pins:
    for k, v in p.items():
      if k == 'g':
        gpio.output(v, True)
      else:
        mcp.output(v, True)

def turnOff(pins):
  for p in pins:
    for k, v in p.items():
      if k == 'g':
        gpio.output(v, False)
      else:
        mcp.output(v, False)
        
def SHUTDOWN():
  
  turnOff(allPins) 
  turnOff([pinItIs])  # turn off "it is"
  time.sleep(0.8)
  offSeq = [pinItIs, pinMinHalf, pinMinTen]
  for i in xrange(0, 2):
    turnOn(offSeq)
    time.sleep(0.5)
    turnOff(offSeq)
    time.sleep(0.5)
  print("would be shutting down here...")
  command = "/usr/bin/sudo /sbin/shutdown -r now"  
  #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
  #output = process.communicate()[0]  

class wc(object):
  
  def __init__(self):
    # currentHourPinIndex keeps track of which hour pin (as defined in hourPins) is lit
    # 0 = "one", 1 = "two", etc.    
    self.currentHourPinIndex = 2
    # currentMinutePinsIndex does a similar job to currentHourPinsIndex.
    # 0 = "o'clock", 1 = "five past", ... ,
    # 5 = "twenty five past", 6 = "half past", 7 = "twenty five to", etc.
    self.currentMinuteSequenceIndex = 1
    self.lpTimer = 0    

  def loop(self):
    
    self.lpTimer = 0
    
    #Move the minutes onto the next step
    turnOff(minuteSequence[currentMinuteSequenceIndex])
    currentMinuteSequenceIndex +=1
  
    #If we hit the end of the minutePins array, add one to the hour index
    if(currentMinuteSequenceIndex >= numberOfMinuteSequences):
      currentMinuteSequenceIndex = 0
  
    turnOn(minuteSequence[currentMinuteSequenceIndex])
  
    #Check for hour change
    if(currentMinuteSequenceIndex == hourChangeIndex):
      turnOff(hourPins[currentHourPinIndex])
      currentHourPinIndex += 1
  
      #If we hit the end of the hourPins array, go back to 0
      if(currentHourPinIndex >= numberOfHourPins):
          currentHourPinIndex = 0
  
      turnOn(hourPins[currentHourPinIndex])
    
    # 20 * 15 seconds = 300seconds (5mins)
    # So loop every 5 minutes, but check every 15 seconds
    # if the switch has been turned off
    
    while self.lpTimer < 19:
      if gpio.input(switch):
          SHUTDOWN()
      time.sleep(15)
      self.lpTimer += 1
      
      
  def moveTime(self, pin):
    # INCREMENT THE TIME INDEX BY 1    
    self.currentMinuteSequenceIndex +=1
    self.lpTimer = 0


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

  # turn on "it is"....
  turnOn([pinItIs])  

  # start counting time
  
  clock.loop()
