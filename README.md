# Forge

**Forge** is a self-hosting systems programming language that combines the power of assembly with the clarity of Python-like syntax and formal safety guarantees. It compiles directly to native x86_64 machine code (ELF64) with minimal footprint — no VM, no runtime overhead.

---

## Philosophy

Forge is designed for two domains at the frontier of systems programming:

- **Reverse Engineering** — binary layout matching, bi-directional IR, and precise control over memory representation.
- **Artificial Intelligence** — local-first context, JSON-AST streaming, and infrastructure for distributed compilation workloads.

---

## Bootstrap Pipeline

Forge achieves self-hosting through a three-stage bootstrap:

| Stage | Language | Description |
|-------|----------|-------------|
| **Stage 0** | C | Minimal compiler: lexer with indentation tracking, recursive descent parser, opcode IR, and x86_64 codegen emitting ELF64 binaries directly. |
| **Stage 1** | Forge-Sub | A restricted subset of Forge, compiled by Stage 0, capable of parsing and compiling the full language. |
| **Stage 2** | Full Forge | The complete self-hosting compiler — Forge compiles itself. |

---

## Syntax

Forge uses the **off-side rule** (indentation-based block structure), familiar to users of Python. Control flow, function definitions, and type annotations rely on consistent indentation rather than braces or keywords.

```
func main() -> int
    print("Hello from Forge")
    return 0
```

---

## Safety Model

Forge provides four safety annotations that let the programmer explicitly declare the contract for each function or block:

| Annotation | Meaning |
|------------|---------|
| `safety(pure)` | No side effects; deterministic, referentially transparent. |
| `safety(bounded)` | Operates within a fixed memory region; bounds-checked. |
| `safety(hardware)` | Direct hardware access; unchecked by design. |
| `safety(unbounded)` | No safety guarantees; full programmer responsibility. |

---

## Stage 0 Compiler Internals

The Stage 0 compiler, written in C, includes:

- **Lexer** — tokenizes source with full indentation tracking (dedent/indent tokens).
- **Parser** — recursive descent, producing an AST directly.
- **Intermediate Representation** — opcode-based IR suitable for analysis and optimization.
- **Code Generator** — emits x86_64 machine code and packages it as an ELF64 binary, writing all sections (text, data, rodata, symtab, strtab) and the program header table directly.

---

## Subagent Architecture

Forge includes a built-in **subagent** system — 100 lightweight agents that coordinate for distributed compilation, static analysis, and parallel code generation, enabling rapid iteration on large codebases.

---

## Getting Started

Building Forge requires:

- A C compiler (Clang or GCC)
- `make`
- `nasm` (for assembler-level verification)

### Build Stage 0

```
make stage0
```

### Bootstrap to Stage 1

```
./stage0 examples/forge_sub.fg -o stage1
```

### Full Self-Hosted Build

```
./stage1 examples/full_forge.fg -o forge
./forge examples/hello.fg -o hello
./hello
```

---

## License

MIT
