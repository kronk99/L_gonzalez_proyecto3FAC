import tkinter as tk
from tkinter import ttk

class Memory:
    def __init__(self, size=1024):
        self.memory = [0] * size
    
    def read(self, address):
        return self.memory[address]
    
    def write(self, address, data):
        self.memory[address] = data

class RegisterFile:
    def __init__(self, size=32):
        self.registers = [0] * size
    
    def read(self, reg_num):
        return self.registers[reg_num]
    
    def write(self, reg_num, data):
        self.registers[reg_num] = data

class MulticycleProcessor:
    def __init__(self):
        self.pc = 0
        self.memory = Memory()
        self.registers = RegisterFile()
        self.state = 'IF'
        self.instruction = None
    
    def reset(self):
        self.pc = 0
        self.state = 'IF'
        self.instruction = None
    
    def fetch_instruction(self):
        self.instruction = self.memory.read(self.pc)
        self.pc += 4
        self.state = 'ID'
    
    def decode_instruction(self):
        # Decodificación de la instrucción (ejemplo simplificado)
        self.state = 'EX'
    
    def execute_instruction(self):
        # Ejecución de la instrucción (ejemplo simplificado)
        self.state = 'MEM'
    
    def memory_access(self):
        # Acceso a memoria (ejemplo simplificado)
        self.state = 'WB'
    
    def write_back(self):
        # Escritura de resultados (ejemplo simplificado)
        self.state = 'IF'
    
    def execute_cycle(self):
        if self.state == 'IF':
            self.fetch_instruction()
        elif self.state == 'ID':
            self.decode_instruction()
        elif self.state == 'EX':
            self.execute_instruction()
        elif self.state == 'MEM':
            self.memory_access()
        elif self.state == 'WB':
            self.write_back()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Procesador Multiciclo")
        self.geometry("800x600")
        
        self.processor = MulticycleProcessor()
        self.create_widgets()
    
    def create_widgets(self):
        self.execution_control = ExecutionControl(self)
        self.execution_control.pack()
        
        self.status_display = StatusDisplay(self)
        self.status_display.pack()
        
        self.statistics_display = StatisticsDisplay(self)
        self.statistics_display.pack()

class ExecutionControl(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self, text="Control de Ejecución")
        self.label.pack()
        
        self.step_button = tk.Button(self, text="Paso a Paso", command=self.step_execution)
        self.step_button.pack()
        
        self.timed_button = tk.Button(self, text="Ejecución a Ritmo", command=self.timed_execution)
        self.timed_button.pack()
        
        self.full_button = tk.Button(self, text="Ejecución Completa", command=self.full_execution)
        self.full_button.pack()
    
    def step_execution(self):
        self.parent.processor.execute_cycle()
        self.parent.status_display.update_status()
    
    def timed_execution(self):
        # Implementar la ejecución a ritmo constante
        pass
    
    def full_execution(self):
        # Implementar la ejecución completa
        pass

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

class StatisticsDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="Estadísticas de Ejecución")
        self.label.pack()
        
        self.stats_label = tk.Label(self, text="CPI: 0.0, Duración: 0 ciclos, Tiempo: 0s")
        self.stats_label.pack()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
