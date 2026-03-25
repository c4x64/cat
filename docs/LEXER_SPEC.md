# CAT Lexer Specification

> **Version 1.0.0** | Phase 1 of the CAT compiler

---

## Overview

The CAT lexer transforms raw source text into a flat stream of tokens. It is designed for maximum throughput — targeting **10 million tokens/second** on modern hardware with SIMD acceleration and zero heap allocations per token.

---

## Token Kinds

### Keywords

| Token | Lexeme | Description |
|-------|--------|-------------|
| `Fn` | `fn` | Function declaration |
| `Type` | `type` | Type/struct declaration |
| `Const` | `const` | Compile-time constant |
| `Global` | `global` | Module-level variable |
| `Local` | `local` | Stack variable |
| `Import` | `import` | Module import |
| `Export` | `export` | Symbol export |
| `If` | `if` | Conditional |
| `Else` | `else` | Else branch |
| `While` | `while` | While loop |
| `For` | `for` | For loop |
| `Return` | `return` | Explicit return (high-level) |
| `Break` | `break` | Break from loop |
| `Continue` | `continue` | Continue loop |
| `True` | `true` | Boolean true |
| `False` | `false` | Boolean false |
| `Null` | `null` | Null pointer |

### Built-in Types

| Token | Lexeme |
|-------|--------|
| `I8`–`I128` | `i8`, `i16`, `i32`, `i64`, `i128` |
| `U8`–`U128` | `u8`, `u16`, `u32`, `u64`, `u128` |
| `F32`, `F64` | `f32`, `f64` |
| `Bool` | `bool` |
| `Void` | `void` |
| `Ptr` | `ptr` |

Note: Arbitrary-width bit types `u1`–`u7`, `i1`–`i7` are parsed as `IntLit` suffix types rather than keywords.

### Instructions

| Group | Tokens |
|-------|--------|
| Data move | `Mov`, `Lea` |
| Arithmetic | `Add`, `Sub`, `Mul`, `Div`, `Mod`, `Neg` |
| Bitwise | `And`, `Orr`, `Xor`, `Not`, `Shl`, `Shr`, `Sar`, `Rol`, `Ror` |
| Compare | `Cmp`, `Ceq`, `Cne`, `Clt`, `Cle`, `Cgt`, `Cge` |
| Branch | `Jmp`, `Je`, `Jne`, `Jl`, `Jle`, `Jg`, `Jge`, `Jz`, `Jnz` |
| Call | `Call`, `Ret`, `Sel` |

### Directives

Directives start with `@`. Lexed as a single `Directive` token. The lexeme includes the `@` prefix.

Examples: `@inline`, `@static`, `@packed`, `@align`, `@comptime`, `@interrupt`, `@extern`, `@export`, `@register`, `@mmio`, `@cpuid`, `@rdtsc`, `@rdmsr`, `@wrmsr`, `@rdpmc`, `@inb`, `@inw`, `@inl`, `@outb`, `@outw`, `@outl`, `@cli`, `@sti`, `@hlt`, `@lfence`, `@sfence`, `@mfence`, `@atomic_load`, `@atomic_store`, `@atomic_add`, `@atomic_sub`, `@atomic_swap`, `@atomic_cas`, `@atomic_fence_acquire`, `@atomic_fence_release`, `@atomic_fence_seq_cst`, `@simd_load`, `@simd_store`, `@simd_add`, `@simd_sub`, `@simd_mul`, `@simd_div`, `@simd_fma`, `@simd_dot`, `@simd_sqrt`, `@read_cr0`, `@write_cr0`, `@read_cr2`, `@read_cr3`, `@write_cr3`, `@read_cr4`, `@write_cr4`, `@invlpg`, `@invlpgb`.

Unknown `@name` identifiers are also lexed as `Directive` — the parser validates which are legal.

### Flags

| Token | Lexeme | Description |
|-------|--------|-------------|
| `Flag` | `&c4` | Unsafe hot-reload mode marker |

### Symbols

| Token | Lexeme |
|-------|--------|
| `LParen` | `(` |
| `RParen` | `)` |
| `LBrace` | `{` |
| `RBrace` | `}` |
| `LBracket` | `[` |
| `RBracket` | `]` |
| `Colon` | `:` |
| `Semi` | `;` |
| `Comma` | `,` |
| `Dot` | `.` |
| `Arrow` | `->` |
| `Walrus` | `:=` |
| `Assign` | `=` |
| `Eq` | `==` |
| `Ne` | `!=` |
| `Le` | `<=` |
| `Ge` | `>=` |
| `Lt` | `<` |
| `Gt` | `>` |
| `Shl` | `<<` |
| `Shr` | `>>` |
| `Plus` | `+` |
| `Minus` | `-` |
| `Star` | `*` |
| `Slash` | `/` |
| `Percent` | `%` |
| `Amp` | `&` |
| `Pipe` | `\|` |
| `Caret` | `^` |
| `Tilde` | `~` |
| `Bang` | `!` |
| `And` | `&&` |
| `Or` | `\|\|` |

### Literals

#### Integer Literals

Formats accepted:
- **Decimal**: `42`, `1_000_000`
- **Hexadecimal**: `0xFF`, `0x1A2B_CDEF`
- **Binary**: `0b1010`, `0b1111_0000`
- **Octal**: `0o755`, `0o644`

Optional type suffix (appended directly, no space):
- `42i8`, `255u8`, `65535u16`, `0xFF_FFu32`, `0xDEAD_BEEF_u64`

Underscores `_` may appear between digits for readability and are ignored.

#### Float Literals

- `3.14`, `2.5e10`, `1.5e-5`, `0.0`
- Optional suffix: `3.14f32`, `2.5f64`

#### String Literals

Delimited by double quotes. Supported escape sequences:

| Sequence | Meaning |
|----------|---------|
| `\n` | Newline (0x0A) |
| `\r` | Carriage return (0x0D) |
| `\t` | Tab (0x09) |
| `\\` | Backslash |
| `\"` | Double quote |
| `\0` | Null byte |
| `\xHH` | Hex byte (2 hex digits) |
| `\u{HHHHHH}` | Unicode codepoint (1-6 hex digits) |

#### Character Literals

Single Unicode codepoint in single quotes. Accepts same escape sequences as strings.

Examples: `'a'`, `'Z'`, `'\n'`, `'\x41'`, `'\u{03B1}'`

#### Comments

- **Single-line**: `# comment` — extends to end of line.
- **Multi-line**: `/* ... */` — may be nested: `/* outer /* inner */ still outer */`

Comments produce a `Comment` token (the parser discards them, but the cache records them for round-trip accuracy).

---

## Token Structure

```cat
type TokenKind = enum {
    # Keywords
    Fn, Type, Const, Global, Local, Import, Export,
    If, Else, While, For, Return, Break, Continue,
    True, False, Null,

    # Built-in types
    I8, I16, I32, I64, I128,
    U8, U16, U32, U64, U128,
    F32, F64, Bool, Void, Ptr,

    # Instructions
    Mov, Lea, Add, Sub, Mul, Div, Mod, Neg,
    And, Orr, Xor, Not, Shl, Shr, Sar, Rol, Ror,
    Cmp, Ceq, Cne, Clt, Cle, Cgt, Cge,
    Jmp, Je, Jne, Jl, Jle, Jg, Jge, Jz, Jnz,
    Call, Ret, Sel,

    # Special
    Directive,   # @name
    Flag,        # &c4

    # Symbols
    LParen, RParen, LBrace, RBrace, LBracket, RBracket,
    Colon, Semi, Comma, Dot, Arrow, Assign, Walrus,
    Eq, Ne, Lt, Gt, Le, Ge, Shl2, Shr2,
    Plus, Minus, Star, Slash, Percent,
    Amp, Pipe, Caret, Tilde, Bang, LgAnd, LgOr,

    # Literals
    Ident,
    IntLit,
    FloatLit,
    StringLit,
    CharLit,

    # Meta
    Comment,
    Eof,
    Error,
}

type Token = struct {
    kind:    TokenKind
    lexeme:  String        # Zero-copy view into source buffer
    line:    u32
    column:  u32
    literal: union {
        int_val:    i128   # All integer types fit in i128
        float_val:  f64
        string_val: String
        char_val:   u32    # Unicode codepoint
    }
}
```

---

## Formal Grammar (EBNF)

```ebnf
token        = keyword | type_kw | instruction | directive | flag
             | symbol | ident | int_lit | float_lit | string_lit
             | char_lit | comment | EOF

keyword      = "fn" | "type" | "const" | "global" | "local"
             | "import" | "export" | "if" | "else" | "while"
             | "for" | "return" | "break" | "continue"
             | "true" | "false" | "null"

type_kw      = "i8" | "i16" | "i32" | "i64" | "i128"
             | "u8" | "u16" | "u32" | "u64" | "u128"
             | "f32" | "f64" | "bool" | "void" | "ptr"

instruction  = "mov" | "lea" | "add" | "sub" | "mul" | "div" | "mod" | "neg"
             | "and" | "orr" | "xor" | "not" | "shl" | "shr" | "sar"
             | "rol" | "ror" | "cmp" | "ceq" | "cne" | "clt" | "cle"
             | "cgt" | "cge" | "jmp" | "je"  | "jne" | "jl"  | "jle"
             | "jg"  | "jge" | "jz"  | "jnz" | "call"| "ret" | "sel"

directive    = "@" ident
flag         = "&c4"

ident        = (letter | "_") { letter | digit | "_" }
letter       = [a-zA-Z]
digit        = [0-9]

int_lit      = dec_lit | hex_lit | bin_lit | oct_lit
dec_lit      = digit { digit | "_" } [ int_suffix ]
hex_lit      = "0x" hex_digit { hex_digit | "_" } [ int_suffix ]
bin_lit      = "0b" [01] { [01] | "_" } [ int_suffix ]
oct_lit      = "0o" [0-7] { [0-7] | "_" } [ int_suffix ]
int_suffix   = ("i" | "u") ("8"|"16"|"32"|"64"|"128")

float_lit    = digit { digit } "." { digit } [ exp ] [ float_suffix ]
exp          = ("e"|"E") ["+"|"-"] digit { digit }
float_suffix = "f32" | "f64"

string_lit   = '"' { str_char } '"'
str_char     = any_char_except_'"'_and_'\' | escape_seq
escape_seq   = '\' ( 'n'|'r'|'t'|'\'|'"'|'0' | 'x' hex2 | 'u{' hex_codepoint '}' )
hex2         = hex_digit hex_digit
hex_codepoint = hex_digit { hex_digit }   # 1-6 digits

char_lit     = "'" str_char "'"

comment      = "#" { any_char_except_newline } newline
             | "/*" { any | nested_comment } "*/"
nested_comment = "/*" { any | nested_comment } "*/"
```

---

## Lexer State Machine

```
START
 ├── whitespace           → skip, advance
 ├── '#'                  → LINE_COMMENT
 ├── '/' '*'              → BLOCK_COMMENT (depth=1)
 ├── '@'                  → DIRECTIVE (read ident)
 ├── '&'                  → check 'c4' → Flag, else Amp
 ├── '.'                  → check ident after → Label, else Dot
 ├── '"'                  → STRING
 ├── "'"                  → CHAR
 ├── '0' 'x'              → HEX_LIT
 ├── '0' 'b'              → BIN_LIT
 ├── '0' 'o'              → OCT_LIT
 ├── digit                → DEC_LIT (or FLOAT if '.' encountered)
 ├── letter | '_'         → IDENT_OR_KEYWORD
 ├── two-char symbol      → emit two-char token (==, :=, ->, <=, >=, <<, >>, &&, ||, !=)
 ├── one-char symbol      → emit one-char token
 └── EOF                  → Eof
```

---

## Error Handling

1. **Collect all errors** — Never stop on first error. Emit `Error` tokens, continue.
2. **Sync on newlines/semicolons/braces.**
3. **Error format:**

```
error: Unexpected character '$'
  --> kernel.cat:1:8
   |
 1 | fn bad$ example {
   |        ^ Invalid character
   |
help: Remove this character
```

Error categories:
- `E001` — Unexpected character
- `E002` — Unterminated string literal
- `E003` — Unterminated block comment
- `E004` — Invalid number format
- `E005` — Integer overflow (exceeds i128 range)
- `E006` — Invalid escape sequence
- `E007` — Invalid Unicode codepoint (> 0x10FFFF)
- `E008` — Empty character literal
- `E009` — Multi-character character literal
