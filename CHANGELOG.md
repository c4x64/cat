# Changelog

All notable changes to the Forge project will be documented in this file.

## [0.1.0] — 2026-06-02

### Added

- Stage 0 compiler in C: lexer, parser, codegen (opcode IR → x86_64), ELF64 writer
- Lexer with indentation tracking (Python-style off-side rule), keywords, string literals
- Recursive descent parser for Forge-Sub grammar: functions, asm blocks, if/while/for, data declarations
- Codegen: IR → x86_64 machine code with ELF64 direct output (no external linker)
- Exit syscall example (47 bytes code, 175 bytes ELF binary)
- Hello World example with string data and RIP-relative LEA (92 bytes code, 220 bytes ELF binary)
- Fibonacci with recursive function calls in asm blocks (128 bytes code, 256 bytes ELF binary)
- Data declarations (:name "string") with forward-reference label resolution
- Function call codegen (N_CALL → IR_CALL → call rel32)
- Label resolution for jumps and calls across asm blocks and functions
- 100 subagents for distributed compilation and parallel analysis
- Clean build with zero compiler warnings
