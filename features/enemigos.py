import pygame
import os
import random

TAM = 32

class Enemigo:
    def __init__(self, x, y):
        self.direccion = random.choice(["arriba", "abajo", "izquierda", "derecha"])
        self.velocidad = 1
        self.vivo = True

        ruta = os.path.join(os.path.dirname(__file__), "..", "assets", "enemigos", "ene_normal.png")
        self.sprite = pygame.image.load(ruta)
        self.sprite = pygame.transform.scale(self.sprite, (TAM, TAM))
        self.rect = self.sprite.get_rect(topleft=(x, y))

    def puede_moverse(self, nuevo_rect, matriz):
        for punto in [
            (nuevo_rect.left, nuevo_rect.top),
            (nuevo_rect.right - 1, nuevo_rect.top),
            (nuevo_rect.left, nuevo_rect.bottom - 1),
            (nuevo_rect.right - 1, nuevo_rect.bottom - 1),
        ]:
            fila = punto[1] // TAM
            col = punto[0] // TAM
            if fila < 0 or col < 0 or fila >= len(matriz) or col >= len(matriz[0]):
                return False
            if matriz[fila][col] in ('I', 'D'):
                return False
        return True

    def mover(self, matriz):
        if not self.vivo:
            return

        dx, dy = 0, 0
        if self.direccion == "arriba":
            dy = -self.velocidad
        elif self.direccion == "abajo":
            dy = self.velocidad
        elif self.direccion == "izquierda":
            dx = -self.velocidad
        elif self.direccion == "derecha":
            dx = self.velocidad

        nuevo_rect = self.rect.move(dx, dy)
        if self.puede_moverse(nuevo_rect, matriz):
            self.rect = nuevo_rect
        else:
            self.direccion = random.choice(["arriba", "abajo", "izquierda", "derecha"])

    def actualizar(self, jugador, vida, matriz, tiempo_actual, cooldown_golpe):
        self.mover(matriz)
        if self.vivo and self.rect.colliderect(jugador.rect):
            if tiempo_actual - jugador.ultimo_golpe > cooldown_golpe:
                vida.perder_corazones()
                jugador.ultimo_golpe = tiempo_actual

    def verificar_muerte(self, explosiones):
        if not self.vivo:
            return False
        for x, y in explosiones:
            rect_exp = pygame.Rect(x, y, TAM, TAM)
            if self.rect.colliderect(rect_exp):
                self.vivo = False
                return True
        return False

    def dibujar(self, ventana):
        if self.vivo:
            ventana.blit(self.sprite, self.rect)
