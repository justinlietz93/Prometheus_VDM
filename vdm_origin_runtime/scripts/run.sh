#!/usr/bin/env bash
set -euo pipefail
steps="${1:-1000}"
out="${2:-runs/logs/out.ndjson}"
./origin_run "$steps" "$out"
