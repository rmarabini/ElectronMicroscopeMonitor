import spidev
import time
import numpy as np
import sys
import matplotlib.pyplot as plt

import adxl355

################################################################################
# Some values for the recording                                                #
################################################################################
# Filename for output
outfilename = 'output.csv'
# Measurement time in seconds
mtime = 1  # sec
# Data rate, only some values are possible. All others will crash
# possible: 4000, 2000, 1000, 500, 250, 125, 62.5, 31.25, 15.625, 7.813, 3.906 
#rate = 250 # do not go over 250, since pi does not handle higher speeds
rate =  62.5 # do not go over 250, since pi does not handle higher speeds
# under 1.10
#      0.1 -- 125
# 0 -> 0.05 -- 250
#      0.035 - 500
#rate = 3.906

################################################################################
# Initialize the SPI interface                                                 #
################################################################################
spi = spidev.SpiDev()
bus = 0
#device = 0
device = 1
spi.open(bus, device)
spi.max_speed_hz = 3900000
spi.mode = 0b00 #ADXL 355 has mode SPOL=0 SPHA=0, its bit code is 0b00

################################################################################
# Initialize the ADXL355                                                       #
################################################################################
acc = adxl355.ADXL355(spi.xfer2)
acc.start()
time.sleep(1)
acc.setrange(adxl355.SET_RANGE_2G) # set range to 2g
acc.setfilter(hpf=0b00, lpf = adxl355.ODR_TO_BIT[rate]) # set data rate

#ODR_TO_BIT = {4000: SET_ODR_4000,
#              2000: SET_ODR_2000,
#              1000: SET_ODR_1000,
#              500: SET_ODR_500,
#              250: SET_ODR_250,
#              125: SET_ODR_125,
#              62.5: SET_ODR_62_5,
#              31.25: SET_ODR_31_25,
#              15.625: SET_ODR_15_625,
#              7.813: SET_ODR_7_813,
#              3.906: SET_ODR_3_906}
	      

################################################################################
# Record data                                                                  #
################################################################################
datalist = []
t0 = time.time()
tc = time.time()

msamples = mtime * rate
mperiod = 1.0 / rate

datalist = []
#my_list = np.zeros(100)
acc.emptyfifo()

start_time=time.time()

while (len(datalist) < msamples):
    if acc.fifooverrange():
        print("The FIFO overrange bit was set. That means some data was lost.")
        print("Consider slower sampling. Or faster host computer.")
    if acc.hasnewdata():
        datalist += acc.get3Vfifo()
        
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
# meassurement is always low
gdatalist[0] = gdatalist[1]


# PLOT meassurements
# gdatalist2 = acc.convertRawtog1D(acc.convertlisttoRaw(datalist))
# xrange=[]
# for i in range(len(gdatalist2)):
#    xrange.append(i)
# fig2, ax2 = plt.subplots()
# ax2.plot(xrange, gdatalist2)
# print (gdatalist2)
# plt.show()


# Compute Fourier transform
# convert to np array
alldatanp = np.array(gdatalist)
f = np.fft.rfft(alldatanp, norm="ortho")  # rfftn The n-dimensional FFT of real input.
                                          # norm = ortho -> normalize by 1/sqrt(N)
f[0] = f[1]  # better visualization 
#fft_fshift = np.fft.fftshift(f)
magnitude_spectrum = np.log( 1. + np.abs(f))


# Plot fourier transform
# compute frequencies
freqs = np.fft.rfftfreq(len(alldatanp)) * rate
fig1, ax1 = plt.subplots()
ax1.plot(freqs, magnitude_spectrum)
ax1.set_xlabel('Frequency in Hertz [Hz]')
plt.show()

print("done")
# Save it as a csv file    
# np.savetxt(outfilename, magnitude_spectrum, delimiter=",")
#print (gdatalist)
# Add a column with a timestamp
# print("freqs", freqs)
# stop chip
acc.stop()



# sudo apt-get install libopenjp2-7
# sudo apt-get install python3-tk
# sudo pip3 install matplotlib
