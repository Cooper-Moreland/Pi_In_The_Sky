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

led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT
sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin) 
sensor = adafruit_mpl3115a2.MPL3115A2(i2c) # set up for variables and pin locations

sensor.sealevel_pressure = 1019.25
# standard pressure is 1013.25 hPa set this to however much gives the initial point 0 height
start_time = time.monotonic()

while True: 
    time_elapsed = time.monotonic() - start_time
    altitude = sensor.altitude # new var
    print("Altitude: {0:0.4f} meters".format(altitude)) 
    # print the altitude up to 2 decimal points (0.2f) in the default meters (format(pressure))
    time.sleep(0.45)
    if not storage.getmount("/").readonly: # call back to the boot.py file
        with open("/data.csv", "a") as datalog:
            time_elapsed = time.monotonic() - start_time
            csv_string = f"{time_elapsed},{altitude}\n"
            # f string showing time and altitude
            datalog.write(csv_string)
            led.value = True
            time.sleep(0.1)
            led.value = False # blink led to show switch between modes
            datalog.flush() # record stuff to the datalog
            time.sleep(0.45)
    else:
        time.sleep(0.165)