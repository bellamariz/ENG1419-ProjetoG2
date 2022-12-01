import RPi.GPIO as GPIO
from .motor import *

# Car: class for defining Car attributes
class Car:

  def __init__(self, speed = 0.3, angle = 0.0, direction = "F"):
    self.speed = speed          # float in interval: (0,1]
    self.angle = angle          # float in interval: [-360, 360] (negative: left, positive: right)
    self.direction = direction  # F - forward, B - backward, N - neither
    self.modeAuto = True        # True - auto, False - manual
    self.motorControl = MotorControl(speed, angle, direction)

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

  # Car functions
  # Moves car forwards or backwards based on user input
  def move(self):
    if self.direction == "F":
      self.motorControl.moveForward(self.speed)
    elif self.direction == "B":
      self.motorControl.moveBackward(self.speed)
    else:
      self.motorControl.stop()

  # Turns car to left for negative angles and to right for positive angles
  def turn(self):
    if self.angulo < 0:
      self.motorControl.turnLeft(self.angle, self.speed)
    elif self.angulo > 0:
      self.motorControl.turnRight(self.angle, self.speed)
    else:
      self.move()

  # Switch car operation mode
  def switchMode(self):
    self.motorControl.stop()
    self.modeAuto = (not self.modeAuto)

    if self.modeAuto:
      print("Modo auto")
    else:
      print("Modo manual")

  # Stop car
  def stop(self):
    self.motorControl.stop()
    self.motorControl.resetMotors()
    

if __name__ == "__main__":
  # Initialize GPIO pins
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  # Reads user input
  speed = float(input("Velocidade no intervalo (0, 100]: "))/100
  angle = float(input("Angulo que deseja girar no intervalo [-360, 360]: "))
  direction = input("Direcao que deseja andar, frente -> F, tras -> T: ")

  print("Direcao: %s\n Angulo %.2f graus\n Velocidade: %.2f\n"%(direction, angle, speed*100))

  # Initialize car
  car = Car(speed, angle, direction)



