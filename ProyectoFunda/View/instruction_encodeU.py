# instruction_encode.py

registers = {
    'x0': 0, 'zero': 0, 'x1': 1, 'ra': 1, 'x2': 2, 'sp': 2, 'x3': 3, 'gp': 3, 'x4': 4, 'tp': 4,
    'x5': 5, 't0': 5, 'x6': 6, 't1': 6, 'x7': 7, 't2': 7, 'x8': 8, 's0': 8, 'fp': 8, 'x9': 9, 's1': 9,
    'x10': 10, 'a0': 10, 'x11': 11, 'a1': 11, 'x12': 12, 'a2': 12, 'x13': 13, 'a3': 13, 'x14': 14, 'a4': 14, 'x15': 15, 'a5': 15,
    'x16': 16, 'a6': 16, 'x17': 17, 'a7': 17, 'x18': 18, 's2': 18, 'x19': 19, 's3': 19, 'x20': 20, 's4': 20, 'x21': 21, 's5': 21,
    'x22': 22, 's6': 22, 'x23': 23, 's7': 23, 'x24': 24, 's8': 24, 'x25': 25, 's9': 25, 'x26': 26, 's10': 26, 'x27': 27, 's11': 27,
    'x28': 28, 't3': 28, 'x29': 29, 't4': 29, 'x30': 30, 't5': 30, 'x31': 31, 't6': 31
}

def parse_instruction(_instructions):
    _labels = {}
    _instrs = []
    _address = 0

    for _instr in _instructions:
        if ':' in _instr:
            _label, _instr = _instr.split(':')
            _label = _label.strip()
            _labels[_label] = _address
            _instr = _instr.strip()
        _instrs.append([_address, _instr])
        _address += 4
    return _labels, _instrs

def encode(_instructions):
    _labels, _instructions = parse_instruction(_instructions)
    _binary_instrs = []
    opcodes = {
        'lw':   ('0000011', '010', '0000000'),
        'sw':   ('0100011', '010', '0000000'),
        'addi': ('0010011', '000', '0000000'),
        'beq':  ('1100011', '000', '0000000'),
        'bne':  ('1100011', '001', '0000000'),
        'jal':  ('1101111', '000', '0000000'),
        'add':  ('0110011', '000', '0000001'),
        'sub':  ('0110011', '000', '0100000'),
        'slt':  ('0110011', '010', '0000000'),
        'or':   ('0110011', '110', '0000000'),
        'and':  ('0110011', '111', '0000000'),
        'mul':  ('0110011', '000', '0000000')
    }

    for _instr in _instructions:
        parts = _instr[1].split()
        opcode, f3, f7 = opcodes.get(parts[0], (None, None, None))
        if not opcode:
            print(f"Error: Opcode no reconocido '{parts[0]}' en la instrucción '{_instr[1]}'")
            continue

        if parts[0] == 'addi':
            try:
                rd = parts[1].strip(',')
                rs1 = parts[2].strip(',')
                imm = int(parts[3])
                rd_bin = format(registers[rd], '05b')
                rs1_bin = format(registers[rs1], '05b')
                imm_bin = format(imm & 0xFFF, '012b')  # Inmediato de 12 bits
                binary_instruction = imm_bin + rs1_bin + f3 + rd_bin + opcode
            except ValueError as e:
                print(f"Error decodificando instrucción '{_instr[1]}': {e}")
                continue

        elif parts[0] == 'lw':
            try:
                rd = parts[1].strip(',')
                offset, rs1 = parts[2].split('(')
                rs1 = rs1.strip(')')
                imm = int(offset)
                rd_bin = format(registers[rd], '05b')
                rs1_bin = format(registers[rs1], '05b')
                imm_bin = format(imm & 0xFFF, '012b')
                binary_instruction = imm_bin + rs1_bin + f3 + rd_bin + opcode
            except ValueError as e:
                print(f"Error decodificando instrucción '{_instr[1]}': {e}")
                continue

        elif parts[0] == 'sw':
            try:
                rs2 = parts[1].strip(',')
                offset, rs1 = parts[2].split('(')
                rs1 = rs1.strip(')')
                imm = int(offset)
                rs2_bin = format(registers[rs2], '05b')
                rs1_bin = format(registers[rs1], '05b')
                imm_bin = format(imm & 0xFFF, '012b')
                imm_bin_upper = imm_bin[:7]
                imm_bin_lower = imm_bin[7:]
                binary_instruction = imm_bin_upper + rs2_bin + rs1_bin + f3 + imm_bin_lower + opcode
            except ValueError as e:
                print(f"Error decodificando instrucción '{_instr[1]}': {e}")
                continue

        elif parts[0] in {'add', 'sub', 'slt', 'or', 'and', 'mul'}:
            try:
                rd = parts[1].strip(',')
                rs1 = parts[2].strip(',')
                rs2 = parts[3].strip(',')
                rd_bin = format(registers[rd], '05b')
                rs1_bin = format(registers[rs1], '05b')
                rs2_bin = format(registers[rs2], '05b')
                binary_instruction = f7 + rs2_bin + rs1_bin + f3 + rd_bin + opcode
            except KeyError as e:
                print(f"Error decodificando instrucción '{_instr[1]}': {e}")
                continue

        elif parts[0] in {'beq', 'bne'}:
            try:
                rs1 = parts[1].strip(',')
                rs2 = parts[2].strip(',')
                offset = parts[3]
                rs1_bin = format(registers[rs1], '05b')
                rs2_bin = format(registers[rs2], '05b')
                imm = _labels[offset] - _instr[0] - 4
                imm_bin = format(imm, '013b')
                imm_bin = imm_bin[0] + imm_bin[2:8] + imm_bin[8:12] + imm_bin[1]
                binary_instruction = imm_bin[0] + imm_bin[1:7] + rs2_bin + rs1_bin + f3 + imm_bin[7:] + imm_bin[6] + opcode
            except KeyError as e:
                print(f"Error decodificando instrucción '{_instr[1]}': {e}")
                continue

        elif parts[0] == 'jal':
            try:
                rd = parts[1].strip(',')
                offset = parts[2]
                rd_bin = format(registers[rd], '05b')
                imm = _labels[offset] - _instr[0] - 4
                imm_bin = format(imm, '021b')
                imm_bin = imm_bin[0] + imm_bin[10:20] + imm_bin[9] + imm_bin[1:9] + '0'
                binary_instruction = imm_bin + rd_bin + opcode
            except KeyError as e:
                print(f"Error decodificando instrucción '{_instr[1]}': {e}")
                continue

        _binary_instrs.append(binary_instruction)

    return _binary_instrs, _labels, _instructions