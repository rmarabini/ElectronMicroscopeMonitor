#!/usr/bin/python3

try:
    from bayeosraspberrypi.mcp3424 import MCP3424
    from bayeosraspberrypi.i2c import I2C
except:
    print("bayeosraspberrypi package is needed")
import time
import os
import numpy
import math

"""
This demo is inspired by
https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/

Initialise the ADC device using the default addresses and sample rate, 
change this value if you have changed the address selection jumpers.
Sample rate can be 12, 14, 16 or 18 bit.

requires bayeosraspberrypi package

The MCP3424 is a four channel low-noise, high accuracy delta-sigma 
A/D converter with differential inputs and up to 18 bits of resolution. 
The on-board precision 2.048V reference voltage enables an input range 
of 2.048V differentially. The device uses a two-wire I2C compatible 
serial interface and operates from a single power supply ranging from 
2.7V to 5.5V. The MCP3424 device performs conversions at rates of 3.75, 
15, 60 or 240 samples per second depending on user controllable 
configuration bit settings using the two-wire I2C compatible serial 
interface. The I2C address is user configurable with two address 
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

"""
LSB resolution (mV) 	resolution (nT) 	DataRate (SPS) 	rate
1                         50                      240            12
0.25                      12.3                     60            14
0.0625                     3.1                     15            16
0.0156                     1.56                     3.75         18
"""
rate = 16
adc = MCP3424(bus, address=0x6E, rate=rate)
adc.set_conversion_mode(1) #  1 = Continuous conversion mode

timeout = time.time() + 1*15    # 2 sec loop
#timeout = time.time() + 60*1   # 1 minute loop

num_list2 = []

while True:
    # read from adc channels and print to screen
    # 1 V -> 50,000 nT
#    magField = adc.read_voltage(2) * 50000
#    print 
#    print ("Channel 1: %02f" % adc.read_voltage(1))
#    print ("Channel 2: %02f" % adc.read_voltage(2))
#    print ("Channel 3: %02f" % adc.read_voltage(3))
#    print ("Channel 4: %02f\n" % adc.read_voltage(4))
    magFieldX = adc.read_voltage(2) * 50000
##    magFieldY = adc.read_voltage(3) * 50000
##    magFieldZ = adc.read_voltage(4) * 50000
##    magField = math.sqrt(magFieldX*magFieldX +
##                         magFieldY*magFieldY +
##                         magFieldZ*magFieldZ)
##
    magField = magFieldX
    num_list2.append(magField)
##    time.sleep(1.0)
##    print("magField=%f"% magField)
    if time.time() > timeout:
        break

factor = 1.0
if rate == 12:
    factor = 50.
elif rate == 14:
    factor = 12.3
elif rate == 16:
    factor = 3.1
elif rate == 18:
    factor = 1.56
factor = 1.0

num_list = num_list2
##num_list = [ ((i//factor) * factor) for i in num_list2]
	
##for number in num_list: 
##    print("%0.2f  "% number, end='')

min = min(num_list)
max = max(num_list)
avg = numpy.mean(num_list)
std = numpy.std(num_list)
print("len =", len(num_list)) 


print(min, max, avg, std)
import matplotlib.pyplot as plt
plt.plot(num_list)
plt.ylabel('some numbers')
plt.show()
