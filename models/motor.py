# Motor - classe para controle do motor

from gpiozero import Motor
from .encoder import *

# H Bridge GPIO pins
# IN3,IN4 (left motor); IN1,IN2 (right motor);
HBRIDGE_IN1 = 10
HBRIDGE_IN2 = 9
HBRIDGE_IN3 = 17
HBRIDGE_IN4 = 27

# CarMotor: class for initializing Motor object
class CarMotor:

  def __init__(self, speed, angle, direction, forward_pin, backward_pin):
    self.speed = speed          # speed input
    self.angle = angle          # angle input
    self.direction = direction  # direction input
    self.currentAngle = 0.0     # car angle based on gapsCounter
    self.gapsCounter = 0        # number of encoder gaps read
    self.motor = Motor(forward_pin, backward_pin)
    self.enconder = Encoder()

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

  def getGapsCounter(self):
    return self.gapsCounter


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




# MotorControl: class for controlling motors (called by Car)
class MotorControl:

  def __init__(self, speed, angle, direction):
    self.motorLeft  = CarMotor(speed, angle, direction, HBRIDGE_IN3, HBRIDGE_IN4)
    self.motorRight = CarMotor(speed, angle, direction, HBRIDGE_IN1, HBRIDGE_IN2)

  # Getters
  def getMotorLeft(self):
    return self.motorLeft

  def getMotorRight(self):
    return self.motorRight
  

  # Motor functions
  def moveForward(self):
    self.motorLeft.motorForward(self.speed)
    self.motorRight.motorForward(self.speed)

  def moveBackward(self):
    self.motorLeft.motorBackward(self.speed)
    self.motorRight.motorBackward(self.speed)

  def stop(self):
    self.motorLeft.motorStop()
    self.motorRight.motorStop()

  def turnLeft(self):
    self.motorLeft.motorBackward(self.speed)
    self.motorRight.motorForward(self.speed)

  def turnRight(self):
    self.motorLeft.motorForward(self.speed)
    self.motorRight.motorBackward(self.speed)

  # Reset motor configuration when Car.stop() is called
  def resetMotors(self):
    self.motorLeft.setCurrentAngle(0.0)
    self.motorRight.setCurrentAngle(0.0)
    self.motorLeft.enconder.setGapsCounter(0)
    self.motorRight.enconder.setGapsCounter(0)

