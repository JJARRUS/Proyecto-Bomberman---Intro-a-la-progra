import pygame
import os
import random

TAM = 32

class ItemPowerUpManager:
    def __init__(self, matriz):
        self.items = []
        self.powerups = []
        self.imagenes = {}
        self.matriz = matriz
        self.recogio_powerup_vida = False
        self.items_recogidos = []       
        self.powerups_visuales = []     
        self.cargar_imagenes()
        self.colocar_objetos()

    def cargar_imagenes(self):
        base = os.path.dirname(__file__)
        ruta = os.path.join(base, "..", "assets", "items_y_powerups")
        archivos = {
            'bomba': "bomba_item.png",
            'velocidad': "velocidad_item.png",
            'escudo': "escudo_item.png",
            'vida': "vida_pu.png",
            'daño': "damage_pu.png",
            'flecha': "arrow.png"
        }
        for clave, nombre in archivos.items():
            imagen = pygame.image.load(os.path.join(ruta, nombre))
            self.imagenes[clave] = pygame.transform.scale(imagen, (TAM, TAM))

    def colocar_objetos(self):
        libres = []
        for fila in range(len(self.matriz)):
            for col in range(len(self.matriz[0])):
                if self.matriz[fila][col] == ' ':
                    libres.append((col * TAM, fila * TAM))
        random.shuffle(libres)
        tipos_items = ['bomba', 'velocidad', 'escudo']
        for tipo in tipos_items:
            if libres:
                x, y = libres.pop()
                self.items.append({'tipo': tipo, 'x': x, 'y': y, 'activo': True})
        tipos_powerups = ['vida', 'daño']
        for tipo in tipos_powerups:
            if libres:
                x, y = libres.pop()
                self.powerups.append({'tipo': tipo, 'x': x, 'y': y, 'activo': True})

    def actualizar(self, jugador, vida):
        jugador_rect = jugador.rect
        for item in self.items:
            if item['activo'] and jugador_rect.colliderect(pygame.Rect(item['x'], item['y'], TAM, TAM)):
                item['activo'] = False
                jugador.items.append(item['tipo'])
                if item['tipo'] not in self.items_recogidos:
                    self.items_recogidos.append(item['tipo'])

        for pu in self.powerups:
            if pu['activo'] and jugador_rect.colliderect(pygame.Rect(pu['x'], pu['y'], TAM, TAM)):
                pu['activo'] = False
                if pu['tipo'] == 'vida':
                    vida.activar_powerup_vida()
                    self.recogio_powerup_vida = True
                elif pu['tipo'] == 'daño':
                    if not hasattr(jugador, 'daño_bomba'):
                        jugador.daño_bomba = 1
                    jugador.daño_bomba += 1
                if pu['tipo'] not in self.powerups_visuales:
                    self.powerups_visuales.append(pu['tipo'])

    def usar_item(self, jugador, tipo):
        if tipo in jugador.items:
            jugador.items.remove(tipo)
            if tipo in self.items_recogidos:
                self.items_recogidos.remove(tipo)
            if tipo == "bomba":
                jugador.bombas_disponibles += 1
            elif tipo == "velocidad":
                jugador.velocidad += 2
                jugador.tiempo_velocidad = pygame.time.get_ticks()
            elif tipo == "escudo":
                jugador.escudo_activo = True
                jugador.tiempo_escudo = pygame.time.get_ticks()

    def dibujar(self, ventana):
        for item in self.items:
            if item['activo']:
                ventana.blit(self.imagenes[item['tipo']], (item['x'], item['y']))
        for pu in self.powerups:
            if pu['activo']:
                ventana.blit(self.imagenes[pu['tipo']], (pu['x'], pu['y']))

    def mostrar_items_superiores(self, ventana, jugador, fuente, alto):
        x_inicio = 10 + jugador.vida_objeto.vida_maxima * 40 + (10 if jugador.vida_objeto.corazones_extra else 0) + 40
        y = alto - 90  
        total = self.items_recogidos + self.powerups_visuales

        # Mostrar flechas si aún quedan y es The Chosen One
        if jugador.personaje_num == 3 and jugador.flechas_disponibles > 0:
            if 'flecha' not in total:
                total.insert(0, 'flecha')
        elif 'flecha' in total:
            total.remove('flecha')

        total = total[:5]

        for i, nombre in enumerate(total):
            if nombre in self.imagenes:
                ventana.blit(self.imagenes[nombre], (x_inicio + i * 40, y))
                if nombre in self.items_recogidos:
                    texto = fuente.render(str(i + 1), True, (255, 255, 255))
                    ventana.blit(texto, (x_inicio + i * 40 + 20, y + 25))

