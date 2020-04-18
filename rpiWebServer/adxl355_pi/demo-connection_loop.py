import spidev
import time
import numpy as np
import sys

import adxl355

################################################################################
# Initialize the SPI interface                                                 #
################################################################################
spi = spidev.SpiDev()
bus = 0
device = 1 # pin 26 -> CE1
spi.open(bus, device)
spi.max_speed_hz = 5000000
spi.mode = 0b00 #ADXL 355 has mode SPOL=0 SPHA=0, its bit code is 0b00

################################################################################
# Initialize the ADXL355                                                       #
################################################################################
acc = adxl355.ADXL355(spi.xfer2)
acc.start()
time.sleep(1)
acc.setrange(adxl355.SET_RANGE_2G) # set range to 2g
rate = 31.25 # do not go over 250, since pi does not handle higher speeds
acc.setfilter(hpf=0b00, lpf = adxl355.ODR_TO_BIT[rate]) # set data rate

# Print some info
acc.dumpinfo()
time.sleep(1)

while True:
    #if acc.fifooverrange():
    #    print("The FIFO overrange bit was set. That means some data was lost.")
    #    print("Consider slower sampling. Or faster host computer.")
    if acc.hasnewdata():
        print("Temperature in Celsius: {:.2f}".format(acc.temperature()))
        print("Ac--: ", np.linalg.norm(acc.get3V()))
        print("Ac--: ", acc.get3V())
    #time.sleep(1)

