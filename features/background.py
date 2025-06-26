#Background
import pygame
import os

ruta_base = os.path.dirname(__file__)
ruta_background = os.path.join(ruta_base, "..", "assets", "fondos", "background.png")
ruta_bloque_indestruible = os.path.join(ruta_base, "..", "assets", "bloques", "bloque_indestruible.png")
ruta_bloque_destruible = os.path.join(ruta_base, "..", "assets", "bloques", "bloque_destruible.png")

background_img = pygame.image.load(ruta_background)
bloque_indestruible_img = pygame.image.load(ruta_bloque_indestruible)
bloque_destruible_img = pygame.image.load(ruta_bloque_destruible)

bloque_indestruible_img = pygame.transform.scale(bloque_indestruible_img, (32, 32))
bloque_destruible_img = pygame.transform.scale(bloque_destruible_img, (32, 32))

def dibujar_background(pantalla, matriz):
    ancho = len(matriz[0]) * 32
    alto = len(matriz) * 32
    fondo_escalado = pygame.transform.scale(background_img, (ancho, alto))
    pantalla.blit(fondo_escalado, (0, 0))

    for fila_idx, fila in enumerate(matriz):
        for col_idx, celda in enumerate(fila):
            x = col_idx * 32
            y = fila_idx * 32

            if celda == "I":
                pantalla.blit(bloque_indestruible_img, (x, y))
            elif celda == "D":
                pantalla.blit(bloque_destruible_img, (x, y))
