#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
DATA_DIR=${1:-/mnt/data/work_aura}
OUT_DIR=${2:-$ROOT/outputs}
METRIC_INV=${3:-/mnt/data/aura_metric_inventory.csv}
mkdir -p "$OUT_DIR"
python "$HERE/01_dashboard_metrics.py" --events "$DATA_DIR/events.jsonl" --html "$DATA_DIR/vdm_dashboard.html --utd "$DATA_DIR/utd_events" --out "$OUT_DIR"
python "$HERE/02_h5_structural.py" --h5_dir "$DATA_DIR" --out "$OUT_DIR"
python "$HERE/03_utd_analysis.py" --utd_dir "$DATA_DIR/utd_events" --out "$OUT_DIR"
python "$HERE/04_manifest_tables.py" --aura_dir "$DATA_DIR" --metric_inventory "$METRIC_INV" --out "$OUT_DIR"
python "$HERE/vdm_report.py" "$DATA_DIR/state_17400.h5 --events "$DATA_DIR/utd_events.jsonl
echo "Wrote outputs to $OUT_DIR"
