 #!/usr/local/bin/python

import RPi.GPIO as GPIO
import time

# Use Broadcom SOC channel pin numbers
GPIO.setmode(GPIO.BCM)

# Set up header GPIO pin 17 as an output
GPIO.setup(17, GPIO.OUT)


while True:
	GPIO.output(17, True)
	
	time.sleep(1)
	
	GPIO.output(17, False)
	
	
	
