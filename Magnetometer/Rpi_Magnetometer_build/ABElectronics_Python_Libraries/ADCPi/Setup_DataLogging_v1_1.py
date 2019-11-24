#!/usr/bin/python

# Code to write out values to screen as quickly as psossible
# to allow the sensor head to be correctly aligned. Does not save any data
# modified by Ciaran Beggan 
# 14-Jan-2015: initial code 
# 27-Jul-2015: added in code to read and record temperature from TMP36 sensor

import time, datetime, signal, sys, math, numpy
from datetime import date, timedelta
from time import strftime, gmtime
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers


def signal_handler(signal, frame):
        print ('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

# Initialise the ADC device using the default addresses and sample rate, change this value if you have changed the address selection jumpers
# Sample rate can be 12,14, 16 or 18
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 12)


# Create empty arrays
x = [0,0,0,0,0,0,0,0]
y = [0,0,0,0,0,0,0,0]
z = [0,0,0,0,0,0,0,0]
f = [0,0,0,0,0,0,0,0]
c = [0,0,0,0,0,0,0,0]


currentTime = time.gmtime
currentDay  = currentTime()[2]
currentMonth= currentTime()[1]
# Run until killed by Ctrl-C
while 1:
        # Read in 8 values, average, call the time and record to file
        for i in range(len(x)):
                # Read channels in single-ended mode using the settings above
                x[i] = (adc.read_voltage(1) ) * 50000
                y[i] = (adc.read_voltage(2) ) * 50000
                z[i] = (adc.read_voltage(3) ) * 50000
		# Channel 4 is temperature
		c[i] = (adc.read_voltage(4) - 0.5) * 100
                sum = (x[i]*x[i] + y[i]*y[i] + z[i]*z[i])
                f[i] = math.sqrt(sum)
                #print i, x[i], y[i], z[i], f[i]

        x_out = numpy.mean(x)
        y_out = numpy.mean(y)
        z_out = numpy.mean(z)
        f_out = numpy.mean(f)
	c_out = numpy.mean(c)
        t = time.gmtime
        print t()[0], t()[1], t()[02], t()[3], t()[4], t()[5],  x_out, y_out, z_out, f_out, c_out
        
       
