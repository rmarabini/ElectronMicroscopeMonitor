#dictLabels = {"01": "Input Water Temp",
#               "02": "Output Water Temp"}
dictLabels = {"01": "Cryo ARM 300",
               "02": "Talos Arctica"}

dictSensors = {"01": "/sys/bus/w1/devices/28-01144fd138aa/w1_slave",
               "02": "/sys/bus/w1/devices/28-0114509470aa/w1_slave"}
# influxdb
MIC='Talos Artica'
RASPB='carson'
DATABASE='microscope'
MEASUREMENTTMP='probeTmp'
MEASUREMENTMAG='probeMag'
MEASUREMENTVIBRA='probeVibra'

# database name
sqliteDbName = '/home/pi/temp_sensor/Database/temp.db'
tableName = "temp"

# database schema
# CREATE TABLE {tableName}(
#    time timestamp,
#    sensorID char(2),
#    sensorValue float, -- Degree Celsius
# );
