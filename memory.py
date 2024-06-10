class Memory:
    def __init__(self, size=1024):
        self.memory = [0] * size
    
    def read(self, address):
        if 0 <= address < len(self.memory):
            return self.memory[address]
        else:
            raise IndexError(f"Memory read error: address {address} out of range")
    
    def write(self, address, data):
        if 0 <= address < len(self.memory):
            self.memory[address] = data
        else:
            raise IndexError(f"Memory write error: address {address} out of range")
