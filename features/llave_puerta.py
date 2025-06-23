import pygame
import os

class Llave:
    def __init__(self, x, y):
        principal = os.path.dirname(__file__)
        ruta_img = os.path.join(principal, "..", "assets", "items", "llave.png")
        self.imagen = pygame.image.load(ruta_img)
        self.imagen = pygame.transform.scale(self.imagen, (28, 28)) 
        self.x = x
        self.y = y
        self.recogida = False
        self.visible = False  

    def cambio(self):
        self.visible = True

    def dibujar(self, ventana):
        if self.visible and not self.recogida:
            ventana.blit(self.imagen, (self.x, self.y))

    def dibujar_llave(self, ventana):
        if self.recogida:
            ventana.blit(self.imagen, (10, ventana.get_height() - 70)) 


class Puerta:
    def __init__(self, x, y):
        principal = os.path.dirname(__file__)
        ruta_img = os.path.join(principal, "..", "assets", "items", "puerta.png")
        self.imagen = pygame.image.load(ruta_img)
        self.imagen = pygame.transform.scale(self.imagen, (28, 28))
        self.x = x
        self.y = y
        self.activa = False

    def dibujar(self, ventana):
        if self.activa:
            ventana.blit(self.imagen, (self.x, self.y))


#Explicacion

"""
La clase llave carga llave.png con oygame.image.load(ruta_img) que busca
el archivo. Se escalo a 28x28 con pygame.transform.scale()

Si la llave fue recogida entonces false. Si es visible tambien false.
El def cambio es para hacerla visible. Esto es para que la llave no sea
visible para el usuario hasta que destruya el bloque y la obtenga. dibujar_llave
la pone a la par de los corazones. Osea abajo a la izquierda con respecto
al tamaño de la ventana (ventana.get_height()

La clase puerta se activa cuando se obtiene la llave si es true.

"""
