import tkinter as tk

class PantallaPuntajes(tk.Frame):
    def __init__(self, master, lista_puntajes):
        tk.Frame.__init__(self, master)
        self.master = master
        self.lista_puntajes = lista_puntajes
        self.config(bg="black")
        self.crear_interfaz()

    def crear_interfaz(self):
        titulo = tk.Label(self, text="== MEJORES PUNTAJES ==", font=("Fixedsys", 20), fg="white", bg="black")
        titulo.pack(pady=20)

        for i in range(5):
            if i < len(self.lista_puntajes):
                jugador = self.lista_puntajes[i][0]
                puntaje = self.lista_puntajes[i][1]
                texto = str(i + 1) + ". " + jugador + " - " + str(puntaje)
            else:
                texto = str(i + 1) + ". " + "-----" + " - " + "0"

            etiqueta = tk.Label(self, text=texto, font=("Fixedsys", 16), fg="red", bg="black")
            etiqueta.pack(pady=4)

        boton_volver = tk.Button(
            self,
            text="VOLVER",
            font=("Fixedsys", 14),
            fg="black",
            bg="red",
            activebackground="darkred",
            activeforeground="white",
            command=self.volver_menu,
            relief="flat",
            padx=10,
            pady=5
        )
        boton_volver.pack(pady=30)

    def volver_menu(self):
        self.master.destroy()

# Código para ejecutar la pantalla
ventana = tk.Tk()
ventana.title("Pantalla de Puntajes")
ventana.geometry("400x400")
ventana.config(bg="black")

# Puntajes de ejemplo
puntajes_prueba = [
    ["ANA", 150],
    ["LUIS", 120],
    ["SOFIA", 100],
    ["CARLOS", 90],
    ["MARTA", 80]
]

pantalla = PantallaPuntajes(ventana, puntajes_prueba)
pantalla.pack(fill="both", expand=True)

ventana.mainloop()
