import random
from constantes import *

def posiciones_automaticas() -> str:
    letra = letras_posibles[random.randint(0, len(letras_posibles) - 1)]
    numero = numeros_posibles[random.randint(0, len(numeros_posibles) - 1)]
    direccion = direcciones_posibles[random.randint(0, len(direcciones_posibles) - 1)]
    return letra + str(numero) + direccion

def ataques_automaticos() -> str:
    letra = letras_posibles[random.randint(0, len(letras_posibles) - 1)]
    numero = numeros_posibles[random.randint(0, len(numeros_posibles) - 1)]
    return letra + str(numero)