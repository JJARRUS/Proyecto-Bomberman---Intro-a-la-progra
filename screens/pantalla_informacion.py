from features.imports import *
from features.config import musica_activada, cargar_musica

class PantallaInformacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Información")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg="black")
        
        #Scrollbar:
        main_frame = tk.Frame(ventana, bg="black")
        main_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_frame, bg="black", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="black")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
                )
            )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.abajo = scrollable_frame
        self.fuente = ("Fixedsys", 12)

        # Botón Volver
        tk.Button(ventana, text="Volver", command=self.volver,
                font=self.fuente, bg="red", fg="white").pack(pady=20)
        
        self.datos_autores()
        
        # Hacer que la ventana sea modal y centrada
        ventana.grab_set()  # Hacer que la ventana sea modal
        ventana.focus_set()  # Dar focus a la ventana
        
        # Configurar el evento de cerrar ventana
        ventana.protocol("WM_DELETE_WINDOW", self.volver)
        
        #--- Agregado de música ---#
        # Solo cargar música si está activada
        if musica_activada:
            try:
                cargar_musica()
            except:
                pass  # Si falla, continuamos sin música

    def volver(self):
        """Cierra la ventana de información y vuelve al menú"""
        self.ventana.quit()  # Salir del mainloop
        self.ventana.destroy()  # Destruir la ventana
        # No importamos main aquí para evitar imports circulares
        # El main manejará la reactivación de música

    def datos_autores(self):
        tk.Label(self.abajo, text="Pantalla de Información", font=("Fixedsys", 18), bg="black", fg="red").pack(pady=10)
        archivos = os.path.dirname(__file__)
        foto_joel = os.path.join(archivos, "..", "assets", "imagenes", "joel.png")
        
        foto_fabiola = os.path.join(archivos, "..", "assets", "imagenes", "Fabiola.png")
        self.mostrar_autor("Jarot Joel Picado Gomez", "2024109895", foto_joel)
        self.mostrar_autor("Fabiola Gonzalez Gomez", "2025065028", foto_fabiola)
        self.mostrar_info("Institución", "Instituto Tecnológico de Costa Rica (ITCR)")
        tk.Label(self.abajo, text="  El Tecnológico de Costa Rica es una universidad pública de Costa Rica creada el 10 de junio de 1971. Su enfoque es en las carreras de ingeniería y tecnología.", font=self.fuente, bg="black", fg="white", wraplength=760, justify="left").pack(anchor="w", padx=30)
        self.mostrar_info("Asignatura", "Introducción a la Computación")
        tk.Label(self.abajo, text="  Curso que constituye los conceptos básicos para modelar y solucionar problemas de una manera algorítmica.", font=self.fuente, bg="black", fg="white", wraplength=760, justify="left").pack(anchor="w", padx=30)
        self.mostrar_info("Carrera", "Ingeniería en Computadores")
        tk.Label(self.abajo, text="  Los ingenieros de esta carrera resuelven problemas complejos relacionados con la mezcla de hardware y software.", font=self.fuente, bg="black", fg="white", wraplength=760, justify="left").pack(anchor="w", padx=30)
        self.mostrar_info("Profesores", "Jeff Schmidt Peralta, Diego Mora Rojas")
        self.mostrar_info("País", "Costa Rica")
        self.mostrar_info("Versión del Programa", "1.0")
        tk.Label(self.abajo, text="\nInformación del juego", font=("Fixedsys", 14), bg="black", fg="red").pack(anchor="w", pady=(10, 0), padx=10)

        ayuda = "- Movimiento: w (arriba), a (izquierda), d (derecha), s (abajo)"
        tk.Label(self.abajo, text=ayuda, font=self.fuente, bg="black", fg="white", justify="left", wraplength=760).pack(anchor="w", padx=20, pady=(5, 10))

    def mostrar_autor(self, nombre, carnet, archivos_foto):
        autor = tk.Frame(self.abajo, bg="black")
        autor.pack(pady=5)
        if archivos_foto and os.path.exists(archivos_foto):
            try:
                imagen_original = Image.open(archivos_foto)
                imagen_redimensionada = imagen_original.resize((100, 100), Image.Resampling.LANCZOS) #nueva version
                imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
                imagen_ajustar = tk.Label(autor, image=imagen_tk, bg="black")
                imagen_ajustar.image = imagen_tk
                imagen_ajustar.pack(side="left", padx=10)
            except Exception as e:
                print(f"Error cargando imagen {archivos_foto}: {e}")
        texto = nombre + "\nCarnet: " + carnet
        tk.Label(autor, text=texto, font=self.fuente, bg="black", fg="white", justify="left").pack(side="left")

    def mostrar_info(self, titulo, contenido):
        ajuste = tk.Frame(self.abajo, bg="black")
        ajuste.pack(anchor="w", pady=2, padx=20) #hacia el oeste se alinea el texto 
        tk.Label(ajuste, text=titulo + ":", font=self.fuente, bg="black", fg="red").pack(side="left")
        tk.Label(ajuste, text=contenido, font=self.fuente, bg="black", fg="white").pack(side="left")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = PantallaInformacion(ventana)
    ventana.mainloop()

#Explicacion del codigo:
"""
En este codigo se utiliza PIL para hacer que las imagenes se puedan ajustar y os
para las rutas de los archivos.

archivos_foto (boolean) confirma que no sea vacio o falso.
os.path.exists(archivos_foto) confirma sobre si hay un archiva en la ruta 
Esto hace que el programa no se caiga si se ententa cargar una imagen que no existe

La funcion de datos_autores muestra el contenido de la pantalla.
La funcion mostrar_autor muestra a la persona , verifica que existe y redimensioan a 100x100 pixeles
La funcion mostrar_info se usa para colocar etiquetas en la misma linea.
El if __nam__ crea la ventana de aplicacion
"""