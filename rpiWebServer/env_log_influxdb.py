#!/usr/bin/env python3
# this file is executed by a crontab and saves the temperatures each
# minute in a the temporal series database fluxdb
#
# crontab command
#* * * * *  python3 /home/pi/temp_sensor/rpiWebServer/env_log_influxdb.py


from constants import dictSensors
from influxdb import InfluxDBClient
from sensitive_data import (PASSWORD, USERNAME, MIC, RASPB,
                            PORT, HOST, DATABASE, MEASUREMENTTMP)

def log_values(tags, fields):
    # create a new instance of the InfluxDBClient (API docs),
    # with information about the server that we want to access
    client = InfluxDBClient(host=HOST,
                            port=PORT,
                            username=USERNAME,
                            password=PASSWORD,
                            database=DATABASE)

    # create database to store data (this needs to be done only once"
    # client.create_database('microscope')
    # alternative:
    # export INFLUX_USERNAME=r...
    # export INFLUX_PASSWORD=t...
    # > CREATE DATABASE microscope
    # > SHOW DATABASES

    # select database
    # client.switch_database('microscope')

    # insert data
    try:
        dataPoint = [{'measurement': MEASUREMENTTMP, 'tags':tags, 'fields':fields}]
        client.write_points(dataPoint)
    except Exception:
        print("Cannot write to InfluxDB, check the service state "
                "on %s." % HOST)
        return
    # check data
    # > select * from mic_data
    # close connection
    client.close()


# tables date, sensorName, sensorValue
# time is handled by log_values function
fields={}
for key, sensor in dictSensors.items():
    sensorFile = open(sensor)
    thetest = sensorFile.read()
    sensorFile.close()
    tempData = thetest.split("\n")[1].split(" ")[9]
    temperature = float(tempData[2:])/1000.
    # testing temperature
    # temperature = random.randint(10,30)
    fields[key] = temperature

tags={"microscope" : MIC,
      "probeHost"  : RASPB}

log_values(tags, fields)
