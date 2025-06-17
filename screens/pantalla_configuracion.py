from features.imports import *

def mostrar_pantalla_configuracion():
    pygame.mixer.init()
    musica_activada = True

    def activar(nivel_actual):
        if nivel_actual == 4:
            nombre_archivo = "musica_boss.mp3"
        else:
            nombre_archivo = "musica_niveles.mp3"
        archivo_musica = os.path.join(proyecto_bomberman, "assets", "sonidos", nombre_archivo)
        if os.path.exists(archivo_musica):
            pygame.mixer.music.load(archivo_musica)
            pygame.mixer.music.play(-1)

    def detener():
        pygame.mixer.music.stop()

    def musica():
        global musica_activada
        if musica_activada:
            detener()
            boton.config(text="Habilitar")
            musica_activada = False
        else:
            activar(nivel_actual=1)
            boton.config(text="Deshabilitar")
            musica_activada = True

    actual = os.path.abspath(__file__)
    proyecto_bomberman = os.path.dirname(os.path.dirname(actual))

    Principal = tk.Tk()
    Principal.title("Pantalla de Configuracion")
    Principal.geometry("600x600")
    Principal.configure(bg="black")

    font_configuracion = ("Fixedsys", 24, "bold")  
    font_audio = ("Fixedsys", 18, "bold")          
    font_boton = ("Fixedsys", 14, "bold")       
    espaciado = 10

    titulo = tk.Label(Principal, text="Configuraciones", font=font_configuracion, fg="white", bg="black")
    titulo.pack(pady=espaciado)

    Audio = tk.Label(Principal, text="Audio", font=font_audio, fg="white", bg="black")
    Audio.pack(pady=espaciado)

    boton = tk.Button(Principal, text="Deshabilitar", font=font_boton, command=musica, bg="gray20", fg="white")
    boton.pack(pady=espaciado)

    archivos = os.path.join(proyecto_bomberman, "assets", "imagenes", "imagen_configuraciones.png")
    if os.path.exists(archivos):
        imagen = tk.PhotoImage(file=archivos)
        imagen_bomberman = tk.Label(Principal, image=imagen, bg="black")
        imagen_bomberman.image = imagen
        imagen_bomberman.pack(pady=15)

    activar(nivel_actual=1)
    Principal.mainloop()


#Explicacion del codigo:

"""
import os se usa para las rutas de los archivos sin importar que sea de windows
(en mi caso) u ottro. Ahora se empieza conla musica_activada en true que cambia su
valor si esta habilitado o deshabilitado. Ademas, se reproduce en un bucle con
pygame.mixer.music.play(-1).

actual = os.path.abspath(file) obtiene la ruta del archivo y la hace absoluto. Despues
iguale el nombre del archivo a os.path.dirname(os.path.dirname(actual)) para los niveles de las carpetas
(subcarpetas). Primero subo al directorio padre y despues subo al directorio padre de ese basicamente.

Tambien menciono que el nivel actual empieza en 1 para que usuario esuche la musica inmediatamente despues
de abrir la pantalla
"""