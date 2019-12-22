"""Python script to measure temperature, humidity and CO2 concentration with a Raspberry Pi.
A SHT21 sensor and a MCP3424 analog digital converter are connected to gpio pins, i.e. to the I2C bus.
The BayEOSGatewayClient class is extended to transfer data to the BayEOSGateway.
The sender runs in a separate process. Origin frames are sent to distinguish CO2 chambers."""

import sys, numpy  # apt-get install python-numpy
from scipy import stats  # apt-get install python-scipy
from time import sleep, time
from thread import start_new_thread

from bayeosgatewayclient import BayEOSGatewayClient, bayeos_confparser
from gpio import GPIO
from i2c import I2C
from sht21 import SHT21
from mcp3424 import MCP3424

class RaspberryPiClient(BayEOSGatewayClient):
    """Raspberry Pi client class."""

    def init_writer(self):
        """Overwrites the init_writer() method of the BayEOSGatewayClient class."""
        # gpio pins
        ADDR_PINS = [11, 12, 13, 15, 16, 18]  # GPIO 17, 18, 27, 22, 23, 24
        DATA_PIN = 24  # GPIO 8
        EN_PIN = 26  # GPIO 7
        self.gpio = GPIO(ADDR_PINS, EN_PIN, DATA_PIN)

        self.init_sensors()
        self.addr = 1  # current address

    def read_data(self):
        """Overwrites the read_data() method of the BayEOSGatewayClient class."""
        # address 0 is reserved for flushing with air
        self.gpio.set_addr(0)  # set flushing address
        sleep(.6)  # flush for 60 seconds
        self.gpio.reset()  # stop flushing

        self.gpio.set_addr(self.addr)  # start measuring wait 60 seconds, 240 measure
        measurement_data = self.measure(3)
        self.gpio.reset()

        return measurement_data

    def save_data(self, values=[], origin='CO2_Chambers'):
        """Overwrites the save_data() method of the BayEOSGatewayClient class."""
        self.writer.save(values, origin='RaspberryPi-Chamber-' + str(self.addr))
        self.writer.flush()
        print 'saved data: ' + str(values)
        
        self.addr += 1
        if self.addr > 15:
            self.addr = 1

    def init_sensors(self):
        """Initializes the I2C Bus including the SHT21 and MCP3424 sensors."""
        try:
            self.i2c = I2C()
            self.sht21 = SHT21(1)
            self.mcp3424 = MCP3424(self.i2c.get_smbus())
        except IOError as err:
            sys.stderr.write('I2C Connection Error: ' + str(err) + '. This must be run as root. Did you use the right device number?')

    def measure(self, seconds=10):
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
            start_new_thread(temp.append, (self.sht21.read_temperature(),))
            start_new_thread(hum.append, (self.sht21.read_humidity(),))
            start_new_thread(co2.append, (self.mcp3424.read_voltage(1),))
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

OPTIONS = bayeos_confparser('../config/bayeosraspberrypi.ini')

client = RaspberryPiClient(OPTIONS['name'], OPTIONS)
client.run(thread=False) # sender runs in a separate process 