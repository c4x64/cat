# cVSL: Portable Assembly Specification (v1.0)

`cVSL` is the third circle of the CAT ecosystem. It provides a portable, architecture-independent assembly language that can be compiled to native machine code (CatArch, x86-64, etc.).

## 🔑 Core Concepts

### 1. Unified Registers
Instead of architecture-specific names (like `R10` or `RAX`), cVSL uses:
- `v0` - `v255`: Virtual general-purpose registers.
- `sp`: Virtual stack pointer.
- `pc`: Virtual program counter.

### 2. Variable Mapping
cVSL supports declaring virtual registers as named variables:
```cvsl
var count = v10
var ptr = v11
```

### 3. Abstract Stack operations
`push` and `pop` are standardized and don't require manual stack pointer manipulation.

### 4. Function Blocks
Functions are defined with clear boundaries:
```cvsl
func main:
    mov v0, 42
    ret
endfunc
```

## 🛠️ Instruction Mappings (Universal)
- `mov dst, src`
- `add dst, src1, src2`
- `load dst, [ptr+off]`
- `store [ptr+off], src`
- `call label`
- `ret`
- `syscall`

## 🎯 Target Backends
- **CatArch**: Compiles direct to 32-bit CatArch instructions.
- **x86-64**: Future support for native Linux/Windows ELFs.
