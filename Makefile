# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CAT Compiler — Makefile
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CC      ?= gcc
CFLAGS  ?= -O2 -Wall -Wextra -std=c11
SRC_DIR  = src
BUILD_DIR = build
BIN_DIR  = bin

.PHONY: all bootstrap build clean hello test benchmark check

# Default target
all: bootstrap

# ── Bootstrap ─────────────────────────────────────
# Phase 1: Compile the C bootstrap stub into catc
bootstrap:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🔥 CAT COMPILER BOOTSTRAP"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@mkdir -p $(BUILD_DIR) $(BIN_DIR)
	$(CC) $(CFLAGS) $(SRC_DIR)/bootstrap_compiler.c -o catc
	@echo "✅ Bootstrap complete: ./catc"

# ── Build (alias for bootstrap until self-hosting) ─
build: bootstrap

# ── Compile hello example ─────────────────────────
hello: bootstrap
	@mkdir -p examples
	./catc examples/hello.cat -o examples/hello

# ── Run tests ─────────────────────────────────────
test: bootstrap
	./catc tests/test_lexer.cat --run-tests

# ── Run benchmarks ────────────────────────────────
benchmark: bootstrap
	./catc tests/benchmark_lexer.cat --benchmark --max-ms=500

# ── Static check ──────────────────────────────────
check: bootstrap
	./catc src/lexer.cat --check --Werror

# ── Clean ─────────────────────────────────────────
clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR) catc
	rm -f examples/hello
	rm -f src/*.cache
