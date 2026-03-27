# 🐈 CatArch: Layered Computing Ecosystem

![CatArch Logo](assets/logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CatArch](https://img.shields.io/badge/Architecture-CatArch-blue)](https://ctlang.netlify.app)
[![VM](https://img.shields.io/badge/VM-CatVM-green)](https://ctlang.netlify.app)

**CatArch** is organized into logical layers, following the "7 Circles" philosophy of the CAT system.

## 📂 Repository Structure

- **`asm/`**: The Foundation (Layer 0 & 1).
  - **`casm/`**: CatArch Assembler (`casm.py`, `casm.casm`).
  - **`cvm/`**: CatArch Virtual Machine (`cvm.py`, `cvm.c`).
- **`cl/`**: Circle 1 — Raw Machine Code Compiler.
- **`csl/`**: Circle 2 — System-Level Language.
- **`cvsl/`**: Circle 3 — Portable Assembly (Current Focus).
- **`libraries/`**: Standard and Third-Party Libraries (Future).
- **`assets/`**: Visual branding and logos.

## 🚀 Vision
The goal is a fully self-hosted, dependency-free toolchain. Each layer is built using the tools provided by the previous layer.

## 🛠️ Getting Started
```bash
# Example: Build the native VM
gcc asm/cvm/cvm.c -o bin/cvm

# Example: Run the self-hosted assembler
./bin/cvm asm/casm/casm.bin < my_prog.casm > my_prog.bin
```

## 🌐 Official Website
For more information, visit: **[ctlang.netlify.app](https://ctlang.netlify.app)**
