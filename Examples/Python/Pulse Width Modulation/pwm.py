import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

p = GPIO.PWM(17,50) # Pin number and frequency in Hz (controls the frequency of the pulses)

p.start(0)


while True:
	for i in range(100):
		p.ChangeDutyCycle(i)   # Controls the length of the pulses (This will fade LED from 0-100%)
		
	for i in range(100):
		p.ChangeDutyCycle(100-i)

