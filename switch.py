import RPi.GPIO as io
import time

io.setmode(io.BCM)
switch = 9
io.setup(switch, io.IN)


while True:

  if io.input(switch):
    print "switch one way"
  else:
    print "switch the other way"

  time.sleep(1)
