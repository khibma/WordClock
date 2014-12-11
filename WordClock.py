#quick, dirty port of https://github.com/jonnyarnold/wordclock/blob/master/inos/wordclock.ino
#hopefully this will work instead of reinventing the wheel

import time
import datetime
#import GPIO

#currentHourPinIndex keeps track of which hour pin (as defined in hourPins) is lit
#0 = "one", 1 = "two", etc.
currentHourPinIndex = 8

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
pinMinTen = 1
pinMinQuarter = 7
pinMinTwenty = 3
pinMinHalf = 8
pinMinOClock = 13

pinPast = 9
pinTo = 2

pinHourOne = 10
pinHourTwo = 4
pinHourThree = 11
pinHourFour = 21
pinHourFive = 23
pinHourSix = 22
pinHourSeven = 19
pinHourEight = 20
pinHourNine = 0
pinHourTen = 18
pinHourEleven = 6
pinHourTwelve = 12

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
  time.sleep(300)

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


def turnOn(pins):
  i = 0
  for i in range(0, 3): #Assumed length of 3
    turnOn(pins[i])

def turnOn(pin):
  digitalWrite(pin, HIGH)

def turnOff(pins):
  i=0
  for i in range(0, 3): #Assumed length of 3
    turnOff(pins[i])

def turnOff(pin):
  digitalWrite(pin, LOW)
