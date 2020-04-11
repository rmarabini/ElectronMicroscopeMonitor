"""Here is our Python script to measure and display
the temperature once every second:"""

import time
from constants import dictSensors

while 1:
    for sensor in dictSensors.values():
        sensorFile = open(sensor)
        thetest = sensorFile.read()
        sensorFile.close()
        tempData = thetest.split("\n")[1].split(" ")[9]
        temperature = float(tempData[2:])
        temperature /= 1000.
        print("{:.1f}".format(temperature))
    print("")
    time.sleep(1)

