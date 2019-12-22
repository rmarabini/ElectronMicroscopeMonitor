#!/usr/bin/env python3
# this file is executed by a crontab and saves the magnetic field each
# minute in a the temporal series database fluxdb
#
# adquires data during 60 decs and stores, mean. min. max, stvdev
# crontab command
#* * * * *  python3 /home/pi/temp_sensor/rpiWebServer/mag_log_influxdb.py

from constants import (dictSensors, MIC, RASPB, MEASUREMENTMAG)
from log_base import log_values
DEBUG=True

try:
    from bayeosraspberrypi.mcp3424 import MCP3424
    from bayeosraspberrypi.i2c import I2C
except:
    print("bayeosraspberrypi package is needed")
import time
import numpy

"""
The MCP3424 is a four channel low-noise, high accuracy delta-sigma 
A/D converter with differential inputs and up to 18 bits of resolution. 
The on-board precision 2.048V reference voltage enables an input range 
of ±2.048V differentially. The device uses a two-wire I2C™ compatible 
serial interface and operates from a single power supply ranging from 
2.7V to 5.5V. The MCP3424 device performs conversions at rates of 3.75, 
15, 60 or 240 samples per second depending on user controllable 
configuration bit settings using the two-wire I2C™ compatible serial 
interface. The I2C™ address is user configurable with two address 
selection pins. This device has an onboard programmable gain amplifier 
(PGA). User can select the PGA gain of x1, x2, x4, or x8 before the 
analog-to-digital conversion takes place. This allows the MCP3424 
device to convert a smaller input signal with high resolution. 
The device has two conversion modes: (a) Continuous mode and 
(b) One-Shot mode. In One-Shot mode, the device enters a low current 
standby mode automatically after one conversion. This reduces current 
consumption greatly during idle periods. The MCP3424 device can be 
used for various high accuracy analog-to-digital data conversion 
applications where ease of use, low power consumption and small 
footprint are major considerations.
"""

i2c_instance = I2C()
bus = i2c_instance.get_smbus()

adc = MCP3424(bus, address=0x68, rate=18)

timeout = time.time() + 60*1   # 1 minute loop

num_list = []

while True:
    # read from adc channels and print to screen
    # 1 V -> 50,000 nT
    magField = adc.read_voltage(1) * 50000
    # print ("Channel 2: %02f\n" % adc.read_voltage(2))
    # print ("Channel 3: %02f" % adc.read_voltage(3))
    # print ("Channel 4: %02f" % adc.read_voltage(4))
    num_list.append(magField)
    time.sleep(1.0)
    print(".", end = '', flush=True)
    if time.time() > timeout:
        break
print("")
min = min(num_list)
max = max(num_list)
avg = numpy.mean(num_list)
std = numpy.std(num_list)
diff = max - min

print(min, max, avg, std, diff)
fields={}
fields['min'] = min
fields['max'] = max
fields['std'] = std
fields['diff'] = diff

# dictionary with  indexable values
tags={"microscope" : MIC,
      "probeHost"  : RASPB}

# store data in database
log_values(tags, fields, MEASUREMENTMAG)

