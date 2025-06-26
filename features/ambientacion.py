# ambientacion.py

import pygame
import random
import os

TAM_CASILLA = 32

class BloqueHielo:
    def __init__(self, matriz_juego, cantidad=2):
        self.imagen = self.cargar_imagen()
        self.posiciones = self.generar_posiciones(matriz_juego, cantidad)
        self.afectando = False
        self.tiempo_afectado = 0
        self.velocidad_original = None

    def cargar_imagen(self):
        ruta = os.path.join(os.path.dirname(__file__), "..", "assets", "Ambientacion", "hielo.png")
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (TAM_CASILLA, TAM_CASILLA))

    def generar_posiciones(self, matriz, cantidad):
        vacios = []
        for fila in range(len(matriz)):
            for col in range(len(matriz[0])):
                if matriz[fila][col] == " ":
                    vacios.append((col * TAM_CASILLA, fila * TAM_CASILLA))
        return random.sample(vacios, min(cantidad, len(vacios)))

    def dibujar(self, ventana):
        for pos in self.posiciones:
            ventana.blit(self.imagen, pos)

    def aplicar_efecto(self, jugador):
        jugador_rect = jugador.rect
        nuevas_posiciones = []
        for hielo_pos in self.posiciones:
            rect_hielo = pygame.Rect(hielo_pos[0], hielo_pos[1], TAM_CASILLA, TAM_CASILLA)
            if jugador_rect.colliderect(rect_hielo):
                if not self.afectando:
                    self.afectando = True
                    self.tiempo_afectado = pygame.time.get_ticks()
                    self.velocidad_original = jugador.velocidad
                    jugador.velocidad /= 2
            else:
                nuevas_posiciones.append(hielo_pos)
        self.posiciones = nuevas_posiciones

        if self.afectando:
            if pygame.time.get_ticks() - self.tiempo_afectado > 3000:
                jugador.velocidad = self.velocidad_original
                self.afectando = False
