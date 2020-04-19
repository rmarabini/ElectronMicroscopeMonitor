import spidev
import time
import numpy as np
import sys
import matplotlib.pyplot as plt

import adxl355_pi.adxl355 as adxl355
from log_base import log_values
from sensitive_data import (MIC, RASPB)
from log_base import log_values, log_multiple_values
from constants import (MEASUREMENTVIBRAFFT, MEASUREMENTVIBRA)

DEBUG = False

def getData(mtime, rate, acc):
    """ read data fro adxl355 accelerometer
        mtime: get data during this seconds
        rate: number of samples per second
        acc: adxl355 handler
    """
    acc.start()  # start probe
    time.sleep(1) # wait 1 sec before accesing probe
    datalist = [] # store measssurement here 
    msamples = mtime * rate  # total number of samples
    mperiod = 1.0 / rate # sampleach each mperiod seconds

    datalist = []  # samples are stored here

    if DEBUG:
        start_time=time.time()
    acc.emptyfifo() # adxl has a small buffer clean it
    
    # loop to retrieve meassurement, we must use len(datalist) instead a counter
    # beacuse a single call to the adxl Rwill retreave all the meassurement stored 
    # in the buffer
    while(len(datalist) < msamples):
        # complain if the adxl buffer is full and therefore some data is lost
        if DEBUG:
            if acc.fifooverrange():
                print("The FIFO overrange bit was set. That means some data was lost.\n"
                      "Consider slower sampling. Or faster host computer.")
        # if new data retrieve it
        if acc.hasnewdata():
            datalist += acc.get3Vfifo()
    
    if DEBUG:
        elapsed_time = time.time() - start_time
        print("elapsed_time", elapsed_time)
    
    # The get3Vfifo only returns raw data. That means three bytes per coordinate,
    # three coordinates per data point. Data needs to be converted first to <int>,
    # including, a twocomplement conversion to allow for negative values.
    # Afterwards, values are converted to <float> g values.
    
    # Convert the bytes to <int> (including twocomplement conversion)
    rawdatalist = acc.convertlisttoRaw(datalist)
    # Convert the <int> to <float> in g
    gdatalist = acc.convertRawtog1D(acc.convertlisttoRaw(datalist))
    
    # copy second element into first one since the first
    # meassurement is always undervalued
    gdatalist[0] = gdatalist[1]
    
    # Compute Fourier transform
    # convert to np array
    alldatanp = np.array(gdatalist)
    f = np.fft.rfft(alldatanp, norm="ortho")  # rfftn The n-dimensional FFT of real input.
                                              # norm = ortho -> normalize by 1/sqrt(N)
    f[0] = f[1]  # better visualization 
    #fft_fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log( 1. + np.abs(f))
    acc.stop()
    return   magnitude_spectrum, alldatanp
    
    
################################################################################
# Some values for the recording                                                #
################################################################################
# Measurement time in seconds
mtime = 1  # sec
# Data rate, only some values are possible. All others will crash
# possible: 4000, 2000, 1000, 500, 250, 125, 62.5, 31.25, 15.625, 7.813, 3.906 
#rate = 250 # do not go over 250, since pi does not handle higher speeds
rate = 125 # do not go over 250, since pi does not handle higher speeds
goodValue = {31.25: 0.1,
             62.5:  0.1,
             125:   0.07, 
             250:   0.05, 
	     500:   0.035}

counter = 0
while counter < 5:
    ################################################################################
    # Initialize the SPI interface                                                 #
    ################################################################################
    spi = spidev.SpiDev()
    bus = 0
    #device = 0  # CE0
    device = 1  # CE1
    spi.open(bus, device)
    spi.max_speed_hz = 3900000
    spi.mode = 0b00 #ADXL 355 has mode SPOL=0 SPHA=0, its bit code is 0b00
    
    ################################################################################
    # Initialize the ADXL355                                                       #
    ################################################################################
    acc = adxl355.ADXL355(spi.xfer2)
    acc.setrange(adxl355.SET_RANGE_2G) # set range to 2g
    acc.setfilter(hpf=0b00, lpf = adxl355.ODR_TO_BIT[rate]) # set data rate
    	      
    
    ################################################################################
    # Record data                                                                  #
    ################################################################################
    
    magnitude_spectrum, alldatanp = getData(mtime, rate, acc)
    print(time.time(), counter, magnitude_spectrum[0])
    if DEBUG:
        print(alldatanp)
        print(magnitude_spectrum[0], goodValue[rate], counter)
    if magnitude_spectrum[0] > goodValue[rate]:
        break
    time.sleep(1)
    counter += 1

if DEBUG:
    print("after while")

# Plot fourier transform
# compute frequencies
freqs = np.fft.rfftfreq(len(alldatanp)) * rate
if DEBUG:
    fig1, ax1 = plt.subplots()
    ax1.plot(freqs, magnitude_spectrum)
    ax1.set_xlabel('Frequency in Hertz [Hz]')
    plt.show()


# log values FFT
fields = []
for freq, mag in zip(freqs, magnitude_spectrum):
    field={}
    field['log_abs_fft'] = mag
    field['freqs'] = freq
    fields.append(field)  
    
# dictionary with  indexable values
tags={"microscope" : MIC,
      "probeHost"  : RASPB,
      }
log_multiple_values(tags, fields, MEASUREMENTVIBRAFFT)

# log values VIB
fields={}
fields['min']  = min(alldatanp)
fields['max']  = max(alldatanp)
fields['avg']  = np.mean(alldatanp)
fields['std']  = np.std(alldatanp)
fields['diff'] = fields['max'] - fields['min']
tags={"microscope" : MIC,
      "probeHost"  : RASPB}

# store data in database
log_values(tags, fields, MEASUREMENTVIBRA)

 
      
if DEBUG:
    print("done")



# if plotting is done you need to install
# sudo apt-get install libopenjp2-7
# sudo apt-get install python3-tk
# sudo pip3 install matplotlib
