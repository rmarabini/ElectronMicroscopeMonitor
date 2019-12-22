#!/usr/bin/env python3
# this file is executed by a crontab and saves the magnetic field each
# minute in a the temporal series database fluxdb
#
# adquires data during 60 decs and stores, mean. min. max, stvdev
# crontab command
#* * * * *  python3 /home/pi/temp_sensor/rpiWebServer/mag_log_influxdb.py

from constants import (dictSensors, MIC, RASPB, MEASUREMENTTMP)
from log_base import log_values
DEBUG=True

try:
    from bayeosraspberrypi.mcp3424 import MCP3424
    from bayeosraspberrypi.i2c import I2C
except:
    print("bayeosraspberrypi package is needed")
import time
import os




# read temperature from mag probes and create a dictionary
fields={}
for key, sensor in dictSensors.items():
    if DEBUG:  # testing, do not access to probes
        import random
        temperature = random.randint(10,30)
    else:
        sensorFile = open(sensor)
        thetest = sensorFile.read()
        sensorFile.close()
        tempData = thetest.split("\n")[1].split(" ")[9]
        temperature = float(tempData[2:])/1000.  # convert miliC to c
    fields[key] = temperature


# dictionary with  indexable values
tags={"microscope" : MIC,
      "probeHost"  : RASPB}

# store data in database
log_values(tags, fields, MEASUREMENTTMP)
