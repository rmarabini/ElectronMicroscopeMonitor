import spidev
import time
import numpy as np
import sys

import adxl355

# check for output filename
if len(sys.argv) == 2:
    outfilename = sys.argv[1]
else:
    outfilename = 'output.csv'

# init spi interface
spi = spidev.SpiDev()
bus = 0
device = 0
spi.open(bus, device)
spi.max_speed_hz = 5000000
# important - ADXL 355 has mode SPOL=0 SPHA=0
spi.mode = 0b00

# init adxl355
acc = adxl355.ADXL355(spi.xfer2)

acc.start()

time.sleep(1)
acc.dumpinfo()
time.sleep(1)

print("Temperature ADC value: {:d}".format(acc.temperatureRaw()))
print("Temperature in Celsius: {:.2f}".format(acc.temperature()))


print("Compare different measurement ranges")
acc.setrange(adxl355.SET_RANGE_2G)
while(not acc.hasnewdata()):
    continue
val = acc.getXRaw()
print("2g-x raw value: {:d}".format(val))
print("2g-x value in g: {:f}".format(val * acc.factor))
val = acc.getYRaw()
print("2g-y raw value: {:d}".format(val))
print("2g-y value in g: {:f}".format(val * acc.factor))
val = acc.getZRaw()
print("2g-z raw value: {:d}".format(val))
print("2g-z value in g: {:f}".format(val * acc.factor))

acc.setrange(adxl355.SET_RANGE_4G)
while(not acc.hasnewdata()):
    continue
val = acc.getZRaw()
print("4g raw value: {:d}".format(val))
print("4g value in g: {:f}".format(val * acc.factor))

acc.setrange(adxl355.SET_RANGE_8G)
while(not acc.hasnewdata()):
    continue
val = acc.getZRaw()
print("8g raw value: {:d}".format(val))
print("8g value in g: {:f}".format(val * acc.factor))


acc.setrange(adxl355.SET_RANGE_2G) # reset to 2G
acc.setfilter(lpf = adxl355.SET_ODR_2000)


acc.setrange(adxl355.SET_RANGE_2G) # reset to 2G
# set data rate (with low pass filter settings)
acc.setfilter(lpf = adxl355.SET_ODR_4000)
# collecting samples
acc.emptyfifo()
t0 = time.time()
sampleno = 2000
data = acc.fastgetsamples(sampleno)
t1 = time.time()
print("Collected {:d} samples in {:f} seconds, {:f} samples/s".format(sampleno, t1 - t0, sampleno / (t1 - t0)))

# set data rate (with low pass filter settings)
acc.setfilter(lpf = adxl355.SET_ODR_2000)
# collecting samples
acc.emptyfifo()
t0 = time.time()
sampleno = 1000
data = acc.fastgetsamples(sampleno)
t1 = time.time()
print("Collected {:d} samples in {:f} seconds, {:f} samples/s".format(sampleno, t1 - t0, sampleno / (t1 - t0)))

# set data rate (with low pass filter settings)
acc.setfilter(lpf = adxl355.SET_ODR_1000)
# collecting samples
acc.emptyfifo()
t0 = time.time()
sampleno = 500
data = acc.fastgetsamples(sampleno)
t1 = time.time()
print("Collected {:d} samples in {:f} seconds, {:f} samples/s".format(sampleno, t1 - t0, sampleno / (t1 - t0)))

# set data rate (with low pass filter settings)
acc.setfilter(lpf = adxl355.SET_ODR_500)
# collecting samples
acc.emptyfifo()
t0 = time.time()
sampleno = 250
data = acc.fastgetsamples(sampleno)
t1 = time.time()
print("Collected {:d} samples in {:f} seconds, {:f} samples/s".format(sampleno, t1 - t0, sampleno / (t1 - t0)))

# set data rate (with low pass filter settings)
acc.setfilter(lpf = adxl355.SET_ODR_250)
# collecting samples
acc.emptyfifo()
t0 = time.time()
sampleno = 125
data = acc.fastgetsamples(sampleno)
t1 = time.time()
print("Collected {:d} samples in {:f} seconds, {:f} samples/s".format(sampleno, t1 - t0, sampleno / (t1 - t0)))

# set data rate (with low pass filter settings)
acc.setfilter(lpf = adxl355.SET_ODR_31_25)
# collecting samples
acc.emptyfifo()
t0 = time.time()
sampleno = 30
data = acc.fastgetsamples(sampleno)
t1 = time.time()
print("Collected {:d} samples in {:f} seconds, {:f} samples/s".format(sampleno, t1 - t0, sampleno / (t1 - t0)))




