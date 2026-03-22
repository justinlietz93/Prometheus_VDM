from pathlib import Path
import json
import sys

p = Path(sys.argv[1] if len(sys.argv) > 1 else "runs/logs/out.ndjson")
counts = {}
if p.exists():
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        ev = json.loads(line)
        counts[ev["kind"]] = counts.get(ev["kind"], 0) + 1
print(counts)
