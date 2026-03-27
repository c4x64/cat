#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define FLAG_ZERO 1
#define FLAG_NEG  2

typedef struct {
    uint64_t regs[256];
    uint8_t *mem;
    uint32_t mem_size;
    uint32_t flags;
    int halted;
} VM;

void vm_init(VM *vm, uint32_t size) {
    memset(vm->regs, 0, sizeof(vm->regs));
    vm->mem = calloc(size, 1);
    vm->mem_size = size;
    vm->regs[254] = size - 1024;
    vm->regs[255] = 0;
    vm->flags = 0;
    vm->halted = 0;
}

void vm_step(VM *vm) {
    uint32_t pc = (uint32_t)vm->regs[255];
    if (vm->halted || pc + 4 > vm->mem_size) { vm->halted = 1; return; }
    uint32_t instr = *(uint32_t*)(vm->mem + pc);
    uint8_t op = (instr >> 24) & 0xFF;
    uint8_t rd = (instr >> 16) & 0xFF;
    uint8_t rs1 = (instr >> 8) & 0xFF;
    uint8_t rs2 = instr & 0xFF;
    int16_t imm16 = (int16_t)(instr & 0xFFFF);
    uint32_t next_pc = pc + 4;
    int jumped = 0;

    switch (op) {
        case 0x01: vm->regs[rd] = vm->regs[rs1]; break;
        case 0x02: vm->regs[rd] = (int64_t)imm16; break;
        case 0x04: {
            uint32_t addr = (uint32_t)(vm->regs[rs1] + (int8_t)rs2) & 0xFFFFFF;
            vm->regs[rd] = *(uint64_t*)(vm->mem + addr);
            break;
        }
        case 0x05: {
            uint32_t addr = (uint32_t)(vm->regs[rs1] + (int8_t)rs2) & 0xFFFFFF;
            *(uint64_t*)(vm->mem + addr) = vm->regs[rd];
            break;
        }
        case 0x10: vm->regs[rd] = vm->regs[rs1] + vm->regs[rs2]; break;
        case 0x2B: vm->regs[rd] = vm->regs[rs1] & rs2; break;
        case 0x30: {
            int64_t res = (int64_t)vm->regs[rd] - (int64_t)vm->regs[rs1];
            vm->flags = 0;
            if (res == 0) vm->flags |= FLAG_ZERO;
            if (res < 0) vm->flags |= FLAG_NEG;
            break;
        }
        case 0x48: if (!(vm->flags & FLAG_ZERO)) { next_pc = pc + imm16; jumped = 1; } break;
        case 0xF0: {
            if (vm->regs[0] == 0) vm->regs[1] = fread(vm->mem + (vm->regs[5] & 0xFFFFFF), 1, vm->regs[3], stdin);
            else if (vm->regs[0] == 1) { 
                vm->regs[1] = fwrite(vm->mem + (vm->regs[5] & 0xFFFFFF), 1, vm->regs[3], stdout);
                fflush(stdout);
            }
            else if (vm->regs[0] == 60) vm->halted = 1;
            break;
        }
        case 0xFF: vm->halted = 1; break;
    }
    if (!vm->halted) vm->regs[255] = next_pc;
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    VM vm; vm_init(&vm, 0x1000000);
    fread(vm.mem, 1, 0x1000000, f); fclose(f);
    while (!vm.halted) vm_step(&vm);
    return 0;
}
