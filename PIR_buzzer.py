#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

PIR = 11
BUZZ = 12

# Setup board
def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(BUZZ, GPIO.OUT)     # Set Buzzer Led Pin mode to output
	GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(PIR, GPIO.BOTH, callback=detect)
	off(); # Ensure buzzer is off
	
def on():
	GPIO.output(BUZZ, GPIO.LOW)

def off():
	GPIO.output(BUZZ, GPIO.HIGH)

def beep(x):
	on()
	time.sleep(x)
	off()
	time.sleep(x)

# Detect change in input
def detect(chn):
	if GPIO.input(PIR) == 1:
		print('detect')
		on()
	if GPIO.input(PIR) == 0:
		print('detect end')
		off()

def loop():
	while True:
		pass # Main loop does nothing, code is in the detect

def destroy():
	GPIO.output(BUZZ, GPIO.HIGH)       # Buzzer off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
