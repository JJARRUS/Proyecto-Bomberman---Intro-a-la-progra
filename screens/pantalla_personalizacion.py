from features.imports import *
from classes.jugador import Jugador

#---0--- PANTALLA PERSONALIZACIÓN ---0---#

def mostrar_pantalla_personalizacion(ventana):
    
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("arial", 28)

    # Configuración de personajes
    personajes = {
        1: {"nombre": "Bomberman", "path": "assets/personajes/PJ1/bombman_pj1.png"},
        2: {"nombre": "Bombergirl", "path": "assets/personajes/PJ2/bombgirl_pj2.png"},
        3: {"nombre": "The Chosen One", "path": "assets/personajes/PJ3/the_chosen_one_pj3.png"}
    }

# Estado de la pantalla
    input_text = ""
    personaje_seleccionado = 1
    input_activo = False
    
    #--- BOTONES ---#
    boton_continuar = pygame.Rect(300, 450, 200, 50)
    boton_volver = pygame.Rect(50, 500, 120, 40)
    input_rect = pygame.Rect(250, 150, 300, 40)
    
    #---0--- Si la ventana esta corriendo entonces: ---0---#
    corriendo = True
    while corriendo:
        
        #Un color de fondo:
        ventana.fill((30, 30, 60)) 
        
        #Título:
        titulo = fuente.render("Selecciona tu Personaje", True, (255, 255, 255))
        ventana.blit(titulo, (250, 50))
        
        #Entrada de nombre:
        pygame.draw.rect(ventana, (255, 255, 255) if input_activo else (100, 100, 100), input_rect, 2)
        texto = input_text if input_text else "Ingresa tu nombre..."
        color = (255, 255, 255) if input_text else (150, 150, 150)
        ventana.blit(fuente.render(texto, True, color), (input_rect.x + 10, input_rect.y + 5))
        
        #Mostrar personajes:
        for i, pj in personajes.items():
            x = 150 + (i-1) * 200
            rect = pygame.Rect(x, 250, 100, 100)
            
            #Cargar sprites para la selección de personajes:
            try:
                sprite = pygame.image.load(pj["path"]).convert_alpha()
                sprite = pygame.transform.scale(sprite, (80, 80))
                ventana.blit(sprite, (x+10, 250))
            except:
                pass
            
            # Resaltar selección
            if i == personaje_seleccionado:
                pygame.draw.rect(ventana, (0, 255, 0), rect, 3)
            
            # Nombre del personaje
            ventana.blit(fuente.render(pj["nombre"], True, (255, 255, 255)), (x, 350))
        
#---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---#

    #---0--- DISEÑO DE BOTONES ---0---#
    
        #Continuar:
        pygame.draw.rect(ventana, (0, 200, 100), boton_continuar)
        ventana.blit(
            fuente.render("Continuar", True, (255, 255, 255)),
            (boton_continuar.x + 40, boton_continuar.y + 10))
        
        #Volver:
        pygame.draw.rect(ventana, (200, 50, 50), boton_volver)
        ventana.blit(fuente.render("Volver", True, (255, 255, 255)), (boton_volver.x + 20, boton_volver.y + 10))
        
    #---0--- MANEJO DE EVENTOS ---0---#
    
        #Eventos:
        for evento in pygame.event.get():
            
            #Salir:
            if evento.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
                sys.exit()
            
            #Sleccion de personajes:
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for i in personajes:
                    rect = pygame.Rect(150 + (i-1)*200, 250, 100, 100)
                    if rect.collidepoint(evento.pos):
                        personaje_seleccionado = i
            
                #Continuar:
                if boton_continuar.collidepoint(evento.pos) and input_text.strip():
                    jugador = Jugador(
                        nombre=input_text,
                        personaje_num=personaje_seleccionado,
                        sprite_path=personajes[personaje_seleccionado]["path"]
                    )
                    
                    # Aquí iría la transición al juego
                    # mostrar_pantalla_juego(ventana, jugador)
                    print(f"Jugador creado: {jugador.nombre} ({jugador.personaje_num})")
                    return
                
                #Volver al menú
                elif boton_volver.collidepoint(evento.pos):
                    return
            
            elif evento.type == pygame.KEYDOWN and input_activo:
                if evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) < 12:
                    input_text += evento.unicode
        
        # Detectar clic en input
        if pygame.mouse.get_pressed()[0]:
            input_activo = input_rect.collidepoint(pygame.mouse.get_pos())
        
        #Y lo de los FPS:
        pygame.display.update()
        reloj.tick(60)