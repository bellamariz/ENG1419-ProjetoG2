# Motor - classe para controle do motor

import RPi.GPIO as GPIO
from gpiozero import Motor
import encoder

class CarMotor:

  def __init__(self, speed, angle, direction, forward_pin, backward_pin):
    self.speed = speed          # speed input
    self.angle = angle          # angle input
    self.direction = direction  # direction input
    self.gapsEncoder = 0        # number of encoder gaps read
    self.currentAngle = 0.0     # car angle based on gapsEncoder
    self.motor = Motor(forward_pin, backward_pin)


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

  def setCurrentAngle(self, angle):
    self.currentAngle = angle

  def getCurrentAngle(self):
    return self.currentAngle


  # Direction control
  def motorForward(self, inputSpeed = 0.5):
    # TODO: calibrar valor --> setSpeed(inputSpeed)
    self.motor.forward(self.speed)

  def motorBackward(self, inputSpeed = 0.5):
    # TODO: calibrar valor --> setSpeed(inputSpeed)
    self.motor.backward(self.speed)

  def motorStop(self):
    # TODO: criar função para parar gradualmente
    self.motor.stop()