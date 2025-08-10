
# FUM Real‑Time Runtime (Scaffold v3)

This is a **minimal, production‑oriented** runtime that matches your Nexus ⇄ UTE/UTD vision.
It runs continuously, ingests input, updates the connectome with your *void equations* if
present (`FUM_Void_Equations.py`), logs metrics, and renders dashboards and connectome images.

> Entry point: `python -m fum_rt.run_nexus`

## Quick start

```bash
pip install -r requirements.txt
export PYTHONPATH=.
python -m fum_rt.run_nexus --neurons 800 --hz 10 --domain biology_consciousness --viz-every 5
```

Artifacts land in `runs/<timestamp>/`:
- `events.jsonl`   — structured logs
- `dashboard.png`  — metrics (updated)
- `connectome.png` — graph snapshot (updated)
- `state_<step>.h5` (or `.npz` fallback) — checkpointed engram state (see `--checkpoint-every`, `--checkpoint-keep`)

### Where to put your functions
If your repo already contains `FUM_Void_Equations.py` and `FUM_Void_Debt_Modulation.py` on `PYTHONPATH`,
this runtime will import them automatically.

If not, drop those files at the project root (next to `fum_rt/`) **or** copy them into `fum_rt/core/`.
The adapter will prefer your versions and only fall back to an internal stub if not found.

### What “real‑time” means here
The Nexus loop ticks at `--hz` (default 10 Hz). Each tick:
1. UTE collects any inbound messages (stdin/queue/synthetic “tick” generator).
2. Connectome applies your void dynamics to the node field vector `W` (vectorized).
3. Metrics -> logs; UTD can emit text events opportunistically.
4. On schedule it saves a dashboard and a connectome image.

### Checkpoints
Engram checkpoints are saved as HDF5 (`.h5`) by default when `h5py` is available; otherwise snapshots fall back to `.npz`.
Use `--checkpoint-every S` to enable periodic saves; files live in `runs/<timestamp>/` as `state_<step>.h5` (or `.npz`).
Use `--checkpoint-keep K` to keep only the last K checkpoints (per format); set `0` to disable retention.

---

## CLI

```
python -m fum_rt.run_nexus [--neurons N] [--k K] [--hz HZ] [--domain NAME]
                           [--viz-every S] [--log-every S] [--checkpoint-every S]
                           [--duration S] [--use-time-dynamics/--no-time-dynamics]
                           [--seed SEED]
```

Domains supported (for auto‑modulation): `quantum`, `standard_model`, `dark_matter`,
`biology_consciousness`, `cosmogenesis`, `higgs`. You can override the factor in code if desired.

---

## Layout

- `fum_rt/run_nexus.py` — CLI entrypoint.
- `fum_rt/nexus.py` — the real‑time orchestrator.
- `fum_rt/core/void_dynamics_adapter.py` — loads your void functions or a minimal stub.
- `fum_rt/core/connectome.py` — kNN‑ish graph + vectorized update step.
- `fum_rt/core/metrics.py` — sparsity/cohesion/complexity metrics.
- `fum_rt/core/visualizer.py` — dashboard & graph rendering (matplotlib).
- `fum_rt/core/memory.py` — engram snapshots (.npz).
- `fum_rt/io/ute.py` — Universal Temporal Encoder (stdin & synthetic tick sources).
- `fum_rt/io/utd.py` — Universal Transduction Decoder (stdout & file sink).
- `fum_rt/utils/logging_setup.py` — structured logger helper.
- `requirements.txt` — only `numpy`, `networkx`, `matplotlib`.

All modules are tiny and documented so you can extend fast.

---

## Event scanning (UTD/Nexus)

During runs, UTD writes macro/text emissions to `runs/<timestamp>/utd_events.jsonl`.
Nexus writes structured logs (including speak gating) to `runs/<timestamp>/events.jsonl`.

A helper scanner is provided:

- Script: `tools/utd_event_scan.py`
- Purpose: Extract UTD “macro” (e.g., say) and “text” records, optionally include Nexus `speak_suppressed` events
- Output: NDJSON (default) or CSV

Examples:

```bash
# 1) Scan a specific run for “say” macros and print NDJSON
python tools/utd_event_scan.py runs/2025-08-10_21-00-00 --macro say

# 2) Scan all runs, include Nexus speak_suppressed, write CSV
python tools/utd_event_scan.py runs --macro say --include-nexus --format csv --out say_events.csv

# 3) Include UTD status text payloads as well
python tools/utd_event_scan.py runs/2025-08-10_21-00-00 --macro say --include-text

# 4) Persist a macro board synthesized from observed macros for a run
python tools/utd_event_scan.py runs/2025-08-10_21-00-00 --emit-macro-board runs/2025-08-10_21-00-00/macro_board.json

# 5) Build a simple vocabulary from “say” texts
python tools/utd_event_scan.py runs/2025-08-10_21-00-00 --emit-lexicon runs/2025-08-10_21-00-00/lexicon.json
```

### Macro board persistence

- At runtime, newly used macro names are automatically registered and persisted to `runs/<timestamp>/macro_board.json`.
- On startup, the Nexus also registers macro keys from:
  1) the run’s `macro_board.json` (preferred), or
  2) `from_physicist_agent/macro_board_min.json` (fallback).
- This allows new macro keys (e.g., `say`, `status`) to accumulate across runs without additional configuration.

