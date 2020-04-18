#dictLabels = {"01": "Input Water Temp",
#               "02": "Output Water Temp"}
dictLabels = {"01": "Cryo ARM 300",
               "02": "Talos Arctica"}

#carson
#dictSensors = {"01": "/sys/bus/w1/devices/28-01144fd138aa/w1_slave",
#               "02": "/sys/bus/w1/devices/28-0114509470aa/w1_slave",
#               "03": "/sys/bus/w1/devices/28-01144fcdf4aa/w1_slave"}
#carson4
dictSensors = {"01": "/sys/bus/w1/devices/28-01145077a7aa/w1_slave",
#               "02": "/sys/bus/w1/devices/28-0114508701aa/w1_slave",
#               "03": "/sys/bus/w1/devices/28-01145077a7aa/w1_slave"
}


# influxdb
MIC='cryoArm'
RASPB='carson4'
DATABASE='microscope'
MEASUREMENTTMP='probeTmp'
MEASUREMENTMAG='probeMag'
MEASUREMENTVIBRA='probeVibra'
MEASUREMENTVIBRAFFT='probeVibraFFT'

# database name
#sqliteDbName = '/home/pi/temp_sensor/Database/temp.db'
#tableName = "temp"

