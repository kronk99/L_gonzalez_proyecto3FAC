class Processor:
    def __init__(self):
        self.registers = [0] * 32  # 32 registros
        self.memory = [0] * 1024   # Memoria con 1024 palabras (puede ajustarse)
        self.PC = 0                # Contador de programa
        self.IR = 0                # Registro de instrucción
        self.current_cycle = 0     # Ciclo actual
        self.state = "IF"          # Estado inicial
        self.instruction = ""      # Instrucción actual en formato texto
        self.program_size = 0      # Tamaño del programa cargado
        self.total_cycles = 0      # Total de ciclos ejecutados
        self.instructions_executed = 0  # Total de instrucciones ejecutadas
        self.latency = {
            "IF": 1,
            "ID": 1,
            "EX": 2,
            "MEM": 2,
            "WB": 1
        }

    def fetch(self):
        self.IR = self.memory[self.PC]
        self.PC += 1
        self.state = "ID"
        self.instruction = f"Fetch: {self.IR:032b}"
        self.current_cycle += self.latency["IF"]

    def decode(self):
        self.opcode = self.IR & 0x7F
        self.rd = (self.IR >> 7) & 0x1F
        self.funct3 = (self.IR >> 12) & 0x07
        self.rs1 = (self.IR >> 15) & 0x1F
        self.rs2 = (self.IR >> 20) & 0x1F
        self.funct7 = (self.IR >> 25) & 0x7F
        self.imm = (self.IR >> 20) & 0xFFF  # Simplificado para instrucciones tipo I

        if self.opcode == 0x33:  # Tipo R
            self.instruction = f"Decode: ADD x{self.rd}, x{self.rs1}, x{self.rs2}"
        elif self.opcode == 0x13:  # Tipo I (Ejemplo: ADDI)
            self.instruction = f"Decode: ADDI x{self.rd}, x{self.rs1}, {self.imm}"
        elif self.opcode == 0x03:  # Tipo I (Ejemplo: LW)
            self.instruction = f"Decode: LW x{self.rd}, {self.imm}(x{self.rs1})"
        elif self.opcode == 0x23:  # Tipo S (Ejemplo: SW)
            self.instruction = f"Decode: SW x{self.rs2}, {self.imm}(x{self.rs1})"
        else:
            self.instruction = "Decode: Instrucción no soportada"

        self.state = "EX"
        self.current_cycle += self.latency["ID"]

    def execute(self):
        if self.opcode == 0x33:  # Tipo R (Ejemplo: ADD)
            if self.funct3 == 0x0:
                if self.funct7 == 0x00:
                    self.result = self.registers[self.rs1] + self.registers[self.rs2]
                elif self.funct7 == 0x20:
                    self.result = self.registers[self.rs1] - self.registers[self.rs2]
            self.state = "WB"
        elif self.opcode == 0x13:  # Tipo I (Ejemplo: ADDI)
            if self.funct3 == 0x0:
                self.result = self.registers[self.rs1] + self.imm
            self.state = "WB"
        elif self.opcode == 0x03:  # Tipo I (Ejemplo: LW)
            if self.funct3 == 0x0:
                self.address = self.registers[self.rs1] + self.imm
            self.state = "MEM"
        elif self.opcode == 0x23:  # Tipo S (Ejemplo: SW)
            if self.funct3 == 0x0:
                self.address = self.registers[self.rs1] + self.imm
            self.state = "MEM"
        else:
            self.state = "IF"  # Estado por defecto para instrucciones no soportadas
        self.instruction = f"Execute: {self.instruction.split(': ')[1]}"
        self.current_cycle += self.latency["EX"]

    def memory_access(self):
        if self.opcode == 0x03:  # LW
            self.result = self.memory[self.address]
            self.state = "WB"
        elif self.opcode == 0x23:  # SW
            self.memory[self.address] = self.registers[self.rs2]
            self.state = "IF"
        self.current_cycle += self.latency["MEM"]

    def write_back(self):
        if self.opcode in [0x33, 0x13, 0x03]:  # Instrucciones tipo R, I y LW
            self.registers[self.rd] = self.result
        self.state = "IF"
        self.instruction = f"Write Back: {self.instruction.split(': ')[1]}"
        self.current_cycle += self.latency["WB"]
        self.instructions_executed += 1

    def run_cycle(self):
        while self.PC < self.program_size or self.state != "IF":
            if self.state == "IF":
                self.fetch()
            elif self.state == "ID":
                self.decode()
            elif self.state == "EX":
                self.execute()
            elif self.state == "MEM":
                self.memory_access()
            elif self.state == "WB":
                self.write_back()
            self.total_cycles = self.current_cycle
            print(f"Cycle: {self.total_cycles}, PC: {self.PC}, State: {self.state}")
            print(f"Registers: {self.registers[:4]}")  # Mostrar los primeros 4 registros
            print(f"Instruction: {self.instruction}")
            print("-" * 40)

    def load_program(self, program):
        for i in range(len(program)):
            self.memory[i] = program[i]
        self.program_size = len(program)

# Parámetros de la matriz
M = 3  # Número de columnas en A (también filas en B)
P = 3  # Número de columnas en B
N = 3  # Número de filas en A

# Programa de prueba (código de ejemplo en formato binario)
program = [
    0b00000000000000000000001010010011,  # ADDI x5 (t0), x0, 0
    0b00000000000000000000001100010011,  # ADDI x6 (t1), x0, 0
    0b00000000000000000000001110010011,  # ADDI x7 (t2), x0, 0
    0b00000000000100000000000010010011,  # ADDI x1, x0, 1
    0b00000000001000000000000100010011,  # ADDI x2, x0, 2
    0b00000000001000010000000110110011,  # ADD x3, x2, x1
    0b00000000001100010000001000000011,  # LW x4, 3(x2)
    # Instrucciones para la multiplicación de matrices
    0b00000000000000000000001100010011,  # ADDI x6 (t1), x0, 0
    0b00000000000000000000011000010011,  # ADDI x12 (t3), x0, 0
    0b00000000000000000000010010010011,  # ADDI x9 (t4), x0, 0
    0b00000000001101000110010110110011,  # MUL x10 (t5), x8 (t0), x3
    0b00000000010101001000010110110011,  # ADD x11 (t6), x10 (t5), x7 (t2)
    0b00000000001101001010010110110011,  # MUL x13 (t7), x9 (t4), x3
    0b00000000010101001100010110110011,  # ADD x14 (t8), x13 (t7), x6 (t1)
    0b00000000011001001100001010000011,  # LW x18 (t9), 100(x11)
    0b00000000110001101100001010000011,  # LW x20 (t10), 200(x14)
    0b00000000101010001100010110110011,  # MUL x18 (t9), x18 (t9), x20 (t10)
    0b00000000100101101000010110110011,  # ADD x12 (t3), x12 (t3), x18 (t9)
    0b00000000000101001000010010010011,  # ADDI x9 (t4), x9 (t4), 1
    0b00000001011001100010001000100011,  # SW x12 (t3), 300(x11)
    0b00000000000101001100001100010011,  # ADDI x6 (t1), x6 (t1), 1
    0b00000000000101000000001010010011   # ADDI x5 (t0), x5 (t0), 1
]

# Crear el procesador y cargar el programa
processor = Processor()
processor.load_program(program)

# Inicialización de las matrices en memoria
matrix_A = [1, 2, 3, 4, 5, 6, 7, 8, 9]
matrix_B = [9, 8, 7, 6, 5, 4, 3, 2, 1]
matrix_C = [0] * 9  # Matriz resultado

# Cargar matrices en la memoria
processor.memory[100:109] = matrix_A
processor.memory[200:209] = matrix_B
processor.memory[300:309] = matrix_C

# Verificar que el programa y la memoria se hayan cargado correctamente
print("Memoria cargada con el programa:")
for i in range(len(program)):
    print(f"Mem[{i}] = {processor.memory[i]:032b}")

print("\nMemoria inicial de matrices:")
for i in range(100, 110):  # Mostrar los valores de matrix_A
    print(f"matrix_A[{i-100}] = {processor.memory[i]}")
for i in range(200, 210):  # Mostrar los valores de matrix_B
    print(f"matrix_B[{i-200}] = {processor.memory[i]}")
for i in range(300, 310):  # Mostrar los valores de matrix_C
    print(f"matrix_C[{i-300}] = {processor.memory[i]}")

# Ejecutar el ciclo de instrucción
processor.run_cycle()

# Imprimir el estado final de todos los registros
print("\nEstado final de los registros:")
for i in range(8):  # Mostrar los primeros 8 registros para verificar
    print(f"x{i} = {processor.registers[i]}")

# Imprimir el estado final de matrix_C
print("\nEstado final de matrix_C:")
for i in range(300, 310):  # Mostrar los valores de matrix_C
    print(f"matrix_C[{i-300}] = {processor.memory[i]}")

# Calcular los valores solicitados
latencia_promedio = processor.total_cycles / processor.instructions_executed
cpi = processor.total_cycles / processor.instructions_executed
ipc = processor.instructions_executed / processor.total_cycles
tiempo_total = processor.total_cycles

# Mostrar los resultados
print(f"\nLatencia promedio: {latencia_promedio:.2f}")
print(f"Tiempo total de ejecución: {tiempo_total} ciclos")
print(f"CPI (Cycles Per Instruction): {cpi:.2f}")
print(f"IPC (Instructions Per Cycle): {ipc:.2f}")
