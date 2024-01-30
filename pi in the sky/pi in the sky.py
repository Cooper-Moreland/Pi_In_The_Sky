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