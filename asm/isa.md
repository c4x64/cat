# CatArch ISA Specification (v1.0)
## Register File
- 256 general-purpose registers (R0-R255), 256-bit wide.
- R0: Hardwired to zero.
- R1: Return value.
- R2-R9: Function arguments.
- R254: Stack Pointer (SP).
- R255: Program Counter (PC).

## Instruction Format
- All instructions are 32-bit (4 bytes).
- Type A (reg-reg): [op:8][rd:8][rs1:8][rs2:8]
- Type B (reg-imm): [op:8][rd:8][imm16:16]
- Type C (branch): [op:8][cond:4][unused:4][off16:16] (PC-relative)
- Type D (memory): [op:8][rd:8][rs1:8][off8:8]

## Opcode Map (Partial)
- 0x01: MOV rd, rs
- 0x02: MOVI rd, imm16
- 0x04: LOAD rd, [rs+off]
- 0x05: STORE [rd+off], rs
- 0x10: ADD rd, rs1, rs2
- 0x30: CMP rd, rs1
- 0x48: JNZ off16
- 0xF0: SYSCALL
- 0xFF: HALT
