#!/usr/bin/env bash
set -euo pipefail

echo "============================================"
echo "  CEG Metriplectic Instrument — Quickstart"
echo "============================================"

REPO_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
CODE_DIR="$REPO_ROOT/Derivation/code"

echo ""
echo "[1/4] Checking Python + dependencies..."
python3 -c "import numpy, scipy; print('  numpy:', numpy.__version__, ' scipy:', scipy.__version__)"

echo ""
echo "[2/4] Running preflight test (small grid, fast)..."
cd "$CODE_DIR"
python3 -m pytest tests/metriplectic/test_assisted_echo_preflight.py -v --tb=short 2>&1 | tail -5

echo ""
echo "[3/4] Running canonical CEG experiment (N=256, 12 seeds, ~30s)..."
python3 -m physics.metriplectic.assisted_echo \
  --spec physics/metriplectic/specs/assisted_echo.v1c.json \
  --allow-unapproved

echo ""
echo "[4/4] Checking outputs..."
LOG_DIR="$CODE_DIR/outputs/logs/metriplectic"
FIG_DIR="$CODE_DIR/outputs/figures/metriplectic"
echo "  Logs:    $(ls -1 "$LOG_DIR"/*assisted_echo* 2>/dev/null | wc -l) files in $LOG_DIR"
echo "  Figures: $(ls -1 "$FIG_DIR"/*assisted_echo* 2>/dev/null | wc -l) files in $FIG_DIR"

echo ""
echo "============================================"
echo "  Done. Check outputs above."
echo "============================================"
