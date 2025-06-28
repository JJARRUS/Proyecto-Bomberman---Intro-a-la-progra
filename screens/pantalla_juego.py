import pygame
import sys
import os
import random
from features.background import dibujar_background
from features.logica_background import obtener_matriz_y_posiciones
from features.vida_jugador import Vida
from features.llave_puerta import Llave, Puerta
from features.movimiento_personajes import Jugador
from features.bombas_explosion import Explosivax
from features.ambientacion import BloqueHielo, Oscuridad, Mina, ZonaVeneno
from features.enemigos import Enemigo, obtener_posiciones_spawn
from features.monedas import Moneda
from features.items_powerups import ItemPowerUpManager
from features.habilidades import aplicar_habilidad_personaje, Flecha
from screens.pantalla_final import mostrar_pantalla_final

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

def obtener_spawn_boss(matriz):
    opciones = []
    for fila in range(1, len(matriz)-1):
        for col in range(1, len(matriz[0])-1):
            if (matriz[fila][col] == " " and matriz[fila+1][col] == " " and
                matriz[fila][col+1] == " " and matriz[fila+1][col+1] == " "):
                opciones.append((col * TAM_CASILLA, fila * TAM_CASILLA))
    if not opciones:
        return (TAM_CASILLA * (len(matriz[0])//2), TAM_CASILLA * (len(matriz)//2))
    return random.choice(opciones)

def mostrar_pantalla_juego(VENTANA, jugador_objeto, nivel_actual=1, puntos_acumulados=0):
    fuente_chica = pygame.font.SysFont("fixedsys", 20)
    tiempo_inicio = pygame.time.get_ticks()
    puntos = puntos_acumulados

    matriz_juego, pos_llave, pos_puerta, pos_matriz_llave = obtener_matriz_y_posiciones(nivel_actual)
    fila_llave, col_llave = pos_matriz_llave
    col_puerta = pos_puerta[0] // TAM_CASILLA
    fila_puerta = pos_puerta[1] // TAM_CASILLA
    puerta_visible = False

    vida = Vida(cantidad_vida=3)
    llave = Llave(pos_llave[0], pos_llave[1])
    puerta = Puerta(pos_puerta[0], pos_puerta[1])
    tiene_llave = False

    jugador = Jugador(TAM_CASILLA, TAM_CASILLA, personaje_num=jugador_objeto.personaje_num, matriz_juego=matriz_juego)
    jugador.vida = vida
    jugador.ultimo_golpe = 0

    # Habilidad individual del personaje
    aplicar_habilidad_personaje(jugador, jugador.personaje_num)

    explosivos = Explosivax(max_bombas=3)
    monedas = Moneda(matriz_juego)
    items_manager = ItemPowerUpManager(matriz_juego)

    # --- Ambientaciones ---
    bloques_hielo = minas = veneno = oscuridad = None
    if nivel_actual == 1:
        bloques_hielo = BloqueHielo(matriz_juego)
    elif nivel_actual == 2:
        oscuridad = Oscuridad(jugador, matriz_juego, ANCHO, ALTO)
    elif nivel_actual == 3:
        minas = Mina(matriz_juego)
    elif nivel_actual == 4:
        veneno = ZonaVeneno(matriz_juego)

    jugador_spawn = (1, 1)
    llave_spawn = (col_llave, fila_llave)
    puerta_spawn = (col_puerta, fila_puerta)
    posiciones_prohibidas = {jugador_spawn, llave_spawn, puerta_spawn}

    jefe_muerto = False

    # --- SPAWN ENEMIGOS POR NIVEL ---
    if nivel_actual == 4:
        cantidad_enemigos = 3
        spawns = obtener_posiciones_spawn(matriz_juego, cantidad_enemigos-1, posiciones_prohibidas=posiciones_prohibidas)
        boss_spawn = obtener_spawn_boss(matriz_juego)
        enemigos = [
            Enemigo(spawns[0][0], spawns[0][1], tipo="flechas"),
            Enemigo(spawns[1][0], spawns[1][1], tipo="flechas"),
            Enemigo(boss_spawn[0], boss_spawn[1], tipo="boss"),
        ]
    elif nivel_actual == 3:
        cantidad_enemigos = 5
        spawns = obtener_posiciones_spawn(matriz_juego, cantidad_enemigos, posiciones_prohibidas=posiciones_prohibidas)
        enemigos = [
            Enemigo(spawns[0][0], spawns[0][1], tipo="normal"),
            Enemigo(spawns[1][0], spawns[1][1], tipo="normal"),
            Enemigo(spawns[2][0], spawns[2][1], tipo="veloz"),
            Enemigo(spawns[3][0], spawns[3][1], tipo="flechas"),
            Enemigo(spawns[4][0], spawns[4][1], tipo="flechas"),
        ]
    elif nivel_actual == 2:
        cantidad_enemigos = 4
        spawns = obtener_posiciones_spawn(matriz_juego, cantidad_enemigos, posiciones_prohibidas=posiciones_prohibidas)
        enemigos = [
            Enemigo(spawns[0][0], spawns[0][1], tipo="normal"),
            Enemigo(spawns[1][0], spawns[1][1], tipo="normal"),
            Enemigo(spawns[2][0], spawns[2][1], tipo="veloz"),
            Enemigo(spawns[3][0], spawns[3][1], tipo="veloz"),
        ]
    else:
        cantidad_enemigos = 3
        spawns = obtener_posiciones_spawn(matriz_juego, cantidad_enemigos, posiciones_prohibidas=posiciones_prohibidas)
        enemigos = [
            Enemigo(spawns[0][0], spawns[0][1], tipo="normal"),
            Enemigo(spawns[1][0], spawns[1][1], tipo="normal"),
            Enemigo(spawns[2][0], spawns[2][1], tipo="normal"),
        ]

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

    bombas_dañando = set()
    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                # Colocar bomba
                if evento.key == pygame.K_x:
                    x_bomba, y_bomba = jugador.obtener_posicion_bomba()
                    fila = y_bomba // TAM_CASILLA
                    col = x_bomba // TAM_CASILLA
                    if 0 <= fila < len(matriz_juego) and 0 <= col < len(matriz_juego[0]):
                        if matriz_juego[fila][col] == " ":
                            explosivos.colocar_bomba(x_bomba, y_bomba, jugador=jugador)
                # Usar ítems con teclas 1 a 3
                elif evento.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    tecla = str(evento.key - pygame.K_0)
                    tipo = jugador.items.get(tecla)
                    if tipo:
                        items_manager.usar_item(jugador, tipo, vida)
                # PU de vida: R
                elif evento.key == pygame.K_r:
                    if items_manager.pu_vida_recogido and not vida.powerup_activo:
                        vida.ganar_vida()
                        items_manager.pu_vida_recogido = False
                # PU de daño: T
                elif evento.key == pygame.K_t:
                    if items_manager.pu_daño_recogido:
                        jugador.daño_bomba += 1
                        items_manager.pu_daño_recogido = False
                # Disparar flecha (solo The Chosen One, con F)
                elif evento.key == pygame.K_f and jugador.personaje_num == 3:
                    tiempo_actual = pygame.time.get_ticks()
                    if hasattr(jugador, "flechas_disponibles") and jugador.flechas_disponibles > 0:
                        if tiempo_actual - getattr(jugador, "tiempo_ultima_flecha", 0) >= getattr(jugador, "cooldown_flecha", 2000):
                            flecha = Flecha(jugador.rect.centerx, jugador.rect.centery, jugador.direccion if jugador.direccion != "parado" else "abajo")
                            jugador.flechas.append(flecha)
                            jugador.flechas_disponibles -= 1
                            jugador.tiempo_ultima_flecha = tiempo_actual

        teclas = pygame.key.get_pressed()
        jugador.movimiento(teclas)
        jugador.actualizar_estado()
        explosivos.actualizar()

        # ----------- DIBUJADO DEL FONDO Y OSCURIDAD ------------
        dibujar_background(VENTANA, matriz_juego, nivel=nivel_actual)
        if oscuridad:
            oscuridad.dibujar(VENTANA)
        # -------------------------------------------------------

        if bloques_hielo:
            bloques_hielo.aplicar_efecto(jugador)
        if minas:
            minas.verificar_detonacion(jugador, vida)
        if veneno:
            veneno.aplicar_efecto(jugador, vida)

        items_manager.actualizar(jugador, vida)
        tiempo_actual = pygame.time.get_ticks()

        # Enemigos y flechas enemigas
        for enemigo in enemigos:
            enemigo.actualizar(jugador, vida, matriz_juego, tiempo_actual, 1000)

        # Flechas de enemigos dañan al jugador
        for enemigo in enemigos:
            if hasattr(enemigo, "flechas"):
                for flecha in enemigo.flechas[:]:
                    if flecha.rect.colliderect(jugador.rect):
                        if jugador.tiene_escudo:
                            jugador.tiene_escudo = False
                        elif vida.powerup_activo:
                            vida.powerup_activo = False
                        else:
                            vida.perder_corazones()
                        enemigo.flechas.remove(flecha)

        # Flechas del jugador (The Chosen One) - FIX: ignora None
        if jugador.personaje_num == 3 and hasattr(jugador, "flechas"):
            for flecha in [f for f in jugador.flechas if f is not None]:
                flecha.mover()
                fila = flecha.rect.centery // TAM_CASILLA
                col = flecha.rect.centerx // TAM_CASILLA
                fuera_mapa = (
                    fila < 0 or fila >= len(matriz_juego) or
                    col < 0 or col >= len(matriz_juego[0])
                )
                # Colisión con bloques destructibles
                if not fuera_mapa and matriz_juego[fila][col] == "D":
                    matriz_juego[fila][col] = " "
                    jugador.flechas.remove(flecha)
                # Colisión con bloques indestructibles o fuera del mapa
                elif fuera_mapa or (not fuera_mapa and matriz_juego[fila][col] == "I"):
                    jugador.flechas.remove(flecha)

        explosiones = []
        for bomba in explosivos.bombas:
            if bomba.exploto:
                explosiones.extend(bomba.jugador_esta)

        for enemigo in enemigos:
            if enemigo.verificar_muerte(explosiones):
                puntos += 200
                if hasattr(enemigo, "is_boss") and enemigo.is_boss:
                    jefe_muerto = True

        for bomba in explosivos.bombas:
            if bomba.exploto:
                coords = bomba.jugador_esta
                for x_bloq, y_bloq in coords:
                    destruido, fila, col = destruir_bloque(matriz_juego, x_bloq, y_bloq)
                    if destruido:
                        puntos += 10
                        if (x_bloq, y_bloq) == (col_llave * TAM_CASILLA, fila_llave * TAM_CASILLA):
                            llave.visible = True
                        if (x_bloq, y_bloq) == (col_puerta * TAM_CASILLA, fila_puerta * TAM_CASILLA):
                            puerta_visible = True
                        items_manager.liberar_objeto(col, fila)

                if bomba not in bombas_dañando:
                    jugador_centro = pygame.Rect(jugador.rect.centerx, jugador.rect.centery, 1, 1)
                    for x_exp, y_exp in coords:
                        rect_exp = pygame.Rect(x_exp, y_exp, TAM_CASILLA, TAM_CASILLA)
                        if rect_exp.colliderect(jugador_centro):
                            if jugador.tiene_escudo:
                                jugador.tiene_escudo = False
                            elif vida.powerup_activo:
                                vida.powerup_activo = False
                            else:
                                vida.perder_corazones()
                            bombas_dañando.add(bomba)
                            break

        explosivos.bombas = [b for b in explosivos.bombas if not b.exploto or pygame.time.get_ticks() - b.tiempo_explosion < b.tiempo_explota]

        puntos += monedas.recoger(jugador.rect)

        # Llave solo aparece tras jefe muerto en nivel 4
        if nivel_actual == 4 and not tiene_llave and not llave.recogida:
            if jefe_muerto:
                llave.visible = True

        if not tiene_llave and not llave.recogida and llave.visible and jugador.rect.colliderect(pygame.Rect(llave.x, llave.y, TAM_CASILLA, TAM_CASILLA)):
            tiene_llave = True
            llave.recogida = True
            puntos += 100

        if puerta_visible and jugador.rect.colliderect(pygame.Rect(puerta.x, puerta.y, TAM_CASILLA, TAM_CASILLA)):
            if tiene_llave:
                if nivel_actual < MAX_NIVELES:
                    mostrar_texto_nivel(VENTANA, f"NIVEL {nivel_actual + 1}")
                    return mostrar_pantalla_juego(VENTANA, jugador_objeto, nivel_actual + 1, puntos)
                else:
                    duracion = (pygame.time.get_ticks() - tiempo_inicio) // 1000
                    minutos = duracion // 60
                    segundos = duracion % 60
                    duracion_texto = f"{minutos}:{segundos:02}"
                    mostrar_pantalla_final(VENTANA, jugador_objeto.nombre, puntos, duracion_texto, True)
                    return

        if vida.vida_actual <= 0:
            duracion = (pygame.time.get_ticks() - tiempo_inicio) // 1000
            minutos = duracion // 60
            segundos = duracion % 60
            duracion_texto = f"{minutos}:{segundos:02}"
            mostrar_pantalla_final(VENTANA, jugador_objeto.nombre, puntos, duracion_texto, False)
            return

        # -------- DIBUJADO RESTANTE --------
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
            if hasattr(enemigo, "flechas"):
                for flecha in enemigo.flechas:
                    VENTANA.blit(flecha.image, flecha.rect)

        # Flechas del jugador (The Chosen One) - FIX: ignora None
        if jugador.personaje_num == 3 and hasattr(jugador, "flechas"):
            for flecha in [f for f in jugador.flechas if f is not None]:
                VENTANA.blit(flecha.image, flecha.rect)

        if (nivel_actual < 4 or jefe_muerto) and not tiene_llave and not llave.recogida and llave.visible:
            llave.dibujar(VENTANA)

        if puerta_visible:
            puerta.activa = True
            puerta.dibujar(VENTANA)

        explosivos.dibujar(VENTANA)
        jugador.dibujar(VENTANA)

        pygame.draw.rect(VENTANA, (30, 30, 30), (0, ALTO - HUD_HEIGHT, ANCHO, HUD_HEIGHT))
        vida.visual(VENTANA, pos_x=10, pos_y=ALTO - 40)
        if tiene_llave:
            llave.dibujar_llave(VENTANA)

        tiempo_jugado = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        texto_tiempo = fuente_chica.render(f"Tiempo: {tiempo_jugado}s", True, (255, 255, 255))
        VENTANA.blit(texto_tiempo, (310, ALTO - 35))
        texto_bombas = fuente_chica.render(f"Bombas: {jugador.bombas_disponibles}", True, (255, 255, 255))
        VENTANA.blit(texto_bombas, (200, ALTO - 35))
        texto_puntos = fuente_chica.render(f"Puntos: {puntos}", True, (255, 215, 0))
        VENTANA.blit(texto_puntos, (30, ALTO - 75))

        items_manager.mostrar_items_superiores(VENTANA, jugador, fuente_chica, ALTO)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
