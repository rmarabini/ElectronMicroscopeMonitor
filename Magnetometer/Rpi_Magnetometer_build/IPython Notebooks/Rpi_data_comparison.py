# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 21:11:00 2015

@author: CDB
"""

# This is a tutorial sheet to load in some data from the Raspberry Pi (RPi) magnetometer, compare it to data from a BGS observatory and then apply a temperature correction to the RPi data.
# The magnetic field measured by the sensors are strongly affected by changes in temperature - about 4 nanoTesla per degree. If the RPi magnetometer is running in a room without temperature control (e.g. air conditioning or heating), or sitting on a window ledge in the open sun, then the measurements recorded can be affected by changes from both the change of the Earth's magnetic field and how the sensors themselves react to warming or cooling.
# 
# The Raspberry Pi data were recorded in Edinburgh on the 29-Aug-2015 in an open room, with sunlight shining on the sensor from around 13.00--19.00, causing a rise in temperature of around 10 degrees C. The GDAS data were recorded in Eskdalemuir Observatory in the Scottish Borders. This sensor sits in a temperature controlled underground vault where the variation is less than 0.1 degrees over a day.
# 
# Notebook Author: Ciaran Beggan [ciar@bgs.ac.uk]
# 
# Date created: 02-Sep-2015
# 
# Date last modified: 02-Sep-2015
# 
# v0: Initial tutorial

# <headingcell level=2>

# Initialise the Notebook - load useful modules

# <codecell>

import sys
import pandas as pd
import os.path as pth
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# <headingcell level=2>

# RPi: Load data and plot Horizontal component

# <codecell>

DATA_DIR =r'/Users/ciaran/Documents/work/Rpi_code/IPython Notebooks'
DATA_FILENAME = 'MagData_29_Aug_2015.dat'

''' The RPi data file contains 11 columns. The first six are the time units (year, month, day, hour, minute, second)
the next three (X,Y,Z) are the orthogonal components of the magnetic field in SI units of nanoTesla (nT).
The tenth column is the computed total field strength (F) in nanoTesla and the final column is the temperature in degrees Celsuis '''

DATA_COL_NAMES = ['year', 'month', 'day', 'hour', 'minute', 'second', 'x', 'y', 'z', 'f', 'temperature']
TIME_COLS = ['year', 'month', 'day', 'hour', 'minute', 'second']  
data_file = pth.join(DATA_DIR, DATA_FILENAME)

# Define a small function to turn the six time columns into the Python 'datetime' number
def minutely_date_parser(year, month, day, hour, minute, second):
    from datetime import datetime
    year, month, day, hour, minute, second = [int(x) 
                     for x in [year, month, day, hour, minute, second]]
    return (datetime(year, month, day, hour, minute, second))

# Read in the Rpi data using Comma Separated Value (CSV) in the Pandas module
Rpi_data = pd.read_csv(data_file,
                   delim_whitespace=True,
                   names = DATA_COL_NAMES,                       
                   parse_dates={'datetime':TIME_COLS},
                   date_parser = minutely_date_parser,
                   index_col='datetime')

# Display some values from the file
Rpi_data[1:10]

# <markdowncell>

# Plot out the Horizontal variation of $H = \sqrt(X^2 + Y^2)$ of the Raspberry Pi data. The 29-Aug-2015 was a relatively active data geomagnetically speaking with a large slow change of around 80 nT between 09:00 and 20:00. 
# 
# There are also more rapid variations over several minutes to hours. These are typically caused by <i> magnetospheric pulsations </i> or <i>auroral electrojet activity</i> at higher latitudes.

# <codecell>

Rpi_H = np.sqrt(Rpi_data.x**2 + Rpi_data.y**2)    

fig = plt.figure()
plt.plot(Rpi_data.index, Rpi_H)
plt.ylabel(' Strength [nT]')
plt.xlabel('Time')
plt.title('RPi Horizontal: 29-Aug-2015')

# <headingcell level=2>

# GDAS: Load data and plot Horizontal component

# <markdowncell>

# The GDAS (Geomagnetic Data Acquisition System) data comes from the BGS scientific observatory instruments at Eskdalemuir. These instruments operate in temperature controlled environments and record the data in picoTesla (pT), which are very small units of measurement: 1000 pT = 1 nT. The original file format has been converted to match that of the Rpi format above.

# <codecell>

DATA_DIR =r'/Users/ciaran/Documents/work/Rpi_code/IPython Notebooks'
DATA_FILENAME = 'Esk_29_Aug_2015.dat'

''' The GDAS data file contains 9 columns. The first six are the time units (year month day hour minute second)
the next three (H,E,Z) are the orthogonal components of the magnetic field in SI units of nanoTesla (nT).'''

DATA_COL_NAMES = ['year', 'month', 'day', 'hour', 'minute', 'second', 'h', 'e', 'z']
TIME_COLS = ['year', 'month', 'day', 'hour', 'minute', 'second']  
data_file = pth.join(DATA_DIR, DATA_FILENAME)

# Define a small function to turn the six time columns into the Python 'datetime' number
def minutely_date_parser(year, month, day, hour, minute, second):
    from datetime import datetime
    year, month, day, hour, minute, second = [int(x) 
                     for x in [year, month, day, hour, minute, second]]
    return (datetime(year, month, day, hour, minute, second))

# Read in the Rpi data using Comma Separated Value (CSV) in the Pandas module
GDAS_data = pd.read_csv(data_file,
                   delim_whitespace=True,
                   names = DATA_COL_NAMES,                       
                   parse_dates={'datetime':TIME_COLS},
                   date_parser = minutely_date_parser,
                   index_col='datetime')
# Display some values from the file
GDAS_data[1:10]

# <markdowncell>

# Plot the Horizontal variation of the GDAS data. Note this is not the full Horizontal component (like that measured with the Rpi) - this is the variation of the horizontal field strength over the day about some arbitrary mean value.

# <codecell>

GDAS_H = (GDAS_data.h)    

fig = plt.figure()
plt.plot(GDAS_data.index, GDAS_H)
plt.ylabel(' Strength [nT]')
plt.xlabel('Time')
plt.title('GDAS Esk Horizontal: 29-Aug-2015')

# <markdowncell>

# Oh dear ... at first inspection these datasets are broadly similar but not exactly identical. Note the different size of the peaks for example. Why are they so different? Let's remove the mean value from each dataset and plot them alongside one another on the same graph to see where the discrepancies are.

# <codecell>

Rpi_H_zm = Rpi_H - np.mean(Rpi_H)
GDAS_H_zm = GDAS_H - np.mean(GDAS_H)
len(GDAS_H)

fig = plt.figure()
plt.hold(True)
plt.plot(GDAS_data.index, GDAS_H_zm, color='blue', linestyle='none', marker='.',markersize=2)
plt.plot(Rpi_data.index, Rpi_H_zm, color='red', linestyle='none', marker='.',markersize=2)
         
plt.ylabel(' Strength [nT]')
plt.xlabel('Time')
plt.title('GDAS_H vs Rpi Horizontal: 29-Aug-2015')
plt.legend(['GDAS', 'RPi'], loc=2)

# <markdowncell>

# The red line is clearly above the blue line during the afternoon period of the day. Now, let's plot out the temperature recorded by the sensor to see if there is any correlation with the <i> difference </i> between the Raspberry Pi data and the Eskdalemuir data.
# 
# To plot the difference between Eskdalemuir and the Raspberry Pi data, we wil have to interpolate the Raspberry Pi measurements to the same time points as the Eskdalemuir data.

# <codecell>

# Compute the Differences between Raspberry Pi and Eskdalemuir data by interpolation of the RPi data to 1-second time points
Rpi_data_sec = Rpi_data.resample('S', fill_method='bfill', how='last')
Rpi_data_sec_H = np.sqrt(Rpi_data_sec.x**2 + Rpi_data_sec.y**2)  
Rpi_data_sec_H_zm =  Rpi_data_sec_H - np.mean(Rpi_data_sec_H)  
H_diff =  GDAS_H_zm -   Rpi_data_sec_H_zm

# <codecell>

fig = plt.figure(9)
# Temperature
plt.plot(Rpi_data_sec.index, Rpi_data_sec.temperature, color='gray', linestyle='none', marker='.',markersize=2)
plt.hold(True)
plt.plot(Rpi_data_sec.index, H_diff[0:len(Rpi_data_sec.index)], color='black', linestyle='none', marker='.',markersize=2)
         
plt.ylabel(' Temperature [$^\circ$C] / Difference [nT]')
plt.xlabel('Time')
plt.title('Data: 29-Aug-2015')



# <markdowncell>

# There is clearly a correlation between the difference in variation between the 

#A = [ones(length(Esk_interp_s),1) Temperature_s-min(Temperature_s) (Temperature_s-min(Temperature_s)).^2  ];
#sc_off = A\(Esk_interp_s - (MagPi_H_s - mean(MagPi_H_s)))
Temp_rm = Rpi_data_sec.temperature - np.mean(Rpi_data_sec.temperature)
temp_nomean = Temp_rm.values

A = np.array([temp_nomean**2, temp_nomean, np.ones(len(temp_nomean ))])
d = np.transpose(H_diff.values[0:len(temp_nomean)])
x = np.linalg.lstsq(np.transpose(A), d)

sc_off = x[0]   # Store the first array from x - offset and scaling coefficients 

print '   Correction coefficients [nT]    '
print '  2nd Order      Linear     Offset'
print sc_off

# Now plot a corrected version of the RPi data/

Rpi_H_regress = Rpi_data_sec_H_zm  + sc_off[0]*(temp_nomean)**2 + sc_off[1]*(temp_nomean) + sc_off[2]

fig = plt.figure(10)
plt.hold(True)
plt.plot(Rpi_data_sec.index, Rpi_data_sec_H_zm, color='black', linestyle='none', marker='.',markersize=2)
plt.plot(GDAS_data.index, GDAS_H_zm, color='blue', linestyle='none', marker='.',markersize=2)

plt.plot(Rpi_data_sec.index, Rpi_H_regress, color='green', linestyle='none', marker='.',markersize=2)
         
plt.legend(['RPi H', 'GDAS H', 'Corrected RPi H'], loc=2)
plt.xlabel('Time')
plt.ylabel('[nT]')
plt.title('Temperature Corrected RPi data: 29-Aug-2015')
