import pygame
import sys
import os
from features.background import dibujar_background
from features.logica_background import obtener_matriz_y_posiciones
from features.vida_jugador import Vida
from features.llave_puerta import Llave, Puerta
from features.movimiento_personajes import Jugador
from features.bombas_explosion import Explosivax
from features.ambientacion import BloqueHielo, Oscuridad, Mina, ZonaVeneno
from features.enemigos import Enemigo
from features.monedas import Moneda
from features.items_powerups import ItemPowerUpManager
from screens.pantalla_final import mostrar_pantalla_final
from features.habilidades import aplicar_habilidad_personaje, Flecha

ANCHO = 416
ALTO = 480 + 50
TAM_CASILLA = 32
HUD_HEIGHT = 50
MAX_NIVELES = 4

def mostrar_texto_nivel(ventana, texto="NIVEL 1"):
    ventana.fill((0, 0, 0))
    fuente = pygame.font.SysFont("fixedsys", 36)
    render = fuente.render(texto, True, (255, 255, 255))
    rect = render.get_rect(center=(ANCHO // 2, ALTO // 2))
    ventana.blit(render, rect)
    pygame.display.flip()
    pygame.time.delay(2000)

def destruir_bloque(matriz, x, y):
    fila = y // TAM_CASILLA
    col = x // TAM_CASILLA
    if 0 <= fila < len(matriz) and 0 <= col < len(matriz[0]):
        if matriz[fila][col] == 'D':
            matriz[fila][col] = ' '
            return True, fila, col
    return False, None, None

def mostrar_pantalla_juego(VENTANA, jugador_objeto, nivel_actual=1, puntos_acumulados=0):
    fuente_chica = pygame.font.SysFont("fixedsys", 20)
    tiempo_inicio = pygame.time.get_ticks()
    puntos = puntos_acumulados

    matriz_juego, pos_llave, pos_puerta, pos_matriz_llave = obtener_matriz_y_posiciones(nivel_actual)
    fila_llave, col_llave = pos_matriz_llave
    fila_puerta, col_puerta = pos_puerta[1] // TAM_CASILLA, pos_puerta[0] // TAM_CASILLA
    puerta_visible = False

    vida = Vida(cantidad_vida=3)
    jugador = Jugador(TAM_CASILLA, TAM_CASILLA, personaje_num=jugador_objeto.personaje_num, matriz_juego=matriz_juego)
    jugador.vida = vida
    jugador.ultimo_golpe = 0

    aplicar_habilidad_personaje(jugador, jugador.personaje_num)

    jugador.bombas_disponibles = max(1, jugador.bombas_disponibles - (nivel_actual - 1))

    llave = Llave(pos_llave[0], pos_llave[1])
    puerta = Puerta(pos_puerta[0], pos_puerta[1])
    tiene_llave = False

    explosivos = Explosivax(max_bombas=jugador.bombas_disponibles)
    monedas = Moneda(matriz_juego)
    items_manager = ItemPowerUpManager(matriz_juego)

    if jugador.personaje_num == 3:
        if "flecha" not in items_manager.items_recogidos:
            items_manager.items_recogidos.append("flecha")

    bloques_hielo = BloqueHielo(matriz_juego) if nivel_actual == 1 else None
    oscuridad = Oscuridad(jugador, matriz_juego, ANCHO, ALTO) if nivel_actual == 2 else None
    minas = Mina(matriz_juego) if nivel_actual == 3 else None
    veneno = ZonaVeneno(matriz_juego) if nivel_actual == 4 else None

    enemigos = [Enemigo(160, 160), Enemigo(320, 160), Enemigo(160, 320)]

    mostrar_texto_nivel(VENTANA, f"NIVEL {nivel_actual}")

    if nivel_actual == 4:
        ruta_boss = os.path.join("assets", "sonidos", "musica_boss.mp3")
        if os.path.exists(ruta_boss):
            pygame.mixer.music.load(ruta_boss)
            pygame.mixer.music.play(-1)
    else:
        ruta_normal = os.path.join("assets", "sonidos", "musica_niveles.mp3")
        if os.path.exists(ruta_normal):
            pygame.mixer.music.load(ruta_normal)
            pygame.mixer.music.play(-1)

    flechas = []
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
                    if matriz_juego[fila][col] == " ":
                        explosivos.colocar_bomba(x_bomba, y_bomba, jugador=jugador)
                elif evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    tecla = str(evento.key - pygame.K_0)
                    tipo = jugador.items.get(tecla)
                    if tipo:
                        items_manager.usar_item(jugador, tipo, vida)
                elif evento.key == pygame.K_r:
                    if "vida" in items_manager.powerups_visibles:
                        vida.activar_powerup_vida()
                        items_manager.powerups_visibles.remove("vida")
                elif evento.key == pygame.K_t:
                    if "daño" in items_manager.powerups_visibles:
                        jugador.daño_bomba += 1
                        items_manager.powerups_visibles.remove("daño")
                elif evento.key == pygame.K_l and jugador.personaje_num == 3:
                    if jugador.flechas_disponibles > 0:
                        nueva = Flecha(jugador.rect.centerx, jugador.rect.centery, jugador.direccion, matriz_juego)
                        flechas.append(nueva)
                        jugador.flechas_disponibles -= 1
                        jugador.tiempo_ultima_flecha = pygame.time.get_ticks()
                        if jugador.flechas_disponibles == 0 and "flecha" in items_manager.items_recogidos:
                            items_manager.items_recogidos.remove("flecha")

        teclas = pygame.key.get_pressed()
        jugador.movimiento(teclas)
        jugador.actualizar_estado()
        explosivos.actualizar()

        if bloques_hielo:
            bloques_hielo.aplicar_efecto(jugador)
        if minas:
            minas.verificar_detonacion(jugador, vida)
        if veneno:
            veneno.aplicar_efecto(jugador, vida)

        items_manager.actualizar(jugador, vida)

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

        for flecha in flechas[:]:
            flecha.actualizar()
            if flecha.colisiono:
                flechas.remove(flecha)

        for bomba in explosivos.bombas:
            if bomba.exploto:
                for x_bloq, y_bloq in bomba.jugador_esta:
                    destruido, fila, col = destruir_bloque(matriz_juego, x_bloq, y_bloq)
                    if destruido:
                        if (x_bloq, y_bloq) == (col_llave * TAM_CASILLA, fila_llave * TAM_CASILLA):
                            llave.visible = True
                        if (x_bloq, y_bloq) == (col_puerta * TAM_CASILLA, fila_puerta * TAM_CASILLA):
                            puerta_visible = True
                        items_manager.liberar_objeto(col, fila)
                if bomba not in bombas_dañando:
                    jugador_centro = pygame.Rect(jugador.rect.centerx, jugador.rect.centery, 1, 1)
                    for x_exp, y_exp in bomba.jugador_esta:
                        if pygame.Rect(x_exp, y_exp, TAM_CASILLA, TAM_CASILLA).colliderect(jugador_centro):
                            if jugador.tiene_escudo:
                                jugador.tiene_escudo = False
                            else:
                                vida.perder_corazones()
                            bombas_dañando.add(bomba)
                            break

        explosivos.bombas = [
            b for b in explosivos.bombas
            if not b.exploto or pygame.time.get_ticks() - b.tiempo_explosion < b.tiempo_explota
        ]

        puntos += monedas.recoger(jugador.rect)

        if not tiene_llave and not llave.recogida and llave.visible and jugador.rect.colliderect(pygame.Rect(llave.x, llave.y, TAM_CASILLA, TAM_CASILLA)):
            tiene_llave = True
            llave.recogida = True

        if puerta_visible and jugador.rect.colliderect(pygame.Rect(puerta.x, puerta.y, TAM_CASILLA, TAM_CASILLA)):
            if tiene_llave:
                if nivel_actual < MAX_NIVELES:
                    return mostrar_pantalla_juego(VENTANA, jugador_objeto, nivel_actual + 1, puntos)
                else:
                    duracion = (pygame.time.get_ticks() - tiempo_inicio) // 1000
                    mostrar_pantalla_final(VENTANA, jugador_objeto.nombre, puntos, f"{duracion // 60}:{duracion % 60:02}", True)
                    return

        if vida.vida_actual <= 0:
            duracion = (pygame.time.get_ticks() - tiempo_inicio) // 1000
            mostrar_pantalla_final(VENTANA, jugador_objeto.nombre, puntos, f"{duracion // 60}:{duracion % 60:02}", False)
            return

        dibujar_background(VENTANA, matriz_juego, nivel=nivel_actual)
        if bloques_hielo:
            bloques_hielo.dibujar(VENTANA)
        if minas:
            minas.dibujar(VENTANA)
        if veneno:
            veneno.dibujar(VENTANA)
        monedas.dibujar(VENTANA)
        items_manager.dibujar(VENTANA)

        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)

        for flecha in flechas:
            flecha.dibujar(VENTANA)

        if not tiene_llave and not llave.recogida:
            llave.dibujar(VENTANA)
        if puerta_visible:
            puerta.activa = True
            puerta.dibujar(VENTANA)

        explosivos.dibujar(VENTANA)
        jugador.dibujar(VENTANA)

        if oscuridad:
            oscuridad.dibujar(VENTANA)

        pygame.draw.rect(VENTANA, (30, 30, 30), (0, ALTO - HUD_HEIGHT, ANCHO, HUD_HEIGHT))
        vida.visual(VENTANA, pos_x=10, pos_y=ALTO - 40)

        if tiene_llave:
            llave.dibujar_llave(VENTANA)

        tiempo_jugado = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        texto_tiempo = fuente_chica.render(f"Tiempo: {tiempo_jugado}s", True, (255, 255, 255))
        VENTANA.blit(texto_tiempo, (310, ALTO - 35))
        texto_bombas = fuente_chica.render(f"Bombas: {jugador.bombas_disponibles}", True, (255, 255, 255))
        VENTANA.blit(texto_bombas, (200, ALTO - 35))

        items_manager.mostrar_items_superiores(VENTANA, jugador, fuente_chica, ALTO)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
