import RPi.GPIO as GPIO
from car import *
import pins
from datetime import datetime, timedelta
from gpiozero import DistanceSensor

global gapCounterLeft, gapCounterRight, inputDirection, inputAngle, inputSpeed, inputDistance
global finished, timeNowLeft, timeInitLeft, timeNowRight, timeInitRight
global counterTeste
counterTeste = 0
gapCounterLeft = 0       
gapCounterRight = 0      
inputAngle = 0.0         
inputSpeed = 0.0         
inputDirection = ""      
inputDistance = 0.0
finished = False
timeInitLeft = None
timeNowLeft = None
timeInitRight = None
timeNowRight = None

# Initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Encoder signal pin setup
GPIO.setup(pins.ENCODER1_SIGNAL_PIN,GPIO.IN)
GPIO.setup(pins.ENCODER2_SIGNAL_PIN,GPIO.IN)

# Reads user input
def initialize():
  global inputDirection, inputAngle, inputSpeed, inputDistance, timeInitLeft, timeInitRight

  inputDirection = input("Para qual direcao deseja andar, 'F', 'T' ou 'NENHUMA'?\n")
  
  if inputDirection == 'F' or inputDirection == 'T':
    inputDistance = float(input("Quanto de distancia deseja andar? (em m)\n"))*100
  else:
    inputDistance = 0.0
  inputAngle = float(input("Para qual angulo deseja girar (em graus)?\n"))
  inputSpeed = float(input("Com quanto de velocidade, entre 0 e 100 porcento?\n"))/100

  print("Direcao: %s\n Angulo %.2f graus\n Velocidade: %.2f\n Distancia: %.2f m\n"%(inputDirection, inputAngle, inputSpeed*100, inputDistance/100)) 
  timeInitLeft = datetime.now()
  timeInitRight = datetime.now()

# Handlers for encoder pin interrupts
def encoder1_handler(pin):
  global gapCounterLeft, timeNowLeft, timeInitLeft
  timeNowLeft = datetime.now()
  
  if timeNowLeft - timeInitLeft > timedelta(milliseconds=50):
##    print("Inc encoder esq!\n")
    gapCounterLeft+=1
    timeInitLeft = timeNowLeft
  
def encoder2_handler(pin):
  global gapCounterRight, timeNowRight, timeInitRight
  timeNowRight = datetime.now()
  
  if timeNowRight - timeInitRight > timedelta(milliseconds=50):
##    print("Inc encoder dir!\n")
    gapCounterRight+=1
    timeInitRight = timeNowRight

def print_parameters(obj):
    speed = obj.getSpeed()
    angle = obj.getAngle()
    direction = obj.getDirection()
    distance = obj.getDistance()
    
    print("speed = %.3f, angle = %.3f, dir = %s, dist = %.3f"%(speed, angle, direction, distance))

# Initialize
initialize()
car = Car(inputSpeed, inputAngle, inputDirection, inputDistance)

GPIO.add_event_detect(pins.ENCODER1_SIGNAL_PIN, GPIO.RISING, encoder1_handler)
GPIO.add_event_detect(pins.ENCODER2_SIGNAL_PIN, GPIO.RISING, encoder2_handler)

distanceSensor = DistanceSensor(echo=pins.DISTANCE_ECHO, trigger=pins.DISTANCE_TRIGGER)
distanceSensor.threshold_distance = 0.2 # 20cm or 0.2m

while True:
  finished = car.turn(gapCounterLeft, gapCounterRight)
  #finished = car.move(gapCounterLeft, gapCounterRight)
  print("Finished: ", finished)
  if finished:
    print("Terminou!")
    break
