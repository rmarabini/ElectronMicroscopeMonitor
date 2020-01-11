"""Here is our Python script to measure and display
the temperature once every second:"""

import time

listSensors = ["/sys/bus/w1/devices/28-01144fd138aa/w1_slave",  # one
               "/sys/bus/w1/devices/28-0114509470aa/w1_slave",  # two
               "/sys/bus/w1/devices/28-01144fcdf4aa/w1_slave"]  # three

while 1:
    for sensor in listSensors:
        sensorFile = open(sensor)
        thetest = sensorFile.read()
        sensorFile.close()
        tempData = thetest.split("\n")[1].split(" ")[9]
        temperature = float(tempData[2:])
        temperature /= 1000.
        print(temperature)
    print("")
    time.sleep(1)

