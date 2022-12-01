# Motor - classe para controle do motor

from gpiozero import Motor
from .encoder import *
import pins

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
  def motorForward(self):
    self.motor.forward(self.speed)

  def motorBackward(self):
    self.motor.backward(self.speed)

  def motorStop(self):
    # TODO: criar função para parar gradualmente
    self.motor.stop()


# MotorControl: class for controlling motors (called by Car)
class MotorControl:

  def __init__(self, speed, angle, direction):
    self.motorLeft  = CarMotor(speed, angle, direction, pins.HBRIDGE_IN3, pins.HBRIDGE_IN4)
    self.motorRight = CarMotor(speed, angle, direction, pins.HBRIDGE_IN1, pins.HBRIDGE_IN2)
    self.speed = speed
    self.angle = angle

  # Getters
  def getMotorLeft(self):
    return self.motorLeft

  def getMotorRight(self):
    return self.motorRight
  

  # Motor functions
  def moveForward(self, inputSpeed = 0.5):
    # TODO: calibrar velocidade inputSpeed
    self.motorLeft.motorForward(self.speed)
    self.motorRight.motorForward(self.speed)

  def moveBackward(self, inputSpeed = 0.5):
    # TODO: calibrar velocidade inputSpeed
    self.motorLeft.motorBackward(self.speed)
    self.motorRight.motorBackward(self.speed)

  def turnLeft(self, inputAngle = 45, inputSpeed = 0.5):
    # TODO: calibrar velocidade inputSpeed + angulo inputAngle
    self.motorLeft.motorBackward(self.speed)
    self.motorRight.motorForward(self.speed)

  def turnRight(self, inputAngle = 45, inputSpeed = 0.5):
    # TODO: calibrar velocidade inputSpeed + angulo inputAngle
    self.motorLeft.motorForward(self.speed)
    self.motorRight.motorBackward(self.speed)

  # Stop motors
  def stop(self):
    self.motorLeft.motorStop()
    self.motorRight.motorStop()

  # Reset motor configuration when Car.stop() is called
  def resetMotors(self):
    self.motorLeft.setCurrentAngle(0.0)
    self.motorRight.setCurrentAngle(0.0)
    self.motorLeft.enconder.setGapsCounter(0)
    self.motorRight.enconder.setGapsCounter(0)

