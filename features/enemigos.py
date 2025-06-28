import pygame
import os
import random

TAM = 32

def obtener_posiciones_spawn(matriz, cantidad, posiciones_prohibidas=None):
    vacios = []
    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):
            if matriz[fila][col] == " ":
                if posiciones_prohibidas is None or (col, fila) not in posiciones_prohibidas:
                    vacios.append((col * TAM, fila * TAM))
    random.shuffle(vacios)
    return vacios[:cantidad]

class FlechaEnemiga:
    def __init__(self, x, y, direccion):
        self.x = x
        self.y = y
        self.direccion = direccion
        self.velocidad = 6
        ruta_img = os.path.join("assets", "enemigos", "flecha.png")
        self.image = pygame.image.load(ruta_img).convert_alpha()
        if direccion in ["izquierda", "derecha"]:
            self.image = pygame.transform.scale(self.image, (28, 12))
        else:
            self.image = pygame.transform.scale(self.image, (12, 28))
        if direccion == "arriba":
            self.image = pygame.transform.rotate(self.image, 90)
        elif direccion == "abajo":
            self.image = pygame.transform.rotate(self.image, -90)
        elif direccion == "izquierda":
            self.image = pygame.transform.rotate(self.image, 180)
        # Derecha queda igual
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def mover(self):
        if self.direccion == "arriba":
            self.y -= self.velocidad
        elif self.direccion == "abajo":
            self.y += self.velocidad
        elif self.direccion == "izquierda":
            self.x -= self.velocidad
        elif self.direccion == "derecha":
            self.x += self.velocidad
        self.rect.center = (self.x, self.y)

class Enemigo:
    def __init__(self, x, y, tipo="normal"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        self.tiempo_cambio = pygame.time.get_ticks()
        self.tiempo_golpeado = 0

        self.is_boss = False

        if tipo == "normal":
            self.vida = 1
            self.velocidad = 2
            ruta_img = os.path.join("assets", "enemigos", "ene_normal.png")
        elif tipo == "veloz":
            self.vida = 2
            self.velocidad = 4
            ruta_img = os.path.join("assets", "enemigos", "ene_veloz.png")
        elif tipo == "flechas":
            self.vida = 3
            self.velocidad = 2
            ruta_img = os.path.join("assets", "enemigos", "ene_flechas.png")
            self.flechas = []
            self.tiempo_ultima_flecha = pygame.time.get_ticks()
        elif tipo == "boss":
            self.vida = 4
            self.velocidad = 2
            ruta_img = os.path.join("assets", "enemigos", "N-Gage - Bomberman - Bosses.png")
            self.flechas = []
            self.tiempo_ultima_flecha = pygame.time.get_ticks()
            self.is_boss = True

        self.image = pygame.image.load(ruta_img).convert_alpha()
        # Boss un poco más grande (48x48), otros 32x32
        if tipo == "boss":
            self.image = pygame.transform.scale(self.image, (48, 48))
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        else:
            self.image = pygame.transform.scale(self.image, (TAM, TAM))
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        self.vivo = True

    def actualizar(self, jugador, vida, matriz, tiempo_actual, cooldown=1000):
        if not self.vivo:
            return

        dx, dy = 0, 0
        if self.direccion == "arriba":
            dy = -1
        elif self.direccion == "abajo":
            dy = 1
        elif self.direccion == "izquierda":
            dx = -1
        elif self.direccion == "derecha":
            dx = 1

        nuevo_rect = self.rect.move(dx * self.velocidad, dy * self.velocidad)
        puede_moverse = True
        for punto in [
            (nuevo_rect.left, nuevo_rect.top),
            (nuevo_rect.right - 1, nuevo_rect.top),
            (nuevo_rect.left, nuevo_rect.bottom - 1),
            (nuevo_rect.right - 1, nuevo_rect.bottom - 1),
        ]:
            fila = punto[1] // TAM
            col = punto[0] // TAM
            if (
                fila < 0 or col < 0 or
                fila >= len(matriz) or col >= len(matriz[0]) or
                matriz[fila][col] in ("I", "D")
            ):
                puede_moverse = False
                break

        if puede_moverse:
            self.rect = nuevo_rect
        else:
            self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])

        # Colisión con el jugador (daño una vez por cooldown)
        if self.rect.colliderect(jugador.rect):
            if tiempo_actual - self.tiempo_golpeado > cooldown:
                if hasattr(jugador, 'tiene_escudo') and jugador.tiene_escudo:
                    jugador.tiene_escudo = False
                elif hasattr(vida, 'powerup_activo') and vida.powerup_activo:
                    vida.powerup_activo = False
                else:
                    vida.perder_corazones()
                self.tiempo_golpeado = tiempo_actual

        # ----- FLECHAS -----
        if self.tipo in ["flechas", "boss"] and self.vivo:
            ahora = pygame.time.get_ticks()
            # Boss dispara flechas más seguido (cada 800ms), flechero cada 1500ms
            cooldown_flecha = 800 if self.tipo == "boss" else 1500
            if ahora - self.tiempo_ultima_flecha > cooldown_flecha:
                direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
                self.flechas.append(FlechaEnemiga(self.rect.centerx, self.rect.centery, direccion))
                self.tiempo_ultima_flecha = ahora

            for flecha in self.flechas[:]:
                flecha.mover()
                fila = flecha.rect.centery // TAM
                col = flecha.rect.centerx // TAM
                fuera_mapa = (
                    fila < 0 or fila >= len(matriz) or
                    col < 0 or col >= len(matriz[0])
                )
                if not fuera_mapa and matriz[fila][col] not in (" "):
                    self.flechas.remove(flecha)
                elif fuera_mapa:
                    self.flechas.remove(flecha)

    def verificar_muerte(self, explosiones):
        if not self.vivo:
            return False
        for x, y in explosiones:
            rect_exp = pygame.Rect(x, y, TAM, TAM)
            if rect_exp.colliderect(self.rect):
                self.vida -= 1
                if self.vida <= 0:
                    self.vivo = False
                    return True
        return False

    def dibujar(self, ventana):
        if self.vivo:
            ventana.blit(self.image, self.rect)
