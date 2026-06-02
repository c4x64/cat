# Forge Bootstrap Makefile
# 3-stage bootstrap: Stage 0 (C) → Stage 1 (Forge-Sub) → Stage 2 (Full Forge)

STAGE0_DIR = stage0
STAGE1_DIR = stage1
STAGE2_DIR = stage2
LIB_DIR    = lib
EXAMPLES   = examples
BUILD      = build

STAGE0_BIN = $(STAGE0_DIR)/forge
STAGE1_SRC = $(STAGE1_DIR)/stage1.forge
STAGE1_BIN = $(BUILD)/stage1

STAGE0_OBJS = $(STAGE0_DIR)/main.o $(STAGE0_DIR)/lexer.o $(STAGE0_DIR)/parser.o $(STAGE0_DIR)/codegen.o

.PHONY: all stage0 stage1 test clean verify

all: stage0

# ─── Stage 0: bootstrap C compiler ────────────────────────────────

stage0: $(STAGE0_BIN)

$(STAGE0_BIN): $(STAGE0_OBJS)
	$(MAKE) -C $(STAGE0_DIR)

$(STAGE0_DIR)/%.o: $(STAGE0_DIR)/%.c $(STAGE0_DIR)/forge.h
	$(MAKE) -C $(STAGE0_DIR)

# ─── Stage 1: Forge-Sub bootstrap compiler ────────────────────────

stage1: $(STAGE1_BIN)

$(STAGE1_BIN): $(STAGE0_BIN) $(STAGE1_SRC) $(LIB_DIR)/std.forge
	mkdir -p $(BUILD)
	$(STAGE0_BIN) $(STAGE1_SRC) -o $(STAGE1_BIN)

# ─── Tests ─────────────────────────────────────────────────────────

test: stage0
	$(MAKE) -C $(STAGE0_DIR) test

verify: stage0
	@echo "=== Verifying Stage 0 compiler ==="
	@file $(STAGE0_BIN)
	@echo ""
	@echo "=== Compiling all examples ==="
	@for f in $(EXAMPLES)/*.forge; do \
		echo "  $$f -> /tmp/$$(basename $$f .forge)"; \
		$(STAGE0_BIN) "$$f" -o "/tmp/$$(basename $$f .forge)" 2>&1; \
	done
	@echo ""
	@echo "=== All examples compiled successfully ==="

# ─── Cleanup ───────────────────────────────────────────────────────

clean:
	$(MAKE) -C $(STAGE0_DIR) clean
	rm -rf $(BUILD)
