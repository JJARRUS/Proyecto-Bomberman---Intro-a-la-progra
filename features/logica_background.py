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
    destructibles = [(fila, col) for fila in range(len(matriz)) for col in range(len(matriz[0])) if matriz[fila][col] == 'D']
    seleccionadas = random.sample(destructibles, 2)

    fila_llave, col_llave = seleccionadas[0]
    fila_puerta, col_puerta = seleccionadas[1]

    pos_llave = (col_llave * 32, fila_llave * 32)
    pos_puerta = (col_puerta * 32, fila_puerta * 32)

    return pos_llave, pos_puerta, (fila_llave, col_llave)

def obtener_matriz_y_posiciones(nivel):
    # Por ahora solo tenemos nivel 1, pero lo hacemos escalable
    matriz = [fila.copy() for fila in matriz_logica]
    pos_llave, pos_puerta, pos_matriz_llave = posicion_llave_y_puerta(matriz)
    return matriz, pos_llave, pos_puerta, pos_matriz_llave
