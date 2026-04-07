import os
from constantes import *
import ast

def titulo() -> None:
    print("""██╗  ██╗██╗   ██╗███╗   ██╗██████╗ ██╗██████╗ 
██║  ██║██║   ██║████╗  ██║██╔══██╗██║██╔══██╗
███████║██║   ██║██╔██╗ ██║██║  ██║██║██████╔╝
██╔══██║██║   ██║██║╚██╗██║██║  ██║██║██╔══██╗
██║  ██║╚██████╔╝██║ ╚████║██████╔╝██║██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝╚═╝  ╚═╝

██╗      █████╗     ███████╗██╗      ██████╗ ████████╗ █████╗ 
██║     ██╔══██╗    ██╔════╝██║     ██╔═══██╗╚══██╔══╝██╔══██╗
██║     ███████║    █████╗  ██║     ██║   ██║   ██║   ███████║
██║     ██╔══██║    ██╔══╝  ██║     ██║   ██║   ██║   ██╔══██║
███████╗██║  ██║    ██║     ███████╗╚██████╔╝   ██║   ██║  ██║
╚══════╝╚═╝  ╚═╝    ╚═╝     ╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝
""")

def dibujar_tableros(tablero_usuario:dict, tablero_oponente:dict) -> None:
    print("    ", end = " ")
    for _ in range(2):
        for numero in tablero_usuario["A"]:
            print(numero, end = "    ")
        print("  ", end = "")
    print()
    print()
    for letra, numeros in tablero_usuario.items():
        print(letra, end = "   ")
        for agua in numeros.values():
            print(agua, end = " ")
        print(" ", end = "")
        print(letra, end = " ")
        numeros = tablero_oponente[letra]
        for agua in numeros.values():
            print(agua, end = " ")
        print()
        print()

def limpiar_pantalla() -> None:
    pasar = " "
    while pasar != "":
        pasar = input("Pulse enter para continuar")
        if pasar == "":
            os.system('cls' if os.name == 'nt' else 'clear')

def elegir_colocacion() -> bool:
    colocacion_correcta = False
    while not colocacion_correcta:
        colocacion = input("Escoja colocación manual (CM) o colocación automática (CA)")
        if colocacion.upper() == "CM":
            colocacion_correcta = True
            colocacion_manual  = True
        elif colocacion.upper() == "CA":
            colocacion_correcta = True
            colocacion_manual  = False
    return colocacion_manual

def jugar_contra_maquina(cargar:bool) -> bool:
    maquina_correcta = False
    while not maquina_correcta:
        if not cargar:
            maquina = input("¿Quieres jugar contra la máquina (S/N)?")
        else:
            maquina = input("¿Quieres continuar la partida contra una máquina (S/N)?")
        if maquina.upper() == "S":
            jugar_maquina = True
            maquina_correcta = True
            print("Tu serás el Usuario 1 y la máquina el Usuario 2")
        elif maquina.upper() == "N":
            print("Elegid quién será el Usuario 1 y quién el Usuario 2")
            maquina_correcta = True
    return jugar_maquina

def guardar(tablero_usuario1:dict, tablero_oponente1:dict, tablero_usuario2:dict, tablero_oponente2:dict, barcos1:list, barcos2:list, barcos_hundidos_del_1:int, barcos_hundidos_del_2:int) -> None:
    """Guarda todos los diccionarios y listas como strings"""
    with open("partida.txt", "w", encoding = "utf-8") as partida_guardada:
        a, b, c, d, e, f, g, h = str(tablero_usuario1), str(tablero_oponente1), str(tablero_usuario2), str(tablero_oponente2), str(barcos1), str(barcos2), str(barcos_hundidos_del_1), str(barcos_hundidos_del_2)
        partida_guardada.write(f"{a}\n{b}\n{c}\n{d}\n{e}\n{f}\n{g}\n{h}")

def recargar_partida() -> dict:
    """Pasa de string a lo que sea originariamente gracias a la librería ast, 
    que reconoce la estructura de cada tipo de dato y lo trasforma a este mismo"""
    with open("partida.txt", "r", encoding="utf-8") as partida_guardada:
        lineas = partida_guardada.readlines()

        tablero_usuario1 = ast.literal_eval(lineas[0].strip())
        tablero_oponente1 = ast.literal_eval(lineas[1].strip())
        tablero_usuario2 = ast.literal_eval(lineas[2].strip())
        tablero_oponente2 = ast.literal_eval(lineas[3].strip())
        barcos1 = ast.literal_eval(lineas[4].strip())
        barcos2 = ast.literal_eval(lineas[5].strip())
        barcos_hundidos_del_1 = ast.literal_eval(lineas[6].strip())
        barcos_hundidos_del_2 = ast.literal_eval(lineas[7].strip())
        return dict(tablero_usuario1), dict(tablero_oponente1), dict(tablero_usuario2), dict(tablero_oponente2), list(barcos1), list(barcos2), int(barcos_hundidos_del_1), int(barcos_hundidos_del_2)
    
def menu() -> bool:
    opcion_correcta = False
    while not opcion_correcta:
        opciones = input("""¿Qué desea hacer?
1. Crear nueva partida
2. Cargar una partida guardada\n""")
        if opciones == "1":
            opcion_correcta = True
            cargar = False
        elif opciones == "2":
            opcion_correcta = True
            cargar =  True
    return cargar