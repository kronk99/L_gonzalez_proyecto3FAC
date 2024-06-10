import tkinter as tk

class StatisticsDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="Estadísticas de Ejecución")
        self.label.pack()
        
        self.stats_label = tk.Label(self, text="CPI: 0.0, Duración: 0 ciclos, Tiempo: 0s")
        self.stats_label.pack()
