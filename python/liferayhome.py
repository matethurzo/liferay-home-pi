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

# Setup GPIO for LCD displays
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setting up segments for LCD displays
#left high
lefthigh = 27
GPIO.setup(lefthigh,GPIO.OUT)

#top
top = 22
GPIO.setup(top,GPIO.OUT)

#right high
righthigh = 18
GPIO.setup(righthigh,GPIO.OUT)

#mid
mid = 17
GPIO.setup(mid,GPIO.OUT)

#left low
leftlow = 23
GPIO.setup(leftlow,GPIO.OUT)

#bottom
bottom = 24
GPIO.setup(bottom,GPIO.OUT)

#right low
rightlow = 25
GPIO.setup(rightlow,GPIO.OUT)

lcd1 = []
lcd1.append([lefthigh, top, righthigh])
lcd1.append([0, mid, 0])
lcd1.append([leftlow, bottom, rightlow])

#zlefthigh
zlefthigh = 20
GPIO.setup(zlefthigh,GPIO.OUT)

#ztop
ztop = 16
GPIO.setup(ztop,GPIO.OUT)

#zrighthigh
zrighthigh = 26
GPIO.setup(zrighthigh,GPIO.OUT)

#zmid
zmid = 21
GPIO.setup(zmid,GPIO.OUT)

#zleftlow
zleftlow = 19
GPIO.setup(zleftlow,GPIO.OUT)

#zbottom
zbottom = 13
GPIO.setup(zbottom,GPIO.OUT)

#zrightlow
zrightlow = 6
GPIO.setup(zrightlow,GPIO.OUT)

lcd2 = []
lcd2.append([zlefthigh, ztop, zrighthigh])
lcd2.append([0, zmid, 0])
lcd2.append([zleftlow, zbottom, zrightlow])

def setupPins(lcd):
	for row in lcd:
		for pin in row:
			if pin != 0:
				GPIO.setup(pin, GPIO.OUT)

def resetlcd():
	GPIO.output(top,GPIO.LOW)
	GPIO.output(mid,GPIO.LOW)
	GPIO.output(bottom,GPIO.LOW)
	GPIO.output(lefthigh,GPIO.LOW)
	GPIO.output(leftlow,GPIO.LOW)
	GPIO.output(righthigh,GPIO.LOW)
	GPIO.output(rightlow,GPIO.LOW)

	GPIO.output(ztop,GPIO.LOW)
	GPIO.output(zmid,GPIO.LOW)
	GPIO.output(zbottom,GPIO.LOW)
	GPIO.output(zlefthigh,GPIO.LOW)
	GPIO.output(zleftlow,GPIO.LOW)
	GPIO.output(zrighthigh,GPIO.LOW)
	GPIO.output(zrightlow,GPIO.LOW)


def lightSegment(segmentPin):
	GPIO.output(segmentPin, GPIO.HIGH)

def showNumber(number,actualLcd):
	lcd = lcd1

	if actualLcd == 2:
		lcd = lcd2

	segments = []

	if number == 1:
		segments.append(1)
		segments.append(7)
	elif number == 2:
		segments.append(2)
		lightSegment(actualLcd[0][1])
		lightSegment(actualLcd[0][2])
		lightSegment(actualLcd[1][1])
		lightSegment(actualLcd[2][0])
		lightSegment(actualLcd[2][1])
		lightSegment(actualLcd[2][2])
	elif number == 3:
		lightSegment(actualLcd[0][1])
		lightSegment(actualLcd[0][2])

def printnumber(num):
	if num == 1:
		GPIO.output(righthigh,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
	elif num == 2:
		GPIO.output(top,GPIO.HIGH)
		GPIO.output(righthigh,GPIO.HIGH)
		GPIO.output(mid,GPIO.HIGH)
		GPIO.output(leftlow,GPIO.HIGH)
		GPIO.output(bottom,GPIO.HIGH)
	elif num == 3:
		GPIO.output(top,GPIO.HIGH)
		GPIO.output(righthigh,GPIO.HIGH)
		GPIO.output(mid,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
		GPIO.output(bottom,GPIO.HIGH)
	elif num == 4:
		GPIO.output(lefthigh,GPIO.HIGH)
		GPIO.output(righthigh,GPIO.HIGH)
		GPIO.output(mid,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
	elif num == 5:
		GPIO.output(top,GPIO.HIGH)
		GPIO.output(lefthigh,GPIO.HIGH)
		GPIO.output(mid,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
		GPIO.output(bottom,GPIO.HIGH)
	elif num == 6:
		GPIO.output(top,GPIO.HIGH)
		GPIO.output(lefthigh,GPIO.HIGH)
		GPIO.output(leftlow,GPIO.HIGH)
		GPIO.output(bottom,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
		GPIO.output(mid,GPIO.HIGH)
	elif num == 7:
		GPIO.output(top,GPIO.HIGH)
		GPIO.output(righthigh,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
	elif num == 8:
		GPIO.output(top,GPIO.HIGH)
		GPIO.output(mid,GPIO.HIGH)
		GPIO.output(bottom,GPIO.HIGH)
		GPIO.output(lefthigh,GPIO.HIGH)
		GPIO.output(leftlow,GPIO.HIGH)
		GPIO.output(righthigh,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
	elif num == 9:
		GPIO.output(top,GPIO.HIGH)
		GPIO.output(lefthigh,GPIO.HIGH)
		GPIO.output(righthigh,GPIO.HIGH)
		GPIO.output(mid,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
	elif num == 0:
		GPIO.output(top,GPIO.HIGH)
		GPIO.output(righthigh,GPIO.HIGH)
		GPIO.output(rightlow,GPIO.HIGH)
		GPIO.output(bottom,GPIO.HIGH)
		GPIO.output(leftlow,GPIO.HIGH)
		GPIO.output(lefthigh,GPIO.HIGH)

def zprintnumber(num):
	if num == 1:
		GPIO.output(zrighthigh,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
	elif num == 2:
		GPIO.output(ztop,GPIO.HIGH)
		GPIO.output(zrighthigh,GPIO.HIGH)
		GPIO.output(zmid,GPIO.HIGH)
		GPIO.output(zleftlow,GPIO.HIGH)
		GPIO.output(zbottom,GPIO.HIGH)
	elif num == 3:
		GPIO.output(ztop,GPIO.HIGH)
		GPIO.output(zrighthigh,GPIO.HIGH)
		GPIO.output(zmid,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
		GPIO.output(zbottom,GPIO.HIGH)
	elif num == 4:
		GPIO.output(zlefthigh,GPIO.HIGH)
		GPIO.output(zrighthigh,GPIO.HIGH)
		GPIO.output(zmid,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
	elif num == 5:
		GPIO.output(ztop,GPIO.HIGH)
		GPIO.output(zlefthigh,GPIO.HIGH)
		GPIO.output(zmid,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
		GPIO.output(zbottom,GPIO.HIGH)
	elif num == 6:
		GPIO.output(ztop,GPIO.HIGH)
		GPIO.output(zlefthigh,GPIO.HIGH)
		GPIO.output(zleftlow,GPIO.HIGH)
		GPIO.output(zbottom,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
		GPIO.output(zmid,GPIO.HIGH)
	elif num == 7:
		GPIO.output(ztop,GPIO.HIGH)
		GPIO.output(zrighthigh,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
	elif num == 8:
		GPIO.output(ztop,GPIO.HIGH)
		GPIO.output(zmid,GPIO.HIGH)
		GPIO.output(zbottom,GPIO.HIGH)
		GPIO.output(zlefthigh,GPIO.HIGH)
		GPIO.output(zleftlow,GPIO.HIGH)
		GPIO.output(zrighthigh,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
	elif num == 9:
		GPIO.output(ztop,GPIO.HIGH)
		GPIO.output(zlefthigh,GPIO.HIGH)
		GPIO.output(zrighthigh,GPIO.HIGH)
		GPIO.output(zmid,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
	elif num == 0:
		GPIO.output(ztop,GPIO.HIGH)
		GPIO.output(zrighthigh,GPIO.HIGH)
		GPIO.output(zrightlow,GPIO.HIGH)
		GPIO.output(zbottom,GPIO.HIGH)
		GPIO.output(zleftlow,GPIO.HIGH)
		GPIO.output(zlefthigh,GPIO.HIGH)

def openFile(fileName):
	if fileName is None:
		return None

	f = open(fileName, 'a', 0)
	return f

resetlcd()

time.sleep(5)

printnumber(0)
GPIO.output(zleftlow, GPIO.HIGH)
GPIO.output(zlefthigh, GPIO.HIGH)
GPIO.output(ztop, GPIO.HIGH)
GPIO.output(zrighthigh, GPIO.HIGH)
GPIO.output(zrightlow, GPIO.HIGH)

time.sleep(2)

outputfile = openFile('liferayhome.out')

for i in range(0, 4999):

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	humstr = '{0:0.1f}'.format(humidity)[:1]
	zhumstr = '{0:0.1f}'.format(humidity)[-3:-2]

	resetlcd()
	printnumber(int(humstr))
	zprintnumber(int(zhumstr))

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
		print(time.time())
		print('T={0:0.1f} H={1:0.1f}'.format(temperature, humidity))
		outputfile.write(str(time.time()))
		outputfile.write(' ')
		outputfile.write('T={0:0.1f} H={1:0.1f}'.format(temperature, humidity))
		outputfile.write('\n')
	else:
		print('Skipped read')

resetlcd()

printnumber(0)
GPIO.output(zleftlow, GPIO.HIGH)
GPIO.output(zlefthigh, GPIO.HIGH)
GPIO.output(zmid, GPIO.HIGH)
GPIO.output(ztop, GPIO.HIGH)

print('TempAVG {0:0.1f} TempAbsMax {1:0.1f} TempAbsMin {2:0.1f}'.format(tempavg / 5000, tempabsmax, tempabsmin))
print('HumASVG {0:0.1f} HumAbsMax {1:0.1f} HumAbsMin {2:0.1f}'.format(humavg / 5000, humabsmax, humabsmin))