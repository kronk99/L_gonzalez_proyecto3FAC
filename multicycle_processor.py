from memory import Memory
from register_file import RegisterFile

class MulticycleProcessor:
    def __init__(self):
        self.pc = 0
        self.memory = Memory()
        self.registers = RegisterFile()
        self.state = 'Fetch'
        self.instruction = None
        self.alu_out = 0
        self.data_reg = 0

        # Adding test instructions (example)
        self.memory.write(0, 0x20100001)  # ADDI $t0, $zero, 1 (t0 = 1)
        self.memory.write(4, 0x20110002)  # ADDI $t1, $zero, 2 (t1 = 2)
        self.memory.write(8, 0x02094020)  # ADD $t0, $t0, $t1 (t0 = t0 + t1)
    
    def reset(self):
        self.pc = 0
        self.state = 'Fetch'
        self.instruction = None
    
    def fetch_instruction(self):
        try:
            self.instruction = self.memory.read(self.pc)
            self.pc += 4
            self.state = 'Decode'
        except IndexError as e:
            print(e)
            self.state = 'Fetch'  # Volver al estado Fetch si hay un error de lectura
    
    def decode_instruction(self):
        opcode = (self.instruction >> 26) & 0x3F
        if opcode == 0x23:  # LDR
            self.state = 'MemAdr'
        elif opcode == 0x2B:  # STR
            self.state = 'MemAdr'
        elif opcode == 0x00:  # R-type
            self.state = 'ExecuteR'
        elif opcode == 0x04:  # Branch
            self.state = 'Branch'
        else:
            self.state = 'Fetch'  # No operation for now
    
    def mem_adr(self):
        base_reg = (self.instruction >> 21) & 0x1F
        offset = self.instruction & 0xFFFF
        self.alu_out = self.registers.read(base_reg) + offset
        opcode = (self.instruction >> 26) & 0x3F
        if opcode == 0x23:  # LDR
            self.state = 'MemRead'
        elif opcode == 0x2B:  # STR
            self.state = 'MemWrite'
    
    def mem_read(self):
        try:
            self.data_reg = self.memory.read(self.alu_out)
            self.state = 'MemWB'
        except IndexError as e:
            print(e)
            self.state = 'Fetch'
    
    def mem_write(self):
        base_reg = (self.instruction >> 16) & 0x1F
        try:
            self.memory.write(self.alu_out, self.registers.read(base_reg))
            self.state = 'Fetch'
        except IndexError as e:
            print(e)
            self.state = 'Fetch'
    
    def mem_wb(self):
        dest_reg = (self.instruction >> 16) & 0x1F
        self.registers.write(dest_reg, self.data_reg)
        self.state = 'Fetch'
    
    def execute_r(self):
        src_a = (self.instruction >> 21) & 0x1F
        src_b = (self.instruction >> 16) & 0x1F
        func = self.instruction & 0x3F
        if func == 0x20:  # ADD
            self.alu_out = self.registers.read(src_a) + self.registers.read(src_b)
        self.state = 'ALUWB'
    
    def execute_i(self):
        src = (self.instruction >> 21) & 0x1F
        imm = self.instruction & 0xFFFF
        self.alu_out = self.registers.read(src) + imm
        self.state = 'ALUWB'
    
    def alu_wb(self):
        dest_reg = (self.instruction >> 11) & 0x1F
        self.registers.write(dest_reg, self.alu_out)
        self.state = 'Fetch'
    
    def branch(self):
        offset = (self.instruction & 0xFFFF) << 2
        if self.registers.read(0) == self.registers.read((self.instruction >> 21) & 0x1F):
            self.pc += offset
        self.state = 'Fetch'
    
    def execute_cycle(self):
        if self.state == 'Fetch':
            self.fetch_instruction()
        elif self.state == 'Decode':
            self.decode_instruction()
        elif self.state == 'MemAdr':
            self.mem_adr()
        elif self.state == 'MemRead':
            self.mem_read()
        elif self.state == 'MemWrite':
            self.mem_write()
        elif self.state == 'MemWB':
            self.mem_wb()
        elif self.state == 'ExecuteR':
            self.execute_r()
        elif self.state == 'ExecuteI':
            self.execute_i()
        elif self.state == 'ALUWB':
            self.alu_wb()
        elif self.state == 'Branch':
            self.branch()
