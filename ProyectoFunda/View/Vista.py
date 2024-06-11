import tkinter as tk
from tkinter import ttk
import uniciclo
import multiciclo
import pipeline1
import pipeline2

class AplicacionPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de procesadores básicos")
        self.geometry("800x400")

        self.frame_izquierdo = tk.Frame(self, bg="gray", width=200)
        self.frame_izquierdo.pack(side="left", fill="y")

        self.label_seleccion = tk.Label(self.frame_izquierdo, text="Seleccionar procesador")
        self.label_seleccion.pack(pady=20)

        self.procesadores = ["Uniciclo", "Multiciclo", "Segmentado con riesgos y solucionando con stalls","Segmentado con unidad de riesgos y adelantamiento"]
        self.seleccion = ttk.Combobox(self.frame_izquierdo, values=self.procesadores)
        self.seleccion.pack(pady=10)
        self.seleccion.bind("<<ComboboxSelected>>", self.cambiar_ventana)

        self.frame_derecho = tk.Frame(self, bg="navy")
        self.frame_derecho.pack(side="right", fill="both", expand=True)

        self.label_bienvenida = tk.Label(self.frame_derecho, text="Simulador de procesadores básicos", font=("Arial", 24), fg="white", bg="navy")
        self.label_bienvenida.pack(expand=True)

    def cambiar_ventana(self, event):
        seleccion = self.seleccion.get()
        self.withdraw()
        if seleccion == "Uniciclo":
            uniciclo.procesadorUniciclo(self)
        elif seleccion == "Multiciclo":
            multiciclo.procesadorMulticiclo(self)
        elif seleccion == "Segmentado con riesgos y solucionando con stalls":
            pipeline1.procesadorPipeline(self)
        elif seleccion == "Segmentado con unidad de riesgos y adelantamiento":
            pipeline2.procesadorPipeline2(self)

if __name__ == "__main__":
    app = AplicacionPrincipal()
    app.mainloop()
