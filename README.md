# Pi_In_The_Sky

## Table of Contents

* [overview](#overview)
* [cad renderings](#cad_renderings)
* [images](#images)
* [materials used](#materials_used)
* [wiring diagram](#wiring_diagram)
* [code](#code)
* [obstacles/errors](#obstacles)
* [tips](#tips)

## [planning document](https://docs.google.com/document/d/1hiuoh_CVGpjotOG-Ltabho9DP55JUnkYqFjeEnz9gQs/edit?usp=sharing)

## [onshape document](https://cvilleschools.onshape.com/documents/b313d57e8a07c5155702993d/w/2811ce274d49858bedab9adb/e/824d5d8ea7da9445accad4a9?renderMode=0&uiState=659ee2e4b4bc340ccd11b5aa)

## overview

Our project is based on Angry Birds. There will be a green pig with a crown our projectile (designed as Chuck) will try to hit. Altitude and time will be recorded using an altimeter and the pico will have foam around it to prevent it from breaking on impact. We will make a graph from the data after it's done to show the flight path by recording how far the projectile traveled in the x-direction. Basic physics can be used to find what angle and power to use to land at a specific place.

## cad_renderings

![1](https://github.com/Cooper-Moreland/Pi_In_The_Sky/blob/main/pi_body.png?raw=true)

![1](https://github.com/Cooper-Moreland/Pi_In_The_Sky/blob/main/pi_body_2.png?raw=true)

## images

## materials_used

* raspberry pico
* battery
* altimeter
* panel mount switch
* panel mount led
* acrylic
* 3D print material
* adafruit picowbell
* wires

## wiring_diagram

![1](https://github.com/Cooper-Moreland/Pi_In_The_Sky/blob/main/pi_in_the_sky_wiring_diagram.png?raw=true)

## [code](https://github.com/Cooper-Moreland/Pi_In_The_Sky/blob/main/pi%20in%20the%20sky/pi%20in%20the%20sky.py)

```python
# type: ignore
# libraries: adafruit_mpl3115a2.mpy
import adafruit_mpl3115a2
import busio
import board
import time
import displayio 
import digitalio
import storage # imports

displayio.release_displays() # this needs to be first in the code

led1 = digitalio.DigitalInOut(board.GP16)
led1.direction = digitalio.Direction.OUTPUT
sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin) 
sensor = adafruit_mpl3115a2.MPL3115A2(i2c) # set up for variables and pin locations

sensor.sealevel_pressure = 1005.6
# standard pressure is 1013.25 hPa set this to however much gives the initial point 0 height
start_time = time.monotonic()

while True: 
    time_elapsed = time.monotonic() - start_time # restarts count after rerunning the code
    altitude = sensor.altitude # new var
    print("Altitude: {0:0.3f} meters".format(altitude)) 
    # print the altitude up to 4 decimal points (0.4f) in the default meters (format(altitude))
    time.sleep(0.4)
    with open("/data.csv", "a") as datalog:
        csv_string = f"{time_elapsed},{altitude}\n"
        # f string showing time and altitude
        datalog.write(csv_string) # write the f string out on microsoft excel sheet
        datalog.flush() # record stuff to the datalog
        time.sleep(0.1)

```

## obstacles

I had exact sizing for the laser cut piece that held the pico to slide into the 3d printed rocket but 3d print isn't exact so we had to sand the acrylic to have it fit well. Having to wait for 10 blinks to indicate data mode is annoying, so I changed it to 5 blinks and reduced the total "time.sleep" value for the boot.py file, making the measurement of altitude more consistent. To switch between code and data mode unplug the pico first then flip the switch connected to GP0. The time intervals for each altitude reading aren't exactly a second, I had to change the values of "time.sleep" to make it as accurate as possible. The picowbell seems confusing  but you just solder each pin to the corresponding one on the pico and wire it the exact same as on a regular breadboard.


## tips

leave a hole for the panel mount switch and led and a hole to unplug and replug the pico to fix any mistakes in the code. We left 0.18 inches of diameter in the PVC pipe to fit the styrofoam around. The holes for the screws are 2.8mm to have them have a snug fit so it can hold the cap onto the bottom of chuck/the projectile. [helpful website for the picowbell](https://learn.adafruit.com/picowbell-proto?view=all) which is the attachable breadboard to the pico via soldering. On the altimeter connect power to Vin not 3vo
