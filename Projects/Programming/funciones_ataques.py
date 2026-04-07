from excepciones import *
from constantes import *
import funciones_generales as fung
import funciones_extra as funex

def ataque(tablero_usuario2:dict, tablero_oponente1:dict, tablero_usuario1:dict, barcos1:list[list], barcos_hundidos_del_2:int, tablero_oponente2:dict, guardar:bool, barcos2:list, barcos_hundidos_del_1, jugar_maquina:bool) -> None:
    """Marca si es tocado, agua o hundido
    Si se pone Guardar en la posición se para el programa y se guarda la partida"""
    posicion_correcta = False
    while not posicion_correcta:
        if not jugar_maquina:
            fung.dibujar_tableros(tablero_usuario1, tablero_oponente1)
            posicion = input("¿Qué posición desea atacar (Puedes poner GUARDAR para guardar la partida, se borrará si hay otra guardada)?\n")
        else:
            posicion = funex.ataques_automaticos()
        try:
            guardar = comprobar_posicion_ataque(posicion)
            if not guardar:
                letra = posicion[0]
                numero = int(posicion[1:])
                contador = 0
                contador_golpes = 0
                for barco in barcos1:
                    if letra + str(numero) in barco:
                        indice = barco.index(letra + str(numero))  
                        barco[indice] = f"{posicion}**"
                        tablero_oponente1[letra][numero] = f"{FONDO_ROJO} ** {DEFECTO}"
                        tablero_usuario2[letra][numero] = f"{FONDO_ROJO} ** {DEFECTO}"
                        print(f"{ROJO} TOCADO {DEFECTO}")
                        if is_hundido(barco):
                            barcos_hundidos_del_2 = display_hundido(tablero_oponente1, tablero_usuario2, barco, barcos_hundidos_del_2)
                        posicion_correcta = True
                    elif tablero_oponente1[letra][numero] in (f"{FONDO_ROJO} ** {DEFECTO}", "!!", f"{FONDO_VERDE} ++ {DEFECTO}"):
                        contador_golpes += 1
                        if contador_golpes == len(barcos1):
                            print("Esta posición ya ha sido bombardeada, perdiste tu turno")
                    else:
                        contador += 1
                        if contador == len(barcos1):
                            tablero_oponente1[letra][numero] = f"{FONDO_VERDE} ++ {DEFECTO}"
                            tablero_usuario2[letra][numero] = f"{FONDO_VERDE} ++ {DEFECTO}"
                            print(f"{VERDE} AGUA {DEFECTO}")
                            posicion_correcta = True     
                return barcos_hundidos_del_2, guardar
            else:
                fung.guardar(tablero_usuario1, tablero_oponente1, tablero_usuario2, tablero_oponente2, barcos1, barcos2, barcos_hundidos_del_1, barcos_hundidos_del_2)
                return barcos_hundidos_del_2, guardar
        except PosicionError as error:
            print(error)

def comprobar_posicion_ataque(posicion) -> bool:
    """Comprueba que la posición de ataque sea válida, sino raisea PosicionError para diferentes casos"""
    if len(posicion) in range(2, 4):
        try:
            numero_posicion = int(posicion[1:])
        except ValueError:
            raise PosicionError("Introduzca un número después de la letra")
        if posicion[0] not in letras_posibles and letras_posibles:
            if posicion[0].upper() in letras_posibles:
                raise PosicionError("Las letras deben de ir en mayúscula")
            else:
                raise PosicionError("El primer carácter debe ser la letra")
        elif numero_posicion not in numeros_posibles:
            raise PosicionError("El número introducido no es válido")
    elif posicion.upper() == "GUARDAR":
        return True
    else:
        raise PosicionError("La posición introducida no es válida")
    
def is_hundido(barco:list) -> bool:
    """Los barcos tocados se les añade a la posición **, por ejemplo E5**
    Si tiene eso en todos está hundido y devuelve True"""
    tocados = 0
    for posicion_barco in barco:
        if posicion_barco.endswith("**"):
            tocados += 1
    if tocados == len(barco):
        return True
    else:
        return False    
    
def display_hundido(tablero_oponente1:dict, tablero_usuario2:dict, barco:list, barcos_hundidos:int) -> int:
    """Añade un barco está hundido y lo pone en los tableros"""
    barcos_hundidos += 1
    print(f"{NARANJA} Y HUNDIDOOOOOOO {DEFECTO}")
    for posicion in barco:
        letra = posicion[0]
        numero = int(posicion[1:len(posicion) - 2])
        tablero_oponente1[letra][numero] = f"{FONDO_NEGRO} !! {DEFECTO}"
        tablero_usuario2[letra][numero] = f"{FONDO_NEGRO} !! {DEFECTO}"
    return barcos_hundidos