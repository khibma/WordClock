#quick, dirty port of https://github.com/jonnyarnold/wordclock/blob/master/inos/wordclock.ino
#hopefully this will work instead of reinventing the wheel

from Adafruit_I2C import Adafruit_I2C
import Adafruit_MCP230xx as ada
import time
import datetime
#import smbus


#currentHourPinIndex keeps track of which hour pin (as defined in hourPins) is lit
#0 = "one", 1 = "two", etc.
currentHourPinIndex = 2

#currentMinutePinsIndex does a similar job to currentHourPinsIndex.
#0 = "o'clock", 1 = "five past", ... ,
#5 = "twenty five past", 6 = "half past", 7 = "twenty five to", etc.
currentMinuteSequenceIndex = 1

#CONSTANTS

#This constant is used as a 'null'
#The code will ignore this value when it is found
pinNoPin = -1

#Pin numbers (these will all depend on the hardware wiring)
pinMinFive = 5
pinMinTen = 2
pinMinQuarter = 3
pinMinTwenty = 4
pinMinHalf = 1
pinMinOClock = 13

pinPast = 8
pinTo = 6

pinHourOne = 9
pinHourTwo = 10
pinHourThree = 11
pinHourFour = 12
pinHourFive = 13
pinHourSix = 14
pinHourSeven = 15
pinHourEight = 16
pinHourNine = 16
pinHourTen = 16
pinHourEleven = 16
pinHourTwelve = 16

#All pins (used to clear clock face)
allPins = [pinMinFive, pinMinTen, pinMinQuarter, pinMinTwenty, pinMinHalf,
            pinMinOClock, pinPast, pinTo, pinHourOne, pinHourTwo, pinHourThree,
            pinHourFour, pinHourFive, pinHourSix, pinHourSeven, pinHourEight,
            pinHourNine, pinHourTen, pinHourEleven, pinHourTwelve]
numberOfPins = 20

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

def setup(numberOfPins):
  #Setup all pins as output
  i = 0
  for i in range(0, numberOfPins):
    pinMode(allPins[i], OUTPUT)

  turnOn(minuteSequence[currentMinuteSequenceIndex])
  turnOn(hourPins[currentHourPinIndex])


def loop():
  #Wait 5 minutes = 300sec
  #time.sleep(300)

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

  time.sleep(20)


def turnOn(pins):
  i = 0
  for i in range(0, 3): #Assumed length of 3    
    On(pins[i])

def On(pin):
  print "on : {}".format(pin)
  mcp.output(pin, 1)

def turnOff(pins):
  i=0
  for i in range(0, 3): #Assumed length of 3
    Off(pins[i])

def Off(pin):
  print "off : {}".format(pin)
  mcp.output(pin, 0)


if __name__ == '__main__':

  mcp = ada.Adafruit_MCP230XX(address = 0x20, num_gpios = 16)

  for i in range(0, 16):
    mcp.config(i, mcp.OUTPUT)
  
  loop()
  
