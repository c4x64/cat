import sys
import struct

FLAG_ZERO = 1
FLAG_NEG = 2

def sex8(v): return ((v + 0x80) & 0xFF) - 0x80
def sex16(v): return ((v + 0x8000) & 0xFFFF) - 0x8000

class CatVM:
    def __init__(self, mem_size=16*1024*1024):
        self.regs = [0] * 256
        self.mem = bytearray(mem_size)
        self.mask = (1 << 256) - 1
        self.flags = 0
        self.halted = False
        self.regs[254] = mem_size - 1024 # SP

    def load(self, prog):
        for i in range(len(prog)):
            self.mem[i] = prog[i]

    def run(self):
        while not self.halted:
            self.step()

    def step(self):
        pc_val = self.regs[255]
        if pc_val + 4 > len(self.mem): self.halted = True; return
        instr = struct.unpack_from('<I', self.mem, int(pc_val))[0]
        op = (instr >> 24) & 0xFF
        rd = (instr >> 16) & 0xFF
        rs1 = (instr >> 8) & 0xFF
        rs2 = instr & 0xFF
        imm16 = instr & 0xFFFF

        next_pc = (pc_val + 4) & self.mask; jumped = False
        if op == 0x00: pass
        elif op == 0x01: self.regs[rd] = self.regs[rs1]
        elif op == 0x02: self.regs[rd] = sex16(imm16) & self.mask
        elif op == 0x04:
            addr = int((self.regs[rs1] + sex8(rs2)) & 0xFFFFFF)
            self.regs[rd] = struct.unpack_from('<Q', self.mem, addr)[0]
        elif op == 0x05:
            addr = int((self.regs[rs1] + sex8(rs2)) & 0xFFFFFF)
            struct.pack_into('<Q', self.mem, addr, int(self.regs[rd] & ((1<<64)-1)))
        elif op == 0x10: self.regs[rd] = (self.regs[rs1] + self.regs[rs2]) & self.mask
        elif op == 0x2B: self.regs[rd] = (self.regs[rs1] & rs2) & self.mask
        elif op == 0x29: self.regs[rd] = (self.regs[rs1] << (rs2 & 0xFF)) & self.mask
        elif op == 0x30:
            res = self.regs[rd] - self.regs[rs1]
            self.flags = 0
            if res == 0: self.flags |= FLAG_ZERO
            if res < 0: self.flags |= FLAG_NEG
        elif op == 0x48:
            if not (self.flags & FLAG_ZERO):
                next_pc = (pc_val + sex16(imm16)) & self.mask; jumped = True
        elif op == 0xF0:
            sys_num = self.regs[0]
            if sys_num == 0:
                data = sys.stdin.buffer.read(int(self.regs[3]))
                addr = int(self.regs[5] & 0xFFFFFF)
                for i in range(len(data)):
                    self.mem[addr + i] = data[i]
                self.regs[1] = len(data)
            elif sys_num == 1:
                addr = int(self.regs[5] & 0xFFFFFF)
                length = int(self.regs[3])
                data_list = []
                for i in range(length):
                    data_list.append(self.mem[addr + i])
                data_bytes = bytes(data_list)
                sys.stdout.buffer.write(data_bytes); sys.stdout.buffer.flush()
                self.regs[1] = len(data_bytes)
            elif sys_num == 60: self.halted = True
        elif op == 0xFF: self.halted = True
        
        if not self.halted: self.regs[255] = next_pc
        else:
            # Print success if R3 is 1
            if self.regs[3] == 1: print("SUCCESS: R3 = 1")
            else: print(f"HALTED: R3 = {self.regs[3]}")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    with open(sys.argv[1], "rb") as f: prog = f.read()
    vm = CatVM(); vm.load(prog); vm.run()
