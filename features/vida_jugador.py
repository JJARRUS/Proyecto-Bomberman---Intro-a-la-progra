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
        if self.vida_actual < self.vida_maxima: #se uso para la prueba. Pero se puede quitar.
            self.vida_actual += 1

    def reiniciar(self): #Para los niveles nuevos 
        self.vida_actual = self.vida_maxima

    def visual(self, ventana, pos_x=10, pos_y=10):  
        for i in range(self.vida_maxima):
            x = pos_x + i * 40  
            y = pos_y
            if i < self.vida_actual:
                ventana.blit(self.completo, (x, y))
            else:
                ventana.blit(self.vacio, (x, y))
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
