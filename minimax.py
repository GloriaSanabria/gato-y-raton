import random
import time

# Tamaño del tablero
tamano_tablero = 6

# Inicialización del tablero con asteriscos
tablero = [["*" for _ in range(tamano_tablero)] for _ in range(tamano_tablero)]

# Posiciones iniciales del ratón y el gato
pos_ini_raton = [3, 3]
pos_ini_gato = [5, 5]

# Escondite del ratón
escondite_raton = (0, 0)

# Función para imprimir el tablero
def crear_tabla(tablero):
    for fila in tablero:
        print("  ".join(fila))
    print()

# Función para actualizar el tablero con las nuevas posiciones del ratón y el gato
def actualizar_tablero(tablero, pos_gato, pos_raton):
    for x in range(tamano_tablero):
        for y in range(tamano_tablero):
            tablero[x][y] = "*"
    tablero[pos_gato[0]][pos_gato[1]] = 'G'  # Posición del gato
    tablero[pos_raton[0]][pos_raton[1]] = 'R'  # Posición del ratón
    tablero[escondite_raton[0]][escondite_raton[1]] = "E"  # Escondite del ratón
    crear_tabla(tablero)  # Actualizar el tablero

# Función para calcular los movimientos posibles para un jugador
def mov_posibles(pos, tamano_tablero):
    x, y = pos
    movimientos = []
    if x > 0:
        movimientos.append((x-1, y))  # Arriba
    if x < tamano_tablero - 1:
        movimientos.append((x+1, y))  # Abajo
    if y > 0:
        movimientos.append((x, y-1))  # Izquierda
    if y < tamano_tablero - 1:
        movimientos.append((x, y+1))  # Derecha
    return movimientos

# Función de evaluación para el algoritmo minimax
def evaluar(pos_gato, pos_raton):
    return abs(pos_gato[0] - pos_raton[0]) + abs(pos_gato[1] - pos_raton[1])

# Función minimax para la toma de decisiones del gato
def minimax(pos_gato, pos_raton, profundidad, turno_gato, tamano_tablero):
    if profundidad == 0 or pos_gato == pos_raton:
        return evaluar(pos_gato, pos_raton)
    if turno_gato:
        mejor_valor = float('inf')
        for movimiento in mov_posibles(pos_gato, tamano_tablero):
            valor = minimax(movimiento, pos_raton, profundidad-1, False, tamano_tablero)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('-inf')
        for movimiento in mov_posibles(pos_raton, tamano_tablero):
            valor = minimax(pos_gato, movimiento, profundidad-1, True, tamano_tablero)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor

# Función para el movimiento inteligente del ratón
def mov_raton_inteligent(pos_gato, pos_raton, tamano_tablero):
    movimientos_disponibles = mov_posibles(pos_raton, tamano_tablero)
    movimientos_alejados = []
    for movimiento in movimientos_disponibles:
        if evaluar(pos_gato, movimiento) > evaluar(pos_gato, pos_raton):
            movimientos_alejados.append(movimiento)
    if movimientos_alejados:
        return random.choice(movimientos_alejados)
    else:
        return random.choice(movimientos_disponibles)

# Función para el movimiento inteligente del gato
def mov_gato_inteligent(pos_gato, pos_raton, tamano_tablero):
    mejor_movimiento = None
    mejor_valor = float('inf')
    for movimiento in mov_posibles(pos_gato, tamano_tablero):
        valor = minimax(movimiento, pos_raton, 3, False, tamano_tablero)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento
    return mejor_movimiento

# Posiciones iniciales de los jugadores
pos_raton = pos_ini_raton
pos_gato = pos_ini_gato

# Inicializar y mostrar el tablero
actualizar_tablero(tablero, pos_gato, pos_raton)
time.sleep(3)  # Hacer una pausa para que los jugadores puedan ver el tablero

# Bucle principal del juego
while True:
    # Movimiento del ratón
    pos_raton = mov_raton_inteligent(pos_gato, pos_raton, tamano_tablero)
    actualizar_tablero(tablero, pos_gato, pos_raton)
    
    # Verificar si el ratón alcanzó su escondite
    if escondite_raton == pos_raton:
        print('El raton se escapo, gano el raton!')
        break
    
    time.sleep(1)  # Hacer una pausa antes del siguiente movimiento
    
    # Movimiento del gato
    pos_gato = mov_gato_inteligent(pos_gato, pos_raton, tamano_tablero)
    actualizar_tablero(tablero, pos_gato, pos_raton)
    
    # Verificar si el gato atrapó al ratón
    if pos_gato == pos_raton:
        print("¡El gato atrapó al ratón! Juego terminado.")
        break
    
    time.sleep(1)  # Hacer una pausa antes del siguiente movimiento