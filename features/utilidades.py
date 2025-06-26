import os

def guardar_puntaje(nombre_jugador, puntaje):
    try:
        ruta = os.path.join("utilities", "puntajes.txt")
        with open(ruta, "a") as archivo:
            archivo.write(f"{nombre_jugador},{puntaje}\n")
        print(f"Puntaje guardado: {nombre_jugador} - {puntaje}")
    except Exception as e:
        print(f"Error al guardar: {e}")
