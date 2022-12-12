import RPi.GPIO as GPIO
from motor import *
from gpiozero import DistanceSensor
import pins

# Car: class for defining Car attributes
class Car:

  def __init__(self, speed, angle, direction, distance):
    self.speed = speed          # float in interval: (0,1]
    self.angle = angle          # float in interval: [-360, 360] (negative: left, positive: right)
    self.direction = direction  # F - forward, B - backward, N - neither
    self.distance = distance    # in cm
    self.modeAuto = True        # True - auto, False - manual
    self.distanceSensor = DistanceSensor(echo=pins.DISTANCE_ECHO, trigger=pins.DISTANCE_TRIGGER)
    self.motorControl = MotorControl(speed, angle, direction, distance)

  # Getters and Setters
  def setSpeed(self, speed):
    self.speed = speed
    self.motorControl.setSpeed(speed)

  def getSpeed(self):
    return self.speed

  def setAngle(self, angle):
    self.angle = angle
    self.motorControl.setAngle(angle)

  def getAngle(self):
    return self.angle

  def setDirection(self, direction):
    self.direction = direction
    self.motorControl.setDirection(direction)

  def getDirection(self):
    return self.direction

  def setDistance(self, distance):
    self.distance = distance
    self.motorControl.setDistance(distance)
    
  def getDistance(self):
    return self.distance

  def setModeAuto(self, modeAuto):
    self.modeAuto = modeAuto

  def getModeAuto(self):
    return self.modeAuto

  # Car functions
  # Moves car forwards or backwards based on user input
  def move(self, gapCounterLeft, gapCounterRight):
    finished = False
    if self.direction == "F":
      finished = self.motorControl.moveForward(gapCounterLeft)
    elif self.direction == "B":
      finished = self.motorControl.moveBackward(gapCounterLeft)
    else:
      self.motorControl.stop()
      return True
    
    return finished

  # Turns car to left for negative angles and to right for positive angles
  def turn(self, gapCounterLeft, gapCounterRight):
    finished = False
    if self.angle < 0:
      finished = self.motorControl.turnLeft(gapCounterLeft)
    elif self.angle > 0:
      finished = self.motorControl.turnRight(gapCounterLeft)
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


  # Distance sensor function
  def checkDistSensor(threshold):
    self.distanceSensor.threshold_distance = threshold
    return self.distanceSensor.distance <= threshold


  # Stop car
  def stop(self):
    self.motorControl.stop()


  


