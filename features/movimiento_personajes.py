# movimiento_personaje.py

import pygame
import os

tamaño = 32

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, personaje_num, matriz_juego):
        super().__init__()
        self.personaje_num = personaje_num
        self.direccion = 'parado'
        self.velocidad = 4
        self.matriz = matriz_juego  # Ahora usa matriz dinámica
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
        nuevo_rect = self.rect.move(dx * self.velocidad, dy * self.velocidad)
        for punto in [
            (nuevo_rect.left, nuevo_rect.top),
            (nuevo_rect.right - 1, nuevo_rect.top),
            (nuevo_rect.left, nuevo_rect.bottom - 1),
            (nuevo_rect.right - 1, nuevo_rect.bottom - 1),
        ]:
            fila = punto[1] // tamaño
            col = punto[0] // tamaño
            if fila < 0 or col < 0 or fila >= len(self.matriz) or col >= len(self.matriz[0]):
                return False
            if self.matriz[fila][col] in ('I', 'D'):
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
        if self.direccion == 'parado':
            x_bomba = (self.rect.centerx // tamaño) * tamaño
            y_bomba = (self.rect.centery // tamaño) * tamaño
        else:
            x_bomba = self.rect.centerx
            y_bomba = self.rect.centery
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
