#!/usr/bin/python

# Copyright (c) 2017 Liferay Home

import Adafruit_DHT
import time
import RPi.GPIO as GPIO

# Setting up sensor type. Adafruit library will handle the type properly
sensor = Adafruit_DHT.DHT22

# Setting up GPIO pin 4 for sensor
pin = 4

# Setting up variables for basic temperature and humidity calculations
tempavg = 0.0
humavg = 0.0

tempabsmax = 0.0
tempabsmaxcounter = 0
tempabsmin = 0.0
tempabsmincounter = 0

humabsmax = 0.0
humabsmaxcounter = 0
humabsmin = 0.0
humabsmincounter = 0

for i in range(0, 4999):

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	humstr = '{0:0.1f}'.format(humidity)[:1]
	zhumstr = '{0:0.1f}'.format(humidity)[-3:-2]

	if temperature > tempabsmax:
		tempabsmax = temperature

	if temperature < tempabsmin or tempabsmin == 0.0:
		tempabsmin = temperature

	if humidity > humabsmax:
		humabsmax = humidity

	if humidity < humabsmin or humabsmin == 0.0:
		humabsmin = humidity

	tempavg = tempavg + temperature
	humavg = humavg + humidity

	humiditymin = humidity - ((humidity / 100) * 5)
	humiditymax = humidity + ((humidity / 100) * 5)

	tempmin = temperature - 2
	tempmax = temperature + 2
	
	if humidity is not None and temperature is not None:
		print(i)
		print('Temp={0:0.1f}*C Hum={1:0.1f}%'.format(temperature, humidity))
#    		print('TempMIN={0:0.1f}*C TempMAX={1:0.1f}*C'.format(tempmin, tempmax))
#		print('HumidityMIN={0:0.1f}%  HumidityMAX={1:0.1f}%'.format(humiditymin, humiditymax))

	else:
		print('Skipped read')

print('TempAVG {0:0.1f} TempAbsMax {1:0.1f} TempAbsMin {2:0.1f}'.format(tempavg / 5000, tempabsmax, tempabsmin))
print('HumASVG {0:0.1f} HumAbsMax {1:0.1f} HumAbsMin {2:0.1f}'.format(humavg / 5000, humabsmax, humabsmin))