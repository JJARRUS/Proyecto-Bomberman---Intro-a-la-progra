import pygame
import sys
from features.background import dibujar_background
from features.logica_background import matriz_logica as matriz, posicion_llave_y_puerta
from features.vida_jugador import Vida
from features.llave_puerta import Llave, Puerta
from features.movimiento_personajes import Jugador
from features.bombas_explosion import Explosivox

ancho = 416  
alto = 480 + 50  
TAM_CASILLA = 32
HUD_HEIGHT = 50

def destruir_bloque(matriz, x, y):
    fila = y // TAM_CASILLA
    col = x // TAM_CASILLA
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
    llave = Llave(pos_llave[0], pos_llave[1])
    puerta = Puerta(pos_puerta[0], pos_puerta[1])
    tiene_llave = False
    jugador = Jugador(TAM_CASILLA, TAM_CASILLA, personaje_num=1)
    Explosivox = Explosivox(max_bombas=3)
    texto_nivel(ventana, 1)
    bombas_dañando = set()  

    caminando = True
    while caminando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                caminando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_x:
                    x_bomba, y_bomba = jugador.obtener_posicion_bomba()
                    Explosivox.colocar_bomba(x_bomba, y_bomba)

        teclas = pygame.key.get_pressed()
        jugador.movimiento(teclas)
        Explosivox.actualizar()

        for bomba in Explosivox.bombas:
            if bomba.exploto:
                coords = [
                    (bomba.x, bomba.y),
                    (bomba.x + TAM_CASILLA, bomba.y),
                    (bomba.x - TAM_CASILLA, bomba.y),
                    (bomba.x, bomba.y + TAM_CASILLA),
                    (bomba.x, bomba.y - TAM_CASILLA),
                ]
                for x_bloq, y_bloq in coords:
                    if destruir_bloque(matriz_juego, x_bloq, y_bloq):
                        fila, col = pos_matriz_llave
                        if x_bloq == col * TAM_CASILLA and y_bloq == fila * TAM_CASILLA:
                            llave.recogida = False

                if bomba not in bombas_dañando:
                    jugador_centro = jugador.rect.center
                    for x_exp, y_exp in coords:
                        rect_exp = pygame.Rect(x_exp, y_exp, TAM_CASILLA, TAM_CASILLA)
                        if rect_exp.collidepoint(jugador_centro):
                            vida.perder_corazones()
                            print("💥 ¡Te alcanzó la explosión! -1 vida")
                            bombas_dañando.add(bomba)
                            break

        Explosivox.bombas = [b for b in Explosivox.bombas if not b.exploto]

        if not tiene_llave and not llave.recogida and jugador.rect.colliderect(pygame.Rect(llave.x, llave.y, TAM_CASILLA, TAM_CASILLA)):
            tiene_llave = True
            llave.recogida = True
            print("¡Has recogido la llave!")

        if jugador.rect.colliderect(pygame.Rect(puerta.x, puerta.y, TAM_CASILLA, TAM_CASILLA)):
            if tiene_llave:
                print("¡Has abierto la puerta y pasado al siguiente nivel!")
                caminando = False
            else:
                print("Necesitas la llave para abrir la puerta.")

        ventana.fill((0, 0, 0))
        dibujar_background(ventana, matriz_juego)

        if not tiene_llave and not llave.recogida:
            llave.dibujar(ventana)

        puerta.activa = True
        puerta.dibujar(ventana)
        Explosivox.dibujar(ventana)
        jugador.dibujar(ventana)

        pygame.draw.rect(ventana, (30, 30, 30), (0, alto - HUD_HEIGHT, ancho, HUD_HEIGHT))
        vida.visual(ventana, pos_x=10, pos_y=alto - 40)

        if tiene_llave:
            img_llave = pygame.transform.scale(pygame.image.load("assets/items/llave.png"), (32, 32))
            ventana.blit(img_llave, (120, alto - 40))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
