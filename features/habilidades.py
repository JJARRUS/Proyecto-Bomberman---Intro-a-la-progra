import pygame
import os

TAM_CASILLA = 32

class Flecha:
    def __init__(self, x, y, direccion, matriz):
        ruta = os.path.join(os.path.dirname(__file__), "..", "assets", "items_y_powerups", "arrow.png")
        self.imagen = pygame.image.load(ruta).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (TAM_CASILLA, TAM_CASILLA))
        self.x = x
        self.y = y
        self.direccion = direccion
        self.velocidad = 8
        self.rect = pygame.Rect(self.x, self.y, TAM_CASILLA, TAM_CASILLA)
        self.matriz = matriz
        self.colisiono = False

    def mover(self):
        if self.direccion == "arriba":
            self.y -= self.velocidad
        elif self.direccion == "abajo":
            self.y += self.velocidad
        elif self.direccion == "izquierda":
            self.x -= self.velocidad
        elif self.direccion == "derecha":
            self.x += self.velocidad
        self.rect.topleft = (self.x, self.y)

    def verificar_colision(self):
        fila = self.rect.centery // TAM_CASILLA
        col = self.rect.centerx // TAM_CASILLA
        if 0 <= fila < len(self.matriz) and 0 <= col < len(self.matriz[0]):
            if self.matriz[fila][col] == 'D':
                self.matriz[fila][col] = ' '
                self.colisiono = True
            elif self.matriz[fila][col] == 'I':
                self.colisiono = True
        else:
            self.colisiono = True

    def actualizar(self):
        if not self.colisiono:
            self.mover()
            self.verificar_colision()

    def dibujar(self, ventana):
        if not self.colisiono:
            ventana.blit(self.imagen, (self.x, self.y))


def aplicar_habilidad_personaje(jugador, tipo):
    if tipo == 1:  # Bombman: 2 bombas extra
        jugador.bombas_disponibles += 2
    elif tipo == 2:  # Bombgirl: 1 vida adicional
        jugador.vida.corazones_extra = 1
    elif tipo == 3:  # The Chosen One
        jugador.flechas_disponibles = 2  # Solo 2 por nivel
