import pygame
import random
import os

TAM_CASILLA = 32

class BloqueHielo:
    def __init__(self, matriz_juego, cantidad=2):
        self.imagen = self.cargar_imagen()
        self.posiciones = self.generar_posiciones(matriz_juego, cantidad)
        self.afectando = False
        self.tiempo_afectado = 0
        self.velocidad_original = None

    def cargar_imagen(self):
        ruta = os.path.join(os.path.dirname(__file__), "..", "assets", "Ambientacion", "hielo.png")
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (TAM_CASILLA, TAM_CASILLA))

    def generar_posiciones(self, matriz, cantidad):
        vacios = []
        for fila in range(len(matriz)):
            for col in range(len(matriz[0])):
                if matriz[fila][col] == " ":
                    vacios.append((col * TAM_CASILLA, fila * TAM_CASILLA))
        return random.sample(vacios, min(cantidad, len(vacios)))

    def dibujar(self, ventana):
        for pos in self.posiciones:
            ventana.blit(self.imagen, pos)

    def aplicar_efecto(self, jugador):
        jugador_rect = jugador.rect
        nuevas_posiciones = []
        for hielo_pos in self.posiciones:
            rect_hielo = pygame.Rect(hielo_pos[0], hielo_pos[1], TAM_CASILLA, TAM_CASILLA)
            if jugador_rect.colliderect(rect_hielo):
                if not self.afectando:
                    self.afectando = True
                    self.tiempo_afectado = pygame.time.get_ticks()
                    self.velocidad_original = jugador.velocidad
                    jugador.velocidad /= 2
            else:
                nuevas_posiciones.append(hielo_pos)
        self.posiciones = nuevas_posiciones

        if self.afectando:
            if pygame.time.get_ticks() - self.tiempo_afectado > 3000:
                jugador.velocidad = self.velocidad_original
                self.afectando = False

class Oscuridad:
    def __init__(self, jugador, matriz, ancho, alto):
        self.jugador = jugador
        self.superficie = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        self.radio = 100
        self.matriz = matriz

    def dibujar(self, ventana):
        self.superficie.fill((0, 0, 0, 200))  

        centro_x = self.jugador.rect.centerx
        centro_y = self.jugador.rect.centery
        pygame.draw.circle(self.superficie, (0, 0, 0, 0), (centro_x, centro_y), self.radio)
        for fila in [0, len(self.matriz) - 1]:
            for col in range(len(self.matriz[0])):
                x = col * TAM_CASILLA
                y = fila * TAM_CASILLA
                pygame.draw.rect(self.superficie, (0, 0, 0, 0), (x, y, TAM_CASILLA, TAM_CASILLA))

        for fila in range(len(self.matriz)):
            for col in [0, len(self.matriz[0]) - 1]:
                x = col * TAM_CASILLA
                y = fila * TAM_CASILLA
                pygame.draw.rect(self.superficie, (0, 0, 0, 0), (x, y, TAM_CASILLA, TAM_CASILLA))

        ventana.blit(self.superficie, (0, 0))

class Mina:
    def __init__(self, matriz_juego, cantidad=2):
        self.imagen = self.cargar_imagen()
        self.posiciones = self.generar_posiciones(matriz_juego, cantidad)
        self.detonadas = set()

    def cargar_imagen(self):
        ruta = os.path.join(os.path.dirname(__file__), "..", "assets", "Ambientacion", "mina.png")
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (TAM_CASILLA, TAM_CASILLA))

    def generar_posiciones(self, matriz, cantidad):
        vacios = []
        for fila in range(len(matriz)):
            for col in range(len(matriz[0])):
                if matriz[fila][col] == " ":
                    vacios.append((col * TAM_CASILLA, fila * TAM_CASILLA))
        return random.sample(vacios, min(cantidad, len(vacios)))

    def dibujar(self, ventana):
        for pos in self.posiciones:
            if pos not in self.detonadas:
                ventana.blit(self.imagen, pos)

    def verificar_detonacion(self, jugador, vida):
        jugador_rect = jugador.rect
        for pos in self.posiciones:
            if pos in self.detonadas:
                continue
            mina_rect = pygame.Rect(pos[0], pos[1], TAM_CASILLA, TAM_CASILLA)
            if jugador_rect.colliderect(mina_rect):
                self.detonadas.add(pos)
                if jugador.tiene_escudo:
                    jugador.tiene_escudo = False
                elif vida.powerup_activo:
                    vida.powerup_activo = False
                else:
                    vida.perder_corazones()

class ZonaVeneno:
    def __init__(self, matriz_juego, cantidad=3):
        self.imagen = self.cargar_imagen()
        self.posiciones = self.generar_posiciones(matriz_juego, cantidad)
        self.tiempo_ultimo_daño = {}

    def cargar_imagen(self):
        ruta = os.path.join(os.path.dirname(__file__), "..", "assets", "Ambientacion", "veneno.png")
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (TAM_CASILLA, TAM_CASILLA))

    def generar_posiciones(self, matriz, cantidad):
        vacios = []
        for fila in range(len(matriz)):
            for col in range(len(matriz[0])):
                if matriz[fila][col] == " ":
                    vacios.append((col * TAM_CASILLA, fila * TAM_CASILLA))
        return random.sample(vacios, min(cantidad, len(vacios)))

    def dibujar(self, ventana):
        for pos in self.posiciones:
            ventana.blit(self.imagen, pos)

    def aplicar_efecto(self, jugador, vida):
        ahora = pygame.time.get_ticks()
        jugador_rect = jugador.rect
        for pos in self.posiciones:
            rect = pygame.Rect(pos[0], pos[1], TAM_CASILLA, TAM_CASILLA)
            if jugador_rect.colliderect(rect):
                tiempo_anterior = self.tiempo_ultimo_daño.get(pos, 0)
                if ahora - tiempo_anterior > 1000:  
                    self.tiempo_ultimo_daño[pos] = ahora
                    if jugador.tiene_escudo:
                        jugador.tiene_escudo = False
                    elif vida.powerup_activo:
                        vida.powerup_activo = False
                    else:
                        vida.perder_corazones()
