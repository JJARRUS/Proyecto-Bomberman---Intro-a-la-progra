from features.imports import *
from features.config import cargar_musica, musica_activada
from screens.pantalla_inicio import mostrar_pantalla_inicio
from screens.pantalla_personalizacion import mostrar_pantalla_personalizacion
from screens.pantalla_final import mostrar_pantalla_final
from screens.pantalla_configuracion import mostrar_pantalla_configuracion

#--- TAMAÑOS DE VENTANA ---#
ANCHO, ALTO = 800, 600 

#--- CREACIÓN DE VENTANA ---#
VENTANA = None

#---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---#

#Función principal del programa:
def main():

   #--- Manejo de audio en la pantalla de inicio ---#
   global VENTANA

   pygame.init() #Inicializa todo los módulos de pygame (como videos, sonidos, etc.)
   
   # No cerramos el mixer aquí, solo lo inicializamos si no está activo
   if not pygame.mixer.get_init():
       pygame.mixer.init()

   VENTANA = pygame.display.set_mode((ANCHO, ALTO))
   pygame.display.set_caption("VINTAGE BOMBERMAN") #Título en la barra de la ventana

   #Música para el menú:
   if musica_activada:
       cargar_musica()

#---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---#

   #--- Manejo de la ventana principal ---#
   while True:
      try:
         # Mostrar el menú principal
         opcion = mostrar_pantalla_inicio(VENTANA)

         #--- OPCIÓN JUGAR ---#
         if opcion == "jugar":
            #Al precionar jugar, dirigir a la pantalla personalización:
            jugador_actual = mostrar_pantalla_personalizacion(VENTANA)

            # Si se creó un jugador (y no se presionó volver):
            if jugador_actual:  

               # TODO: Simulación del juego (esto se reemplazará con pantalla_juego)
               print(f"Jugador creado: {jugador_actual['nombre']}")

               # Simulación de juego terminado (mostrar pantalla final)
               resultado_final = mostrar_pantalla_final(VENTANA, jugador_actual['nombre'], 1500, "3:45", True)
               if resultado_final == "salir":
                  break

         #--- OPCIÓN CONFIGURACIÓN ---#
         elif opcion == "configuracion":
            # Cerrar la ventana de pygame temporalmente
            pygame.display.quit()
            
            # Mostrar pantalla de configuración
            mostrar_pantalla_configuracion()
            
            # Recrear la ventana de pygame
            VENTANA = pygame.display.set_mode((ANCHO, ALTO))
            pygame.display.set_caption("VINTAGE BOMBERMAN")
            
            # Recargar música si está activada
            if musica_activada:
                cargar_musica()

         #--- OPCIÓN INFORMACIÓN ---#
         elif opcion == "informacion":
            # Cerrar la ventana de pygame temporalmente
            pygame.display.quit()
            
            # Mostrar pantalla de información
            from screens.pantalla_informacion import PantallaInformacion
            ventana_info = tk.Tk()
            app_info = PantallaInformacion(ventana_info)
            ventana_info.mainloop()
            
            # Recrear la ventana de pygame
            VENTANA = pygame.display.set_mode((ANCHO, ALTO))
            pygame.display.set_caption("VINTAGE BOMBERMAN")
            
            # Recargar música si está activada
            if musica_activada:
                cargar_musica()

         #OPCIÓN SALIR#
         elif opcion == "salir":
            break

         # Si volvemos al menú (por defecto), asegurar que la música esté activa
         if musica_activada:
             cargar_musica()

      except pygame.error:
         # Reinicializar pygame si hay error
         pygame.init()
         if not pygame.mixer.get_init():
             pygame.mixer.init()
         VENTANA = pygame.display.set_mode((ANCHO, ALTO))
         if musica_activada:
             cargar_musica()

#---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---0---#

   #--- Para finalizar el programa ---#
   pygame.quit()
   sys.exit()

if __name__ == "__main__":
    main()