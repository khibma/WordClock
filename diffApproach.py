from Adafruit_I2C import Adafruit_I2C
import Adafruit_MCP230xx as ada
import time
import datetime


#CONSTANTS

#This constant is used as a 'null'
#The code will ignore this value when it is found
pinNoPin = -1

#Pin numbers (these will all depend on the hardware wiring)
pinMinFive = 4
pinMinTen = 1
pinMinQuarter = 2
pinMinTwenty = 3
pinMinHalf = 0
pinMinOClock = 13

pinPast = 7
pinTo = 6
pinMinutes = 5

pinHourOne = 15
pinHourTwo = 14
pinHourThree = 13
pinHourFour = 12
pinHourFive = 11
pinHourSix = 10
pinHourSeven = 9
pinHourEight = 8
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

hours = {1:pinHourOne,
         2:pinHourTwo,
         3:pinHourThree,
         4:pinHourFour,
         5:pinHourFive,
         6:pinHourSix,
         7:pinHourSeven,
         8:pinHourEight,
         9:pinHourNine,
         10:pinHourTen,
         11:pinHourEleven,
         12:pinHourTwelve}

#The hour pins array gives the order that the pins need to be lit up.
#(Length: 12)
hourPins= [pinHourOne, pinHourTwo, pinHourThree, pinHourFour, pinHourFive,
           pinHourSix, pinHourSeven, pinHourEight, pinHourNine, pinHourTen,
           pinHourEleven, pinHourTwelve]

numberOfHourPins = 12

def AllOff():
    for j in range(0, 16):
        mcp.output(j, 0)

def On(pins):
    for pin in pins:
        print "on : {}".format(pin)
        mcp.output(pin, 1)


def Off(pins):
    for pin in pins:
        print "off : {}".format(pin)
        mcp.output(pin, 0)


if __name__ == '__main__':

    mcp = ada.Adafruit_MCP230XX(address = 0x20, num_gpios = 16)

    for i in range(0, 16):
        mcp.config(i, mcp.OUTPUT)



    while True:
        now =datetime.datetime.time(datetime.datetime.now())

        print now
        m =  now.minute
        h =  now.hour
        s =  now.second
        m = float(m)+(s/100)
        print m

        if m > 30:
            h += 1
        if h > 12:
            h = h -12
        print h,m,s

        if m >2.5 and m< 7.5:
            AllOff()
            On([pinMinFive, pinMinutes, pinPast, hours[h]])
        if m >7.5 and m< 12.5:
            AllOff()
            On([ pinMinTen, pinMinutes, pinPast, hours[h]])
        if m >12.5 and m< 17.5:
            AllOff()
            On([ pinMinQuarter, pinPast, hours[h]])
        if m >17.5 and m< 22.5:
            AllOff()
            On([ pinMinTwenty, pinMinutes, pinPast, hours[h]])
        if m >22.5 and m< 27.5:
            AllOff()
            On([ pinMinTwenty, pinMinFive, pinMinutes, pinPast, hours[h]])
        if m >27.5 and m< 32.5:
            AllOff()
            On([ pinMinHalf, pinPast, hours[h]])
        if m >32.5 and m< 37.5:
            AllOff()
            On([ pinMinTwenty, pinMinFive, pinMinutes, pinTo, hours[h]])
        if m >37.5 and m< 42.5:
            AllOff()
            On([ pinMinTwenty, pinMinutes, pinTo, hours[h]])
        if m >42.5 and m< 47.5:
            AllOff()
            On([pinMinQuarter, pinTo, hours[h]])
        if m >47.5 and m< 52.5:
            AllOff()
            On([ pinMinTen, pinMinutes, pinTo, hours[h]])
        if m >52.5 and m< 57.5:
            AllOff()
            On([ pinMinFive, pinMinutes, pinTo, hours[h]])
        if m >57.5 or m<2.5:
            AllOff()
            On([  hours[h]])


        time.sleep(20)