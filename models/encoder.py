import RPi.GPIO as GPIO
import math
import pins

# Number of gaps in encoder
TOTAL_GAPS = 20
# Wheel external radius (in cm)
WHEEL_RADIUS = 3.2
# Wheel circumference (in cm)
WHEEL_CIRCUMF = 2*math.pi*WHEEL_RADIUS
# Radius between car's midpoint and the wheel
CAR_RADIUS = 6.5

class Encoder:

  def __ini__(self):
    print("Init encoder")

  # Calculations for the arc length travelled by the car
  # Calcula o comprimento de arco percorrido pela roda (dado o num de gaps do encoder detectados)
  def getWheelArcLength(self, gaps):
    return (gaps/TOTAL_GAPS)*WHEEL_CIRCUMF

  # Calculo o angulo (em graus) percorrido pela roda (dado o num de gaps do encoder detectados)
  def getWheelArcAngle(self, gaps):
    return (self.getWheelArcLength(gaps)/WHEEL_RADIUS)*(180/math.pi)

  # Calcula o comprimento de arco percorrido pelo carrinho girando 
  # Eh o mesmo arco percorrido pelo movimento da roda
  def getCarArcLength(self, gaps):
    return self.getWheelArcLength(gaps)

  def getCarArcAngle(self, gaps):
    return (self.getCarArcLength(gaps)/CAR_RADIUS)*(180/math.pi)
