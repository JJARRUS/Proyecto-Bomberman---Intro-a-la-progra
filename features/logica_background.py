# logica_background.py

import random

matriz_logica = [
    ["I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I"],
    ["I", " ", " ", " ", "D", " ", " ", " ", "D", " ", " ", " ", "I"],
    ["I", " ", "I", " ", " ", " ", "I", " ", " ", " ", "I", " ", "I"],
    ["I", "D", " ", " ", " ", " ", " ", " ", " ", " ", " ", "D", "I"],
    ["I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I"],
    ["I", " ", " ", "D", " ", " ", " ", " ", " ", "D", " ", " ", "I"],
    ["I", " ", "I", " ", " ", "I", " ", "I", " ", " ", "I", " ", "I"],
    ["I", " ", " ", " ", "D", " ", " ", " ", "D", " ", " ", " ", "I"],
    ["I", " ", "I", " ", " ", " ", "I", " ", " ", " ", "I", " ", "I"],
    ["I", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "I"],
    ["I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I"],
    ["I", " ", " ", " ", "D", " ", " ", " ", "D", " ", " ", " ", "I"],
    ["I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I"],
]
def posicion_llave_y_puerta(matriz):
    destructibles = []
    espacios_libres = []

    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):
            if matriz[fila][col] == 'D':
                destructibles.append((fila, col))
            elif matriz[fila][col] == ' ':
                espacios_libres.append((fila, col))

    if len(destructibles) < 1 or len(espacios_libres) < 1:
        raise ValueError("No hay suficientes espacios para colocar llave y puerta.")

    fila_llave, col_llave = random.choice(destructibles)
    fila_puerta, col_puerta = random.choice(espacios_libres)

    llave_pos = (col_llave * 32, fila_llave * 32)
    puerta_pos = (col_puerta * 32, fila_puerta * 32)

    return llave_pos, puerta_pos, (fila_llave, col_llave)
