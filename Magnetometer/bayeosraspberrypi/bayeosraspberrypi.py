"""Python script to measure temperature, humidity and CO2 concentration with a Raspberry Pi.
A SHT21 sensor and a MCP3424 analog digital converter are connected to gpio pins, i.e. to the I2C bus.
One BayEOSWriter and one BayEOSSender object is instantiated to transfer data to the BayEOSGateway.
The sender runs in a separate thread. Origin frames are sent to distinguish CO2 chambers."""

import sys, numpy  # apt-get install python-numpy
from scipy import stats  # apt-get install python-scipy
from time import sleep, time
from thread import start_new_thread

from bayeosgatewayclient import BayEOSWriter, BayEOSSender
from i2c import I2C
from sht21 import SHT21
from mcp3424 import MCP3424
from gpio import GPIO

# gpio pins
ADDR_PINS = [11, 12, 13, 15, 16, 18]  # GPIO 17, 18, 27, 22, 23, 24
DATA_PIN = 24  # GPIO 8
EN_PIN = 26  # GPIO 7

# configuration for BayEOSWriter and BayEOSSender
PATH = '/tmp/raspberrypi/'
NAME = 'RaspberryPi'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'

# instantiate objects of BayEOSWriter and BayEOSSender
writer = BayEOSWriter(PATH)
sender = BayEOSSender(PATH, NAME, URL)

# initialize GPIO Board on Raspberry Pi
gpio = GPIO(ADDR_PINS, EN_PIN, DATA_PIN)

# initialize I2C Bus with sensors
try:
    i2c = I2C()
    sht21 = SHT21(1)
    mcp3424 = MCP3424(i2c.get_smbus())
except IOError as err:
    sys.stderr.write('I2C Connection Error: ' + str(err) + '. This must be run as root. Did you use the right device number?')

# measurement method
def measure(seconds=10):
    """Measures temperature, humidity and CO2 concentration.
    @param seconds: how long should be measured
    @return statistically calculated parameters 
    """
    measured_seconds = []
    temp = []
    hum = []
    co2 = []
    start_time = time()
    for i in range(0, seconds):
        start_new_thread(temp.append, (sht21.read_temperature(),))
        start_new_thread(hum.append, (sht21.read_humidity(),))
        start_new_thread(co2.append, (mcp3424.read_voltage(1),))
        measured_seconds.append(time())
        sleep(start_time + i - time() + 1) # to keep in time
    mean_temp = numpy.mean(temp)
    var_temp = numpy.var(temp)
    mean_hum = numpy.mean(hum)
    var_hum = numpy.var(hum)
    lin_model = stats.linregress(measured_seconds, co2)
    slope = lin_model[0]
    intercept = lin_model[1]
    r_squared = lin_model[2]*lin_model[2]
    slope_err = lin_model[4]
    return [mean_temp, var_temp, mean_hum, var_hum, slope, intercept, r_squared, slope_err]

sender.start() # starts sender in a concurrent thread

try:
    while True:
        for addr in range(1, 15):   # address 0 is reserved for flushing with air
            gpio.set_addr(0)        # set flushing address
            sleep(60)              # flush for 60 seconds
            gpio.reset()            # stop flushing
    
            gpio.set_addr(addr)     # start measuring wait 60 seconds, 240 measure
            writer.save(measure(30), origin="RaspberryPi Kammer Nr. " + str(addr))
            writer.flush()          # close the file in order to "feed" sender
            gpio.reset()
except KeyboardInterrupt:
    print 'Stopped measurement loop.'
finally:
    gpio.cleanup()
