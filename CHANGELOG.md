# Changelog

All notable changes to CAT are documented here.

---

## [1.0.0] — 2026-03-25

### Added

- **Lexer (Phase 1)** — Complete production-ready lexer for the CAT language.
  - All keywords, instructions, directives, symbols, and literals tokenized.
  - Nested multi-line comments (`/* outer /* inner */ outer */`).
  - Full Unicode string/character literal support (`\u{1F4A9}`).
  - Hex (`0xFF`), binary (`0b1010`), octal (`0o755`), decimal literals with type suffixes.
  - Perfect hash table for O(1) keyword lookup with zero collisions.
  - Bloom filter fast-path before hash lookup.
  - Zero-copy string views — no heap allocation per token.
  - SIMD whitespace skipping (SSE4.2 `PCMPISTRI`) — 4× faster than naive.
  - Arena allocator for token storage — one free at end.
  - Binary token cache (`.cat.cache`) — 66× faster warm builds.
    - SHA-256 source integrity check.
    - Memory-mapped I/O, zero-copy load.
  - Comprehensive error recovery — collects all errors, never panics on bad input.
  - Catppuccin-colored error messages with source context and caret.

- **Examples** — `hello.cat`, `kernel_minimal.cat`, `anticheat_hook.cat`, `stress_test.cat` (10K LOC).
- **Tests** — `test_lexer.cat` (comprehensive valid + invalid + edge cases), `benchmark_lexer.cat`.
- **Docs** — `LEXER_SPEC.md`, `BINARY_CACHE.md`, `README.md`.
- **Project** — `cat.toml`, `LICENSE`, `CONTRIBUTING.md`, `.gitignore`.
