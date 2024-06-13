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

    def fetch(self):
        self.IR = self.memory[self.PC]
        self.PC += 1
        self.state = "ID"
        self.instruction = f"Fetch: {self.IR:032b}"
        self.current_cycle += 1

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
        else:
            self.instruction = "Decode: Instrucción no soportada"

        self.state = "EX"
        self.current_cycle += 1

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
        else:
            self.state = "IF"  # Estado por defecto para instrucciones no soportadas
        self.instruction = f"Execute: {self.instruction.split(': ')[1]}"
        self.current_cycle += 1

    def memory_access(self):
        if self.opcode == 0x03:  # LW
            self.result = self.memory[self.address]
        self.state = "WB"
        self.current_cycle += 1

    def write_back(self):
        if self.opcode in [0x33, 0x13, 0x03]:  # Instrucciones tipo R e I
            self.registers[self.rd] = self.result
        self.state = "IF"
        self.instruction = f"Write Back: {self.instruction.split(': ')[1]}"
        self.current_cycle += 1

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
            print(f"Cycle: {self.current_cycle}, PC: {self.PC}, State: {self.state}")
            print(f"Registers: {self.registers[:4]}")  # Mostrar los primeros 4 registros
            print(f"Instruction: {self.instruction}")
            print("-" * 40)

    def load_program(self, program):
        for i in range(len(program)):
            self.memory[i] = program[i]
        self.program_size = len(program)

# Programa de prueba (código de ejemplo en formato binario)
program = [
    0b00000000000100000000000010010011,  # ADDI x1, x0, 1
    0b00000000001000000000000100010011,  # ADDI x2, x0, 2
    0b00000000001000010000000110110011,  # ADD x3, x2, x1
    0b00000000001100010000001000000011   # LW x4, 3(x2)
]

# Crear el procesador y cargar el programa
processor = Processor()
processor.load_program(program)

# Inicialización de la memoria con algunos valores para probar LW
processor.memory[5] = 42  # Almacenar el valor 42 en la dirección de memoria 5 (para LW)

# Verificar que el programa y la memoria se hayan cargado correctamente
print("Memoria cargada con el programa:")
for i in range(len(program)):
    print(f"Mem[{i}] = {processor.memory[i]:032b}")

print("\nMemoria inicial:")
for i in range(10):  # Mostrar los primeros 10 valores de la memoria para verificar
    print(f"Mem[{i}] = {processor.memory[i]}")

# Ejecutar el ciclo de instrucción
processor.run_cycle()

# Imprimir el estado final de todos los registros
print("\nEstado final de los registros:")
for i in range(8):  # Mostrar los primeros 8 registros para verificar
    print(f"x{i} = {processor.registers[i]}")
