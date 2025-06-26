from features.imports import *
from features.utilidades import guardar_puntaje

#---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---#

#Función de la pantalla final:
def mostrar_pantalla_final(ventana, nombre, puntos, duración, victoria=True):
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 32, bold=4)
    
    #--- Obtención del puntaje ---#
    guardar_puntaje(nombre, puntos)
    
    
    #--- Mensaje final (Victoria o Derrota) ---#
    mensaje = "¡VICTORIA!" if victoria else "DERROTADO"

        #--- VERDE: Victoria            ROJO: Derrota ---#
    color = (0, 255, 0) if victoria else (255, 0, 0)
    
    #Opciones al finalizar el juego:
    boton_menu = pygame.Rect(200, 400, 180, 50)
    boton_salir = pygame.Rect(420, 400, 180, 50)

    corriendo = True
    while corriendo:
        ventana.fill((0, 0, 20)) #Se fillea la pantalla con un color tipo negro
        
        #El mensaje final será una especie de imagen que podremos dibujar en la ventana 
        mensaje_final = fuente.render(mensaje, True, color) 
        ventana.blit(mensaje_final, (310, 100))

        #Obtenemos la información del usuario:
        info_user = [
            f"Nombre: {nombre}",
            f"Puntaje: {puntos}",
            f"Duración: {duración}"
        ]
        
        
#---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---#

#EDICIÓN DE PANTALLA:        

        for i, linea in enumerate(info_user):
        #i = índice de la lista "info_user"
        #linea = contenido de cada texto. Ejemplo "Nombre: Joel Picado" "Puntaje: 600" "Duración: 1:15"
            
            ventana.blit(fuente.render(linea, True, (255, 255, 255)), (280, 180 + i * 40))

        #remarcamos un cuadro para que se haga notar los botones
        pygame.draw.rect(ventana, (0, 100, 200), boton_menu)
        pygame.draw.rect(ventana, (200, 50, 50), boton_salir)

        #Ponemos el texto dentro de los botones:
        ventana.blit(fuente.render("Menú principal", True, (255, 255, 255)), (boton_menu.x + 10, boton_menu.y + 10))
        ventana.blit(fuente.render("Salir", True, (255, 255, 255)), (boton_salir.x + 50, boton_salir.y + 10))

#---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---#

        #Revisaremos todos los eventos posibles:
        for evento in pygame.event.get():
            
            #Evento 1: cerrar ventana
            if evento.type == pygame.QUIT:
                corriendo = False
            
            #Si se hace click izq:
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                
                #Si el click esta dentro del botón de volver al menú, 
                # entonces volvemos al menú principal.
                if boton_menu.collidepoint(evento.pos):
                    from screens.pantalla_inicio import mostrar_pantalla_inicio
                    mostrar_pantalla_inicio(ventana)
                    return
                
                #Si el evento esta pasando dentro del botón de salir, 
                # entonces salimos del juego completamente.
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update() #Actualización de la ventana para mostrar los cambios
        reloj.tick(60) #Limitamos el bucle a 60 FPS