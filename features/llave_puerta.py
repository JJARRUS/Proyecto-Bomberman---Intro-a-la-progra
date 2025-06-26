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
