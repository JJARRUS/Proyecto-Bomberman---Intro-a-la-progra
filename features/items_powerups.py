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
        self.items_recogidos = []
        self.powerups_visibles = []
        self.pu_vida_recogido = False  # True cuando el jugador recoge el PU vida pero no lo ha activado
        self.pu_daño_recogido = False  # True cuando el jugador recoge el PU daño pero no lo ha activado
        self.cargar_imagenes()
        self.colocar_objetos()

    def cargar_imagenes(self):
        ruta = os.path.join("assets", "items_y_powerups")
        archivos = {
            'bomba': "bomba_item.png",
            'velocidad': "velocidad_item.png",
            'escudo': "escudo_item.png",
            'vida': "vida_pu.png",
            'daño': "damage_pu.png"
        }
        for clave, nombre in archivos.items():
            imagen = pygame.image.load(os.path.join(ruta, nombre))
            self.imagenes[clave] = pygame.transform.scale(imagen, (TAM, TAM))

    def colocar_objetos(self):
        destructibles = [(col, fila) for fila in range(len(self.matriz)) for col in range(len(self.matriz[0])) if self.matriz[fila][col] == 'D']
        random.shuffle(destructibles)
        tipos = ['bomba', 'velocidad', 'escudo', 'vida', 'daño']
        colocados = []

        for tipo in tipos:
            while destructibles:
                col, fila = destructibles.pop()
                x, y = col * TAM, fila * TAM
                ocupado = any(obj['x'] == x and obj['y'] == y for obj in colocados)
                if not ocupado:
                    nuevo = {'tipo': tipo, 'x': x, 'y': y, 'activo': False}
                    colocados.append(nuevo)
                    if tipo in ['bomba', 'velocidad', 'escudo']:
                        self.items.append(nuevo)
                    else:
                        self.powerups.append(nuevo)
                    break

    def liberar_objeto(self, col, fila):
        x, y = col * TAM, fila * TAM
        for obj in self.items + self.powerups:
            if obj['x'] == x and obj['y'] == y:
                obj['activo'] = True

    def actualizar(self, jugador, vida):
        jugador_rect = jugador.rect
        # Ítems: cuando el jugador recoge un ítem
        for item in self.items:
            if item['activo'] and jugador_rect.colliderect(pygame.Rect(item['x'], item['y'], TAM, TAM)):
                item['activo'] = False
                self.items_recogidos.append(item['tipo'])
                for key in jugador.items:
                    if jugador.items[key] is None:
                        jugador.items[key] = item['tipo']
                        break

        # PowerUps: se recogen pero solo se activan con tecla (no al recoger)
        for pu in self.powerups:
            if pu['activo'] and jugador_rect.colliderect(pygame.Rect(pu['x'], pu['y'], TAM, TAM)):
                pu['activo'] = False
                if pu['tipo'] == 'vida':
                    self.pu_vida_recogido = True  # Ya no se activa directamente
                elif pu['tipo'] == 'daño':
                    self.pu_daño_recogido = True  # Ya no se activa directamente
                if pu['tipo'] not in self.powerups_visibles:
                    self.powerups_visibles.append(pu['tipo'])

    def usar_item(self, jugador, tipo, vida):
        # Ítems normales: bomba, velocidad, escudo
        jugador.usar_item(tipo)
        for key, value in jugador.items.items():
            if value == tipo:
                jugador.items[key] = None
                break
        if tipo in self.items_recogidos:
            self.items_recogidos.remove(tipo)
        # PowerUps vida y daño no se activan aquí, sino con las teclas R/T (lo maneja pantalla_juego.py)

    def dibujar(self, ventana):
        for item in self.items:
            if item['activo']:
                ventana.blit(self.imagenes[item['tipo']], (item['x'], item['y']))
        for pu in self.powerups:
            if pu['activo']:
                ventana.blit(self.imagenes[pu['tipo']], (pu['x'], pu['y']))

    def mostrar_items_superiores(self, ventana, jugador, fuente, alto):
        # Mostramos los ítems y los PUs recogidos (solo los que están pendientes de usar)
        x_inicio = 10 + jugador.vida.vida_maxima * 40 + 10
        y = alto - 90

        total = []
        for nombre in self.items_recogidos:
            total.append(nombre)
        # Mostramos PU vida solo si está pendiente de usarse
        if self.pu_vida_recogido:
            total.append('vida')
        if self.pu_daño_recogido:
            total.append('daño')

        total = total[:5]

        for i, nombre in enumerate(total):
            if nombre in self.imagenes:
                ventana.blit(self.imagenes[nombre], (x_inicio + i * 40, y))
                # Números solo para ítems (1,2,3)
                if nombre in self.items_recogidos and i < 3:
                    texto = fuente.render(str(i + 1), True, (255, 255, 255))
                    ventana.blit(texto, (x_inicio + i * 40 + 20, y + 25))
                # Letras para PUs
                if nombre == 'vida':
                    texto = fuente.render('R', True, (255, 255, 255))
                    ventana.blit(texto, (x_inicio + i * 40 + 20, y + 25))
                if nombre == 'daño':
                    texto = fuente.render('T', True, (255, 255, 255))
                    ventana.blit(texto, (x_inicio + i * 40 + 20, y + 25))
