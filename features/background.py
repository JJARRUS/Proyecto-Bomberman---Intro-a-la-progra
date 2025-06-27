#Background
import pygame
import os

TAM_CASILLA = 32

def dibujar_background(ventana, matriz, nivel=1):
    # --- Carga y dibuja el fondo visual único para el nivel ---
    fondo_path = os.path.join("assets", "Fondos", f"background{nivel}.png")
    if os.path.exists(fondo_path):
        fondo = pygame.image.load(fondo_path)
        fondo = pygame.transform.scale(fondo, ventana.get_size())
        ventana.blit(fondo, (0, 0))
    else:
        ventana.fill((0, 0, 0))

    # --- Carga imágenes de los bloques ---
    bloque_indes_path = os.path.join("assets", "bloques", "bloque_indestruible.png")
    bloque_destru_path = os.path.join("assets", "bloques", "bloque_destruible.png")

    bloque_indes = pygame.image.load(bloque_indes_path).convert_alpha()
    bloque_indes = pygame.transform.scale(bloque_indes, (TAM_CASILLA, TAM_CASILLA))

    bloque_destru = pygame.image.load(bloque_destru_path).convert_alpha()
    bloque_destru = pygame.transform.scale(bloque_destru, (TAM_CASILLA, TAM_CASILLA))

    # --- Dibuja bloques según la matriz lógica ---
    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):
            x = col * TAM_CASILLA
            y = fila * TAM_CASILLA
            if matriz[fila][col] == "I":
                ventana.blit(bloque_indes, (x, y))
            elif matriz[fila][col] == "D":
                ventana.blit(bloque_destru, (x, y))
