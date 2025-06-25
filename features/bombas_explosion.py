# bombas_explosion.py

import pygame
import os

modificar = 32

class Bomba:
    def __init__(self, x, y, tiempo=3000, tiempo_explota=1000):
        self.x = x
        self.y = y
        self.tiempo = tiempo
        self.tiempo_colocada = pygame.time.get_ticks()
        self.exploto = False
        self.tiempo_explosion = None
        self.tiempo_explota = tiempo_explota

        principal = os.path.dirname(__file__)
        ruta_bomba1 = os.path.join(principal, "..", "assets", "bombas", "imagen_bomba.png")
        ruta_bomba2 = os.path.join(principal, "..", "assets", "bombas", "imagen_bomba_2.png")
        ruta_explosion = os.path.join(principal, "..", "assets", "bombas", "imagen_explosion.png")

        # Animaciones de la bomba (parpadeo)
        self.bomba_frames = [
            pygame.transform.scale(pygame.image.load(ruta_bomba1), (modificar, modificar)),
            pygame.transform.scale(pygame.image.load(ruta_bomba2), (modificar, modificar))
        ]
        self.indice_frame = 0
        self.tiempo_animacion = 150  # ms
        self.ultimo_frame = pygame.time.get_ticks()

        self.imagen_explosion = pygame.image.load(ruta_explosion)
        self.imagen_explosion = pygame.transform.scale(self.imagen_explosion, (modificar, modificar))

        self.jugador_esta = self.calcular_jugador_esta()

    def calcular_jugador_esta(self):
        return [
            (self.x, self.y),
            (self.x + modificar, self.y),
            (self.x - modificar, self.y),
            (self.x, self.y + modificar),
            (self.x, self.y - modificar),
        ]

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()

        if not self.exploto:
            if tiempo_actual - self.ultimo_frame >= self.tiempo_animacion:
                self.indice_frame = (self.indice_frame + 1) % len(self.bomba_frames)
                self.ultimo_frame = tiempo_actual

            if tiempo_actual - self.tiempo_colocada >= self.tiempo:
                self.exploto = True
                self.tiempo_explosion = tiempo_actual
        else:
            if tiempo_actual - self.tiempo_explosion >= self.tiempo_explota:
                return True  # Marca la bomba para ser eliminada

        return False

    def dibujar(self, ventana):
        if self.exploto:
            for x, y in self.jugador_esta:
                ventana.blit(self.imagen_explosion, (x, y))
        else:
            ventana.blit(self.bomba_frames[self.indice_frame], (self.x, self.y))

class Explosivax:
    def __init__(self, max_bombas=3):
        self.bombas = []
        self.max_bombas = max_bombas

    def colocar_bomba(self, x, y):
        if len(self.bombas) < self.max_bombas:
            bomba = Bomba(x, y)
            self.bombas.append(bomba)

    def actualizar(self):
        bombas_activas = []
        for bomba in self.bombas:
            if not bomba.actualizar():
                bombas_activas.append(bomba)
        self.bombas = bombas_activas

    def dibujar(self, ventana):
        for bomba in self.bombas:
            bomba.dibujar(ventana)
