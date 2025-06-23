from features.imports import *
from features.juego import Juego  # Nueva clase que unificará la lógica

def mostrar_pantalla_juego(ventana, jugador_info):
    juego = Juego(ventana, jugador_info)
    
    corriendo = True
    while corriendo:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            juego.manejar_eventos(evento)
        
        # Actualización
        resultado = juego.actualizar()
        if resultado in ["victoria", "derrota"]:
            return resultado
        
        # Dibujado
        juego.dibujar()
        pygame.display.update()
        juego.reloj.tick(60)
    
    return "menu"