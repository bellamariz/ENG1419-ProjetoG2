# Classe Car - implementacao dos metodos de controle do carrinho
import RPi.GPIO as GPIO
from .motor import CarMotor

# Initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# H Bridge GPIO pins
# IN3,IN4 (left motor); IN1,IN2 (right motor);
HBRIDGE_IN1 = 10
HBRIDGE_IN2 = 9
HBRIDGE_IN3 = 17
HBRIDGE_IN4 = 27

# Initialize motors
global motorLeft, motorRight
motorLeft  = None
motorRight = None

class Car:

  def __init__(self):
    self.speed = 0.3      # (0,1]
    self.angle = 0.0      # negative: left, positive: right
    self.direction = "F"  # F - forward, B - backward, N - neither
    self.modeAuto = True  # True - auto, False - manual

  # Getters and Setters
  def setSpeed(self, speed):
    self.speed = speed

  def getSpeed(self):
    return self.speed

  def setAngle(self, angle):
    self.angle = angle

  def getAngle(self):
    return self.angle

  def setDirection(self, direction):
    self.direction = direction

  def getDirection(self):
    return self.direction

  def setModeAuto(self, modeAuto):
    self.modeAuto = modeAuto

  def getModeAuto(self):
    return self.modeAuto

  # Car motor functions
  def moveForward(self):
    global motorLeft, motorRight
    motorLeft.motorForward(self.speed)
    motorRight.motorForward(self.speed)

  def moveBackward(self):
    global motorLeft, motorRight
    motorLeft.motorBackward(self.speed)
    motorRight.motorBackward(self.speed)

  def stopCar(self):
    global motorLeft, motorRight
    motorLeft.motorStop()
    motorRight.motorStop()

  def turnLeft(self):
    global motorLeft, motorRight
    motorLeft.motorBackward(self.speed)
    motorRight.motorForward(self.speed)

  def turnRight(self):
    global motorLeft, motorRight
    motorLeft.motorForward(self.speed)
    motorRight.motorBackward(self.speed)
      

# Initialize car
car = Car()

motorLeft  = CarMotor(car.getSpeed, car.getAngle, car.getDirection, HBRIDGE_IN3, HBRIDGE_IN4)
motorRight = CarMotor(car.getSpeed, car.getAngle, car.getDirection, HBRIDGE_IN1, HBRIDGE_IN2)




