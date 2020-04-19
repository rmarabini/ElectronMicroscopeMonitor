#!/usr/bin/env python3
# this file is executed by a crontab and saves the magnetic field each
# minute in a the temporal series database fluxdb
#
# adquires data during 60 decs and stores, mean. min. max, stvdev
# crontab command
#* * * * *  python3 /home/pi/temp_sensor/rpiWebServer/mag_log_influxdb.py

from constants import (dictSensors, MEASUREMENTMAG)
from sensitive_data import (MIC, RASPB)
from log_base import log_values
DEBUG=False

try:
    from bayeosraspberrypi.mcp3424 import MCP3424
    from bayeosraspberrypi.i2c import I2C
except:
    print("bayeosraspberrypi package is needed")
import time
import numpy
import math
import signal, os
import datetime

def handler(signum, frame):
    print('Magnetic sensor script did not finish in 55 seconds!!!', signum)
    raise IOError("Aborting mag_log_inplux script")
    
# Set the signal handler and a 5-second alarm
TIMEOUT = 50
signal.signal(signal.SIGALRM, handler)
signal.alarm(TIMEOUT + 5)


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

try:
    adc = MCP3424(bus, address=0x6E, rate=18)
except:
    currentDT = datetime.datetime.now()
    print(str(currentDT), "Can not connect to magnetic sensor")
    exit(0)

timeout = time.time() + TIMEOUT   # 1 minute loop I do not set this to 60
                                  # because They should not be 2 scripts
                                  # running at the same time
				  # if script did not finish in TIMEOUT +5 sec
				  # abort

num_list = []
magFieldX = 0.
magFieldY = 0.
magFieldZ = 0.
# counter=0
while True:
    # print("counter = %d"% counter); counter += 1
    # 1 V -> 50,000 nT
    magFieldX = adc.read_voltage(2) * 50000
    magFieldY = adc.read_voltage(3) * 50000
    magFieldZ = adc.read_voltage(4) * 50000
    magField = math.sqrt(magFieldX*magFieldX +
                         magFieldY*magFieldY +
                         magFieldZ*magFieldZ)
    num_list.append(magField)

    if time.time() > timeout:
        break
    time.sleep(1.0)
    # print("end")

fields={}
fields['min']  = min(num_list)
fields['max']  = max(num_list)
fields['avg']  = numpy.mean(num_list)
fields['std']  = numpy.std(num_list)
fields['diff'] = fields['max'] - fields['min']

# dictionary with  indexable values
tags={"microscope" : MIC,
      "probeHost"  : RASPB}

# store data in database
log_values(tags, fields, MEASUREMENTMAG)
signal.alarm(0) # cancel alarm
