dictLabels = {"01": "Input Water Temp",
               "02": "Output Water Temp"}

dictSensors = {"01": "/sys/bus/w1/devices/28-01144fd138aa/w1_slave",
               "02": "/sys/bus/w1/devices/28-0114509470aa/w1_slave"}

# database name
sqliteDbName = '/home/pi/temp_sensor/Database/temp.db'
tableName = "temp"

# database schema
# CREATE TABLE {tableName}(
#    time timestamp,
#    sensorID char(2),
#    sensorValue float, -- Degree Celsius
# );