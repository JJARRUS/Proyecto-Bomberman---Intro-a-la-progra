import pygame
import os

class Vida:
    def __init__(self, cantidad_vida=3):
        self.vida_maxima = cantidad_vida
        self.vida_actual = cantidad_vida

        original = os.path.dirname(__file__)
        foto_lleno = os.path.join(original, "..", "assets", "items", "corazon.png")
        corazon_none = os.path.join(original, "..", "assets", "items", "corazon_vacio.png")

        completo = pygame.image.load(foto_lleno)
        vacio = pygame.image.load(corazon_none)

        self.completo = pygame.transform.scale(completo, (32, 32))
        self.vacio = pygame.transform.scale(vacio, (32, 32))

    def perder_corazones(self):
        if self.vida_actual > 0:
            self.vida_actual -= 1

    def aumento_vida(self):
        if self.vida_actual < self.vida_maxima:
            self.vida_actual += 1

    def reiniciar(self):
        self.vida_actual = self.vida_maxima

    def visual(self, ventana, pos_x=10, pos_y=10):
        for i in range(self.vida_maxima):
            x = pos_x + i * 40
            y = pos_y
            if i < self.vida_actual:
                ventana.blit(self.completo, (x, y))
            else:
                ventana.blit(self.vacio, (x, y))
