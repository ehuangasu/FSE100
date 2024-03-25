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

# Setup board
def setup():
	GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)
	GPIO.setup(BUZZ, GPIO.OUT)     # Set Buzzer Led Pin mode to output
	off()

# Ultrasonic distance
def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.0001)

    # Ultrasonic sensor outputs
	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time() # Time when ultrasonic output
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time() # Time when ultrasonic gets input back

	during = time2 - time1
	return during * 340 / 2 * 100 # Use speed of sound to get distance

# Turns vibration motor on
def on():
	global buzzState
	GPIO.output(BUZZ, GPIO.HIGH)
	buzzState = 1

# Turns vibration motor off
def off():
	global buzzState
	GPIO.output(BUZZ, GPIO.LOW)
	buzzState = 0

# Flips vibration motor
def flip():
	if buzzState == 1:
		off()
	else:
		on()

def loop():
	global lastDistCheck
	global buzzTime
	global lastBuzz
	
	# Main loop
	while True:
		# Every 0.25 seconds, get distance
		if time.time() - lastDistCheck > 0.25:
			dis = distance()
			print(dis, 'cm')
			lastDistCheck = time.time()

        # Change buzzTime based on distance
		if dis < 200 and dis >= 100:
			buzzTime = 1
		if dis < 100 and dis >= 50:
			buzzTime = 0.5
		if dis < 50:
			buzzTime = 0.25
		
		# Every buzzTime seconds, flip the vibration motor state
		if dis <= 200:
			if time.time() - lastBuzz > buzzTime:
				flip()
				lastBuzz = time.time()
		else:
			off() # Off when doesn't detect anything
		
		time.sleep(0.05)

def destroy():
	GPIO.output(BUZZ, GPIO.HIGH)       # Buzzer off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
		destroy()

