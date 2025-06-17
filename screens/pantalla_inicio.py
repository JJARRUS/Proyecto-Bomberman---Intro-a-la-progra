from features.imports import *
from screens.pantalla_personalizacion import mostrar_pantalla_personalizacion
from screens.pantalla_final import mostrar_pantalla_final #Se usará más adelante

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

    corriendo = True
    while corriendo:
        ventana.blit(fondo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            #TODO: Remplazar los prints por las funciones reales a ejecutar
            #Ejemplo: "print("Iniciar Juego")" se elimina y se pone "mostrar_pantalla_info(ventana)"
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  #Clic izquierdo
                if boton_jugar.collidepoint(evento.pos):  # ejecuta si se hizo clic sobre el área de "Jugar"
                    mostrar_pantalla_personalizacion(ventana)

                elif boton_config.collidepoint(evento.pos):  # clic sobre "Configuración"
                    print("Configuración")

                elif boton_puntajes.collidepoint(evento.pos):  # clic sobre "Mejores Puntajes"
                    print("Mejores Puntajes")

                elif boton_info.collidepoint(evento.pos):  # clic sobre "Información"
                    print("Información")

                elif boton_salir.collidepoint(evento.pos):  # clic sobre "Salir"
                    pygame.quit()
                    sys.exit()

        #Actualización de la pantalla para mostrar cambios. 
        pygame.display.update()
        
        #Mantenemos el bucle ejecutandose a 60 FPS. FIXME
        reloj.tick(60)