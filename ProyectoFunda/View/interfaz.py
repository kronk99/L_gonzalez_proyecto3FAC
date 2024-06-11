import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
class Ventana:
    def __init__(self, root):
        self.root = root

        ancho_ventana = 1200  # Ancho de la ventana principal
        alto_ventana = 600  # Alto de la ventana principal
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")  # Da el tamaño de la ventana
        self.root.resizable(False, False)

        #self.Img_Uniciclo = Image.open("Uniciclo.jpeg")
        #self.Uni_imagen = ImageTk.PhotoImage(self.Img_Uniciclo)

        def mostrar_Uniciclo():
            self.diagram_canva.create_image(300, 200,image=self.Uni_imagen)

        self.barra_menu = tk.Menu()

        self.Tipo = tk.Menu(self.barra_menu, tearoff=False)

        self.Uniciclo = tk.Menu(self.barra_menu, tearoff=False)
        self.Uniciclo.add_command(command=mostrar_Uniciclo, label="Paso a Paso")
        #self.Uniciclo.add_command(command=)



        self.barra_menu.add_cascade(menu=self.Tipo, label="Tipo de procesador")
        self.Tipo.add_cascade(menu=self.Uniciclo, label="Uniciclo")



        self.root.config(menu=self.barra_menu)

#Espacio de avanzar o pausar
        self.boton_retoceda = tk.Button(root, text='«', font=("Arial", 20))
        self.boton_retoceda.place(x=40, y=5)
        self.boton_avance = tk.Button(root, text='»', font=("Arial", 20))
        self.boton_avance.place(x=80, y=5)
        self.boton_pausa = tk.Button(root, text='⏸', font=("Arial", 20))
        self.boton_pausa.place(x=120, y=5)
        self.boton_reversa = tk.Button(root, text='🔁', font=("Arial", 20))
        self.boton_reversa.place(x=180, y=5)

#Espacio para el diagrama o modelado
        self.outer_diagram_frame = tk.Frame(root, highlightbackground="gray", highlightthickness=1)
        self.outer_diagram_frame.place(x=20, y=65)

        self.diagram_canva = tk.Canvas(self.outer_diagram_frame, background="white", width=780, height=380)
        self.diagram_canva.pack(side=tk.TOP, fill=tk.Y)

        #self.y_scrollbar = tk.Scrollbar(self.outer_diagram_frame, orient=tk.VERTICAL, command=self.diagram_canva.yview)
        #self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.x_scrollbar = tk.Scrollbar(self.outer_diagram_frame, orient=tk.HORIZONTAL, command=self.diagram_canva.xview)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.diagram_canva.configure(xscrollcommand=self.x_scrollbar.set)

        self.diagram_canva.config(scrollregion=self.diagram_canva.bbox("all"))

#Espacio para Registers

        # Crear un Frame para contener el Treeview y las Scrollbars
        self.frame = tk.Frame(root)
        self.frame.place(x=850, y=30)

        # Crear las Scrollbars
        vsb = ttk.Scrollbar(self.frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(self.frame, orient="horizontal")
        hsb.pack(side='bottom', fill='x')

        # Crear el Treeview
        tree = ttk.Treeview(self.frame, columns=("col1", "col2"), show='headings', yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)
        tree.pack(fill='both', expand=True)

        # Configurar las Scrollbars
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        # Definir los encabezados de las columnas
        tree.heading("col1", text="Columna 1")
        tree.heading("col2", text="Columna 2")


        # Definir el tamaño de las columnas
        tree.column("col1", width=100)
        tree.column("col2", width=190)


        # Insertar 32 filas de datos en el Treeview
        for i in range(0, 32):
            tree.insert("", "end", values=(f"Item {i}", f"Value {i}"))

        self.label_register = tk.Label(root, text="Registers", font=("Arial", 9))
        self.label_register.place(x=860, y=5)

        #Espacio para informacion de ejecucion
        self.canvas_execute_inf = tk.Canvas(root, width=330, height=200, highlightbackground="black", highlightthickness=1)
        self.canvas_execute_inf.place(x=850, y=300)
        self.label_executeInf = tk.Label(root, text="Execution info", font=("Arial", 9))
        self.label_executeInf.place(x=860, y=290)

        self.entry1_execInf = tk.Entry(self.canvas_execute_inf,width=30, font=("Arial", 9))
        self.entry1_execInf.place(x=100, y=10)
        self.label_execInf1 = tk.Label(self.canvas_execute_inf, text="Cycles:", font=("Arial", 9))
        self.label_execInf1.place(x=20, y=10)

        self.entry2_execInf = tk.Entry(self.canvas_execute_inf, width=30, font=("Arial", 9))
        self.entry2_execInf.place(x=100, y=50)
        self.label_execInf2 = tk.Label(self.canvas_execute_inf, text="Instrs.retired:", font=("Arial", 9))
        self.label_execInf2.place(x=20, y=50)

        self.entry3_execInf = tk.Entry(self.canvas_execute_inf, width=30, font=("Arial", 9))
        self.entry3_execInf.place(x=100, y=90)
        self.label_execInf3 = tk.Label(self.canvas_execute_inf, text="CPI:", font=("Arial", 9))
        self.label_execInf3.place(x=20, y=90)

        self.entry4_execInf = tk.Entry(self.canvas_execute_inf, width=30, font=("Arial", 9))
        self.entry4_execInf.place(x=100, y=130)
        self.label_execInf4 = tk.Label(self.canvas_execute_inf, text="IPC:", font=("Arial", 9))
        self.label_execInf4.place(x=20, y=130)

        self.entry5_execInf = tk.Entry(self.canvas_execute_inf, width=30, font=("Arial", 9))
        self.entry5_execInf.place(x=100, y=170)
        self.label_execInf5 = tk.Label(self.canvas_execute_inf, text="Clock rate:", font=("Arial", 9))
        self.label_execInf5.place(x=20, y=170)




if __name__ == "__main__":
    VentaPri = tk.Tk()
    VentaPri.title("Ripes")
    app = Ventana(VentaPri)
    VentaPri.mainloop()