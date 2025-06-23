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

#Explicacion
"""
Se usa pygame para cargar y dibujar imagenes en una ventana de juego.
Con os.path.dirname(__file__) y os.path.join se usan para cargar las
imagenes del background y de los bloques. Se cargan con pygame.image.load() Y
se redimensionan a 32x32 usando pygame.transform.scale(). Esto basicamente
modifica la imagen para que encaje.

def dibujar_background(pantalla, matriz) pinta el fondo y los bloques.
Recorre la matriz usando enumerate que permite acceder al indice.
Se multiplica por 32 que es el tamaño del sprite.

"""
