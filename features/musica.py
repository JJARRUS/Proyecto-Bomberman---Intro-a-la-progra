from features.imports import *
from features.config import *

class ControladorMusica:
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.musica_activada = True
            cls._instancia.archivo_actual = None
            pygame.mixer.init()  # Inicializa el mixer aquí
        return cls._instancia

def musica_activada(self):
        return self._musica_activada
        
def toggle(self):
    self._musica_activada = not self._musica_activada
    if self._musica_activada:
        if self._archivo_actual:
            self.activar()  # Reactiva la música actual
        else:
            pygame.mixer.music.stop()
        return self._musica_activada
    
def activar(self, nivel=1):
    if not self._musica_activada:
        return False
            
    archivo = "musica_niveles.mp3" if nivel != 4 else "musica_boss.mp3"
        
    try:
        pygame.mixer.music.load(f"assets/sonidos/{archivo}")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
        self._archivo_actual = archivo
        return True
    except Exception as e:
        print(f"Error cargando música: {e}")
        return False