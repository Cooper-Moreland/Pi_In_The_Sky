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