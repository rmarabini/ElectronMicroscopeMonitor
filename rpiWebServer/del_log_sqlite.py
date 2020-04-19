#!/usr/bin/env python3
# this file is executed by a crontab delete
# entries older than 90 days from databse sqliteDbName
#
# crontab command
# start everyday at 1:00
#0 1 * * *  python3 /home/pi/temp_sensor/rpiWebServer/del_log.py

import sqlite3
from constants import sqliteDbName, tableName


conn = sqlite3.connect(sqliteDbName)  # It is important to provide an
# absolute path to the database
# file, otherwise Cron won't be
# able to find it!
curs = conn.cursor()
curs.execute("DELETE FROM %s WHERE time <= date('now','-90 day')"%tableName)
conn.commit()
conn.close()

