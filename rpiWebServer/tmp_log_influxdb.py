#!/usr/bin/env python3
# this file is executed by a crontab and saves the temperatures each
# minute in a the temporal series database fluxdb
#
# crontab command
#* * * * *  python3 /home/pi/temp_sensor/rpiWebServer/tmp_log_influxdb.py

from constants import (MEASUREMENTTMP, dictSensors)
from sensitive_data import (MIC, RASPB,)
from log_base import log_values
DEBUG=False


# read temperature from probes and create a dictionary
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
