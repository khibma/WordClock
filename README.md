# WordClock
Raspberry Pi powered WordClock (scroll down for images)

What is a "Word Clock"? Quite simply, it's a clock, with words instead of numbers. You _read_ the time, quite literally, _read_ the time. A quick google search for _wordclock_ will yield images and more descriptions.

This particular project came about after coming across this project on the internet and wanting to "do it myself". I'd consider this just as much "art" as I would "function".

### Size
* 23" x 18"

### Code / Hardware
First: yes, using a raspberry pi with full blown Linux is a way over the top solution to turn LEDs on and off. But this is the direction I took as the Pi is a straight forward platform where I can use Python.

The code isn't anything revolutionary. It simply sleeps in a loop of 5 minute intervals, incrementing a well-defined list. This means the Pi/LEDs have no notion of the actual time. As the RPi does not have an onboard battery, anytime the power is reset the internal clock might be wrong. As I have not devoted a wifi dongle and don't want to login to update the time when it resets, simply starting at "1 O'clock" is easiest with a button to increment time.

The [WC](WC) script calls the [WordClock.py](WordClock.py) file on startup.

### Approximate Cost  ($CDN, prices include tax)
* Raspberry Pi a+ - 35
* Power adapter and USB cord - 13
* Mirco USB card - 10
* Clock face (laser cut stencil on acrylic) - 80
* LED lights, wire, switch, button, solder, protoboard, MCP23007 chip - 15-25?
* Cut black acrylic and solvent - 20
* Wall mounting kit - 10
  * Total: About 190, maybe a bit more
  
Today, this project could be done cheaper:
* Raspberry Pi Zero - 7
* 18x24 Laser cutting at library (cost of acrylic about 40). However 2 pieces of acrlyic, 1 black, 1 clear would have to be used. This would change the look and weight of the clock.
  * This could bring the project from 190 to about 130
  
### Images
Working out the baffles...

![alt tag](https://cloud.githubusercontent.com/assets/2514926/9621430/0c02e5f8-50f4-11e5-8ed6-5106dcc8801b.JPG)

Wiring up the LEDs/resistors 

![alt tag](https://cloud.githubusercontent.com/assets/2514926/9621432/0f70e87a-50f4-11e5-9b3c-e494c9386f48.JPG)

Baffles with reflectors and wiring

![alt tag](https://cloud.githubusercontent.com/assets/2514926/11747311/7ee7ab08-9ff0-11e5-8ad1-0a452347e11c.JPG)

Clock face lit up

![alt tag](https://cloud.githubusercontent.com/assets/2514926/11747309/7d873184-9ff0-11e5-9dcc-b1a8f04d2fc2.JPG)

Clock in action (time sped up)

![alt tag](https://cloud.githubusercontent.com/assets/2514926/9632293/51dce578-5154-11e5-9c76-504c6d0f3b66.gif)

### What I'd do differently
* Research and understand LED brightness and light angle before committing to any single LED. The LEDs I used have a narrow light angle and don't do well to light up a "word compartment".
* I placed the LEDs at a 90* angle to the face, thus I needed to use a 45* reflector. A future version would work better with surface mount LEDs.
* Plan the wiring better. The wiring I have is fine, but I could have cut down on the wiring mess with more planning at the start.
