from features.imports import *
from screens.pantalla_personalizacion import mostrar_pantalla_personalizacion
from screens.pantalla_final import mostrar_pantalla_final #Se usará más adelante

#---0--- PANTALLA INICIO ---0---#
def mostrar_pantalla_inicio(ventana):

    reloj = pygame.time.Clock() #Esto nos ayudara a controlar los FPS

    #Ponemos la imagen de fondo:
    fondo = pygame.image.load("assets/Fondos/bomberman_main_menu.jpg")
    fondo = pygame.transform.scale(fondo, (800, 600))  #Aseguramos que se adapte a la ventana

    #Aca estarán los botones:
    boton_jugar = pygame.Rect(273, 200, 254, 50)
    boton_config = pygame.Rect(273, 300, 254, 50)
    boton_puntajes = pygame.Rect(273, 400, 254, 50)
    boton_info = pygame.Rect(100, 500, 160, 50)
    boton_salir = pygame.Rect(273, 500, 254, 50)

    #---0--- Si la ventana esta corriendo entonces: ---0---#
    corriendo = True
    while corriendo:

        #Pocisionamos la imagen en 0,0
        ventana.blit(fondo, (0, 0))

        #Obtendremos los eventos y los almacenamos#
        for evento in pygame.event.get():

            #Para cerrar el juego:
            if evento.type == pygame.QUIT:
                corriendo = False
                return "salir"

#---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0#

    #---0--- EVENTOS PRINCIPALES ---0---#

            #TODO: Remplazar los prints por las funciones reales a ejecutar
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  #Clic izquierdo

                #---0--- Click sobre "Jugar" ---0---#
                if boton_jugar.collidepoint(evento.pos):  
                    return "jugar"

                #---0--- Click sobre "Configuración" ---0---#
                elif boton_config.collidepoint(evento.pos):  
                    return "configuracion"

                #---0--- Click sobre "Mejores Puntajes" ---0---#
                elif boton_puntajes.collidepoint(evento.pos):
                    print("Mejores Puntajes")

                #---0--- Click sobre "Información" ---0---#
                elif boton_info.collidepoint(evento.pos):
                    return "informacion"

                #---0--- Click sobre "Salir" ---0---#
                elif boton_salir.collidepoint(evento.pos):  
                    return "salir"

        #Actualización de la pantalla para mostrar cambios. 
        pygame.display.update()

        #Mantenemos el bucle ejecutandose a 60 FPS. FIXME
        reloj.tick(60)