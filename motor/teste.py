from gpiozero import Motor
import RPi.GPIO as GPIO
from time import sleep

gaps = 0

GPIO.setmode(GPIO.BCM)

GPIO.setup(26,GPIO.IN)

encoderStatus = GPIO.input(26)





motorEsq = Motor(2, 3) #in1 forward, in2 backward
motorDir = Motor(27, 4) #in4 forward, in3 backward

##motorEsq.forward(0.5)
##motorDir.forward(0.5)

motorEsq.stop()
motorDir.stop()

while True:
    if GPIO.input(26) == True:
        gaps+=1
        
    print("Gaps:", gaps)
    print("Status:", GPIO.input(26))
    
    sleep(0.1)