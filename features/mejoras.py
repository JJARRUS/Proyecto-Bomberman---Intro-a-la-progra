import pygame
import sys

ANCHO = 416
ALTO = 530
COLOR_FONDO = (0, 0, 0)
COLOR_TEXTO = (255, 255, 255)
TAM_FUENTE = 24

def mostrar_pantalla_mejoras(ventana, jugador, puntos):
    pygame.font.init()
    fuente = pygame.font.SysFont("fixedsys", TAM_FUENTE)

    opciones = [
        {"texto": "+1 BOMBA", "costo": 200, "clave": "bomba"},
        {"texto": "+1 VELOCIDAD (1 min)", "costo": 300, "clave": "velocidad"},
        {"texto": "+1 VIDA", "costo": 500, "clave": "vida"}
    ]

    seleccion = 0
    reloj = pygame.time.Clock()

    disponibles = [opt for opt in opciones if puntos >= opt["costo"]]
    if not disponibles:
        disponibles = [{"texto": "Siguiente nivel", "costo": 0, "clave": None}]

    corriendo = True
    while corriendo:
        ventana.fill(COLOR_FONDO)

        titulo = fuente.render("ELIGE UNA MEJORA", True, COLOR_TEXTO)
        rect_titulo = titulo.get_rect(center=(ANCHO // 2, 60))
        ventana.blit(titulo, rect_titulo)

        puntos_txt = fuente.render(f"Puntos: {puntos}", True, COLOR_TEXTO)
        ventana.blit(puntos_txt, (20, 20))

        for i, opcion in enumerate(disponibles):
            color = (255, 255, 0) if i == seleccion else COLOR_TEXTO
            texto = f"{opcion['texto']} - {opcion['costo']} pts" if opcion["clave"] else opcion["texto"]
            render = fuente.render(texto, True, color)
            rect = render.get_rect(center=(ANCHO // 2, 140 + i * 60))
            ventana.blit(render, rect)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(disponibles)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(disponibles)
                elif evento.key == pygame.K_RETURN:
                    seleccionada = disponibles[seleccion]
                    if seleccionada["clave"]:
                        aplicar_mejora(jugador, seleccionada["clave"])
                        return seleccionada["costo"]
                    else:
                        return 0

        reloj.tick(60)

def aplicar_mejora(jugador, clave):
    if clave == "bomba":
        jugador.bombas_disponibles += 1
    elif clave == "velocidad":
        jugador.velocidad += 1
        jugador.velocidad_temporal = True
        jugador.tiempo_velocidad = pygame.time.get_ticks()
    elif clave == "vida":
        if hasattr(jugador, "vida") and jugador.vida:
            jugador.vida.vida_maxima += 1
            jugador.vida.vida_actual += 1
