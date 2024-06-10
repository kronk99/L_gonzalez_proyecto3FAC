import tkinter as tk

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
        def run():
            if self.parent.processor.state != 'Fetch' or self.parent.processor.pc != 0:
                self.parent.processor.execute_cycle()
                self.parent.status_display.update_status()
                self.parent.after(500, run)  # Ajusta el tiempo según necesites
        run()
    
    def full_execution(self):
        while self.parent.processor.state != 'Fetch' or self.parent.processor.pc != 0:
            self.parent.processor.execute_cycle()
            self.parent.status_display.update_status()
