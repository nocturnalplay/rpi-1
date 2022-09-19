import RPi.GPIO as GPIO
from time import sleep
import socket
import sys
import json

# check the host and port argv values
if len(sys.argv) < 3:
    print("no input argument [host] [port]")
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

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
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        print("socket created...")
        s.connect((host,port))
        print("connected to the server")
        s.send(b'[CLIENT]:Give RGB values to glow the bulb')

        #data collection to prevent the intercept in the soket data
        precolor=[100,100,100]#default in off condition
        while 1:
            try:
                #rgb = list(map(int,input("enter the value space between 0 to 100 [red] [green] [blue]:").split(" ")))
                # rgb =list(map(int,s.recv(1024).decode().split(" ")))
                # print(f'RGB:{rgb}')
                data = list(s.recv(11).decode('utf-8').strip().split(" "))
                if data:
                    rgb=[100,100,100]#default in off condition

                    if len(data) > 3 or len(data) < 3:
                        rgb = precolor
                    else:
                        for i in range(3):
                            for i,value in enumerate(data):
                                if value == "" or value == " " or len(value) > 3:
                                    rgb[i] = int(precolor[i])
                                else:
                                    if int(value) > 100:
                                        rgb[i] = int(precolor[i])
                                    else:
                                        rgb[i] = int(value)
                                
                            precolor = rgb
                            print(f"RGB:{rgb}::DATA:{data}")
                            for i in range(len(channel)):
                                rgbcolor[i].ChangeDutyCycle(rgb[i])
                    del data,rgb
            except ValueError as e:
                print(f"[ERROR]:{e}")
                print("try again...")
                GPIO.cleanup()
                sys.exit()

except KeyboardInterrupt:
    GPIO.cleanup()
    # end the PWM 
    for i in range(len(rgbcolor)):
        rgbcolor[i].stop()
    print("\nExit....")
    #close the socket connection
    s.close()
