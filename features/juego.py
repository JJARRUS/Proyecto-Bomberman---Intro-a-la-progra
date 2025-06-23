from features.imports import *
from features.movimiento_personajes import Jugador
from features.vida_jugador import Vida
from features.bombas_explosion import Explosivax
from features.llave_puerta import Llave, Puerta
from features.background import dibujar_background
from features.logica_background import matriz_logica
from features.enemigos import EnemigoComun, EnemigoVeloz, EnemigoFlechas, JefeFinal
from features.items import Item, PowerUp

class Juego:
    def __init__(self, ventana, jugador_info):
        self.ventana = ventana
        self.reloj = pygame.time.Clock()
        
        # Jugador (usando el código de tu compañera)
        self.jugador = Jugador(32, 32, jugador_info['personaje_num'])
        
        # Sistemas existentes
        self.vida = Vida()
        self.explosivos = Explosivax()
        self.matriz = matriz_logica
        
        # Nuevos sistemas
        self.nivel_actual = 1
        self.puntos = 0
        self.iniciar_nivel(self.nivel_actual)
    
    def iniciar_nivel(self, nivel):
        # Configuración usando el código de llave_puerta.py
        llave_pos, puerta_pos, _ = posicion_llave_y_puerta(self.matriz)
        self.llave = Llave(*llave_pos)
        self.puerta = Puerta(*puerta_pos)
        
        # Configurar enemigos según nivel
        self.enemigos = []
        self.enemigos.append(EnemigoComun(160, 160))
        
        if nivel >= 2:
            self.enemigos.append(EnemigoVeloz(320, 160))
        if nivel >= 3:
            self.enemigos.append(EnemigoFlechas(480, 160))
        if nivel == 4:
            self.enemigos.append(JefeFinal(400, 300))
        
        # Configurar ambientación
        self.fondo = self.cargar_fondo_nivel(nivel)
    
    def cargar_fondo_nivel(self, nivel):
        fondos = {
            1: "normal.png",
            2: "hielo.png",
            3: "oscuridad.png",
            4: "veneno.png"
        }
        return pygame.image.load(f"assets/fondos/{fondos[nivel]}")
    
    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                x, y = self.jugador.obtener_posicion_bomba()
                self.explosivos.colocar_bomba(x, y)
            # Teclas para items (1, 2, 3)
    
    def actualizar(self):
        # Actualizar jugador (código de movimiento_personajes)
        teclas = pygame.key.get_pressed()
        self.jugador.movimiento(teclas)
        
        # Actualizar explosivos (código de bombas_explosion)
        self.explosivos.actualizar()
        
        # Actualizar enemigos
        for enemigo in self.enemigos:
            enemigo.actualizar(self.jugador, self.matriz)
        
        # Verificar colisiones (llave, puerta, explosiones)
        self.verificar_colisiones()
        
        # Verificar condiciones de victoria/derrota
        if self.vida.vida_actual <= 0:
            return "derrota"
        if self.llave.recogida and self.jugador.rect.colliderect(pygame.Rect(self.puerta.x, self.puerta.y, 32, 32)):
            if self.nivel_actual < 4:
                self.nivel_actual += 1
                self.iniciar_nivel(self.nivel_actual)
            else:
                return "victoria"
    
    def dibujar(self):
        # Dibujar fondo usando background.py
        dibujar_background(self.ventana, self.matriz)
        
        # Dibujar elementos del juego
        self.llave.dibujar(self.ventana)
        self.puerta.dibujar(self.ventana)
        for enemigo in self.enemigos:
            enemigo.dibujar(self.ventana)
        self.jugador.dibujar(self.ventana)
        self.explosivos.dibujar(self.ventana)
        
        # Dibujar UI (vida, puntos, nivel)
        self.vida.visual(self.ventana)
        self.dibujar_ui()
    
    def dibujar_ui(self):
        fuente = pygame.font.SysFont("Arial", 24)
        texto_puntos = fuente.render(f"Puntos: {self.puntos}", True, (255, 255, 255))
        texto_nivel = fuente.render(f"Nivel: {self.nivel_actual}/4", True, (255, 255, 255))
        
        self.ventana.blit(texto_puntos, (self.ventana.get_width() - 150, 10))
        self.ventana.blit(texto_nivel, (self.ventana.get_width() - 150, 40))