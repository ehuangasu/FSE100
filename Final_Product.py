#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

TRIG1 = 17
ECHO1 = 22
TRIG2 = 5
ECHO2 = 13
BUZZ = 26
PIR1 = 18
PIR2 = 23
ALARM = 12
TOUCH1 = 25
TOUCH2 = 16
BUZZTOUCH = 21

buzzState = False
lastBuzzTime = 0
lastDistCheck = 0

canBuzz = False
canAlarm = False

# Setup board
def setup():
	GPIO.setmode(GPIO.BCM)          # Numbers GPIOs by GPIO number
	GPIO.setup(TRIG1, GPIO.OUT)
	GPIO.setup(ECHO1, GPIO.IN)
	GPIO.setup(TRIG2, GPIO.OUT)
	GPIO.setup(ECHO2, GPIO.IN)
	GPIO.setup(BUZZ, GPIO.OUT)
	GPIO.setup(PIR1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(PIR2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(PIR1, GPIO.BOTH, callback=detectPir)
	GPIO.add_event_detect(PIR2, GPIO.BOTH, callback=detectPir)
	GPIO.setup(ALARM, GPIO.OUT)
	GPIO.setup(TOUCH1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(TOUCH2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(TOUCH1, GPIO.FALLING, callback=detectTouch1)
	GPIO.add_event_detect(TOUCH2, GPIO.FALLING, callback=detectTouch2)
	GPIO.setup(BUZZTOUCH, GPIO.OUT)
	offBuzz();        # Buzzer off
	offAlarm();       # Alarm off
	offTouch();   # Touch Buzzer off
	print('on');

# Ultrasonic distance
def distance(t, e):
	GPIO.output(t, 0)
	time.sleep(0.00002)

    # Ultrasonic sensor outputs
	GPIO.output(t, 1)
	time.sleep(0.00001)
	GPIO.output(t, 0)

	startTime = time.time()  
	while GPIO.input(e) == 0:
		if time.time() - startTime > 1:  # If no echo sent
			return 8888
	startTime = time.time()  
	
	stopTime = time.time()
	while GPIO.input(e) == 1:
		stopTime = time.time()
		if stopTime - startTime > 0.1:  # If no echo received
			return 9999  

	# Calculate distance
	duration = stopTime - startTime
	return duration * 340 / 2 * 100 # Use speed of sound, 340m/s to get distance (convert m to cm)

def onBuzz():
	global buzzState
	GPIO.output(BUZZ, GPIO.HIGH)
	buzzState = True

def offBuzz():
	global buzzState
	GPIO.output(BUZZ, GPIO.LOW)
	buzzState = False

def onAlarm():
	GPIO.output(ALARM, GPIO.LOW)

def offAlarm():
	GPIO.output(ALARM, GPIO.HIGH)
	
def onTouch():
	GPIO.output(BUZZTOUCH, GPIO.HIGH)

def offTouch():
	GPIO.output(BUZZTOUCH, GPIO.LOW)

def beep():
	print('beep');
	onTouch()
	time.sleep(0.25)
	offTouch()
	time.sleep(0.1)

# Detect touch switch
def detectTouch1(chn):
	global canBuzz
	if canBuzz:
		beep()
		beep()
	else:
		beep()
	canBuzz = not canBuzz

def detectTouch2(chn):
	global canAlarm
	if canAlarm:
		beep()
		beep()
	else:
		beep()
	canAlarm = not canAlarm

# PIR Detect
def detectPir(chn):
	if (GPIO.input(PIR1) == 1 or GPIO.input(PIR2) == 1) and canAlarm:
		print('detect')
		onAlarm()
	if GPIO.input(PIR1) == 0 and GPIO.input(PIR2) == 0 and canAlarm:
		print('detect end')
		offAlarm()

# Flips vibration motor
def flip():
	if buzzState:
		offBuzz()
	else:
		onBuzz()

def loop():
	global lastDistCheck
	global lastBuzzTime
	
	# Main loop
	while True:
		if canBuzz:
			# Every 0.25 seconds, get distance
			if time.time() - lastDistCheck > 0.25:
				dis = min(distance(TRIG1, ECHO1), distance(TRIG2, ECHO2))
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
				offBuzz() # Off when doesn't detect anything
		else:
			offBuzz()
			
		time.sleep(0.05)

def destroy():
	offBuzz();        # Buzzer off
	offAlarm();       # Alarm off
	offTouch();   # Touch Buzzer off
	GPIO.cleanup()    # Release resource
	print('off')

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
		destroy()

