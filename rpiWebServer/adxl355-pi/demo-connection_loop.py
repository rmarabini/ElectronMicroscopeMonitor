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
device = 0
spi.open(bus, device)
spi.max_speed_hz = 5000000
spi.mode = 0b00 #ADXL 355 has mode SPOL=0 SPHA=0, its bit code is 0b00

################################################################################
# Initialize the ADXL355                                                       #
################################################################################
acc = adxl355.ADXL355(spi.xfer2)
acc.start()

# Print some info
acc.dumpinfo()
time.sleep(1)

while True:
  #print("Temperature ADC value: {:d}".format(acc.temperatureRaw()))
  print("Temperature in Celsius: {:.2f}".format(acc.temperature()))
  print("Ac--: ", np.linalg.norm(acc.get3V()))
  time.sleep(1)

