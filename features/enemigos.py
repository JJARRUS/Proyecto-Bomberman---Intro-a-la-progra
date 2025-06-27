import pygame
import os

TAM_CASILLA = 32

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        ruta_img = os.path.join("assets", "enemigos", "ene_normal.png")
        self.image = pygame.image.load(ruta_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TAM_CASILLA, TAM_CASILLA))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.direccion = "abajo"
        self.velocidad = 1
        self.vivo = True

    def actualizar(self, jugador, vida, matriz, tiempo_actual, delay):
        if not self.vivo:
            return

        dx = dy = 0
        if self.direccion == "arriba":
            dy = -1
        elif self.direccion == "abajo":
            dy = 1
        elif self.direccion == "izquierda":
            dx = -1
        elif self.direccion == "derecha":
            dx = 1

        nuevo_rect = self.rect.move(dx * self.velocidad, dy * self.velocidad)
        colision = False

        for punto in [
            (nuevo_rect.left, nuevo_rect.top),
            (nuevo_rect.right - 1, nuevo_rect.top),
            (nuevo_rect.left, nuevo_rect.bottom - 1),
            (nuevo_rect.right - 1, nuevo_rect.bottom - 1),
        ]:
            fila = punto[1] // TAM_CASILLA
            col = punto[0] // TAM_CASILLA
            if fila < 0 or col < 0 or fila >= len(matriz) or col >= len(matriz[0]) or matriz[fila][col] in ("I", "D"):
                colision = True
                break

        if colision:
            self.direccion = self.elegir_direccion_aleatoria()
        else:
            self.rect.x += dx * self.velocidad
            self.rect.y += dy * self.velocidad

        if self.rect.colliderect(jugador.rect):
            if tiempo_actual - jugador.ultimo_golpe > delay:
                if jugador.tiene_escudo:
                    jugador.tiene_escudo = False
                elif jugador.vida.powerup_activo:
                    jugador.vida.powerup_activo = False
                else:
                    jugador.vida.perder_corazones()
                jugador.ultimo_golpe = tiempo_actual

    def elegir_direccion_aleatoria(self):
        import random
        return random.choice(["arriba", "abajo", "izquierda", "derecha"])

    def verificar_muerte(self, coordenadas_explosion):
        if not self.vivo:
            return False
        for x, y in coordenadas_explosion:
            if self.rect.colliderect(pygame.Rect(x, y, TAM_CASILLA, TAM_CASILLA)):
                self.vivo = False
                return True
        return False

    def dibujar(self, ventana):
        if self.vivo:
            ventana.blit(self.image, self.rect)
