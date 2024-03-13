#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

PirPin = 11
Buzzpin = 12
test = 1

def setup():
	GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location
	GPIO.setup(Buzzpin, GPIO.OUT)     # Set Buzzer Led Pin mode to output
	GPIO.setup(PirPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(PirPin, GPIO.BOTH, callback=detect)
	off();
	beep(0.5);
	
def on():
	print('on')
	GPIO.output(Buzzpin, GPIO.LOW)

def off():
	print('off')
	GPIO.output(Buzzpin, GPIO.HIGH)

def beep(x):
	on()
	time.sleep(x)
	off()
	time.sleep(x)

def detect(chn):
	global test
	print('detect' + str(GPIO.input(PirPin)))
	test = GPIO.input(PirPin);
	if GPIO.input(PirPin) == 0:
		on()
	if GPIO.input(PirPin) == 1:
		off()

def loop():
	while True:
		pass

def destroy():
	GPIO.output(Buzzpin, GPIO.HIGH)       # Buzzer off
	GPIO.cleanup()                        # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

