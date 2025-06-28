import pygame
import os
import random

TAM_CASILLA = 32

class FlechaEnemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        ruta = os.path.join("assets", "items_y_powerups", "arrow.png")
        self.image = pygame.image.load(ruta).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TAM_CASILLA, TAM_CASILLA // 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.direccion = direccion
        self.velocidad = 6

    def mover(self):
        if self.direccion == "arriba":
            self.rect.y -= self.velocidad
        elif self.direccion == "abajo":
            self.rect.y += self.velocidad
        elif self.direccion == "izquierda":
            self.rect.x -= self.velocidad
        elif self.direccion == "derecha":
            self.rect.x += self.velocidad

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo="normal"):
        super().__init__()
        self.x = x
        self.y = y
        self.tipo = tipo

        if tipo == "normal":
            self.vida = 1
            ruta_img = os.path.join("assets", "enemigos", "ene_normal.png")
            self.velocidad = 2
        elif tipo == "veloz":
            self.vida = 2
            ruta_img = os.path.join("assets", "enemigos", "ene_veloz.png")
            self.velocidad = 4
        elif tipo == "flechas":
            self.vida = 3
            ruta_img = os.path.join("assets", "enemigos", "ene_flechas.png")
            self.velocidad = 2
            self.flechas = []
            self.cooldown_flecha = 2000  # ms
            self.tiempo_ultima_flecha = 0
        elif tipo == "boss":
            self.vida = 4
            ruta_img = os.path.join("assets", "enemigos", "boss.png")
            self.velocidad = 2
            self.flechas = []
            self.cooldown_flecha = 1200
            self.tiempo_ultima_flecha = 0
            self.is_boss = True
        else:
            self.vida = 1
            ruta_img = os.path.join("assets", "enemigos", "ene_normal.png")
            self.velocidad = 2

        self.image = pygame.image.load(ruta_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TAM_CASILLA, TAM_CASILLA))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direccion = random.choice(["arriba", "abajo", "izquierda", "derecha"])
        self.tiempo_ultimo_mov = pygame.time.get_ticks()
        self.cooldown_mov = 400  # ms
        self.vivo = True
        self.matriz = None
        self.ha_recibido_bomba = set()  # para no recibir daño varias veces de la misma explosión

    def mover(self, matriz):
        dx, dy = 0, 0
        if self.direccion == "arriba":
            dy = -self.velocidad
        elif self.direccion == "abajo":
            dy = self.velocidad
        elif self.direccion == "izquierda":
            dx = -self.velocidad
        elif self.direccion == "derecha":
            dx = self.velocidad

        nuevo_rect = self.rect.move(dx, dy)
        # Chequear colisión con bloques
        colision = False
        for punto in [
            (nuevo_rect.left, nuevo_rect.top),
            (nuevo_rect.right - 1, nuevo_rect.top),
            (nuevo_rect.left, nuevo_rect.bottom - 1),
            (nuevo_rect.right - 1, nuevo_rect.bottom - 1),
        ]:
            fila = punto[1] // TAM_CASILLA
            col = punto[0] // TAM_CASILLA
            if fila < 0 or col < 0 or fila >= len(matriz) or col >= len(matriz[0]):
                colision = True
                break
            if matriz[fila][col] in ('I', 'D'):
                colision = True
                break

        if not colision:
            self.rect = nuevo_rect
        else:
            self.direccion = random.choice(["arriba", "abajo", "izquierda", "derecha"])

    def disparar_flecha(self, jugador):
        now = pygame.time.get_ticks()
        if now - self.tiempo_ultima_flecha > self.cooldown_flecha:
            dx = jugador.rect.centerx - self.rect.centerx
            dy = jugador.rect.centery - self.rect.centery
            if abs(dx) > abs(dy):
                direccion = "derecha" if dx > 0 else "izquierda"
            else:
                direccion = "abajo" if dy > 0 else "arriba"
            flecha = FlechaEnemigo(self.rect.centerx, self.rect.centery, direccion)
            self.flechas.append(flecha)
            self.tiempo_ultima_flecha = now

    def actualizar(self, jugador, vida, matriz, tiempo_actual, tiempo_entre_golpes):
        self.mover(matriz)
        if self.tipo in ["flechas", "boss"]:
            self.disparar_flecha(jugador)
            # Mover flechas y eliminar las que salgan del mapa o toquen bloques
            for flecha in self.flechas[:]:
                # Simular próximo movimiento
                next_rect = flecha.rect.copy()
                if flecha.direccion == "arriba":
                    next_rect.y -= flecha.velocidad
                elif flecha.direccion == "abajo":
                    next_rect.y += flecha.velocidad
                elif flecha.direccion == "izquierda":
                    next_rect.x -= flecha.velocidad
                elif flecha.direccion == "derecha":
                    next_rect.x += flecha.velocidad

                fila = next_rect.centery // TAM_CASILLA
                col = next_rect.centerx // TAM_CASILLA

                if (0 <= fila < len(matriz) and 0 <= col < len(matriz[0]) and matriz[fila][col] in ['I', 'D']):
                    self.flechas.remove(flecha)
                else:
                    flecha.mover()
                    # Fuera de mapa
                    if (flecha.rect.x < 0 or flecha.rect.x >= len(matriz[0]) * TAM_CASILLA or
                        flecha.rect.y < 0 or flecha.rect.y >= len(matriz) * TAM_CASILLA):
                        self.flechas.remove(flecha)

        # Colisión con jugador (un solo golpe por segundo)
        if self.rect.colliderect(jugador.rect):
            if tiempo_actual - getattr(jugador, "ultimo_golpe", 0) > tiempo_entre_golpes:
                if hasattr(jugador, "tiene_escudo") and jugador.tiene_escudo:
                    jugador.tiene_escudo = False
                elif jugador.vida.powerup_activo:
                    jugador.vida.powerup_activo = False
                else:
                    jugador.vida.perder_corazones()
                jugador.ultimo_golpe = tiempo_actual

    def verificar_muerte(self, explosiones):
        """Recibe una lista de (x,y) de celdas explotadas"""
        rect_enemigo = self.rect
        explotado_ahora = False
        for x_exp, y_exp in explosiones:
            rect_exp = pygame.Rect(x_exp, y_exp, TAM_CASILLA, TAM_CASILLA)
            key = (x_exp, y_exp)
            if rect_exp.colliderect(rect_enemigo) and key not in self.ha_recibido_bomba:
                self.vida -= 1
                self.ha_recibido_bomba.add(key)
                explotado_ahora = True
        if self.vida <= 0 and self.vivo:
            self.vivo = False
            return True
        return False

    def dibujar(self, ventana):
        if self.vivo:
            ventana.blit(self.image, self.rect)
            # Opcional: dibujar barra de vida
            if self.tipo in ["veloz", "flechas", "boss"]:
                ancho_barra = TAM_CASILLA
                alto_barra = 5
                x = self.rect.x
                y = self.rect.y - alto_barra - 2
                max_vida = 1
                if self.tipo == "veloz":
                    max_vida = 2
                elif self.tipo == "flechas":
                    max_vida = 3
                elif self.tipo == "boss":
                    max_vida = 4
                barra_ancho = int(ancho_barra * self.vida / max_vida)
                pygame.draw.rect(ventana, (255,0,0), (x, y, ancho_barra, alto_barra))
                pygame.draw.rect(ventana, (0,255,0), (x, y, barra_ancho, alto_barra))

def obtener_posiciones_spawn(matriz, cantidad, posiciones_prohibidas=set()):
    """Devuelve una lista de tuplas (x, y) para spawn de enemigos en celdas vacías no prohibidas"""
    libres = []
    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):
            if matriz[fila][col] == " " and (col, fila) not in posiciones_prohibidas:
                libres.append((col * TAM_CASILLA, fila * TAM_CASILLA))
    random.shuffle(libres)
    return libres[:cantidad]
