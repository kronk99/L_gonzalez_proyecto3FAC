import tkinter as tk

class StatusDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self, text="Estado del Procesador")
        self.label.pack()
        
        self.pc_label = tk.Label(self, text="PC: 0")
        self.pc_label.pack()
        
        self.registers_label = tk.Label(self, text="Registros: [0, 0, 0, ...]")
        self.registers_label.pack()
        
        self.memory_label = tk.Label(self, text="Memoria: [0, 0, 0, ...]")
        self.memory_label.pack()
    
    def update_status(self):
        self.pc_label.config(text=f"PC: {self.parent.processor.pc}")
        self.registers_label.config(text=f"Registros: {self.parent.processor.registers.registers}")
        self.memory_label.config(text=f"Memoria: {self.parent.processor.memory.memory[:10]}") # Mostrar primeros 10 valores de la memoria
