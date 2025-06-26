
import pygame
import os

class Vida:
    def __init__(self, cantidad_vida=3):
        self.vida_maxima = cantidad_vida
        self.vida_actual = cantidad_vida
        self.powerup_activo = False

        original = os.path.dirname(__file__)
        foto_lleno = os.path.join(original, "..", "assets", "items", "corazon.png")
        corazon_none = os.path.join(original, "..", "assets", "items", "corazon_vacio.png")

        self.completo = pygame.transform.scale(pygame.image.load(foto_lleno), (32, 32))
        self.vacio = pygame.transform.scale(pygame.image.load(corazon_none), (32, 32))

    def perder_corazones(self):
        if self.powerup_activo:
            self.powerup_activo = False
        elif self.vida_actual > 0:
            self.vida_actual -= 1

    def aumento_vida(self):
        if self.vida_actual < self.vida_maxima:
            self.vida_actual += 1

    def activar_powerup_vida(self):
        self.powerup_activo = True

    def reiniciar(self):
        self.vida_actual = self.vida_maxima
        self.powerup_activo = False

    def visual(self, ventana, pos_x=10, pos_y=10):
        for i in range(self.vida_maxima):
            x = pos_x + i * 40
            if i < self.vida_actual:
                ventana.blit(self.completo, (x, pos_y))
            else:
                ventana.blit(self.vacio, (x, pos_y))
#Explicacion del codigo

"""
En clase vida se recibe como parametro la cantidad total de vidas (3 en este caso)
y la guarda en self.vida_maxima y self.vbda_actual. Luego con import os
se usa el corazon vacio y lleno.

Se cargan con pygame.image.load() y se escalan con 32x32 con pygame.transform.scale()

El perder_corazones() se llama cuando el jugador recibe un golpe. Si es mayor que 1
le resta 1 corazon. El metodo aumento__vida permite que lo recupere si no ha llego al max

Reiniciar() es para cuando se comienza un nuevo nivel o si pierdes una vida completa

"""
