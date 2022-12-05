import RPi.GPIO as GPIO
from gpiozero import Motor, Button, LED
from time import sleep
import encoder



################
# VARIAVEIS GLOBAIS E CONSTANTES
################

global razaoEncoders, gapCounter1, gapCounter2, anguloDoCarro, inputDirecao, inputAngulo, inputVelocidade
razaoEncoders = 0     # gapCounter1 / gapCounter2
gapCounter1 = 0       # total de gaps lidos (entre 0 e 20)
gapCounter2 = 0       # total de gaps lidos (entre 0 e 20)
anguloDoCarro = 0.0
inputAngulo = 0.0          # entre -180 (esq) e 180 (dir) graus
inputVelocidade = 0.0      # entre 0 e 1
inputDirecao = ""          # frente ou tras

# H Bridge GPIO pins
# IN3,IN4 (left motor); IN1,IN2 (right motor);
HBRIDGE_IN1 = 18
HBRIDGE_IN2 = 23
HBRIDGE_IN3 = 24
HBRIDGE_IN4 = 25



################
# INICIALIZACOES
################

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(encoder.ENCODER1_SIGNAL_PIN,GPIO.IN)
GPIO.setup(encoder.ENCODER2_SIGNAL_PIN,GPIO.IN)

motorEsq = Motor(HBRIDGE_IN3, HBRIDGE_IN4) # IN3 E IN4 (motor esquerda)
motorDir = Motor(HBRIDGE_IN1, HBRIDGE_IN2) # IN1 E IN2 (motor direita) 

def initialize():
  global inputDirecao, inputAngulo, inputVelocidade

  inputDirecao = input("Para qual direcao deseja andar, 'FRENTE', 'TRAS' ou 'NENHUMA'?\n")
  inputAngulo = float(input("Para qual angulo deseja girar (em graus)?\n"))
  inputVelocidade = float(input("Com quanto de velocidade, entre 0 e 100 porcento?\n"))/100

  print("Direcao: %s\n Angulo %.2f graus\n Velocidade: %.2f\n"%(inputDirecao, inputAngulo, inputVelocidade*100))



################
# CONTROLE DO MOTOR
################

def frente():
  global inputVelocidade
  motorEsq.forward(inputVelocidade)
  motorDir.forward(inputVelocidade)

def tras():
  global inputVelocidade
  motorEsq.backward(inputVelocidade)
  motorDir.backward(inputVelocidade)

def esquerda():
  global inputVelocidade
  motorEsq.backward(inputVelocidade)
  motorDir.forward(inputVelocidade)

def direita():
  global inputVelocidade
  motorEsq.forward(inputVelocidade)
  motorDir.backward(inputVelocidade)

def parar():
  motorEsq.stop()
  motorDir.stop()



################
# CONTROLE DO CARRINHO: GIRAR
################

def girar():
  global inputAngulo
  
  if inputAngulo < 0:
    giro_esquerda()
  elif inputAngulo > 0:
    giro_direita()
  else:
    andar()

def giro_esquerda():
  global inputAngulo, anguloDoCarro, gapCounter1

  anguloDoCarro = encoder.calculaAnguloDoCarrinho(gapCounter1)

  if anguloDoCarro < abs(inputAngulo):
    esquerda()
  else:
    print("Terminou de girar! - Angulo Atual: %.4f"%(anguloDoCarro))
    parar()

def giro_direita():
  global inputAngulo, anguloDoCarro, gapCounter1

  anguloDoCarro = encoder.calculaAnguloDoCarrinho(gapCounter1)

  if anguloDoCarro < abs(inputAngulo):
    direita()
  else:
    print("Terminou de girar! - Angulo Atual: %.4f"%(anguloDoCarro))
    parar()



################
# CONTROLE DO CARRINHO: ANDAR
################

def andar():
  global inputDirecao

  if inputDirecao == "FRENTE":
    frente()
  elif inputDirecao == "TRAS":
    tras()
  else:
    parar()



################
# ENCODER
################

def encoder1_handler(pin):
  global gapCounter1, gapCounter2
  gapCounter1+=1

  if gapCounter1 > 100:
    gapCounter1 = 0
    gapCounter2 = 0
  
def encoder2_handler(pin):
  global gapCounter1, gapCounter2
  gapCounter2+=1

  ratioEncoders()

def ratioEncoders():
  global razaoEncoders, gapCounter1, gapCounter2
  razaoEncoders = gapCounter1/gapCounter2
  print("Razao: %.5f"%(razaoEncoders))

GPIO.add_event_detect(encoder.ENCODER1_SIGNAL_PIN, GPIO.RISING, encoder1_handler)
GPIO.add_event_detect(encoder.ENCODER2_SIGNAL_PIN, GPIO.RISING, encoder2_handler)



################
# INICIAR
################

initialize()
