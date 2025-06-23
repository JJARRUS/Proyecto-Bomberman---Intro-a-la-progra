import pygame
import os

modificar = 32

class Bomba:
    def __init__(self, x, y, tiempo=3000, tiempo_explota=1000):
        self.x = x
        self.y = y
        self.tiempo = tiempo
        self.tiempo_colocada = pygame.time.get_ticks()
        self.exploto = False
        self.tiempo_explosion = None
        self.tiempo_explota = tiempo_explota

        principal = os.path.dirname(__file__)
        foto_bomba = os.path.join(principal, "..", "assets", "bombas", "imagen_bomba.png")
        foto_explosion = os.path.join(principal, "..", "assets", "bombas", "imagen_explosion.png")

        self.imagen_bomba = pygame.image.load(foto_bomba)
        self.imagen_bomba = pygame.transform.scale(self.imagen_bomba, (modificar, modificar))

        self.imagen_explosion = pygame.image.load(foto_explosion)
        self.imagen_explosion = pygame.transform.scale(self.imagen_explosion, (modificar, modificar))

        self.jugador_esta = self.calcular_jugador_esta()

    def calcular_jugador_esta(self):
        return [
            (self.x, self.y),
            (self.x + modificar, self.y),
            (self.x - modificar, self.y),
            (self.x, self.y + modificar),
            (self.x, self.y - modificar),
        ]

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        if not self.exploto:
            if tiempo_actual - self.tiempo_colocada >= self.tiempo:
                self.exploto = True
                self.tiempo_explosion = tiempo_actual
        else:
            if tiempo_actual - self.tiempo_explosion >= self.tiempo_explota:
                return True
        return False

    def dibujar(self, ventana):
        if self.exploto:
            for x, y in self.jugador_esta:
                ventana.blit(self.imagen_explosion, (x, y))
        else:
            ventana.blit(self.imagen_bomba, (self.x, self.y))

class Explosivax:
    def __init__(self, max_bombas=3):
        self.bombas = []
        self.max_bombas = max_bombas

    def colocar_bomba(self, x, y):
        if len(self.bombas) < self.max_bombas:
            bomba = Bomba(x, y)
            self.bombas.append(bomba)

    def actualizar(self):
        bombas_activas = []
        for bomba in self.bombas:
            if not bomba.actualizar():
                bombas_activas.append(bomba)
        self.bombas = bombas_activas

    def dibujar(self, ventana):
        for bomba in self.bombas:
            bomba.dibujar(ventana)

#Explicacion
"""
La class Bomba recibe una posicion (x,y) y un tiempo donde espera
antes de que explota (tiempo) y el tiempo sera visible.
Se cargan dos imagenes, la de la bomba y la de la explosion.
Con pygame.time.get_ticks() se guarda el momento en que se coloco la bomba
para de4spues ver cuando se debe explotar.

calcular_jugador_esta deveulve una lista con cinco posiciones (self.x y self.y)
y arriba, abajo, derecha e izquierda como en el juego bomberman.

En actualizar se ve si ya exploto y si paso el tiempo. Si es asi revisa el tiempo
de duracion para despues desaparecerla y devolver true.

el dibujo muestra la imegen.

La clase Explosivax maneja las bombas activas y cuanntas hay al mismo tiempo
Las guarda en una lista. Si no se ha alcanzado el limite entonces puedes
agregar una bomba. Actualizar recorre las bombas y elimina las que hayan terminado
su ciclo

"""
