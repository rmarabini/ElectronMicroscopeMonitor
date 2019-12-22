#!/usr/bin/python

from mcp3424 import MCP3424
from i2c import I2C
import time
import os

"""
This demo is inspired by
https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/

Initialise the ADC device using the default addresses and sample rate, 
change this value if you have changed the address selection jumpers.
Sample rate can be 12, 14, 16 or 18 bit.
"""

i2c_instance = I2C()
bus = i2c_instance.get_smbus()

adc = MCP3424(bus, address=0x68, rate=18)

while (True):
    # clear the console
    # os.system('clear')

    # read from adc channels and print to screen
    print ("Channel 1: %02f %02f\n" % (adc.read_voltage(1) , adc.read_voltage(1) * 50000))
    # print ("Channel 2: %02f\n" % adc.read_voltage(2))
    # print ("Channel 3: %02f" % adc.read_voltage(3))
    # print ("Channel 4: %02f" % adc.read_voltage(4))
 
    # wait 0.5 seconds before reading the pins again
    time.sleep(1.0)
