#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_JSON="$SCRIPT_DIR/data/assisted-echo-t4-prereg-v1c.json"
DATA_CSV="$SCRIPT_DIR/data/ceg_summary.csv"
FIG_DIR="$SCRIPT_DIR/figures"

echo "=== CEG Reproducibility Check ==="

# 1) Validate JSON
python3 -c "import json; json.load(open('$DATA_JSON')); print('JSON seed: OK')"

# 2) Regenerate figures
python3 "$SCRIPT_DIR/scripts/replot_ceg.py" \
  --json "$DATA_JSON" \
  --csv "$DATA_CSV" \
  --outdir "$FIG_DIR"

# 3) Verify outputs
need=("ceg_vs_lambda.png" "gate_pass_rates.png")
for f in "${need[@]}"; do
  test -s "$FIG_DIR/$f" || { echo "MISSING: $FIG_DIR/$f"; exit 2; }
  echo "  ✓ $f"
done

echo "=== All figures regenerated. ==="
