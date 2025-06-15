from ast import main
from features.imports import *
#TODO: from screens.pantalla_inicio import mostrar_pantalla_inicio

pygame.init() #Inicializa todo los módulos de pygame (como videos, sonidos, etc.)

ANCHO, ALTO = 800, 600 #Puede quedar a cambio despues, pues es el tamaño de la ventana

#Creamos la ventana principal del juego con sus dimenciones 
#(Es como el "ventana = tk.Tk()" para crear una ventana en tkinter)
VENTANA = pygame.display.set_mode((ANCHO,ALTO)) 
pygame.display.set_caption("VINTAGE BOMBERMAN") #Título en la barra de la ventana

#TODO:
#def main():
#   mostrar_pantalla_inicio(VENTANA)"

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit