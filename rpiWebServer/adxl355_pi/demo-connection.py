import spidev
import time
import numpy as np
import sys

import adxl355


# reset spi device
# lsmod | grep spi
# sudo rmmod spi_bcm2835
# sudo modprobe spi_bcm2835

################################################################################
# Initialize the SPI interface                                                 #
################################################################################
spi = spidev.SpiDev()
bus = 0
device = 1
spi.open(bus, device)
spi.max_speed_hz = 5000000
spi.mode = 0b00 #ADXL 355 has mode SPOL=0 SPHA=0, its bit code is 0b00

################################################################################
# Initialize the ADXL355                                                       #
################################################################################
acc = adxl355.ADXL355(spi.xfer2)

acc.start()

"""
# acc.setrange(adxl355.SET_RANGE_2G) # set range to 2g, done by default in init
from adxl355 import REG_SELF_TEST, REG_RESET
temp = acc.read(REG_SELF_TEST)
print("self_test_0", bin(temp))
acc.write(REG_SELF_TEST, (temp & 0b11111100) | 0b01)
temp = acc.read(REG_SELF_TEST)
print("self_test_1", bin(temp))
time.sleep(1)
v1 = acc.get3V()
print("Ac--: ", v1)
temp = acc.read(REG_SELF_TEST)
print("self_test_0", bin(temp))
acc.write(REG_SELF_TEST, (temp & 0b11111100) | 0b11)
temp = acc.read(REG_SELF_TEST)
print("self_test_1", bin(temp))
time.sleep(1)
v2 = acc.get3V()
print("Ac--: ", v2)
temp = acc.read(REG_SELF_TEST)
acc.write(REG_SELF_TEST, (temp & 0b11111100) | 0b00)
temp = acc.read(REG_SELF_TEST)
time.sleep(1)
"""


time.sleep(1)

# Print some info
acc.dumpinfo()
time.sleep(1)
#X-Axis .3
#Y .3
#Z 1.5
print("Temperature ADC value: {:d}".format(acc.temperatureRaw()))
print("Temperature in Celsius: {:.2f}".format(acc.temperature()))
print("Ac--: ", acc.get3V())
print("Ac--: ", np.linalg.norm(acc.get3V()))
acc.stop()
#print(np.linalg.norm([0.3, 0.3, 1.5]))
