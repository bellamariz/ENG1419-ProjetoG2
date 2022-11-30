import RPi.GPIO as GPIO
from gpiozero import Motor, Button, LED
from time import sleep
import encoder

# Variaveis globais
global gapsEncoder, enconderStatus, angulo, anguloAtual, velocidade, direcao, modoManual
gapsEncoder = 0       # total de gaps lidos (entre 0 e 20)
angulo = 0.0          # entre -360 e 360 graus
anguloAtual = 0.0
velocidade = 0.0      # entre 0 e 1
direcao = ""          # frente ou tras
modoManual = False    # True - botoes, False - input do usuario


# Inicializacao da leitura dos pinos GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pinagem de leitura do encoder
GPIO.setup(encoder.SIGNAL_PIN,GPIO.IN)

# Pinagem de entrada da ponte H (Esq: ENA,IN1,IN2 / Dir: ENB,IN3,IN4)
HBRIDGE_IN1 = 10
HBRIDGE_IN2 = 9
HBRIDGE_IN3 = 17
HBRIDGE_IN4 = 27

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

  direcao = input("Para qual direcao deseja andar, 'FRENTE', 'TRAS' ou 'NENHUMA'?\n")
  angulo = float(input("Para qual angulo deseja girar (em graus)?\n"))
  velocidade = float(input("Com quanto de velocidade, entre 0 e 100 porcento?\n"))/100

  print("Direcao: %s\n Angulo %.2f graus\n Velocidade: %.2f\n"%(direcao, angulo, velocidade*100))

# Handler da interrupcao do pino do encoder
def encoder_handler(pin):
  # if GPIO.input(encoder.SIGNAL_PIN) == True:
  
  inc_gaps()
  start_car()

  print("Status:", GPIO.input(pin))


# Faz a movimentacao do carrinho (modo automatico)
def start_car():
  global angulo

  calculaAnguloAtual()

  # Movimenta o carrinho
  if angulo < 0:
    giro_esquerda()
  elif angulo > 0:
    giro_direita()
  else:
    andar()

# Calcula o angulo atual
def calculaAnguloAtual():
    global gapsEncoder, anguloAtual

    anguloAtual = encoder.calculaAnguloDoCarrinho(gapsEncoder)
    print("Angulo atual:", anguloAtual)

# Gira o carrinho pra esquerda quando o angulo desejado é negativo (modo automatico)
def giro_esquerda():
  global gapsEncoder, angulo, anguloAtual

  if anguloAtual < abs(angulo):
    esquerda()
  else:
    print("Terminou de girar! - Angulo Atual: %.4f"%(anguloAtual))
    parar()
    angulo = 0.0

# Gira o carrinho pra direita quando o angulo desejado é positivo (modo automatico)
def giro_direita():
  global gapsEncoder, angulo, anguloAtual

  if anguloAtual < abs(angulo):
    direita()
  else:
    print("Terminou de girar! - Angulo Atual: %.4f"%(anguloAtual))
    parar()
    angulo = 0.0

# Anda com o carrinho (modo automatico)
def andar():
  global direcao

  if direcao == "FRENTE":
    frente()
  elif direcao == "TRAS":
    tras()
  else:
    parar()

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

parar()
initialize()

# Interrupcao para a leitura do pino do encoder
GPIO.add_event_detect(encoder.SIGNAL_PIN, GPIO.RISING, encoder_handler)

# Verifica o modo de operacao do carrinho
if modoManual:
  # TODO: Botoes de controle manual do motor
  print("Modo Manual\n")
else:
  print("Modo Auto\n")
  start_car()
##  parar()
    
# TODO: critério de parada do carrinho
# Distancia de um giro completo da roda: 20.1cm --> 20 gaps do encoder


