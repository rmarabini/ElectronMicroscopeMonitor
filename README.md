# temp_sensor
This project will measure the temperature at multiple points using DS18B20 sensors

## Hardware required
  * n x DS18B20 sensors (the waterproof version) (1.3 euros each)
  * 10k Ohm resister (a few cents of euro)
  * Jumper cables with Dupont connectors on the end (a few cents)
  * Raspberry pi versión 3b or 4 (range 30-60 euros depending on model
  * microSD card (8 euros)
  * 5 volt, 3 amp  adapter (8 euros)
## Software Required
  * Raspbian operating system to the RPi
  * Python3
  * Flask, a Python-based web micro-framework
  * uWSGI as the application server for Flask
  * Use Skeleton to make the web UI look better
  * SQLite database 
  * Google Chart API to create visual representations of the sensor data
  * Javascript/JQuery to add interactivity to web pages

## The DS18B20 Sensor
Temperature range is between -55C to 125C and they are accurate to +/- 0.5C between -10C and +85C.
 
It is called a ‘1-Wire’ device as it can operate over a single wire bus
thanks to each sensor having a unique 64-bit serial code. 

```
Wiring
DS18B20          RPi
-------          ---
VDD (red)        GND
GND (black)      GND
DQ (yellow)      GPIO  -- 10k -- 3.3v
```

The w1-gpio-overlay defaults to using GPIO_4 for the data pin. 
Each time you connect a semsor a file should appear at /sys/bus/w1/devices, open it and read the temperature, unit are 1000xcelsius.

## Software
   We will serve the information using flask and uwsgi. Two crontab processes record the temperature each minute (env_log.py) and delete entries older tham 90 days (del_log.py).
   If you want to add another sensor just edit the constant.py file.
   
   Most of the application logic is in file app.py
   
   
   
## Start server on reboot
```
Create a uWSGI startup file
   see file my_app (place it at /etc/systemd/system/)
#Start the process:
   sudo systemctl start temp_sensor

# Check the status
sudo systemctl status temp_sensor.service

# Enable it on startup
sudo systemctl enable temp_sensor
```

## address to connect

http://192.168.0.103:8000/

## Links of interest
  * Install raspbian: https://itsfoss.com/tutorial-how-to-install-raspberry-pi-os-raspbian-wheezy/
  * Script that access the sensors:  http://www.reuk.co.uk/wordpress/raspberry-pi/ds18b20-temperature-sensor-with-raspberry-pi/
  * Code used as base for flask: https://github.com/cwalk/Pi-Temp 
