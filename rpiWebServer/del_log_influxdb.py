#!/usr/bin/env python3
# this file is executed by a crontab delete
# entries older than 90 days from databse sqliteDbName
#
# crontab command
# start everyday at 1:00
#0 1 * * *  python3 /home/pi/temp_sensor/rpiWebServer/del_log.py

# This is no longer needed
# CREATE DATABASE WITH DURATION
# CREATE DATABASE microscope WITH DURATION 90d
