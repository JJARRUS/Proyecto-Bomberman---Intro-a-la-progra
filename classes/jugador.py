from features.imports import *

class Jugador:
    def __init__(self, nombre, personaje_num, sprite_path):
        self.nombre = nombre
        self.personaje_num = personaje_num
        self.sprite = self.cargar_sprite(sprite_path)
        self.x = 0  
        self.y = 0
        self.vidas = 3
        self.bombas_disponibles = 5  
        self.velocidad = 5

        self.configurar_personaje()

    def cargar_sprite(self, path):
        try:
            sprite = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(sprite, (64, 64))
        except:
            sprite = pygame.Surface((64, 64))
            colores = [(255, 255, 255), (255, 100, 100), (100, 100, 255)][self.personaje_num - 1]
            sprite.fill(colores)
            return sprite

    def configurar_personaje(self):
        if self.personaje_num == 1:  # Bombman
            self.daño_bomba = 2
            self.rango_bomba = 2
        elif self.personaje_num == 2:  # Bombgirl
            self.daño_bomba = 1
            self.rango_bomba = 3
            self.velocidad = 6
        elif self.personaje_num == 3:  # The Chosen One
            self.daño_bomba = 3
            self.rango_bomba = 1
            self.vidas = 4

    def puede_colocar_bomba(self):
        return self.bombas_disponibles > 0

    def usar_bomba(self):
        if self.puede_colocar_bomba():
            self.bombas_disponibles -= 1

    def recuperar_bomba(self):
        self.bombas_disponibles += 1

    def dibujar(self, ventana):
        ventana.blit(self.sprite, (self.x, self.y))

    def mover(self, dx, dy):
        self.x += dx * self.velocidad
        self.y += dy * self.velocidad
