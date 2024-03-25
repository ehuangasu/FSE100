#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

TRIG = 11
ECHO = 13
BUZZ = 12

buzzState = False
lastBuzzTime = 0
lastDistCheck = 0

# Setup board
def setup():
	GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)
	GPIO.setup(BUZZ, GPIO.OUT)     # Set Buzzer Led Pin mode to output
	off() # Ensure buzzer is off

# Ultrasonic distance
def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.00002)

    # Ultrasonic sensor outputs
	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	startTime = time.time()
	while GPIO.input(ECHO) == 0:
		startTime = time.time()  

	stopTime = time.time()
	while GPIO.input(ECHO) == 1:
		stopTime = time.time()
		if stopTime - startTime > 0.1:  # If no echo received
			return -1  

	# Calculate distance
	duration = stopTime - startTime
	return duration * 340 / 2 * 100 # Use speed of sound, 340m/s to get distance (convert m to cm)

# Turns vibration motor on
def on():
	global buzzState
	GPIO.output(BUZZ, GPIO.HIGH)
	buzzState = True

# Turns vibration motor off
def off():
	global buzzState
	GPIO.output(BUZZ, GPIO.LOW)
	buzzState = False

# Flips vibration motor
def flip():
	if buzzState:
		off()
	else:
		on()

def loop():
	global lastDistCheck
	global lastBuzzTime
	
	# Main loop
	while True:
		# Every 0.25 seconds, get distance
		if time.time() - lastDistCheck > 0.25:
			dis = distance()
			print(f"{dis:.2f} cm")
			lastDistCheck = time.time()

        # Change buzzTime based on distance
		buzzTime = None
		if dis < 200 and dis >= 100:
			buzzTime = 1
		if dis < 100 and dis >= 50:
			buzzTime = 0.5
		if dis < 50 and dis >= 0:
			buzzTime = 0.25
		
		# Every buzzTime seconds, flip the vibration motor state
		if buzzTime is not None:
			if time.time() - lastBuzzTime > buzzTime:
				flip()
				lastBuzzTime = time.time()
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

