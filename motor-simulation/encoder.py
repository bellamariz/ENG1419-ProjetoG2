# Modulo responsavel por calcular a distancia percorrida pela roda via leitura do encoder 

import math

# Qtde de gaps totais no encoder
GAPS_ENCODER = 20
# Raio externo da roda (em cm)
RAIO_RODA = 3.2
# Circumferencia da roda (em cm)
CIRCUMF_RODA = 2*math.pi*RAIO_RODA

# Raio entre metade do carrinho e a roda (em cm)
RAIO_CARRINHO = 7.9

# Pinagem de leitura do encoder (VCC,GND,SIG)
SIGNAL = 26

# TODO: Leitura do pino SIGNAL do encoder (lib RPi. GPIO) + contagem da qtde de gaps lidos

# Calcula o comprimento de arco percorrido pela roda (dado o num de gaps do encoder detectados)
def calculaArcoDaRoda(gaps):
    return (gaps/GAPS_ENCODER)*CIRCUMF_RODA

# Calculo o angulo (em graus) percorrido pela roda (dado o num de gaps do encoder detectados)
def calculaAnguloDaRoda(gaps):
    return (calculaArcoDaRoda(gaps)/RAIO_RODA)*(180/math.pi)

# Calcula o comprimento de arco percorrido pelo carrinho girando 
# É o mesmo arco percorrido pelo movimento da roda
def calculaArcoDoCarrinho(gaps):
    return calculaArcoDaRoda(gaps)

def calculaAnguloDoCarrinho(gaps):
    return (calculaArcoDoCarrinho(gaps)/RAIO_CARRINHO)*(180/math.pi)


