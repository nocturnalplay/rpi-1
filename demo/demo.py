import RPi.GPIO as GPIO
from time import sleep

ledPin = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
p = GPIO.PWM(ledPin,1000)
p.start(10)

try:
    while 1:
        i = int(input(">"))
        p.ChangeDutyCycle(i)
except KeyboardInterrupt as e:
    print("exit...")

GPIO.cleanup()
p.stop()
# GPIO.output(ledPin, GPIO.LOW)

# try:
#     while 1:
#             GPIO.output(ledPin, GPIO.HIGH)
#             sleep(0.075)
#             GPIO.output(ledPin, GPIO.LOW)
#             sleep(0.075)
# except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
#     GPIO.cleanup() # cleanup all GPIO
