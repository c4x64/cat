# 🐈 CatArch: The Future of Minimalist Computing

![CatArch Logo](cat-arch/assets/logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CatArch](https://img.shields.io/badge/Architecture-CatArch-blue)](https://ctlang.netlify.app)
[![VM](https://img.shields.io/badge/VM-CatVM-green)](https://ctlang.netlify.app)

**CatArch** is a precision-engineered 32-bit RISC instruction set designed for the next generation of high-performance compilers. It eliminates legacy bloat, focusing on a massive 256-register file and a clean, orthogonal design.

## 🚀 Vision
The goal of the CatArch project is to provide a fully self-hosted, architecture-agnostic foundation for the **CAT Programming Language**.

## 🏗️ Architecture Specifications
- **Register File**: 256 general-purpose registers (`R0`-`R255`), 256-bit wide each.
- **Memory Model**: Flat 48-bit address space.
- **Instruction Format**: Fixed 32-bit width for maximum throughput.
- **Sysem Calls**: Native support for Linux-style I/O operations.

## 🛠️ Getting Started (Self-Hosting)
CatArch is designed to be self-sufficient. You can build the native Virtual Machine and use the self-hosted assembler without any external dependencies.

### 1. Build the Native VM
```bash
gcc cat-arch/vm/cvm.c -o cvm
```

### 2. Assemble a Program
```bash
./cvm cat-arch/asm/casm.bin < my_prog.casm > my_prog.bin
```

### 3. Run the Program
```bash
./cvm my_prog.bin
```

## 🌐 Official Website
For more information, documentation, and the full CAT specification, visit:
**[ctlang.netlify.app](https://ctlang.netlify.app)**

---
*Built with ❤️ for the future of computing.*
