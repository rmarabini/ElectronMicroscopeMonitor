#!/usr/bin/env python3
# this file is executed by a crontab and saves the temperatures each
# minute in a the temporal series database fluxdb
#
# crontab command
#* * * * *  python3 /home/pi/temp_sensor/rpiWebServer/env_log_influxdb.py

from influxdb import InfluxDBClient
from sensitive_data import (PASSWORD, USERNAME)
from constants import (dictSensors, MIC, RASPB,
                       PORT, HOST, DATABASE, MEASUREMENTTMP)

def log_values(tags, fields):
    # saves an entry in influxdb storing the information
    # passed in tags and fields
    # InfluxDB lets you specify fields and tags, both being 
    # key/value pairs where the difference is that tags are 
    # automatically indexed. Because fields are not being 
    # indexed at all, on every query where InfluxDB is asked 
    # to find a specified field, it needs to sequentially 
    # scan every value of the field column

    # Before running this script you must 
    # create database to store data (this needs to be done only once"
    # export INFLUX_USERNAME=r...
    # export INFLUX_PASSWORD=t...
    # start influs CLI
    # influx 
    # > show databases
    # > CREATE DATABASE microscope WITH DURATION 90d
    # > SHOW DATABASES
    # > USE microscope
    # > select * from probeTmp
  
    # create a new instance of the InfluxDBClient (API docs),
    # with information about the server that we want to access
    # sensitive information is in sensitive_data file
    client = InfluxDBClient(host=HOST,
                            port=PORT,
                            username=USERNAME,
                            password=PASSWORD,
                            database=DATABASE)


    # insert data    
    # if time is not provided it will be added by the databse
    try:
        dataPoint = [{'measurement': MEASUREMENTTMP,
                      'tags':tags,
                      'fields':fields}]
        client.write_points(dataPoint)
    except Exception:
        print("Cannot write to InfluxDB, check the service state "
                "on %s." % HOST)
        return
      
    # check data
    # > select * probeTmp
    client.close()


# read temperature from probes and create a dictionary
fields={}
for key, sensor in dictSensors.items():
    sensorFile = open(sensor)
    thetest = sensorFile.read()
    sensorFile.close()
    tempData = thetest.split("\n")[1].split(" ")[9]
    temperature = float(tempData[2:])/1000.  # convert miliC to c
    # testing temperature
    # temperature = random.randint(10,30)
    fields[key] = temperature


# dictioanry with  indexable values
tags={"microscope" : MIC,
      "probeHost"  : RASPB}

# store data in database
log_values(tags, fields)
