import tkinter as tk
from multicycle_processor import MulticycleProcessor
from execution_control import ExecutionControl
from status_display import StatusDisplay
from statistics_display import StatisticsDisplay

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

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
