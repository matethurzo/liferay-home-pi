#!/usr/bin/python

# Copyright (c) 2017 Liferay Home

import Adafruit_DHT
import RPi.GPIO as GPIO

import time
import sys

# Read command line arguments
if len(sys.argv) == 1:
	print('Usage: liferayhome.py [readSleepTime] [readIterations]')

	sys.exit()

# Read sleep time
readSleepTime = 5

if sys.argv[1] is not None:
	readSleepTime = int(sys.argv[1])

# Number of iterations
readIterations = 5000

if sys.argv[2] is not None:
	readIterations = int(sys.argv[2])

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

def lightSegment(segmentPin):
	GPIO.output(segmentPin, GPIO.HIGH)

def hideSegment(segmentPin):
	GPIO.output(segmentPin, GPIO.LOW)

def resetlcd():
	hideSegment(top)
	hideSegment(mid)
	hideSegment(bottom)
	hideSegment(lefthigh)
	hideSegment(leftlow)
	hideSegment(righthigh)
	hideSegment(rightlow)

	hideSegment(ztop)
	hideSegment(zmid)
	hideSegment(zbottom)
	hideSegment(zlefthigh)
	hideSegment(zleftlow)
	hideSegment(zrighthigh)
	hideSegment(zrightlow)

def aprintnumber(num):
	if num == 1:
		lightSegment(righthigh)
		lightSegment(rightlow)
	elif num == 2:
		lightSegment(top)
		lightSegment(righthigh)
		lightSegment(mid)
		lightSegment(leftlow)
		lightSegment(bottom)
	elif num == 3:
		lightSegment(top)
		lightSegment(righthigh)
		lightSegment(mid)
		lightSegment(rightlow)
		lightSegment(bottom)
	elif num == 4:
		lightSegment(lefthigh)
		lightSegment(righthigh)
		lightSegment(mid)
		lightSegment(rightlow)
	elif num == 5:
		lightSegment(top)
		lightSegment(lefthigh)
		lightSegment(mid)
		lightSegment(rightlow)
		lightSegment(bottom)
	elif num == 6:
		lightSegment(top)
		lightSegment(lefthigh)
		lightSegment(leftlow)
		lightSegment(bottom)
		lightSegment(rightlow)
		lightSegment(mid)
	elif num == 7:
		lightSegment(top)
		lightSegment(righthigh)
		lightSegment(rightlow)
	elif num == 8:
		lightSegment(top)
		lightSegment(mid)
		lightSegment(bottom)
		lightSegment(lefthigh)
		lightSegment(leftlow)
		lightSegment(righthigh)
		lightSegment(rightlow)
	elif num == 9:
		lightSegment(top)
		lightSegment(lefthigh)
		lightSegment(righthigh)
		lightSegment(mid)
		lightSegment(rightlow)
	elif num == 0:
		lightSegment(top)
		lightSegment(righthigh)
		lightSegment(rightlow)
		lightSegment(bottom)
		lightSegment(leftlow)
		lightSegment(lefthigh)

def zprintnumber(num):
	if num == 1:
		lightSegment(zrighthigh)
		lightSegment(zrightlow)
	elif num == 2:
		lightSegment(ztop)
		lightSegment(zrighthigh)
		lightSegment(zmid)
		lightSegment(zleftlow)
		lightSegment(zbottom)
	elif num == 3:
		lightSegment(ztop)
		lightSegment(zrighthigh)
		lightSegment(zmid)
		lightSegment(zrightlow)
		lightSegment(zbottom)
	elif num == 4:
		lightSegment(zlefthigh)
		lightSegment(zrighthigh)
		lightSegment(zmid)
		lightSegment(zrightlow)
	elif num == 5:
		lightSegment(ztop)
		lightSegment(zlefthigh)
		lightSegment(zmid)
		lightSegment(zrightlow)
		lightSegment(zbottom)
	elif num == 6:
		lightSegment(ztop)
		lightSegment(zlefthigh)
		lightSegment(zleftlow)
		lightSegment(zbottom)
		lightSegment(zrightlow)
		lightSegment(zmid)
	elif num == 7:
		lightSegment(ztop)
		lightSegment(zrighthigh)
		lightSegment(zrightlow)
	elif num == 8:
		lightSegment(ztop)
		lightSegment(zmid)
		lightSegment(zbottom)
		lightSegment(zlefthigh)
		lightSegment(zleftlow)
		lightSegment(zrighthigh)
		lightSegment(zrightlow)
	elif num == 9:
		lightSegment(ztop)
		lightSegment(zlefthigh)
		lightSegment(zrighthigh)
		lightSegment(zmid)
		lightSegment(zrightlow)
	elif num == 0:
		lightSegment(ztop)
		lightSegment(zrighthigh)
		lightSegment(zrightlow)
		lightSegment(zbottom)
		lightSegment(zleftlow)
		lightSegment(zlefthigh)

def printnumber(number,lcd):
	if lcd == 1:
		aprintnumber(number)
	elif lcd == 0:
		zprintnumber(number)

def openFile(fileName):
	if fileName is None:
		return None

	f = open(fileName, 'a', 0)
	return f

resetlcd()

time.sleep(5)

printnumber(0,1)
lightSegment(zleftlow)
lightSegment(zlefthigh)
lightSegment(ztop)
lightSegment(zrighthigh)
lightSegment(zrightlow)

time.sleep(2)

for i in range(0, 4999):

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	humstr = '{0:0.1f}'.format(humidity)[:1]
	zhumstr = '{0:0.1f}'.format(humidity)[-3:-2]

	resetlcd()

	controlfile = open('liferayhome.ctl', 'r')
	
	if controlfile is not None:
		controlvalue = controlfile.readline()

		if controlvalue == 'HEAT':
			printnumber(0,1)
			lightSegment(zleftlow)
			lightSegment(zlefthigh)
			lightSegment(ztop)
			lightSegment(zrighthigh)
			lightSegment(zrightlow)
		elif controlvalue == 'COOL':
			printnumber(0,1)
			lightSegment(zleftlow)
			lightSegment(zlefthigh)
			lightSegment(zmid)
			lightSegment(ztop)
		elif controlvalue == 'NOOP':
			resetlcd()

	controlfile.close()

	#printnumber(int(humstr),1)
	#printnumber(int(zhumstr),0)

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
		sys.stdout.write(str(time.time()) + '#{0:0.1f}#{1:0.1f}'.format(temperature, humidity))
	else:
		sys.stdout.write('Skipped read')

	sys.stdout.write('\n')
	sys.stdout.flush()

	time.sleep(readSleepTime)

resetlcd()

printnumber(0,1)
lightSegment(zleftlow)
lightSegment(zlefthigh)
lightSegment(zmid)
lightSegment(ztop)

sys.stdout.write('TempAVG {0:0.1f} TempAbsMax {1:0.1f} TempAbsMin {2:0.1f}'.format(tempavg / 5000, tempabsmax, tempabsmin))
sys.stdout.write('\n')
sys.stdout.write('HumASVG {0:0.1f} HumAbsMax {1:0.1f} HumAbsMin {2:0.1f}'.format(humavg / 5000, humabsmax, humabsmin))