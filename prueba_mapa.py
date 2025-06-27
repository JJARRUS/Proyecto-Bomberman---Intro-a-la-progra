import pygame
import sys
from features.background import dibujar_background
from features.logica_background import obtener_matriz_y_posiciones
from features.vida_jugador import Vida
from features.llave_puerta import Llave, Puerta
from features.movimiento_personajes import Jugador
from features.bombas_explosion import Explosivax
from features.ambientacion import BloqueHielo, Oscuridad, Mina, ZonaVeneno
from features.items_powerups import ItemPowerUpManager
from features.habilidades import Flecha, aplicar_habilidad_personaje
from screens.pantalla_final import mostrar_pantalla_final

ancho = 416
alto = 480 + 50
TAM_CASILLA = 32
HUD_HEIGHT = 50

def destruir_bloque(matriz, x, y):
    fila = y // TAM_CASILLA
    col = x // TAM_CASILLA
    if 0 <= fila < len(matriz) and 0 <= col < len(matriz[0]):
        if matriz[fila][col] == 'D':
            matriz[fila][col] = ' '
            return True
    return False

def texto_nivel(ventana, nivel):
    fuente = pygame.font.SysFont("fixedsys", 36)
    texto = fuente.render("NIVEL " + str(nivel), True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
    ventana.blit(texto, texto_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

def jugar_nivel(ventana, nivel, vida):
    vida.reiniciar()

    matriz_juego, pos_llave, pos_puerta, pos_matriz_llave = obtener_matriz_y_posiciones(nivel)
    fila_llave, col_llave = pos_matriz_llave

    llave = Llave(pos_llave[0], pos_llave[1])
    puerta = Puerta(pos_puerta[0], pos_puerta[1])
    tiene_llave = False

    jugador = Jugador(TAM_CASILLA, TAM_CASILLA, personaje_num=vida.personaje, matriz_juego=matriz_juego)
    jugador.vida_objeto = vida
    jugador.items = []
    jugador.daño_bomba = 2
    jugador.tiene_escudo = False
    jugador.velocidad_original = jugador.velocidad
    jugador.velocidad_timer = 0
    jugador.escudo_timer = 0

    aplicar_habilidad_personaje(jugador, jugador.personaje_num)
    if jugador.personaje_num == 3:
        jugador.tiempo_ultima_flecha = pygame.time.get_ticks()
        jugador.flechas_disponibles = 2

    explosivos = Explosivax(max_bombas=jugador.bombas_disponibles)
    bloques_hielo = BloqueHielo(matriz_juego) if nivel == 1 else None
    oscuridad = Oscuridad(jugador, matriz_juego, ancho, alto) if nivel == 2 else None
    minas = Mina(matriz_juego) if nivel == 3 else None
    veneno = ZonaVeneno(matriz_juego) if nivel == 4 else None
    items_manager = ItemPowerUpManager(matriz_juego)

    if jugador.personaje_num == 3:
        items_manager.items_recogidos.append("flecha")

    flechas = []
    texto_nivel(ventana, nivel)

    fuente_chica = pygame.font.SysFont("fixedsys", 20)
    tiempo_inicio = pygame.time.get_ticks()
    reloj = pygame.time.Clock()
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
                    explosivos.colocar_bomba(x_bomba, y_bomba, jugador=jugador)
                elif evento.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    indice = evento.key - pygame.K_1
                    if indice < len(jugador.items):
                        tipo = jugador.items[indice]
                        jugador.usar_item(tipo)
                elif evento.key == pygame.K_l and jugador.personaje_num == 3:
                    if jugador.flechas_disponibles > 0:
                        x, y = jugador.rect.center
                        nueva = Flecha(x, y, jugador.direccion, matriz_juego)
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

        for flecha in flechas[:]:
            flecha.actualizar()
            if flecha.colisiono:
                flechas.remove(flecha)

        if items_manager.recogio_powerup_vida:
            items_manager.recogio_powerup_vida = False

        for bomba in explosivos.bombas:
            if bomba.exploto:
                coords = bomba.jugador_esta
                for x_bloq, y_bloq in coords:
                    if destruir_bloque(matriz_juego, x_bloq, y_bloq):
                        if (x_bloq, y_bloq) == (col_llave * TAM_CASILLA, fila_llave * TAM_CASILLA):
                            llave.visible = True
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

        explosivos.bombas = [
            b for b in explosivos.bombas
            if not b.exploto or pygame.time.get_ticks() - b.tiempo_explosion < b.tiempo_explota
        ]

        if not tiene_llave and not llave.recogida and llave.visible and jugador.rect.colliderect(pygame.Rect(llave.x, llave.y, TAM_CASILLA, TAM_CASILLA)):
            tiene_llave = True
            llave.recogida = True

        if jugador.rect.colliderect(pygame.Rect(puerta.x, puerta.y, TAM_CASILLA, TAM_CASILLA)) and tiene_llave:
            return True

        # DERROTA: sin vida o sin bombas
        if vida.vida_actual == 0 and not vida.powerup_activo and not jugador.tiene_escudo:
            mostrar_pantalla_final(ventana, "Jugador", 0, "0:00", victoria=False)
            return False

        if jugador.bombas_disponibles == 0 and not any(not b.exploto for b in explosivos.bombas):
            mostrar_pantalla_final(ventana, "Jugador", 0, "0:00", victoria=False)
            return False

        ventana.fill((0, 0, 0))
        dibujar_background(ventana, matriz_juego)
        if bloques_hielo:
            bloques_hielo.dibujar(ventana)
        if minas:
            minas.dibujar(ventana)
        if veneno:
            veneno.dibujar(ventana)
        items_manager.dibujar(ventana)
        for flecha in flechas:
            flecha.dibujar(ventana)
        if not tiene_llave and not llave.recogida:
            llave.dibujar(ventana)
        puerta.activa = True
        puerta.dibujar(ventana)
        explosivos.dibujar(ventana)
        jugador.dibujar(ventana)
        if oscuridad:
            oscuridad.dibujar(ventana)

        pygame.draw.rect(ventana, (30, 30, 30), (0, alto - HUD_HEIGHT, ancho, HUD_HEIGHT))
        vida.visual(ventana, pos_x=10, pos_y=alto - 40)
        if tiene_llave:
            llave.dibujar_llave(ventana)

        tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        texto_tiempo = fuente_chica.render("Tiempo: " + str(tiempo_actual) + "s", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (310, alto - 35))
        texto_bombas = fuente_chica.render("Bombas: " + str(jugador.bombas_disponibles), True, (255, 255, 255))
        ventana.blit(texto_bombas, (200, alto - 35))

        items_manager.mostrar_items_superiores(ventana, jugador, fuente_chica, alto)
        pygame.display.flip()
        reloj.tick(60)

    return False

def main():
    pygame.init()
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Prueba del mapa")
    vida = Vida(cantidad_vida=3)
    vida.personaje = 2  # Cambiar según personaje: 1, 2, 3

    nivel_actual = 1
    total_niveles = 4

    while nivel_actual <= total_niveles:
        completado = jugar_nivel(ventana, nivel_actual, vida)
        if not completado:
            break
        nivel_actual += 1
        vida.disminuir_vida_maxima()

    mostrar_pantalla_final(ventana, "Jugador", 999, "2:00", victoria=True)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
