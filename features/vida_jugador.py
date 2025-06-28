import pygame
import os

class Vida:
    def __init__(self, cantidad_vida=3):
        self.vida_maxima = cantidad_vida
        self.vida_actual = cantidad_vida
        self.powerup_vida_activo = False
        self.powerup_vida_usado = False
        self.corazones_extra = 0  # Habilidad como Bombgirl
        self.corazones_extra_usados = False

        original = os.path.dirname(__file__)
        ruta_lleno = os.path.join(original, "..", "assets", "items", "corazon.png")
        ruta_vacio = os.path.join(original, "..", "assets", "items", "corazon_vacio.png")

        imagen_lleno = pygame.image.load(ruta_lleno)
        imagen_vacio = pygame.image.load(ruta_vacio)

        self.completo = pygame.transform.scale(imagen_lleno, (32, 32))
        self.vacio = pygame.transform.scale(imagen_vacio, (32, 32))

    def perder_corazones(self):
        if self.powerup_vida_activo and not self.powerup_vida_usado:
            self.powerup_vida_usado = True
        elif self.corazones_extra > 0 and not self.corazones_extra_usados:
            self.corazones_extra_usados = True
        elif self.vida_actual > 0:
            self.vida_actual -= 1

    def aumento_vida(self):
        if self.vida_actual < self.vida_maxima:
            self.vida_actual += 1

    def activar_powerup_vida(self):
        self.powerup_vida_activo = True
        self.powerup_vida_usado = False

    def agregar_corazon_extra(self):
        self.corazones_extra = 1
        self.corazones_extra_usados = False

    def reiniciar(self):
        self.vida_actual = self.vida_maxima
        self.powerup_vida_activo = False
        self.powerup_vida_usado = False
        self.corazones_extra_usados = False

    def visual(self, ventana, pos_x=10, pos_y=10):
        total = self.vida_maxima
        if self.powerup_vida_activo:
            total += 1
        if self.corazones_extra:
            total += 1

        indice = 0
        if self.powerup_vida_activo:
            imagen = self.vacio if self.powerup_vida_usado else self.completo
            ventana.blit(imagen, (pos_x + indice * 40, pos_y))
            indice += 1

        for i in range(self.vida_maxima):
            imagen = self.completo if i < self.vida_actual else self.vacio
            ventana.blit(imagen, (pos_x + indice * 40, pos_y))
            indice += 1

        if self.corazones_extra:
            imagen = self.vacio if self.corazones_extra_usados else self.completo
            ventana.blit(imagen, (pos_x + indice * 40, pos_y))
