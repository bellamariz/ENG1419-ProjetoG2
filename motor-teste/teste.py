from gpiozero import Motor
import RPi.GPIO as GPIO

global gapCounter1, gapCounter2
gapCounter1 = 0
gapCounter2 = 0

# Enconder signal GPIO pin
ENCODER1_SIGNAL_PIN = 26
ENCODER2_SIGNAL_PIN = 4

# H Bridge GPIO pins
# IN3,IN4 (left motor); IN1,IN2 (right motor);
IN1 = 18
IN2 = 23
IN3 = 24
IN4 = 25

def frente(vel):
  motorEsq.forward(vel)
  motorDir.forward(vel)

def tras(vel):
  motorEsq.backward(vel)
  motorDir.backward(vel)

def esquerda(vel):
  motorEsq.backward(vel)
  motorDir.forward(vel)

def direita(vel):
  motorEsq.forward(vel)
  motorDir.backward(vel)

def parar():
  motorEsq.stop()
  motorDir.stop()
  
def encoder1_handler(pin):
  global gapCounter1, gapCounter2
  gapCounter1+=1
  
def encoder2_handler(pin):
  global gapCounter1, gapCounter2
  gapCounter2+=1
  
  print("Razao: %.5f"%(gapCounter1/gapCounter2))
    
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ENCODER1_SIGNAL_PIN,GPIO.IN)
GPIO.setup(ENCODER2_SIGNAL_PIN,GPIO.IN)

GPIO.add_event_detect(ENCODER1_SIGNAL_PIN, GPIO.RISING, encoder1_handler)
GPIO.add_event_detect(ENCODER2_SIGNAL_PIN, GPIO.RISING, encoder2_handler)

motorEsq = Motor(IN3, IN4) # IN3 E IN4 (motor esquerda)
motorDir = Motor(IN1, IN2) # IN1 E IN2 (motor direita) 
