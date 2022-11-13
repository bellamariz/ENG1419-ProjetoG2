import math

GAPS_ENCODER = 20
RAIO_INT_RODA = 4.2 # cm
RAIO_EXT_RODA = 6.8 # cm
CIRCUMF_RODA = 2*math.pi*RAIO_EXT_RODA


def get_arc_length(gaps):
    return (gaps * CIRCUMF_RODA)/GAPS_ENCODER

def get_angle(gaps): # in degrees
    return (get_arc_length(gaps)/RAIO_EXT_RODA)*(180/math.pi)


