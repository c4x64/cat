# Contributing to CAT

Thank you for your interest in building the world's fastest systems programming language.

## Philosophy

Every contribution must honor CAT's core promise:

> **Zero compromises. Performance is the ONLY goal.**

---

## How to Contribute

### Reporting Bugs

Open an issue with:
1. Exact input that triggered the bug
2. Expected output vs actual output
3. OS and architecture

### Submitting a Change

1. Fork the repository
2. Create a branch: `git checkout -b feat/my-change`
3. Follow code style (see below)
4. Write tests for your change
5. Submit a pull request

---

## Code Style

- **4-space indentation** (no tabs)
- **snake_case** for functions and local variables
- **PascalCase** for types and enums
- **SCREAMING_SNAKE_CASE** for constants
- **Comments explain WHY, not WHAT**
- Zero compiler warnings permitted
- Zero undefined behavior permitted

---

## Performance Requirements

Any change that regresses performance will not be merged.

| Benchmark | Minimum |
|-----------|---------|
| Lex 100K LOC (cold) | < 500ms |
| Lex 100K LOC (warm) | < 1ms |
| Peak RAM (100K LOC) | < 50 MB |
| Throughput | > 10M tokens/sec |

---

## Testing

Every change must:
- Pass all existing tests in `tests/test_lexer.cat`
- Add new tests covering new behavior
- Not regress benchmarks in `tests/benchmark_lexer.cat`

---

## License

By contributing, you agree your contributions will be licensed under MIT.
