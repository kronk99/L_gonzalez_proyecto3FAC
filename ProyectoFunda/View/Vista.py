import tkinter as tk
class ventana:
    def __init__(self,root):
        self.root=root #esta es la ventana que le pasa tkinter.
        anchoVentana = 800
        altoVentana= 600
        self.root.geometry(f"{anchoVentana}x{altoVentana}") #establece el tamaño de la ventana
        self.root.resizable(False,False)

if __name__=="__main__":
    main=tk.Tk() #esto es la ventana principal
    main.title("tumagei")#aca se configura el titulo
    app=ventana(main) #a mi clase le meto la ventana
    main.mainloop()