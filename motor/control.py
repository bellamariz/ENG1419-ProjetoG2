import RPi.GPIO as GPIO
from gpiozero import Motor, Button, LED
from time import sleep
import encoder

# Variaveis globais
global gapsEncoder, enconderStatus, angulo, velocidade, direcao, modoManual
gapsEncoder = 0       # total de gaps lidos (entre 0 e 20)
angulo = 0.0          # entre -360 e 360 graus
velocidade = 0.0      # entre 0 e 1
direcao = ""          # frente ou tras
modoManual = False    # True - botoes, False - input do usuario


# Inicializacao da leitura dos pinos GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pinagem de leitura do encoder
GPIO.setup(encoder.SIGNAL,GPIO.IN)
encoderStatus = GPIO.input(encoder.SIGNAL_PIN)

# Pinagem de entrada da ponte H (Esq: ENA,IN1,IN2 / Dir: ENB,IN3,IN4)
HBRIDGE_IN1 = 2
HBRIDGE_IN2 = 3
HBRIDGE_IN3 = 27
HBRIDGE_IN4 = 4

# Inicializa os motores
motorEsq = Motor(HBRIDGE_IN1, HBRIDGE_IN2)
motorDir = Motor(HBRIDGE_IN3, HBRIDGE_IN4)

# Funcoes de controle de direcao do carrinho
def frente():
  global velocidade

  motorEsq.forward(velocidade)
  motorDir.forward(velocidade)

def tras():
  global velocidade

  motorEsq.backward(velocidade)
  motorDir.backward(velocidade)

def esquerda():
  global velocidade

  motorEsq.backward(velocidade)
  motorDir.forward(velocidade)

def direita():
  global velocidade

  motorEsq.forward(velocidade)
  motorDir.backward(velocidade)

def parar():
  motorEsq.stop()
  motorDir.stop()

# Le o input do usuario com as intrucoes de movimento do carrinho
def initialize():
  global angulo, velocidade, direcao

  # direcao = input("Para qual direcao deseja andar, 'frente' ou 'tras'?\n")
  # angulo = float(input("Para qual angulo deseja girar (em graus)?\n"))
  # velocidade = float(input("Com quanto de velocidade, entre 0 e 100 porcento?\n"))/100
  direcao = "frente"
  angulo = 70.0
  velocidade = 0.5

  print("Vc escolheu ir para %s com angulo %.2f graus e velocidade %.2f .\n"%(direcao, angulo, velocidade*100))

# Faz a movimentacao do carrinho (modo automatico)
def start_car():
  global gapsEncoder, angulo, velocidade, direcao

  anguloAtual = encoder.calculaAnguloDoCarrinho(gapsEncoder)
  print("Angulo atual:", anguloAtual)

  # Movimenta o carrinho
  if angulo < 0:
    giro_esquerda(anguloAtual)
  elif angulo > 0:
    giro_direita(anguloAtual)
  else:
    andar()


# Gira o carrinho pra esquerda quando o angulo desejado é negativo (modo automatico)
def giro_esquerda(anguloAtual):
  global angulo

  if anguloAtual < abs(angulo):
    esquerda()
  else:
    parar()
    andar()

# Gira o carrinho pra direita quando o angulo desejado é positivo (modo automatico)
def giro_direita(anguloAtual):
  global angulo

  if anguloAtual < abs(angulo):
    direita()
  else:
    parar()
    andar()

# Anda com o carrinho (modo automatico)
def andar():
  global direcao

  if direcao == "frente":
    frente()
  elif direcao == "tras":
    tras()

# Troca o modo de operacao do carrinho
def trocaModo():
  global modoManual

  # Para os motores pra trocar o modo
  parar()
  # Troca o modo do carrinho
  modoManual = (not modoManual)

  if modoManual:
    print("Modo controle por botoes")
  else:
    print("Modo controle automatico lido da entrada")

# Incrementa o contador de gaps do encoder
def inc_gaps():
  global gapsEncoder
  gapsEncoder+=1

  print("Gaps: %d"%(gapsEncoder))

initialize()

while True: #TODO: substituir while por interrupcao
  # Faz a leitura do pino do encoder
  encoderStatus = GPIO.input(encoder.SIGNAL_PIN)

  if encoderStatus == True:
    inc_gaps()

  print("Status:", encoderStatus)


  # Verifica o modo de operacao do carrinho
  if modoManual:
    # TODO: Botoes de controle manual do motor
    print("Modo Manual\n")
  else:
    print("Modo Auto\n")
    start_car()

    # TODO: critério de parada do carrinho
    # Distancia de um giro completo da roda: 20.1cm --> 20 gaps do encoder

  sleep(0.1)

