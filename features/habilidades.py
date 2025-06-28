import pygame
import os

TAM = 32

class Flecha:
    def __init__(self, x, y, direccion):
        self.x = x
        self.y = y
        self.direccion = direccion
        self.velocidad = 6
        ruta_img = os.path.join("assets", "items_y_powerups", "arrow.png")
        self.image = pygame.image.load(ruta_img).convert_alpha()
        if direccion in ["izquierda", "derecha"]:
            self.image = pygame.transform.scale(self.image, (28, 12))
        else:
            self.image = pygame.transform.scale(self.image, (12, 28))
        if direccion == "arriba":
            self.image = pygame.transform.rotate(self.image, 90)
        elif direccion == "abajo":
            self.image = pygame.transform.rotate(self.image, -90)
        elif direccion == "izquierda":
            self.image = pygame.transform.rotate(self.image, 180)
        # Derecha queda igual
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.activa = True

    def mover(self):
        if self.direccion == "arriba":
            self.y -= self.velocidad
        elif self.direccion == "abajo":
            self.y += self.velocidad
        elif self.direccion == "izquierda":
            self.x -= self.velocidad
        elif self.direccion == "derecha":
            self.x += self.velocidad
        self.rect.center = (self.x, self.y)

def aplicar_habilidad_personaje(jugador, personaje_num):
    # Bombman: 2 bombas extra
    if personaje_num == 1:
        jugador.bombas_disponibles += 2
    # Bombgirl: +1 vida (powerup visual y funcional)
    elif personaje_num == 2 and jugador.vida:
        jugador.vida.ganar_vida()
    # The Chosen One: flechas, inicia con 2 y cooldown
    elif personaje_num == 3:
        jugador.flechas = [None, None]
        jugador.flechas_disponibles = 2
        jugador.cooldown_flecha = 2000
        jugador.tiempo_ultima_flecha = 0
