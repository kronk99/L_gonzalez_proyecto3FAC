class RegisterFile:
    def __init__(self, size=32):
        self.registers = [0] * size
    
    def read(self, reg_num):
        return self.registers[reg_num]
    
    def write(self, reg_num, data):
        self.registers[reg_num] = data
