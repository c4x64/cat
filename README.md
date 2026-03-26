# cL - Circle 1 of the CAT Language Ecosystem

cL is not a programming language.
cL IS machine code with human-readable annotations.

## The 7 Circles

cL is the foundation. Everything else is built on it.

1. **cL** - Raw machine code (you are here)
2. **cSL** - Named registers, basic types
3. **cVSL** - Portable assembly
4. **CAT** - C replacement
5. **CatS** - Rust replacement
6. **CatVS** - Python replacement
7. **CatVVS** - English-like DSL

## Features (exactly 5)

1. Hex bytes: `48 C7 C0 01 00 00 00`
2. Comments: `# this is a comment`
3. Labels: `:label_name`
4. References: `{label_name}`
5. Strings: `"Hello\n"`

## Usage

```bash
python clc.py hello.cl -o hello
./hello
```

Why?
Because the first assemblers were written in machine code.
We start from the ground and build up.
No external dependencies. No cheating.
Pure from raw bytes to high-level language.
