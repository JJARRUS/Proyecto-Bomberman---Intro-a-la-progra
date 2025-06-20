from features.imports import *
from features.config import musica_activada, cargar_musica, parar_musica, toggle_musica

def mostrar_pantalla_configuracion():

    actual = os.path.abspath(__file__)
    proyecto_bomberman = os.path.dirname(os.path.dirname(actual))

    Principal = tk.Tk()
    Principal.title("Pantalla de Configuracion")
    Principal.geometry("600x600")
    Principal.configure(bg="black")

    # Variable para controlar si se debe salir
    salir_configuracion = False

    def musica():
        # Usamos la función toggle del config
        estado = toggle_musica()
        
        # Actualizamos el botón según el estado
        if estado:
            boton.config(text="Deshabilitar", bg="red")
        else:
            boton.config(text="Habilitar", bg="green")
        
        Principal.update()

    def volver():
        nonlocal salir_configuracion
        salir_configuracion = True
        Principal.quit()  # Salir del mainloop
        Principal.destroy()  # Destruir la ventana

    font_configuracion = ("Fixedsys", 24, "bold")
    titulo = tk.Label(Principal, text="Configuraciones", font=font_configuracion, fg="white", bg="black")
    titulo.pack(pady=10)

    frame_audio = tk.Frame(Principal, bg="black")
    frame_audio.pack(pady=10)

    tk.Label(frame_audio, 
        text="Audio:", 
        font=("Fixedsys", 14), 
        bg="black", 
        fg="white").pack(side="left")

    boton = tk.Button(Principal, 
                      text="Deshabilitar" if musica_activada else "Habilitar", 
                      font=14, 
                      command=musica, 
                      bg="red" if musica_activada else "green", 
                      fg="white")
    boton.pack(pady=10)

    tk.Button(Principal, 
              text="Volver al Menú", 
              font=("Fixedsys", 12),
              command=volver, 
              bg="red", 
              fg="white").pack(pady=10)

    fondo = os.path.join(proyecto_bomberman, "assets", "imagenes", "imagen_configuraciones.png")
    if os.path.exists(fondo):
        try:
            imagen = tk.PhotoImage(file=fondo)
            imagen_bomberman = tk.Label(Principal, image=imagen, bg="black")
            imagen_bomberman.pack(pady=15)
            imagen_bomberman.image = imagen
        except Exception as e:
            print(f"Error cargando imagen: {e}")

    # Configurar el evento de cerrar ventana
    Principal.protocol("WM_DELETE_WINDOW", volver)

    # Mantener la ventana en primer plano y centrada
    Principal.grab_set()  # Hacer que la ventana sea modal
    Principal.focus_set()  # Dar focus a la ventana
    
    # Ejecutar el loop principal
    Principal.mainloop()

#Explicacion del codigo:

"""
import os se usa para las rutas de los archivos sin importar que sea de windows
(en mi caso) u otro. Ahora se empieza con la musica_activada en true que cambia su
valor si esta habilitado o deshabilitado. Ademas, se reproduce en un bucle con
pygame.mixer.music.play(-1).

actual = os.path.abspath(__file__) obtiene la ruta del archivo y la hace absoluto. Despues
iguale el nombre del archivo a os.path.dirname(os.path.dirname(actual)) para los niveles de las carpetas
(subcarpetas). Primero subo al directorio padre y despues subo al directorio padre de ese basicamente.

Tambien menciono que el nivel actual empieza en 1 para que usuario esuche la musica inmediatamente despues
de abrir la pantalla
"""