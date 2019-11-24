#!/usr/bin/env python3
""" Report temperature using raspberry pi
    main page just access the sensors
    historic page acess the data stored in a sqlite database
    which is keep uptodate with a crontab job
"""

import datetime
import arrow
import time
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

# This is an stupid trick so my IDE load
# the local lib. only the except part is needed
try:
    from .constants import dictSensors, dictLabels, \
        sqliteDbName, tableName
except:
    from constants import dictSensors, dictLabels, \
        sqliteDbName, tableName


# default page just access the sensors and report temperature
@app.route("/")
def index():
    templateData = {}
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M:%S")
    templateData['TIME'] = timeString

    for key, sensor in dictSensors.items():
        sensorFile = open(sensor)
        thetest = sensorFile.read()
        sensorFile.close()
        tempData = thetest.split("\n")[1].split(" ")[9]
        temperature = float(tempData[2:])
        temperature /= 1000.
        templateData[dictLabels[key]] = "{0:.1f}".format(temperature)

    # get the first lable and check that there is a sensor connected to it
    if templateData[dictLabels[next(iter(dictLabels))]] is not None:
        return render_template("lab_temp.html", templateData=templateData)
    else:
        return render_template("no_sensor.html")


# This function plot the temperature
# you can limit the range in
# Arguments:
# from=2015-03-04&to=2015-03-05
# or
# range_h
@app.route("/lab_env_db", methods=['GET'])
def lab_env_db():
    temperatures, timezone, from_date_str, to_date_str = get_records()

    # Create new record tables so that datetimes are adjusted back
    # to the user browser's time zone.
    time_adjusted_temperatures = {}
    for key in dictSensors.keys():
        time_adjusted_temperatures[key] = []
        for record in temperatures[key]:
            local_timedate = arrow.get(
                record[0], "YYYY-MM-DD HH:mm:ss").to(timezone)
            time_adjusted_temperatures[key].append(
                [local_timedate.format('YYYY-MM-DD HH:mm:ss'), round(record[1] / 1000., 2)])

    key = next(iter(time_adjusted_temperatures))  # get a key from dictionary

    return render_template("lab_env_db.html",
                           timezone=timezone,
                           temp=time_adjusted_temperatures,
                           from_date=from_date_str,
                           to_date=to_date_str,
                           temp_items=len(temperatures[key]),
                           query_string=request.query_string,  # This query string is used
                                                               # by the Plotly link
                           captions=dictLabels.values(),
                           key=key,
                           keys=dictLabels.keys(),
                           )

# get needed records from database
# and parse form arguments
def get_records():
    from_date_str = request.args.get('from', time.strftime("%Y-%m-%d 00:00"))  # Get the from date value from the URL
    to_date_str = request.args.get('to', time.strftime("%Y-%m-%d %H:%M"))  # Get the to date value from the URL
    timezone = request.args.get('timezone', 'Europe/Madrid');
    range_h_form = request.args.get('range_h', '');  # This will return a string, if field range_h exists in the request
    range_h_int = 'nan'  # initialise this variable with not a number

    try:
        range_h_int = int(range_h_form)
    except:
        print("range_h_form not a number", range_h_int, range_h_form)

    if not validate_date(from_date_str):  # Validate date before sending it to the DB
        from_date_str = time.strftime("%Y-%m-%d 00:00")
    if not validate_date(to_date_str):
        to_date_str = time.strftime("%Y-%m-%d %H:%M")  # Validate date before sending it to the DB

    # Create datetime object so that we can convert to UTC
    # from the browser's local time
    from_date_obj = datetime.datetime.strptime(from_date_str, '%Y-%m-%d %H:%M')
    to_date_obj = datetime.datetime.strptime(to_date_str, '%Y-%m-%d %H:%M')

    # If range_h is defined, we don't need the from and to times
    if isinstance(range_h_int, int):
        arrow_time_from = arrow.utcnow().shift(hours=-range_h_int)
        arrow_time_to = arrow.utcnow()
        from_date_utc = arrow_time_from.strftime("%Y-%m-%d %H:%M")
        to_date_utc = arrow_time_to.strftime("%Y-%m-%d %H:%M")
        from_date_str = arrow_time_from.to(timezone).strftime("%Y-%m-%d %H:%M")
        to_date_str = arrow_time_to.to(timezone).strftime("%Y-%m-%d %H:%M")
    else:
        # Convert datetimes to UTC so we can retrieve the appropriate records from the database
        from_date_utc = arrow.get(from_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")
        to_date_utc = arrow.get(to_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect(sqliteDbName)
    # save each sensor temperature in a list
    curs = conn.cursor()
    temperatures = {}
    for key in dictSensors.keys():
        sqlCommand = """SELECT time, sensorValue
                        FROM %s
                        WHERE sensorID = '%s'
                          AND time BETWEEN ? AND ?
                        ORDER by time
        """ % (tableName, key)

        curs.execute(sqlCommand, (from_date_utc.format('YYYY-MM-DD HH:mm'),
                                  to_date_utc.format('YYYY-MM-DD HH:mm')))
        temperatures[key] = curs.fetchall()
    conn.close()

    return [temperatures, timezone, from_date_str, to_date_str]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0')  # , port=80, debug=True)
