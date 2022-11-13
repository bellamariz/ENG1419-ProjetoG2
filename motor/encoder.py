# Modulo responsavel por calcular a distancia percorrida pela roda via leitura do encoder 

import math

# Qtde de gaps no encoder
GAPS_ENCODER = 20
# Raio interno da roda (em cm)
RAIO_INT_RODA = 4.2
# Raio externo da roda (em cm)
RAIO_EXT_RODA = 6.8
# Circumferencia da roda (em cm)
CIRCUMF_RODA = 2*math.pi*RAIO_EXT_RODA


# Calcula o comprimento de arco percorrido dado o numero de gaps
def get_arc_length(gaps):
    return (gaps * CIRCUMF_RODA)/GAPS_ENCODER

# Calculo o angulo (em graus) percorrido dado o numero de gaps
def get_angle(gaps):
    return (get_arc_length(gaps)/RAIO_EXT_RODA)*(180/math.pi)


