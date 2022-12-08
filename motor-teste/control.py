import RPi.GPIO as GPIO
from gpiozero import Motor, Button, LED
from time import sleep
import encoder
from datetime import datetime, timedelta



################
# VARIAVEIS GLOBAIS E CONSTANTES
################

global razaoEncoders, gapCounterEsq, gapCounterDir, anguloDoCarro, distDoCarro, inputDirecao, inputAngulo, inputVelocidade, inputDistancia
global terminou, tempoAtualEsq, tempoInicialEsq, tempoAtualDir, tempoInicialDir
razaoEncoders = 0     # gapCounterEsq / gapCounterDir
gapCounterEsq = 0       # total de gaps lidos (entre 0 e 20)
gapCounterDir = 0       # total de gaps lidos (entre 0 e 20)
anguloDoCarro = 0.0
distDoCarro = 0.0
inputAngulo = 0.0          # entre -180 (esq) e 180 (dir) graus
inputVelocidade = 0.0      # entre 0 e 1
inputDirecao = ""          # frente ou tras
inputDistancia = 0.0
terminou = False
tempoInicialEsq = None
tempoAtualEsq = None
tempoInicialDir = None
tempoAtualDir = None


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
  global inputDirecao, inputAngulo, inputVelocidade, inputDistancia, tempoInicialEsq, tempoInicialDir

  inputDirecao = input("Para qual direcao deseja andar, 'FRENTE', 'TRAS' ou 'NENHUMA'?\n")
  
  if inputDirecao == 'FRENTE' or inputDirecao == 'TRAS':
    inputDistancia = float(input("Quanto de distancia deseja andar? (em m)\n"))*100
  else:
    inputDistancia = 0.0
  inputAngulo = float(input("Para qual angulo deseja girar (em graus)?\n"))
  inputVelocidade = float(input("Com quanto de velocidade, entre 0 e 100 porcento?\n"))/100

  print("Direcao: %s\n Angulo %.2f graus\n Velocidade: %.2f\n"%(inputDirecao, inputAngulo, inputVelocidade*100)) 
  tempoInicialEsq = datetime.now()
  tempoInicialDir = datetime.now()

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
  global inputAngulo, anguloDoCarro, gapCounterEsq, terminou

  anguloDoCarro = encoder.calculaAnguloDoCarrinho(gapCounterEsq)
  
  print("Gaps: %d - Angulo: %.3f"%(gapCounterEsq, anguloDoCarro))

  if anguloDoCarro < abs(inputAngulo)-10:
    esquerda()
  else:
    terminou = True
    print("Terminou de girar! - Angulo Atual: %.3f"%(anguloDoCarro))
    parar()


def giro_direita():
  global inputAngulo, anguloDoCarro, gapCounterDir, terminou

  anguloDoCarro = encoder.calculaAnguloDoCarrinho(gapCounterDir)
  
  print("Gaps: %d - Angulo: %.3f"%(gapCounterDir, anguloDoCarro))

  if anguloDoCarro < abs(inputAngulo)-10:
    direita()
  else:
    terminou = True
    print("Terminou de girar! - Angulo Atual: %.3f"%(anguloDoCarro))
    parar()



################
# CONTROLE DO CARRINHO: ANDAR
################

def andar():
  global inputDirecao
  
  if inputDirecao == "FRENTE":
    andar_frente()
  elif inputDirecao == "TRAS":
    andar_tras()
  else:
    parar()

def andar_frente():
  global inputDistancia, distDoCarro, gapCounterEsq, terminou, inputVelocidade

  distDoCarro = encoder.calculaArcoDaRoda(gapCounterEsq)
  fator = 0.5
  
  print("Gaps: %d - Dist: %.3f"%(gapCounterEsq, distDoCarro/fator))

  if distDoCarro < inputDistancia*fator:
    frente()
  else:
    terminou = True
    print("Terminou de andar! - Dist Atual: %.3f"%(distDoCarro/fator))
    parar()


def andar_tras():
  global inputDistancia, distDoCarro, gapCounterEsq, terminou, inputVelocidade

  distDoCarro = encoder.calculaArcoDaRoda(gapCounterEsq)
  fator = 0.5
  
  print("Gaps: %d - Dist: %.3f"%(gapCounterEsq, distDoCarro/fator))

  if distDoCarro < inputDistancia*fator:
    tras()
  else:
    terminou = True
    print("Terminou de andar! - Dist Atual: %.3f"%(distDoCarro/fator))
    parar()


################
# ENCODER
################

def encoder1_handler(pin):
  global gapCounterEsq, tempoAtualEsq, tempoInicialEsq
  tempoAtualEsq = datetime.now()
  
  if tempoAtualEsq - tempoInicialEsq > timedelta(milliseconds=50):
    gapCounterEsq+=1
    tempoInicialEsq = tempoAtualEsq
  
def encoder2_handler(pin):
  global gapCounterDir, tempoAtualDir, tempoInicialDir
  tempoAtualDir = datetime.now()
  
  if tempoAtualDir - tempoInicialDir > timedelta(milliseconds=50):
    gapCounterDir+=1
    tempoInicialDir = tempoAtualDir

##  ratioEncoders()

def ratioEncoders():
  global razaoEncoders, gapCounterEsq, gapCounterDir
  razaoEncoders = gapCounterEsq/gapCounterDir
  print("Razao: %.5f"%(razaoEncoders))

GPIO.add_event_detect(encoder.ENCODER1_SIGNAL_PIN, GPIO.RISING, encoder1_handler)
GPIO.add_event_detect(encoder.ENCODER2_SIGNAL_PIN, GPIO.RISING, encoder2_handler)



################
# INICIAR
################

initialize()

while True:
  if not terminou:
    #andar()
    girar()
  else:
    terminou = False
    print("Terminou!")
    break