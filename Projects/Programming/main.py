import funciones_crear_tableros as funct
import funciones_ataques as funat
import funciones_generales as fung

fung.titulo()
guardar = False
cargar = fung.menu()
if cargar:
    tablero_usuario1, tablero_oponente1, tablero_usuario2, tablero_oponente2, barcos1, barcos2, barcos_hundidos_del_1, barcos_hundidos_del_2 = fung.recargar_partida()
    jugar_maquina = False
    guardar = False
    jugar_maquina = fung.jugar_contra_maquina(cargar)

if not cargar:
    tablero_usuario1 = funct.crear_tablero()
    tablero_oponente1 = funct.crear_tablero()
    tablero_usuario2 = funct.crear_tablero()
    tablero_oponente2 = funct.crear_tablero()
    barcos_hundidos_del_1 = 0
    barcos_hundidos_del_2 = 0

    jugar_maquina = False
    jugar_maquina = fung.jugar_contra_maquina(cargar)
    numero_barcos = funct.numero_barcos_()
            
    fung.dibujar_tableros(tablero_usuario1, tablero_oponente1)
    colocacion_manual = fung.elegir_colocacion()
    barcos1 = funct.poner_barcos(tablero_usuario1, numero_barcos, colocacion_manual)
    fung.dibujar_tableros(tablero_usuario1, tablero_oponente1)
    fung.limpiar_pantalla()


    if not jugar_maquina:
        print("Ahora turno de que el segundo usuario escoja donde poner sus barcos")
        fung.dibujar_tableros(tablero_usuario2, tablero_oponente2)
        colocacion_manual = fung.elegir_colocacion()
    else:
        colocacion_manual = False
    barcos2 = funct.poner_barcos(tablero_usuario2, numero_barcos, colocacion_manual)
    if not jugar_maquina:
        fung.dibujar_tableros(tablero_usuario2, tablero_oponente2)
        fung.limpiar_pantalla()

victoria = False
while not victoria and not guardar:
    print("Turno de atacar del usuario 1")
    barcos_hundidos_del_2, guardar = funat.ataque(tablero_usuario2, tablero_oponente1, tablero_usuario1, barcos2, barcos_hundidos_del_2, tablero_oponente2, guardar, barcos1, barcos_hundidos_del_1, jugar_maquina = False)
    fung.dibujar_tableros(tablero_usuario1, tablero_oponente1)
    fung.limpiar_pantalla()

    if not guardar:
        print("Turno de atacar del usuario 2")
        barcos_hundidos_del_1, guardar = funat.ataque(tablero_usuario1, tablero_oponente2, tablero_usuario2, barcos1, barcos_hundidos_del_1, tablero_oponente1, guardar, barcos2, barcos_hundidos_del_2, jugar_maquina)
        if not jugar_maquina:
            fung.dibujar_tableros(tablero_usuario2, tablero_oponente2)
            fung.limpiar_pantalla()

    if barcos_hundidos_del_2 == numero_barcos:
        victoria = True
    elif barcos_hundidos_del_1 == numero_barcos:
        victoria = True

if barcos_hundidos_del_2 == barcos_hundidos_del_1 == numero_barcos:
    print("EMPATE")
elif barcos_hundidos_del_1 == numero_barcos:
    print(f"El ganador es el Usuario 2!!!")
elif barcos_hundidos_del_2 == numero_barcos:
    print(f"El ganador es el Usuario 1!!!")