from features.imports import *
# Creamos una instancia global del controlador de música

musica_activada = True
musica_cargada = False

#---0--- Para cargar la música en otras pantallas ---0---#

def cargar_musica():
    #--- Carga la música solo si está activada y no estaba cargada ---#
    global musica_cargada
    try:
        if musica_activada:
            # Verificamos si pygame está inicializado
            if not pygame.get_init():
                pygame.init()
            
            # Verificamos si el mixer está inicializado
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Cargamos y reproducimos la música
            pygame.mixer.music.load("assets/sonidos/musica_niveles.mp3")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
            musica_cargada = True
            return True
        else:
            # Si música está desactivada, paramos cualquier música
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
            return False

    except Exception as e:
        print(f"Error cargando música: {str(e)}")
        return False

def parar_musica():
    """Función para parar la música sin cerrar el mixer"""
    global musica_cargada
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        musica_cargada = False
    except:
        pass

def toggle_musica():
    """Función para cambiar el estado de la música"""
    global musica_activada
    musica_activada = not musica_activada
    
    if musica_activada:
        return cargar_musica()
    else:
        parar_musica()
        return False