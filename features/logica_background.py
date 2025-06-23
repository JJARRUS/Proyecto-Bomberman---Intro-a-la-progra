import random

matriz_logica = [
    ["I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I"],
    ["I", " ", " ", "D", " ", " ", "D", " ", "D", " ", " ", " ", "I"],
    ["I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I"],
    ["I", "D", " ", "D", " ", "D", " ", "D", " ", "D", " ", "D", "I"],
    ["I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I"],
    ["I", " ", " ", " ", " ", "D", " ", "D", " ", " ", " ", " ", "I"],
    ["I", "D", "I", "D", "I", " ", "I", " ", "I", "D", "I", "D", "I"],
    ["I", " ", " ", "D", " ", "D", " ", "D", " ", " ", "D", " ", "I"],
    ["I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I"],
    ["I", "D", " ", " ", " ", "D", " ", "D", " ", " ", " ", "D", "I"],
    ["I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I", " ", "I"],
    ["I", " ", " ", "D", " ", " ", " ", " ", " ", "D", " ", " ", "I"],
    ["I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I"],
]

def posicion_llave_y_puerta(matriz):
    destructibles = []

    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):
            if matriz[fila][col] == 'D':
                destructibles.append((fila, col))


    fila_llave, col_llave = random.choice(destructibles)

    llave_pos = (col_llave * 32, fila_llave * 32)
    puerta_pos = (col_puerta * 32, fila_puerta * 32)

    return llave_pos, puerta_pos, (fila_llave, col_llave)

#Explicacion

"""
Se importa random para que ubique aleatoriamente una llave y una puerta adentro
de de la matriz. La matriz esta hecha basada al backgroun.png. I es un bloque
indestructible y D destructible.

La funcion posicion_llave_y_puerta(matriz) la recorre y guarda las D en una lista
y las vacias en otra. Escoge un campo destructible random para esconder la llave
y otro vacio para la puerta.
Se vuelven en coordenadas al multiplicar las filas y columnas por 32 (tamaño de casilla).

"""
