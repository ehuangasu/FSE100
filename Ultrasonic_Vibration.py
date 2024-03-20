#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

TRIG = 11
ECHO = 13
BUZZ = 12

buzzTime = 1
buzzState = 0
lastBuzz = 0
lastDistCheck = 0

def setup():
	GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)
	GPIO.setup(BUZZ, GPIO.OUT)     # Set Buzzer Led Pin mode to output
	off()

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.0001)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def on():
	global buzzState
	GPIO.output(Buzzpin, GPIO.HIGH)
	buzzState = 1

def off():
	global buzzState
	GPIO.output(BUZZ, GPIO.LOW)
	buzzState = 0

def flip():
	if buzzState == 1:
		off()
	else:
		on()

def loop():
	global lastDistCheck
	global buzzTime
	global lastBuzz
	while True:
		if time.time() - lastDistCheck > 0.25:
			dis = distance()
			print(dis, 'cm')
			lastDistCheck = time.time()

		if dis < 1000 and dis >= 100:
			buzzTime = 1
		if dis < 100 and dis >= 50:
			buzzTime = 0.5
		if dis < 50:
			buzzTime = 0.25
		
		if dis <= 1000:
			if time.time() - lastBuzz > buzzTime:
				flip()
				lastBuzz = time.time()
		else:
			off()
		
		time.sleep(0.1)

def destroy():
	GPIO.output(BUZZ, GPIO.HIGH)       # Buzzer off
	GPIO.cleanup()                        # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
		destroy()

