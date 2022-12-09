import RPi.GPIO as GPIO
from motor import *

# Car: class for defining Car attributes
class Car:

  def __init__(self, speed, angle, direction):
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
  def move(self, gapCounterLeft):
    finished = False
    if self.direction == "F":
      finished = self.motorControl.moveForward(self.distance, gapCounterLeft)
    elif self.direction == "B":
      finished = self.motorControl.moveBackward(self.distance, gapCounterLeft)
    else:
      self.motorControl.stop()
      return True
    
    return finished

  # Turns car to left for negative angles and to right for positive angles
  def turn(self, gapCounterLeft, gapCounterRight):
    finished = False
    if self.angle < 0:
      finished = self.motorControl.turnLeft(self.angle, gapCounterLeft)
    elif self.angle > 0:
      finished = self.motorControl.turnRight(self.angle, gapCounterRight)
    else:
      self.motorControl.stop()
      return True

    return finished

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



