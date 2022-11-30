from gpiozero import Motor
import RPi.GPIO as GPIO

IN1 = 10
IN2 = 9
IN3 = 17
IN4 = 27


motorEsq = Motor(IN3, IN4) # IN3 E IN4 (motor esquerda)
motorDir = Motor(IN1, IN2) # IN1 E IN2 (motor direita) 

def frente():
  motorEsq.forward(0.3)
  motorDir.forward(0.3)

def tras():
  motorEsq.backward(0.3)
  motorDir.backward(0.3)

def esquerda():
  motorEsq.backward(0.3)
  motorDir.forward(0.3)

def direita():
  motorEsq.forward(0.3)
  motorDir.backward(0.3)

def parar():
  motorEsq.stop()
  motorDir.stop()
