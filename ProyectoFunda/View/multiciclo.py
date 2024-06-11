import tkinter as tk

class procesadorMulticiclo(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.title("Procesador: Multiciclo")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.volver_principal)
        self.master = master

        label = tk.Label(self, text="Multicilo", font=("Arial", 20))
        label.pack(expand=True)

        boton_retroceder = tk.Button(self, text="Retroceder", command=self.volver_principal)
        boton_retroceder.pack(pady=20)

    def volver_principal(self):
        self.destroy()
        self.master.deiconify()
