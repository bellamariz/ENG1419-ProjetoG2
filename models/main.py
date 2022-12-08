import RPi.GPIO as GPIO
from car import *
from datetime import datetime, timedelta

global gapCounterLeft, gapCounterRight, inputDirection, inputAngle, inputSpeed, inputDistance
global finished, timeNowLeft, timeInitLeft, timeNowRight, timeInitRight
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

  inputDirection = input("Para qual direcao deseja andar, 'FRENTE', 'TRAS' ou 'NENHUMA'?\n")
  
  if inputDirection == 'FRENTE' or inputDirection == 'TRAS':
    inputDistance = float(input("Quanto de distancia deseja andar? (em m)\n"))*100
  else:
    inputDistance = 0.0
  inputAngle = float(input("Para qual angulo deseja girar (em graus)?\n"))
  inputSpeed = float(input("Com quanto de velocidade, entre 0 e 100 porcento?\n"))/100

  print("Direcao: %s\n Angulo %.2f graus\n Velocidade: %.2f\n"%(inputDirection, inputAngle, inputSpeed*100)) 
  timeInitLeft = datetime.now()
  timeInitRight = datetime.now()

# Handlers for encoder pin interrupts
def encoder1_handler(pin):
  global gapCounterEsq, tempoAtualEsq, tempoInicialEsq
  tempoAtualEsq = datetime.now()
  
  if tempoAtualEsq - tempoInicialEsq > timedelta(milliseconds=50):
    gapCounterEsq+=1
    tempoInicialEsq = tempoAtualEsq
  
def encoder2_handler(pin):
  global gapCounterDir, tempoAtualDir, tempoInicialDir
  tempoAtualDir = datetime.now()
  
  if tempoAtualDir - tempoInicialDir > timedelta(milliseconds=50):
    gapCounterDir+=1
    tempoInicialDir = tempoAtualDir


# Initialize
initialize()
car = Car(inputSpeed, inputAngle, inputDirection)

GPIO.add_event_detect(pins.ENCODER1_SIGNAL_PIN, GPIO.RISING, encoder1_handler)
GPIO.add_event_detect(pins.ENCODER2_SIGNAL_PIN, GPIO.RISING, encoder2_handler)

while True:
  if not finished:
    finished = car.turn(gapCounterLeft, gapCounterRight)
    # finished = car.move(gapCounterLeft)
  else:
    print("Terminou!")
    break