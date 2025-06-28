import pygame
import os

TAM = 32

class Vida:
    def __init__(self, cantidad_vida=3):
        ruta = os.path.join("assets", "items", "corazon.png")
        ruta_vacio = os.path.join("assets", "items", "corazon_vacio.png")

        self.corazon_lleno = pygame.image.load(ruta)
        self.corazon_lleno = pygame.transform.scale(self.corazon_lleno, (TAM, TAM))

        self.corazon_vacio = pygame.image.load(ruta_vacio)
        self.corazon_vacio = pygame.transform.scale(self.corazon_vacio, (TAM, TAM))

        self.vida_maxima = cantidad_vida
        self.vida_actual = cantidad_vida
        self.extra = False
        self.powerup_activo = False

    def perder_corazones(self):
        if self.extra:
            self.extra = False
            self.powerup_activo = False
        elif self.vida_actual > 0:
            self.vida_actual -= 1

    def ganar_vida(self):
        if not self.extra:
            self.extra = True

    def activar_powerup_vida(self):
        self.extra = True
        self.powerup_activo = True

    def visual(self, ventana, pos_x=10, pos_y=450):
        for i in range(self.vida_maxima):
            x = pos_x + i * (TAM + 5)
            ventana.blit(self.corazon_lleno if i < self.vida_actual else self.corazon_vacio, (x, pos_y))
        if self.extra:
            ventana.blit(self.corazon_lleno, (pos_x + self.vida_maxima * (TAM + 5), pos_y))
