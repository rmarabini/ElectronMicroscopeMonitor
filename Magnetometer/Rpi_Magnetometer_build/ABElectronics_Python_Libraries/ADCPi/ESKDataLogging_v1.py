#!/usr/bin/python

# Code to record daily files 
# Adopted forom Moses' work in Aug 2014
# modified by Ciaran Beggan on 14-Jan-2015

import time, datetime, signal, sys, math, numpy
from datetime import date, timedelta
from time import strftime, gmtime
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers


def signal_handler(signal, frame):
        print ('You pressed Ctrl+C!')
        file1.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

def makefilename(outputdir):
        filename = outputdir + "MagData_" + strftime("%d_%b_%Y",gmtime()) + ".dat"
        return filename


# Setting file storage folder
outputdir = '/home/pi/Rpi_data/'
print makefilename(outputdir)

# Initialise the ADC device using the default addresses and sample rate, change this value if you have changed the address selection jumpers
# Sample rate can be 12,14, 16 or 18
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 18)


# Create empty arrays
x = [0,0,0,0,0,0,0,0]
y = [0,0,0,0,0,0,0,0]
z = [0,0,0,0,0,0,0,0]
f = [0,0,0,0,0,0,0,0]
# Open a file to write out data to once per second
file1 = open(makefilename(outputdir),"a")
#starttime = datetime.datetime.now()
currentTime = time.gmtime
currentDay  = currentTime()[2]
currentMonth= currentTime()[1]
# Run until killed by Ctrl-C
while 1:
        # Read in 8 values, average, call the time and record to file
        for i in range(0,8):
                # Read channels in single-ended mode using the settings above
                x[i] = (adc.read_voltage(1) ) * 50000
                y[i] = (adc.read_voltage(2) ) * 50000
                z[i] = (adc.read_voltage(3) ) * 50000
                sum = (x[i]*x[i] + y[i]*y[i] + z[i]*z[i])
                f[i] = math.sqrt(sum)
                #print i, x[i], y[i], z[i], f[i]

        x_out = numpy.mean(x)
        y_out = numpy.mean(y)
        z_out = numpy.mean(z)
        f_out = numpy.mean(f)
        t = time.gmtime
        print t()[0], t()[1], t()[02], t()[3], t()[4], t()[5],  x_out, y_out, z_out, f_out
        
        # Checking whether the logging time interval has been reached
        '''
        if (starttime + datetime.timedelta(days = 1) <= datetime.datetime.now()):
                file1.close()
                file1 = open(makefilename(outputdir),"a")
                starttime = datetime.datetime.now()
        '''
        
        if (1000 * currentMonth + currentDay + 1 <= 1000 * t()[1] + t()[2]):
                file1.close()
                file1 = open(makefilename(outputdir),"a")
                currentDay = t()[2]
                currentMonth= t()[1]
        

        file1.write('%i %i %i %i %i %i %.2f %.2f %.2f %.2f \n' %  (t()[0], t()[1], t()[2], t()[3], t()[4], t()[5],  x_out, y_out, z_out, f_out))

