class Register:
    def __init__(self, size):
        self.register_names = [f"R{i}" for i in range(size)]
        self.registers = [0] * size

    def read(self, index):
        return self.registers[index]

    def write(self, index, value):
        self.registers[index] = value

    def initialize(self):
        self.registers = list(range(len(self.registers)))

    def display(self):
        return {name: self.registers[i] for i, name in enumerate(self.register_names)}
