import pygame
import sys
from features.background import dibujar_background
from features.logica_background import matriz_logica as matriz, posicion_llave_y_puerta
from features.vida_jugador import Vida
from features.llave_puerta import Llave, Puerta
from features.movimiento_personajes import Jugador
from features.bombas_explosion import Explosivax
from features.ambientacion import BloqueHielo
from features.enemigos import Enemigo
from screens.pantalla_final import mostrar_pantalla_final

ancho = 416
alto = 480 + 50
TAM_CASILLA = 32
HUD_HEIGHT = 50

def mostrar_texto_nivel(ventana, texto="NIVEL 1"):
    ventana.fill((0, 0, 0))
    fuente = pygame.font.SysFont("fixedsys", 36)
    render = fuente.render(texto, True, (255, 255, 255))
    rect = render.get_rect(center=(ancho // 2, alto // 2))
    ventana.blit(render, rect)
    pygame.display.flip()
    pygame.time.delay(2500)

def destruir_bloque(matriz, x, y):
    fila = y // TAM_CASILLA
    col = x // TAM_CASILLA
    if 0 <= fila < len(matriz) and 0 <= col < len(matriz[0]):
        if matriz[fila][col] == 'D':
            matriz[fila][col] = ' '
            return True
    return False

def mostrar_pantalla_juego(ventana, jugador_objeto):
    reloj = pygame.time.Clock()
    fuente_chica = pygame.font.SysFont("fixedsys", 20)
    tiempo_inicio = pygame.time.get_ticks()
    puntos = 0

    vida = Vida(cantidad_vida=3)
    matriz_juego = [fila.copy() for fila in matriz]
    pos_llave, pos_puerta, pos_matriz_llave = posicion_llave_y_puerta(matriz_juego)
    fila_llave, col_llave = pos_matriz_llave
    fila_puerta, col_puerta = pos_puerta[1] // TAM_CASILLA, pos_puerta[0] // TAM_CASILLA
    puerta_visible = False

    llave = Llave(pos_llave[0], pos_llave[1])
    puerta = Puerta(pos_puerta[0], pos_puerta[1])
    tiene_llave = False

    jugador = Jugador(TAM_CASILLA, TAM_CASILLA, personaje_num=jugador_objeto.personaje_num, matriz_juego=matriz_juego)
    jugador.ultimo_golpe = 0

    explosivos = Explosivax(max_bombas=3)
    bloques_hielo = BloqueHielo(matriz_juego)

    enemigos = [
        Enemigo(160, 160),
        Enemigo(320, 160),
        Enemigo(160, 320)
    ]

    mostrar_texto_nivel(ventana, "NIVEL 1")

    bombas_dañando = set()
    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_x:
                    x_bomba, y_bomba = jugador.obtener_posicion_bomba()
                    fila = y_bomba // TAM_CASILLA
                    col = x_bomba // TAM_CASILLA
                    if 0 <= fila < len(matriz_juego) and 0 <= col < len(matriz_juego[0]):
                        if matriz_juego[fila][col] == " ":
                            explosivos.colocar_bomba(x_bomba, y_bomba, jugador=jugador)

        teclas = pygame.key.get_pressed()
        jugador.movimiento(teclas)
        explosivos.actualizar()
        bloques_hielo.aplicar_efecto(jugador)

        tiempo_actual = pygame.time.get_ticks()

        for enemigo in enemigos:
            enemigo.actualizar(jugador, vida, matriz_juego, tiempo_actual, 1000)

        explosiones = []
        for bomba in explosivos.bombas:
            if bomba.exploto:
                explosiones.extend(bomba.jugador_esta)

        for enemigo in enemigos:
            if enemigo.verificar_muerte(explosiones):
                puntos += 200

        for bomba in explosivos.bombas:
            if bomba.exploto:
                coords = bomba.jugador_esta
                for x_bloq, y_bloq in coords:
                    if destruir_bloque(matriz_juego, x_bloq, y_bloq):
                        if (x_bloq, y_bloq) == (col_llave * TAM_CASILLA, fila_llave * TAM_CASILLA):
                            llave.visible = True
                        if (x_bloq, y_bloq) == (col_puerta * TAM_CASILLA, fila_puerta * TAM_CASILLA):
                            puerta_visible = True

                if bomba not in bombas_dañando:
                    jugador_centro = pygame.Rect(jugador.rect.centerx, jugador.rect.centery, 1, 1)
                    for x_exp, y_exp in coords:
                        rect_exp = pygame.Rect(x_exp, y_exp, TAM_CASILLA, TAM_CASILLA)
                        if rect_exp.colliderect(jugador_centro):
                            vida.perder_corazones()
                            bombas_dañando.add(bomba)
                            break

        explosivos.bombas = [
            b for b in explosivos.bombas
            if not b.exploto or pygame.time.get_ticks() - b.tiempo_explosion < b.tiempo_explota
        ]

        if not tiene_llave and not llave.recogida and llave.visible and jugador.rect.colliderect(pygame.Rect(llave.x, llave.y, TAM_CASILLA, TAM_CASILLA)):
            tiene_llave = True
            llave.recogida = True

        if puerta_visible and jugador.rect.colliderect(pygame.Rect(puerta.x, puerta.y, TAM_CASILLA, TAM_CASILLA)):
            if tiene_llave:
                duracion = (pygame.time.get_ticks() - tiempo_inicio) // 1000
                minutos = duracion // 60
                segundos = duracion % 60
                duracion_texto = f"{minutos}:{segundos:02}"
                mostrar_pantalla_final(ventana, jugador_objeto.nombre, puntos, duracion_texto, True)
                return

        if vida.vida_actual <= 0:
            duracion = (pygame.time.get_ticks() - tiempo_inicio) // 1000
            minutos = duracion // 60
            segundos = duracion % 60
            duracion_texto = f"{minutos}:{segundos:02}"
            mostrar_pantalla_final(ventana, jugador_objeto.nombre, puntos, duracion_texto, False)
            return

        ventana.fill((0, 0, 0))
        dibujar_background(ventana, matriz_juego)
        bloques_hielo.dibujar(ventana)

        for enemigo in enemigos:
            enemigo.dibujar(ventana)

        if not tiene_llave and not llave.recogida:
            llave.dibujar(ventana)

        if puerta_visible:
            puerta.activa = True
            puerta.dibujar(ventana)

        explosivos.dibujar(ventana)
        jugador.dibujar(ventana)

        pygame.draw.rect(ventana, (30, 30, 30), (0, alto - HUD_HEIGHT, ancho, HUD_HEIGHT))
        vida.visual(ventana, pos_x=10, pos_y=alto - 40)

        if tiene_llave:
            llave.dibujar_llave(ventana)

        tiempo_jugado = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        texto_tiempo = fuente_chica.render(f"Tiempo: {tiempo_jugado}s", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (310, alto - 35))
        texto_bombas = fuente_chica.render(f"Bombas: {jugador.bombas_disponibles}", True, (255, 255, 255))
        ventana.blit(texto_bombas, (200, alto - 35))

        pygame.display.flip()
        reloj.tick(60)
