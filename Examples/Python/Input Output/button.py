#!/usr/bin/env python

from time import sleep
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.IN)
GPIO.setup(17, GPIO.OUT)



while True:
	if ( GPIO.input(22) == False):
		GPIO.output(17, True)
	else:
		GPIO.output(17,False)

	
	sleep(0.1)
