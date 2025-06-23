import pygame
import os
from features.logica_background import matriz_logica  

tamaño = 32

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, personaje_num):
        super().__init__()
        self.personaje_num = personaje_num
        self.direccion = 'parado'
        self.velocidad = 4
        carpeta_personaje = ''
        nombre_base = ''
        if personaje_num == 1:
            carpeta_personaje = 'PJ1'
            nombre_base = 'bomberman'
        elif personaje_num == 2:
            carpeta_personaje = 'PJ2'
            nombre_base = 'bombgirl'
        elif personaje_num == 3:
            carpeta_personaje = 'PJ3'
            nombre_base = 'chosen'
        ruta_base = os.path.join('assets', 'personajes', carpeta_personaje)
        self.imagenes = {
            'arriba': pygame.transform.scale(pygame.image.load(os.path.join(ruta_base, nombre_base + '_arriba.png')), (28, 28)),
            'abajo': pygame.transform.scale(pygame.image.load(os.path.join(ruta_base, nombre_base + '_abajo.png')), (28, 28)),
            'izquierda': pygame.transform.scale(pygame.image.load(os.path.join(ruta_base, nombre_base + '_izquierda.png')), (28, 28)),
            'derecha': pygame.transform.scale(pygame.image.load(os.path.join(ruta_base, nombre_base + '_derecha.png')), (28, 28)),
            'parado': pygame.transform.scale(pygame.image.load(os.path.join(ruta_base, nombre_base + '_parado.png')), (28, 28))
        }

        self.foto = self.imagenes[self.direccion]
        self.rect = self.foto.get_rect()
        self.rect.topleft = (x, y)

    def mover(self, dx, dy):
        nuevo_x = self.rect.x + dx * self.velocidad
        nuevo_y = self.rect.y + dy * self.velocidad
        fila = nuevo_y // tamaño
        col = nuevo_x // tamaño
        filas = len(matriz_logica)
        columnas = len(matriz_logica[0])
        if fila <= 0 or fila >= filas - 1 or col <= 0 or col >= columnas - 1:
            return False
        if matriz_logica[fila][col] == 'I' or matriz_logica[fila][col] == 'D':
            return False
        return True

    def movimiento(self, teclas):
        dx = dy = 0
        if teclas[pygame.K_w]:
            dy = -1
            self.direccion = 'arriba'
        elif teclas[pygame.K_s]:
            dy = 1
            self.direccion = 'abajo'
        elif teclas[pygame.K_a]:
            dx = -1
            self.direccion = 'izquierda'
        elif teclas[pygame.K_d]:
            dx = 1
            self.direccion = 'derecha'
        else:
            self.direccion = 'parado'
        if self.mover(dx, dy):
            self.rect.x += dx * self.velocidad
            self.rect.y += dy * self.velocidad
        self.foto = self.imagenes[self.direccion]
    def obtener_posicion_bomba(self):
        x_bomba = self.rect.x
        y_bomba = self.rect.y
        if self.direccion == 'arriba':
            y_bomba -= tamaño
        elif self.direccion == 'abajo':
            y_bomba += tamaño
        elif self.direccion == 'izquierda':
            x_bomba -= tamaño
        elif self.direccion == 'derecha':
            x_bomba += tamaño
        x_bomba = (x_bomba // tamaño) * tamaño
        y_bomba = (y_bomba // tamaño) * tamaño
        return x_bomba, y_bomba

    def dibujar(self, ventana):
        ventana.blit(self.foto, self.rect)

#Explicacion

"""
el jugador recibe una posicion inicial (x,y) y un numero de personaje que determina
las sprites que va a usar. Estas imagenes se escalan a 28x28 pixeles. Luego se obtiene
un rect para manerjar su posicion y colisciones. rect.topleft coloca la esquina superior
izquierda del personaje

moverr(dx,dy) ve si el jugador puede moveerse en una direccion especifica. dx = -1 es
moverse a la izquierda. Se calcula con (nuevo_x, nueov_y). Luego convierte la posicion en
una seccion de la matrriz dividiendo entre la escala de la casilla (32). Esto para ver
si el jugador esta ir a una casilla valida.
Si por ejemplo esta fuera del borde o es I o D entonces devuelve False.

obtener_posicion_bomba() calcula la posicion donde se debe colocar la bomba segun la direccion
actual del jugador. Se basa desde self.rect.x, self.rect.y y se mueve hacia arriba, abajo
y asi segun self.direccion. 
"""
