# Classe Car - implementacao dos metodos de controle do carrinho

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
