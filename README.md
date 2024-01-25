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

## images

## materials_used

* raspberry pico
* battery
* altimeter
* panel mount switch
* panel mount led
* acrylic
* 3D print material

## wiring_diagram

![1](https://github.com/Cooper-Moreland/Pi_In_The_Sky/blob/main/pi_in_the_sky_wiring_diagram.png?raw=true)

![1](https://github.com/Cooper-Moreland/Pi_In_The_Sky/blob/main/pi_body_2.png?raw=true)

## [code](https://github.com/Cooper-Moreland/Pi_In_The_Sky/blob/main/pi%20in%20the%20sky/pi%20in%20the%20sky.py)

```python
# type: ignore
# libraries: adafruit_mpu6050.mpy | adafruit_bus_device | adafruit_register
import adafruit_mpl3115a2 # replace everything with this device
import busio
import board
import time
import displayio 
import digitalio
import storage # imports

displayio.release_displays() # this needs to be first in the code

led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT
sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin) 
sensor = adafruit_mpl3115a2.MPL3115A2(i2c) # set up for variables and pin locations

sensor.sealevel_pressure = 1011.42 
# standard pressure is 1013.25 hPa set this to however much gives the initial point 0 height
# higher pressure = higher recorded height

while True: 
    altitude = sensor.altitude # new var
    print("Altitude: {0:0.2f} meters".format(altitude)) 
    # print the altitude up to 2 decimal points (0.2f) in the default meters (format(pressure))
    time.sleep(1.0)
    if not storage.getmount("/").readonly: # call back to the boot.py file
        with open("/data.csv", "a") as datalog:
            time_elapsed = time.monotonic() # set time to run normally
            csv_string = f"{time_elapsed},{altitude}\n"
            # f string showing time and altitude
            datalog.write(csv_string) # record f string in separate columns in microsoft excel
            # to switch between data and code mode unplug the pico then flip the switch connected to GP0
            led.value = True
            time.sleep(0.1)
            led.value = False
            time.sleep(0.1) # blink led to show switch between modes
            datalog.flush() # record stuff to the datalog
            time.sleep(1.0)
    else:
        time.sleep(1.0)

```

## obstacles

## tips
