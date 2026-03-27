import sys
import re
import struct

TYPE_A = ["ADD", "SUB", "MUL", "DIV", "MOD", "AND", "OR", "XOR"]
TYPE_B = ["MOVI", "ADDI", "LEA"]
TYPE_C = ["JMP", "JZ", "JNZ", "JE", "JNE", "JL", "JG", "JLE", "JGE"]
TYPE_D = ["LOAD", "STORE"]

OPCODES = {
    "NOP": 0x00, "MOV": 0x01, "MOVI": 0x02, "MOVHI": 0x03, "LOAD": 0x04, "STORE": 0x05,
    "ADD": 0x10, "SUB": 0x11, "MUL": 0x12, "DIV": 0x13, "MOD": 0x14,
    "ANDI": 0x2B, "SHLI": 0x29, "SHRI": 0x2A,
    "CMP": 0x30, "CMPI": 0x31,
    "JMP": 0x40, "JZ": 0x47, "JNZ": 0x48,
    "SYSCALL": 0xF0, "HALT": 0xFF
}

def parse_reg(r):
    return int(r.upper().replace("R", ""))

class AssemblerState:
    def __init__(self):
        self.pc = 0
        self.labels = {}
        self.clean_lines = []

def assemble(filename, outname):
    with open(filename, "r") as f: lines = f.readlines()
    state = AssemblerState()
    
    for line in lines:
        line = line.split("#")[0].strip()
        if not line: continue
        if line.endswith(":"):
            label_name = line.rstrip(":")
            state.labels[label_name] = state.pc
        else:
            state.clean_lines.append((state.pc, line))
            state.pc = state.pc + 4

    with open(outname, "wb") as f:
        for pc_now, line in state.clean_lines:
            parts = re.split(r'[,\s]+', line)
            mnemonic = parts[0].upper()
            opcode = OPCODES.get(mnemonic, 0)
            instr = 0
            if mnemonic in TYPE_A:
                rd = parse_reg(parts[1]); rs1 = parse_reg(parts[2]); rs2 = parse_reg(parts[3])
                instr = (opcode << 24) | (rd << 16) | (rs1 << 8) | rs2
            elif mnemonic in TYPE_B:
                rd = parse_reg(parts[1])
                if parts[2] in state.labels: imm = state.labels[parts[2]] - pc_now
                else: imm = int(parts[2], 0)
                instr = (opcode << 24) | (rd << 16) | (imm & 0xFFFF)
            elif mnemonic in TYPE_C:
                target = state.labels[parts[1]]
                off = target - pc_now
                instr = (opcode << 24) | (off & 0xFFFFFF)
            elif mnemonic in TYPE_D:
                if mnemonic == "LOAD":
                    rd = parse_reg(parts[1])
                    m = re.search(r'\[R(\d+)\+?(-?\d+)?\]', parts[2].upper())
                    if m:
                        rs1 = int(m.group(1)); off = int(m.group(2) or 0)
                    else:
                        rs1 = 0; off = 0
                else:
                    m = re.search(r'\[R(\d+)\+?(-?\d+)?\]', parts[1].upper())
                    if m:
                        rs1 = int(m.group(1)); off = int(m.group(2) or 0)
                    else:
                        rs1 = 0; off = 0
                    rd = parse_reg(parts[2])
                instr = (opcode << 24) | (rd << 16) | (rs1 << 8) | (off & 0xFF)
            elif mnemonic == "MOVI":
                rd = parse_reg(parts[1]); imm = int(parts[2], 0)
                instr = (opcode << 24) | (rd << 16) | (imm & 0xFFFF)
            elif mnemonic == "SYSCALL": instr = (opcode << 24)
            elif mnemonic == "HALT": instr = (opcode << 24)
            
            f.write(struct.pack('<I', instr))

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(1)
    assemble(sys.argv[1], sys.argv[2])
