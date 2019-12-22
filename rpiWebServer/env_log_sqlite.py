#!/usr/bin/env python3
# this file is executed by a crontab and saves the temperatures each
# minute in a the database sqliteDbName
#
# crontab command
#* * * * *  python3 /home/pi/temp_sensor/rpiWebServer/env_log.py
# sqlite verson, updated

import sqlite3
from constants import dictSensors, sqliteDbName, tableName


def log_values(values):
    conn = sqlite3.connect(sqliteDbName)  # It is important to provide an
    # absolute path to the database
    # file, otherwise Cron won't be
    # able to find it!
    curs = conn.cursor()
    for key, value in values.items():
        curs.execute("""INSERT INTO %s 
        values(datetime(CURRENT_TIMESTAMP),  
         (?), (?))"""%tableName, (key, value))  # save data as UCT
    conn.commit()
    conn.close()


# tables date, sensorName, sensorValue
# time is handled by log_values function
values={}
for key, sensor in dictSensors.items():
    sensorFile = open(sensor)
    thetest = sensorFile.read()
    sensorFile.close()
    tempData = thetest.split("\n")[1].split(" ")[9]
    temperature = float(tempData[2:])
    # testing temperature
    # temperature = random.randint(10,30)
    values[key] = temperature

log_values(values)
