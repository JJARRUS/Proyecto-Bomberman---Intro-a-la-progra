import pygame
import os

class Vida:
    def __init__(self, cantidad_vida=3):
        self.vida_maxima = cantidad_vida
        self.vida_actual = cantidad_vida
        self.powerup_activo = False
        self.corazones_extra = 0
        self.corazones_extra_usados = False

        original = os.path.dirname(__file__)
        ruta_lleno = os.path.join(original, "..", "assets", "items", "corazon.png")
        ruta_vacio = os.path.join(original, "..", "assets", "items", "corazon_vacio.png")

        imagen_lleno = pygame.image.load(ruta_lleno)
        imagen_vacio = pygame.image.load(ruta_vacio)

        self.completo = pygame.transform.scale(imagen_lleno, (32, 32))
        self.vacio = pygame.transform.scale(imagen_vacio, (32, 32))

    def perder_corazones(self):
        if self.powerup_activo:
            self.powerup_activo = False
        elif self.corazones_extra > 0 and not self.corazones_extra_usados:
            self.corazones_extra_usados = True
        elif self.vida_actual > 0:
            self.vida_actual -= 1

    def aumento_vida(self):
        if self.vida_actual < self.vida_maxima:
            self.vida_actual += 1

    def activar_powerup_vida(self):
        self.powerup_activo = True

    def agregar_corazon_extra(self):
        self.corazones_extra = 1
        self.corazones_extra_usados = False

    def reiniciar(self):
        self.vida_actual = self.vida_maxima
        self.powerup_activo = False
        self.corazones_extra = 0
        self.corazones_extra_usados = False

    def visual(self, ventana, pos_x=10, pos_y=10):
        # Corazones normales
        for i in range(self.vida_maxima):
            x = pos_x + i * 40
            if i < self.vida_actual:
                ventana.blit(self.completo, (x, pos_y))
            else:
                ventana.blit(self.vacio, (x, pos_y))

        # Corazón extra
        if self.corazones_extra > 0:
            x_extra = pos_x + self.vida_maxima * 40
            if not self.corazones_extra_usados:
                ventana.blit(self.completo, (x_extra, pos_y))
            else:
                ventana.blit(self.vacio, (x_extra, pos_y))
