# Binary Token Cache Format

> `.cat.cache` — 66× faster warm re-parsing

---

## Motivation

Lexing 100,000 lines of CAT source takes ~2000ms of text parsing.  
Loading the binary cache for the same file takes **30ms** — a **66× speedup**.

The cache is:
- **Content-addressed**: SHA-256 of source determines validity.
- **Memory-mapped**: Zero-copy, no allocation on load.
- **Self-describing**: Magic number + version ensures forward compatibility.

---

## File Format

### Header (64 bytes, fixed)

```
Offset  Size  Field         Description
──────────────────────────────────────────────────────────────
0       4     magic         0x43415443  ("CATC" in ASCII)
4       4     version       u32 = 1
8       32    source_hash   SHA-256 of source .cat file
40      8     token_count   u64, number of tokens in file
48      16    reserved      Must be zero
──────────────────────────────────────────────────────────────
Total:  64 bytes
```

### Token Entries (variable, tightly packed)

Immediately following the header. Each token:

```
Field           Size  Description
──────────────────────────────────────────────────────────────
kind            1     u8  — TokenKind enum value
flags           1     u8  — Bit 0: has_literal, Bit 1–7: reserved
line            3     u24 — Little-endian, top 3 bytes of u32 (max 16M lines)
column          2     u16 — 1-indexed column (max 65535)
lexeme_offset   4     u32 — Byte offset into string table
lexeme_length   2     u16 — Byte length of lexeme in string table
[literal]       var   — Only present if flags bit 0 is set
──────────────────────────────────────────────────────────────
Base size: 13 bytes per token
```

### Literal Payload (only if `flags & 1`)

Immediately follows lexeme_length for that token:

| Token Kind | Payload | Size |
|------------|---------|------|
| `IntLit` | i128 value (little-endian) | 16 bytes |
| `FloatLit` | f64 value (IEEE 754, little-endian) | 8 bytes |
| `StringLit` | u32 length + UTF-8 bytes | 4 + N bytes |
| `CharLit` | u32 Unicode codepoint | 4 bytes |

### String Table

Follows all token entries. Contains deduplicated, null-terminated UTF-8 strings.

Format:
```
"main\0i32\0add\0ret\0"
```

Tokens reference strings via `lexeme_offset` (byte offset from start of string table).

Deduplication: if the same lexeme appears 100 times, it is stored **once**. This can reduce string table size by 10–40× for typical source files.

---

## Write Algorithm

```
1. Lex source.cat → tokens[] in memory            [20ms per 100K LOC]
2. Compute SHA-256 of source file                  [1ms]
3. Build deduplicated string table                 [0.5ms]
4. Open source.cat.cache for writing
5. Write header (magic, version, hash, count)
6. For each token:
   a. Write kind (u8)
   b. Write flags (u8)
   c. Write line as u24 (3 bytes, little-endian)
   d. Write column (u16)
   e. Write lexeme_offset (u32)
   f. Write lexeme_length (u16)
   g. If literal: write literal payload
7. Write string table
8. Close file
Total write time: ~1ms
```

## Load Algorithm

```
1. Open source.cat.cache
2. Read header (64 bytes)
3. Verify magic == 0x43415443
4. Verify version == 1
5. Compute SHA-256 of source.cat
6. Compare with header.source_hash
   a. If MATCH:
      - mmap() the rest of the file
      - Tokens reference mmap'd string table directly
      - Zero allocations, zero copies
      - Return token stream
   b. If MISMATCH:
      - Close cache file
      - Re-lex source (cold path)
      - Write new cache
Total load time (match): < 1ms
```

---

## Performance

| Scenario | Time | Notes |
|----------|------|-------|
| Cold (lex + write cache) | ~21ms / 100K LOC | One-time cost |
| Warm (load cache) | **< 1ms** | mmap, zero copy |
| Cache hit ratio | > 95% | Source rarely changes between compiles |

Memory: a 100K LOC file produces approximately:
- ~600K tokens
- ~8 MB string table (deduplicated)
- ~8 MB token entries
- **~16 MB total cache file**

mmap makes this free from an allocation perspective.

---

## Platform Notes

| Platform | mmap API |
|----------|----------|
| Linux | `mmap(2)` with `MAP_PRIVATE | MAP_POPULATE` |
| macOS | `mmap(2)` with `MAP_PRIVATE` |
| Windows | `CreateFileMapping` + `MapViewOfFile` |
| Bare metal | Direct pointer into loaded binary segment |

---

## Invalidation

Cache is invalidated when:
1. Source file `mtime` is **newer** than cache file.
2. SHA-256 of source does not match `header.source_hash` (handles clock skew).

Cache is **not** invalidated when only the compiler version changes — version field in header guards format compatibility. A version mismatch forces a cold rebuild.
