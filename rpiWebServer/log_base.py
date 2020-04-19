#!/usr/bin/env python3
# this file is executed by a crontab and saves the temperatures each
# minute in a the temporal series database fluxdb
#
# crontab command
#* * * * *  python3 /home/pi/temp_sensor/rpiWebServer/env_log_influxdb.py

from influxdb import InfluxDBClient
from sensitive_data import (PASSWORD, USERNAME, HOST, PORT)
from constants import (DATABASE, MEASUREMENTTMP)
import datetime

def delete_meassurement(meassurement):
    """ Delete all data with meassurement = probe """
    client = InfluxDBClient(host=HOST,
                            port=PORT,
                            username=USERNAME,
                            password=PASSWORD,
                            database=DATABASE)
    try:
        client.query('delete from %s' % meassurement)
    except Exception:
        currentDT = datetime.datetime.now()
        print(str(currentDT), "Cannot delete database entry for meassurement = %s (host=%s)" % (meassurement, HOST))
        return
    client.close()

def log_multiple_values(tags, fields, measurament=MEASUREMENTTMP):

    """
    For menupoints point
    tags: dictionary with tags
    fields: list of dictionary with field
    meassurement: string with meassurement
    """
    client = InfluxDBClient(host=HOST,
                            port=PORT,
                            username=USERNAME,
                            password=PASSWORD,
                            database=DATABASE)

    # insert data    
    # if time is not provided it will be added by the databse
    dataPointList = []
    now = datetime.datetime.today()
    _now = datetime.datetime.now()
    counter = 0
    for field in fields:
        dataPoint = {'measurement': measurament,
	             'time': now + datetime.timedelta(0,counter),
                     'tags':tags,
                     'fields':field}
        dataPointList.append(dataPoint)
        counter +=1
    try:
        client.query('delete from %s' %  measurament)
        client.write_points(dataPointList) #, batch_size=50)
    except Exception as e:
        currentDT = datetime.datetime.now()
        print(str(currentDT), "Cannot write to InfluxDB, check the service state "
                "on %s." % HOST, str(e))
		
        return

    client.close()

def log_values(tags, fields, measurament=MEASUREMENTTMP):

    """
    For a single point
    tags: dictionary with tags
    fields: dictionary with field
    meassurement: string with meassurement
    """
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
    # start influx CLI
    # influx 
    # > show databases
    # > CREATE DATABASE microscope WITH DURATION 90d
    # > SHOW DATABASES
    # > USE microscope
    # > select * from probeTmp
    # > delete from probeTmp  
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
        dataPoint = [{'measurement': measurament,
                      'tags':tags,
                      'fields':fields}]
        client.write_points(dataPoint)
    except Exception:
        currentDT = datetime.datetime.now()
        print(str(currentDT), "Cannot write to InfluxDB, check the service state "
                "on %s." % HOST)
        return
      
    # check data
    # > select * probeTmp
    client.close()
