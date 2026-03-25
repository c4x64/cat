#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CAT COMPILER BOOTSTRAP SCRIPT
# This script runs ONCE to get CAT self-hosting
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔥 CAT COMPILER BOOTSTRAP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v gcc >/dev/null 2>&1 || { echo "❌ GCC not found"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git not found"; exit 1; }
command -v make >/dev/null 2>&1 || { echo "❌ Make not found"; exit 1; }
echo "✅ Prerequisites OK"
echo ""

# Run make bootstrap
echo "📋 Building bootstrap compiler..."
make bootstrap
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Run tests:      make test"
echo "  2. Run benchmarks: make benchmark"
echo "  3. Build hello:    make hello"
echo "  4. Once self-hosting: delete this script and bootstrap_compiler.c"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"