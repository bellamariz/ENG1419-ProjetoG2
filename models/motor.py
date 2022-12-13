# Motor - classe para controle do motor

from gpiozero import Motor
from encoder import *
import pins

# CarMotor: class for initializing Motor object
class CarMotor:

  def __init__(self, speed, angle, direction, distance, forward_pin, backward_pin):
    self.speed = speed          # speed input
    self.angle = angle          # angle input
    self.direction = direction  # direction input
    self.distance = distance    # distance input
    self.motor = Motor(forward_pin, backward_pin)
    self.encoder = Encoder()

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

  def setDistance(self, distance):
    self.distance = distance
    
  def getDistance(self):
    return self.distance


  # Direction control
  def motorForward(self):
    self.motor.forward(self.speed)

  def motorBackward(self):
    self.motor.backward(self.speed)

  def motorStop(self):
    self.motor.stop()


# MotorControl: class for controlling motors (called by Car)
class MotorControl:

  def __init__(self, speed, angle, direction, distance):
    self.motorLeft  = CarMotor(speed, angle, direction, distance, pins.HBRIDGE_IN3, pins.HBRIDGE_IN4)
    self.motorRight = CarMotor(speed, angle, direction, distance, pins.HBRIDGE_IN1, pins.HBRIDGE_IN2)
    self.speed = speed
    self.angle = angle
    self.direction = direction
    self.distance = distance

  # Getters
  def getMotorLeft(self):
    return self.motorLeft

  def getMotorRight(self):
    return self.motorRight

  def setSpeed(self, speed):
    self.speed = speed
    self.motorRight.setSpeed(speed)
    self.motorLeft.setSpeed(speed)

  def getSpeed(self):
    return self.speed

  def setAngle(self, angle):
    self.angle = angle
    self.motorRight.setAngle(angle)
    self.motorLeft.setAngle(angle)

  def getAngle(self):
    return self.angle

  def setDirection(self, direction):
    self.direction = direction
    self.motorRight.setDirection(direction)
    self.motorLeft.setDirection(direction)

  def getDirection(self):
    return self.direction

  def setDistance(self, distance):
    self.distance = distance
    self.motorRight.setDistance(distance)
    self.motorLeft.setDistance(distance)
    
  def getDistance(self):
    return self.distance
  

  # Motor functions
  def moveForward(self, gapCounterLeft):
    carDistance = self.motorLeft.encoder.getWheelArcLength(gapCounterLeft)
    factor = 0.5

    print("Gaps: %d - Dist: %.3f"%(gapCounterLeft, carDistance/factor))

    if carDistance < self.distance*factor:
      self.motorLeft.motorForward()
      self.motorRight.motorForward()
    else:
      print("Terminou de andar! - Dist Atual: %.3f"%(carDistance/factor))
      self.stop()

      return True
    
    return False

  def moveBackward(self, gapCounterLeft):
    carDistance = self.motorLeft.encoder.getWheelArcLength(gapCounterLeft)
    factor = 0.5

    print("Gaps: %d - Dist: %.3f"%(gapCounterLeft, carDistance/factor))

    if carDistance < self.distance*factor:
      self.motorLeft.motorBackward()
      self.motorRight.motorBackward()
    else:
      print("Terminou de andar! - Dist Atual: %.3f"%(carDistance/factor))
      self.stop()

      return True
    
    return False


  def turnLeft(self, gapCounterLeft):
    carAngle = self.motorLeft.encoder.getCarArcAngle(gapCounterLeft)
    print("car angle", carAngle,gapCounterLeft)
    
    if self.speed <= 0.3:
      factor = 10
    else:
      factor = 10+(20*self.speed)

    print("Gaps: %d - Angulo: %.3f"%(gapCounterLeft, carAngle))

    if carAngle < abs(self.angle)-factor:
      self.motorLeft.motorBackward()
      self.motorRight.motorForward()
    else:
      print("Terminou de girar! - Angulo Atual: %.3f"%(carAngle))
      self.stop()

      return True
    
    return False

  def turnRight(self, gapCounterLeft):
    carAngle = self.motorLeft.encoder.getCarArcAngle(gapCounterLeft)
    print("car angle", carAngle)
    
    if self.speed <= 0.3:
      factor = 10
    else:
      factor = 10+(20*self.speed)

    print("Gaps: %d - Angulo: %.3f"%(gapCounterLeft, carAngle))

    if carAngle < abs(self.angle)-factor:
      self.motorLeft.motorForward()
      self.motorRight.motorBackward()
    else:
      print("Terminou de girar! - Angulo Atual: %.3f"%(carAngle))
      self.stop()

      return True
    
    return False


  # Stop motors
  def stop(self):
    self.motorLeft.motorStop()
    self.motorRight.motorStop()


