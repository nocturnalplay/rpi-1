import RPi.GPIO as GPIO
from time import sleep
import random

channel = [12,13,19]

# for board setting 
GPIO.setmode(GPIO.BCM)
#setup to pin mode
for i in channel:
    GPIO.setup(i,GPIO.OUT)
#rgb in pwm mode in a list
rgbcolor= [GPIO.PWM(c,1000) for c in channel]
# start the birghtness with 100
for i in range(len(rgbcolor)):
    rgbcolor[i].start(100)
try:
    while 1:
        try:
            # rgb=[random.randrange(0,100) for i in range(3)]
            # print(rgb)
            # rgb = list(map(int,input("enter the value space between 0 to 100 [red] [green] [blue]:").split(" ")))
            
            for i,c in enumerate(channel):
               rgbcolor[i].ChangeDutyCycle(random.randrange(0,100))
            sleep(.1)
        except ValueError as e:
            print(f"[ERROR]:{e}")
except KeyboardInterrupt:
    GPIO.cleanup()
    # end the PWM 
    for i in range(len(rgbcolor)):
        rgbcolor[i].stop()
    print("exit....")

# p = GPIO.PWM(channel,1000)
# p.start(50)

# try:
#     while 1:
#         try:
#             d = int(input("set a duty:"))
#             # f = int(input("frequency:"))
#             if(d == 'q'):
#                 break
#             p.ChangeDutyCycle(d)
#             # p.ChangeFrequency(f)
#         except ValueError as e:
#             pass
# except KeyboardInterrupt as e:
#     pass
# input("Enter the key to quit")
# p.stop()
# GPIO.cleanup()