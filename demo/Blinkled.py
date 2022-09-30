import RPi.GPIO as GPIO
from time import sleep

ledPin = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)

try:
    while 1:
            GPIO.output(ledPin, GPIO.HIGH)
            sleep(0.075)
            GPIO.output(ledPin, GPIO.LOW)
            sleep(0.075)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
