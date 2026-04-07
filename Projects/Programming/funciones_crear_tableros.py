from constantes import *
from excepciones import *
import funciones_extra as funex

def crear_tablero() -> dict:
    """Crea el tablero con ·· para cada posición en azul"""
    usuario_dict = {}
    for ascii_letra in range(ord("A"), ord("J") + 1):
        for numero in range(1, 11):
            if chr(ascii_letra) not in usuario_dict:
                usuario_dict[chr(ascii_letra)] = {}
            usuario_dict[chr(ascii_letra)][numero] = f"{FONDO_AZUL} ·· {DEFECTO}"
    return usuario_dict

def numero_barcos_() -> int:
    """Comprueba que sea un número de barcos válido, sino riasea NumeroBarcosError"""
    numero_barcos_valido = False
    while not numero_barcos_valido:
        numero_barcos = (input("Escoja el número de barcos (2, 5) con los que se jugará. Las longitudes de los barcos serán decrecientes, es decir, al elegir 4 barcos las longitudes erán 5, 4, 3, 2; o con dos barcos: 5, 4\n"))
        try:
            numero_barcos = comprobar_numero_barcos(numero_barcos)
            return numero_barcos
        except NumeroBarcosError as error:
            print(error)

def poner_barcos(usuario_dict:dict, numero_barcos:int, colocacion_manual:bool) -> list[list]:
    """Crea el bucle para que se hagan los barcos que necesite, si recibe errores de funciones de dentor los raisea
    Returnea los barcos que se crean en colocar_barcos"""
    longitud_barco = 5
    barcos_creados = 0
    barcos = []
    while barcos_creados < numero_barcos:
        if colocacion_manual:
            posicion = input(f"Escoja donde quiere poner su barco de {longitud_barco} casillas de longitud. Indique de esta forma: A1abajo (Comenzaría en la casilla A1 y iría hacia abajo)\n")
        else:
            posicion = funex.posiciones_automaticas()
        try:
            indice_numero = comprobar_posicion(posicion) 
            try:
                insertar_barco(usuario_dict, posicion, indice_numero, longitud_barco, barcos, colocacion_manual)
                barcos_creados += 1
                longitud_barco -= 1
            except PonerBarcoError as error:
                print(error)
            except AutomaticoError:
                pass
        except PosicionError as error:
            print(error) 
    return barcos

def comprobar_posicion(posicion:str) -> None:
    """Compruebaque la posición sea correcta y sino raisea PosiciónError para diferentes casos
    También calcula hasta que índice hay número (Para cuando hay un 10)"""
    if len(posicion) > 4:
        indice_numero = 1
        while posicion[indice_numero+1].isdecimal():
            indice_numero += 1
        numero_posicion = int(posicion[1:indice_numero+1])
        if posicion[0] not in letras_posibles:
            if posicion[0].upper() in letras_posibles:
                raise PosicionError("Las letras deben de ir en mayúscula")
            else:
                raise PosicionError("El primer carácter no es correcto")
        elif numero_posicion not in numeros_posibles:
            raise PosicionError("El número introducido no es válido")
        elif posicion[indice_numero+1:] not in direcciones_posibles:
            raise PosicionError("La dirección introducida no es válida")
        return indice_numero
    else:
        raise PosicionError("La posició introducida necesita más información")
    
def comprobar_numero_barcos(numero_barcos:str) -> int:
    """Comprueba que el número de barcos sea el correcto, sino raisea NumeroBarcosError"""
    try:
        numero_barcos_int = int(numero_barcos)
        if numero_barcos_int not in range(2, 6):
            raise NumeroBarcosError("El número de barcos debe estar entre 2 y 5 incluídos")
        else:
            return numero_barcos_int
    except ValueError:
        raise NumeroBarcosError("El número de barcos introducido no es válido")
    
def insertar_barco(usuario_dict:dict, posicion:str, indice_numero:int, longitud_barco:int, barcos:list, colocacion_manual:bool) -> None:
    """Asigna nombres a las variables y agrupa funciones para luego poner los barcos"""
    letra = posicion[0]
    numero = int(posicion[1:indice_numero+1])
    direccion = posicion[indice_numero+1:]
    cambia, signo = reconocer_direcciones(direccion)
    try:
        colocar_barcos(usuario_dict, letra, numero, signo, longitud_barco, cambia, barcos, colocacion_manual)
    except PonerBarcoError as error:
        raise PonerBarcoError(error)
    except AutomaticoError:
        raise AutomaticoError

def reconocer_direcciones(direccion:str) -> tuple[str, str]:
    if direccion == "abajo":
        cambia = "letras"
        signo = "+"
    elif direccion == "arriba":
        cambia = "letras"
        signo = "-"
    elif direccion == "derecha":
        cambia = "numeros"
        signo = "+"
    else:
        cambia = "numeros"
        signo = "-"
    return (cambia, signo)

def colocar_barcos(usuario_dict:dict, letra:str, numero:int, signo:str, longitud_barco:int, cambia:str, barcos:list, colocacion_manual:bool) -> None:
    """Coloca todos los barcos y va bajando la longitud cuando está correctamente puesto
    Evalua si el barco se sale del tablero --> Raise PonerBarcoError y pide otra posición
    Si hay un error mientras está en modo automático se raisea AutomaticoError y prueba de nuevo
    También pone en listas los barcos para tenerlos agrupados"""
    longitud_fija = longitud_barco
    posiciones_poner = []
    barco_ = []
    while longitud_barco > 0:
        if cambia == "numeros":
            letra_ = letra
            if signo == "+":
                numero_ = numero + longitud_barco - 1
            else:
                numero_ = numero - longitud_barco + 1
        else:
            numero_ = numero
            if signo == "+":
                letra_ = chr(ord(letra) + longitud_barco - 1)
            else:
                letra_ = chr(ord(letra)  - longitud_barco + 1)
        if numero_ in range(1, 11) and ord(letra_) in range(ord("A"), ord("J") + 1):
            if not any(letra_ + str(numero_) in barco for barco in barcos):
                posiciones_poner.append(letra_ + str(numero_))
                longitud_barco -= 1
            else:
                if colocacion_manual:
                    raise PonerBarcoError("No se pueden colocar barcos encima de otros barcos")
                else:
                    raise AutomaticoError
        else:
            if colocacion_manual:
                raise PonerBarcoError("El barco se sale del tablero de juego")
            else:
                raise AutomaticoError
    if len(posiciones_poner) == longitud_fija:
        for posicion in posiciones_poner:
            letras = posicion[0]
            numeros = int(posicion[1:])
            usuario_dict[letras][numeros] = f"{FONDO_AMARILLO} ## {DEFECTO}"
            barco_.append(letras + str(numeros))
        barcos.append(barco_)