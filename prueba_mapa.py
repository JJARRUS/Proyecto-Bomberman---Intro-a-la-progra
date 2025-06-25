# prueba_mapa.py

import pygame
import sys
from features.background import dibujar_background
from features.logica_background import matriz_logica as matriz, posicion_llave_y_puerta
from features.vida_jugador import Vida
from features.llave_puerta import Llave, Puerta
from features.movimiento_personajes import Jugador
from features.bombas_explosion import Explosivax

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

def main():
    pygame.init()
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Prueba del mapa")
    reloj = pygame.time.Clock()

    vida = Vida(cantidad_vida=3)
    matriz_juego = [fila.copy() for fila in matriz]

    pos_llave, pos_puerta, pos_matriz_llave = posicion_llave_y_puerta(matriz_juego)
    fila_llave, col_llave = pos_matriz_llave

    llave = Llave(pos_llave[0], pos_llave[1])
    puerta = Puerta(pos_puerta[0], pos_puerta[1])
    tiene_llave = False

    jugador = Jugador(TAM_CASILLA, TAM_CASILLA, personaje_num=1, matriz_juego=matriz_juego)
    explosivos = Explosivax(max_bombas=3)

    texto_nivel(ventana, 1)

    bombas_dañando = set()
    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_x:
                    x_bomba, y_bomba = jugador.obtener_posicion_bomba()
                    explosivos.colocar_bomba(x_bomba, y_bomba)

        teclas = pygame.key.get_pressed()
        jugador.movimiento(teclas)
        explosivos.actualizar()

        for bomba in explosivos.bombas:
            if bomba.exploto:
                coords = bomba.jugador_esta
                for x_bloq, y_bloq in coords:
                    if destruir_bloque(matriz_juego, x_bloq, y_bloq):
                        # Si se destruyó el bloque que ocultaba la llave
                        if (x_bloq, y_bloq) == (col_llave * TAM_CASILLA, fila_llave * TAM_CASILLA):
                            llave.visible = True

                if bomba not in bombas_dañando:
                    jugador_centro = jugador.rect.center
                    for x_exp, y_exp in coords:
                        rect_exp = pygame.Rect(x_exp, y_exp, TAM_CASILLA, TAM_CASILLA)
                        if rect_exp.collidepoint(jugador_centro):
                            vida.perder_corazones()
                            print("Menos vida")
                            bombas_dañando.add(bomba)
                            break

        explosivos.bombas = [b for b in explosivos.bombas if not b.exploto or pygame.time.get_ticks() - b.tiempo_explosion < b.tiempo_explota]

        # Recoger llave
        if not tiene_llave and not llave.recogida and llave.visible and jugador.rect.colliderect(pygame.Rect(llave.x, llave.y, TAM_CASILLA, TAM_CASILLA)):
            tiene_llave = True
            llave.recogida = True
            print("LLave")

        # Activar puerta
        if jugador.rect.colliderect(pygame.Rect(puerta.x, puerta.y, TAM_CASILLA, TAM_CASILLA)):
            if tiene_llave:
                print("Puerta")
                corriendo = False
            else:
                print("Necesitas llave")

        # Dibujo
        ventana.fill((0, 0, 0))
        dibujar_background(ventana, matriz_juego)

        if not tiene_llave and not llave.recogida:
            llave.dibujar(ventana)

        puerta.activa = True
        puerta.dibujar(ventana)
        explosivos.dibujar(ventana)
        jugador.dibujar(ventana)

        pygame.draw.rect(ventana, (30, 30, 30), (0, alto - HUD_HEIGHT, ancho, HUD_HEIGHT))
        vida.visual(ventana, pos_x=10, pos_y=alto - 40)

        if tiene_llave:
            llave.dibujar_llave(ventana)  # Se dibuja la llave junto a los corazones

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
