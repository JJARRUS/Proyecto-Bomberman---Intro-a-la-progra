from ast import main
from features.imports import *
from screens.pantalla_inicio import mostrar_pantalla_inicio
from screens.pantalla_personalizacion import mostrar_pantalla_personalizacion
from screens.pantalla_final import mostrar_pantalla_final


pygame.init() #Inicializa todo los módulos de pygame (como videos, sonidos, etc.)
ANCHO, ALTO = 800, 600 #Puede quedar a cambio despues, pues es el tamaño de la ventana

#Creamos la ventana principal del juego con sus dimenciones 
#(Es como el "ventana = tk.Tk()" para crear una ventana en tkinter)
VENTANA = pygame.display.set_mode((ANCHO,ALTO)) 
pygame.display.set_caption("VINTAGE BOMBERMAN") #Título en la barra de la ventana

def main():
     
   #Estado del jugador:
   jugador_actual = None
   
   while True:
       # Mostrar el menú pricipal
       pantalla_inicial = mostrar_pantalla_inicio(VENTANA)
       
       if pantalla_inicial == "jugar":
          
           # Mostrar pantalla de personalización
           jugador_actual = mostrar_pantalla_personalizacion(VENTANA)
           
           # Si se creó un jugador (no se presionó volver):
           if jugador_actual:  
              
               # Simulación del juego (esto se reemplazará con pantalla_juego)
               print(f"Jugador creado: {jugador_actual['nombre']}")
               print("Iniciando juego...")
               
               # Simulación de juego terminado (mostrar pantalla final)
               resultado_final = mostrar_pantalla_final(
                   VENTANA, 
                   jugador_actual['nombre'], 
                   1500,  # puntaje de ejemplo
                   "3:45",  # duración de ejemplo
                   True  # victoria de ejemplo
               )
               
               if resultado_final == "menu":
                   continue  # Volver al inicio
               elif resultado_final == "salir":
                   break
                   
       elif pantalla_inicial == "salir":
           break

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit