import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import logica

class Ventana:
    def __init__(self, root):
        self.root = root

        ancho_ventana = 1200  # Ancho de la ventana principal
        alto_ventana = 600  # Alto de la ventana principal
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")  # Da el tamaño de la ventana
        self.root.resizable(False, False)

        # Carga la imagen de Uniciclo
        self.Img_Uniciclo = Image.open("Uniciclo.png")
        self.Img_Uniciclo = self.Img_Uniciclo.resize((600, 300), Image.LANCZOS)
        self.Uni_imagen = ImageTk.PhotoImage(self.Img_Uniciclo)

        # Carga la imagen de Multiciclo
        self.Img_Multiciclo = Image.open("Multi.png")
        self.Img_Multiciclo = self.Img_Multiciclo.resize((600, 300), Image.LANCZOS)
        self.Multi_imagen = ImageTk.PhotoImage(self.Img_Multiciclo)

        # Carga la imagen de CRiesgos
        self.Img_CRiesgos = Image.open("UnidadR.png")
        self.Img_CRiesgos = self.Img_CRiesgos.resize((700, 300), Image.LANCZOS)
        self.CRiesgos_imagen = ImageTk.PhotoImage(self.Img_CRiesgos)

        # Carga la imagen de SRiesgos
        self.Img_SRiesgos = Image.open("Riesgos.png")
        self.Img_SRiesgos = self.Img_SRiesgos.resize((750, 200), Image.LANCZOS)
        self.SRiesgos_imagen = ImageTk.PhotoImage(self.Img_SRiesgos)


        # Canvas para mostrar imágenes
        self.diagram_canva = tk.Canvas(self.root, width=ancho_ventana, height=alto_ventana)
        self.diagram_canva.pack()

        def mostrar_Uniciclo():
            self.diagram_canva.delete("all")
            self.diagram_canva.create_image(300, 200, image=self.Uni_imagen)

        def mostrar_Multiciclo():
            self.diagram_canva.delete("all")
            self.diagram_canva.create_image(300, 200, image=self.Multi_imagen)

        def mostrar_CRiesgos():
            self.diagram_canva.delete("all")
            self.diagram_canva.create_image(400, 200, image=self.CRiesgos_imagen)

        def mostrar_SRiesgos():
            self.diagram_canva.delete("all")
            self.diagram_canva.create_image(400, 200, image=self.SRiesgos_imagen)

        self.barra_menu = tk.Menu(self.root)

        self.Tipo = tk.Menu(self.barra_menu, tearoff=False)

        # Crear submenú Uniciclo
        self.Uniciclo = tk.Menu(self.barra_menu, tearoff=False)
        self.Uniciclo.add_command(command=mostrar_Uniciclo, label="Ejecución paso a paso")
        self.Uniciclo.add_command(command=mostrar_Uniciclo, label="Ejecución a un ritmo")
        self.Uniciclo.add_command(command=mostrar_Uniciclo, label="Ejecución completa")

        # Crear submenú Multiciclo
        self.Multiciclo = tk.Menu(self.barra_menu, tearoff=False)
        self.Multiciclo.add_command(command=mostrar_Multiciclo, label="Ejecución paso a paso")
        self.Multiciclo.add_command(command=mostrar_Multiciclo, label="Ejecución a un ritmo")
        self.Multiciclo.add_command(command=mostrar_Multiciclo, label="Ejecución completa")

        # Crear submenú CRiesgos
        self.CRiesgos = tk.Menu(self.barra_menu, tearoff=False)
        self.CRiesgos.add_command(command=mostrar_CRiesgos, label="Ejecución paso a paso")
        self.CRiesgos.add_command(command=mostrar_CRiesgos, label="Ejecución a un ritmo")
        self.CRiesgos.add_command(command=mostrar_CRiesgos, label="Ejecución completa")

        # Crear submenú SRiesgos
        self.SRiesgos = tk.Menu(self.barra_menu, tearoff=False)
        self.SRiesgos.add_command(command=mostrar_SRiesgos, label="Ejecución paso a paso")
        self.SRiesgos.add_command(command=mostrar_SRiesgos, label="Ejecución a un ritmo")
        self.SRiesgos.add_command(command=mostrar_SRiesgos, label="Ejecución completa")

        # Añadir menús desplegables al menú principal
        self.barra_menu.add_cascade(menu=self.Tipo, label="Tipo de procesador")
        self.Tipo.add_cascade(menu=self.Uniciclo, label="Uniciclo")
        self.Tipo.add_cascade(menu=self.Multiciclo, label="Multiciclo")
        self.Tipo.add_cascade(menu=self.CRiesgos, label="Segmentado con riesgos y stalls")
        self.Tipo.add_cascade(menu=self.SRiesgos, label="Segmentado con unidad de riesgos y adelantamiento")

        self.root.config(menu=self.barra_menu)

        # Espacio de avanzar o pausar
        self.boton_retoceda = tk.Button(root, text='«', font=("Arial", 20))
        self.boton_retoceda.place(x=40, y=5)
        self.boton_avance = tk.Button(root, text='»', font=("Arial", 20))
        self.boton_avance.place(x=80, y=5)
        self.boton_play = tk.Button(root, text='▶', font=("Arial", 20))
        self.boton_play.place(x=120, y=5)
        self.boton_pausa = tk.Button(root, text='⏸', font=("Arial", 20))
        self.boton_pausa.place(x=157, y=5)
        self.boton_reversa = tk.Button(root, text='🔁', font=("Arial", 20))
        self.boton_reversa.place(x=217, y=5)

        # Espacio para el diagrama o modelado
        self.outer_diagram_frame = tk.Frame(root, highlightbackground="gray", highlightthickness=1)
        self.outer_diagram_frame.place(x=20, y=65)

        self.diagram_canva = tk.Canvas(self.outer_diagram_frame, background="white", width=780, height=380)
        self.diagram_canva.pack(side=tk.TOP, fill=tk.Y)

        self.x_scrollbar = tk.Scrollbar(self.outer_diagram_frame, orient=tk.HORIZONTAL, command=self.diagram_canva.xview)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.diagram_canva.configure(xscrollcommand=self.x_scrollbar.set)

        self.diagram_canva.config(scrollregion=self.diagram_canva.bbox("all"))

        # Espacio para Registers

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
        tree.heading("col1", text="Nombre")
        tree.heading("col2", text="Valor")

        # Definir el tamaño de las columnas
        tree.column("col1", width=100)
        tree.column("col2", width=190)

        # Insertar 32 filas de datos en el Treeview
        tree.insert("", "end", values=(f"x0", logica.reg0))
        tree.insert("", "end", values=(f"x1", logica.reg1))
        tree.insert("", "end", values=(f"x2", logica.reg2))
        tree.insert("", "end", values=(f"x3", logica.reg3))
        tree.insert("", "end", values=(f"x4", logica.reg4))
        tree.insert("", "end", values=(f"x5", logica.reg5))
        tree.insert("", "end", values=(f"x6", logica.reg6))
        tree.insert("", "end", values=(f"x7", logica.reg7))
        tree.insert("", "end", values=(f"x8", logica.reg8))
        tree.insert("", "end", values=(f"x9", logica.reg9))
        tree.insert("", "end", values=(f"x10", logica.reg10))
        tree.insert("", "end", values=(f"x11", logica.reg11))
        tree.insert("", "end", values=(f"x12", logica.reg12))
        tree.insert("", "end", values=(f"x13", logica.reg13))
        tree.insert("", "end", values=(f"x14", logica.reg14))
        tree.insert("", "end", values=(f"x15", logica.reg15))
        tree.insert("", "end", values=(f"x16", logica.reg16))
        tree.insert("", "end", values=(f"x17", logica.reg17))
        tree.insert("", "end", values=(f"x18", logica.reg18))
        tree.insert("", "end", values=(f"x19", logica.reg19))
        tree.insert("", "end", values=(f"x20", logica.reg20))
        tree.insert("", "end", values=(f"x21", logica.reg21))
        tree.insert("", "end", values=(f"x22", logica.reg22))
        tree.insert("", "end", values=(f"x23", logica.reg23))
        tree.insert("", "end", values=(f"x24", logica.reg24))
        tree.insert("", "end", values=(f"x25", logica.reg25))
        tree.insert("", "end", values=(f"x26", logica.reg26))
        tree.insert("", "end", values=(f"x27", logica.reg27))
        tree.insert("", "end", values=(f"x28", logica.reg28))
        tree.insert("", "end", values=(f"x29", logica.reg29))
        tree.insert("", "end", values=(f"x30", logica.reg30))
        tree.insert("", "end", values=(f"x31", logica.reg31))

        self.label_register = tk.Label(root, text="Registers", font=("Arial", 9))
        self.label_register.place(x=860, y=5)

        # Espacio para informacion de ejecucion
        self.canvas_execute_inf = tk.Canvas(root, width=330, height=200, highlightbackground="black", highlightthickness=1)
        self.canvas_execute_inf.place(x=850, y=300)
        self.label_executeInf = tk.Label(root, text="Execution info", font=("Arial", 9))
        self.label_executeInf.place(x=860, y=290)

        self.entry1_execInf = tk.Entry(self.canvas_execute_inf, width=30, font=("Arial", 9))
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
