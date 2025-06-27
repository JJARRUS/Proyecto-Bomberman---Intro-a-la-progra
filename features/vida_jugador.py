import pygame
import os

TAM_CASILLA = 32

class Vida:
    def __init__(self, cantidad_vida=3):
        ruta = os.path.join("assets", "items", "corazon.png")
        ruta_vacio = os.path.join("assets", "items", "corazon_vacio.png")

        self.corazon_lleno = pygame.image.load(ruta)
        self.corazon_lleno = pygame.transform.scale(self.corazon_lleno, (TAM_CASILLA, TAM_CASILLA))

        self.corazon_vacio = pygame.image.load(ruta_vacio)
        self.corazon_vacio = pygame.transform.scale(self.corazon_vacio, (TAM_CASILLA, TAM_CASILLA))

        self.vida_maxima = cantidad_vida
        self.vida_actual = cantidad_vida
        self.extra = False  
        self.powerup_activo = False  

    def perder_corazones(self):
        if self.extra:
            self.extra = False
        elif self.vida_actual > 0:
            self.vida_actual -= 1

    def ganar_vida(self):
        if not self.extra:
            self.extra = True
            self.powerup_activo = True

    def visual(self, ventana, pos_x=10, pos_y=450):
        for i in range(self.vida_maxima):
            x = pos_x + i * (TAM_CASILLA + 5)
            if i < self.vida_actual:
                ventana.blit(self.corazon_lleno, (x, pos_y))
            else:
                ventana.blit(self.corazon_vacio, (x, pos_y))
        if self.extra:
            x_extra = pos_x + self.vida_maxima * (TAM_CASILLA + 5)
            ventana.blit(self.corazon_lleno, (x_extra, pos_y))
