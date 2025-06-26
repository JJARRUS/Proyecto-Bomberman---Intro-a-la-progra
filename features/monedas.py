import pygame
import os
import random

TAM = 32

class Moneda:
    def __init__(self, matriz, cantidad=15):
        ruta = os.path.join("assets", "items", "moneda.png")
        self.imagen = pygame.image.load(ruta)
        self.imagen = pygame.transform.scale(self.imagen, (TAM, TAM))
        self.posiciones = []
        self.generar_monedas(matriz, cantidad)

    def generar_monedas(self, matriz, cantidad):
        libres = [(x, y) for y in range(len(matriz)) for x in range(len(matriz[0])) if matriz[y][x] == ' ']
        seleccionadas = random.sample(libres, min(cantidad, len(libres)))
        self.posiciones = [(col * TAM, fila * TAM) for col, fila in seleccionadas]

    def dibujar(self, ventana):
        for x, y in self.posiciones:
            ventana.blit(self.imagen, (x, y))

    def recoger(self, jugador_rect):
        recogidas = []
        for x, y in self.posiciones:
            if jugador_rect.colliderect(pygame.Rect(x, y, TAM, TAM)):
                recogidas.append((x, y))
        for pos in recogidas:
            self.posiciones.remove(pos)
        return 100 * len(recogidas)
