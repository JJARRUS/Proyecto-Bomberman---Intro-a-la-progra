import pygame
import sys

ANCHO = 416
ALTO = 530
COLOR_FONDO = (0, 0, 0)
COLOR_TEXTO = (255, 255, 255)
TAM_FUENTE = 24

def mostrar_pantalla_mejoras(ventana, jugador):
    fuente = pygame.font.SysFont("fixedsys", TAM_FUENTE)
    opciones = ["+1 BOMBA", "+1 VELOCIDAD", "+1 VIDA"]
    seleccion = 0
    reloj = pygame.time.Clock()

    corriendo = True
    while corriendo:
        ventana.fill(COLOR_FONDO)

        texto_titulo = fuente.render("ELIGE UNA MEJORA", True, COLOR_TEXTO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, 80))
        ventana.blit(texto_titulo, rect_titulo)

        for i, texto in enumerate(opciones):
            color = (255, 255, 0) if i == seleccion else COLOR_TEXTO
            render = fuente.render(texto, True, color)
            rect = render.get_rect(center=(ANCHO // 2, 160 + i * 60))
            ventana.blit(render, rect)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    aplicar_mejora(jugador, seleccion)
                    corriendo = False

        reloj.tick(60)

def aplicar_mejora(jugador, opcion):
    if opcion == 0:  # +1 bomba
        jugador.bombas_disponibles += 1
    elif opcion == 1:  # +1 velocidad
        jugador.velocidad += 1
    elif opcion == 2:  # +1 vida
        if jugador.vida:
            jugador.vida.vida_maxima += 1
            jugador.vida.vida_actual += 1
