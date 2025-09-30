
# FUM Real‑Time Runtime (Scaffold v3)

> Logical entry point: `fum_rt.run_nexus`

## Quick start

### Web Dashboard
```bash
pip install -r requirements.txt
python fum_live.py
```

### CLI
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
- `fum_rt/nexus.py` — the real‑time orchestrator (thin façade; delegates loop/telemetry/control‑plane to runtime/*).
- `fum_rt/runtime/loop.py` — main loop extracted from Nexus.run (parity‑preserving).
- `fum_rt/runtime/telemetry.py` — telemetry packagers (`macro_why_base`, `status_payload`) and `tick_fold`.
- `fum_rt/runtime/phase.py` — external control‑plane (phase.json) profiles, apply/poll.
- `fum_rt/runtime/retention.py` — checkpoint retention policy.
- `fum_rt/runtime/events_adapter.py` — Observation → core events adapter for event‑driven metrics.
- `fum_rt/runtime/runtime_helpers.py` — behavior‑preserving helpers (ingest, speak gating, viz, checkpoints).
- `fum_rt/runtime/emitters.py` — MacroEmitter/ThoughtEmitter initialization.
- `fum_rt/runtime/orchestrator.py` — orchestrator seam (delegates to Nexus for parity).
- `fum_rt/runtime/state.py` — optional small runtime context (tick/time, small rings); not required for parity.
- `fum_rt/core/engine.py` — CoreEngine seam (snapshot, engram_load/save pass‑throughs).
- `fum_rt/core/signals.py` — core signals seam (B1 detector apply, VT/cohesion/TD helpers).
- `fum_rt/core/void_dynamics_adapter.py` — loads your void functions or a minimal stub.
- `fum_rt/core/connectome.py` — kNN‑ish graph + vectorized update step.
- `fum_rt/core/metrics.py` — sparsity/cohesion/complexity metrics.
- `fum_rt/core/visualizer.py` — dashboard & graph rendering (matplotlib).
- `fum_rt/core/memory.py` — engram snapshots (.npz/.h5).
- `fum_rt/io/lexicon/store.py` — phrase templates and lexicon I/O (learned vocabulary).
- `fum_rt/io/ute.py` — Universal Temporal Encoder (stdin & synthetic tick sources).
- `fum_rt/io/utd.py` — Universal Transduction Decoder (stdout & file sink).
- `fum_rt/utils/logging_setup.py` — structured logger helper.
- `requirements.txt` — only `numpy`, `networkx`, `matplotlib`.

All modules are tiny and documented so you can extend fast.

### Modularization and façade notes

- [Nexus](fum_rt/nexus.py:1) is a thin façade; the main loop is [run_loop()](fum_rt/runtime/loop.py:40). External imports remain unchanged.
- Telemetry packaging and tick fold live in [tick_fold()](fum_rt/runtime/telemetry.py:99), with B1 gating via [apply_b1_detector()](fum_rt/core/signals.py:218).
- Orchestrator/core seams: [Orchestrator()](fum_rt/runtime/orchestrator.py:22) delegates to [CoreEngine()](fum_rt/core/engine.py:29) for snapshot and engram ops.
- Runtime helpers provide behavior-preserving ingest/speak/viz/checkpoint: [maybe_auto_speak()](fum_rt/runtime/runtime_helpers.py:234), [maybe_visualize()](fum_rt/runtime/runtime_helpers.py:392), [save_tick_checkpoint()](fum_rt/runtime/runtime_helpers.py:414).
- Lexicon/phrase bank I/O lives in [store.py](fum_rt/io/lexicon/store.py:1); IDF is composer/telemetry-only and never affects dynamics.
- Event-driven metrics (ON by default; telemetry-only) fold bus observations via [observations_to_events()](fum_rt/runtime/events_adapter.py:22) and ADC via [adc_metrics_to_event()](fum_rt/runtime/events_adapter.py:96). Disable with ENABLE_EVENT_METRICS=0.
- Void cold scouts (ON by default; telemetry-only) explore cold regions with budgeted walkers and feed evt_* probes; disable with ENABLE_COLD_SCOUTS=0.
- Thought ledger emission is behind ENABLE_THOUGHTS=1 and uses runtime emitters; see [initialize_emitters()](fum_rt/runtime/emitters.py:23).
- Composer novelty gain can be tuned with COMPOSER_IDF_K (default 0.0), applied only in the composer, not in SIE/ADC/connectome.

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
- On startup, the Nexus registers macro keys from the run’s `macro_board.json`.
- Defaults `status` and `say` are always available.



---

## Language output: Macro board, phrase bank, and lexicon

Overview
- Macro board is a simple on-disk registry of macro names used by the UTD output path.
- Phrase bank provides optional sentence templates the runtime can use to compose richer “say” messages.
- Lexicon persists a lightweight vocabulary, learned from inbound text and emitted speech.

Files and where they live
- Macro board (auto‑persisted each run): runs/&lt;timestamp&gt;/macro_board.json
  - Runtime source: [fum_rt/io/utd.py](fum_rt/io/utd.py)
  - Nexus reads macros at boot: [fum_rt/nexus.py](fum_rt/nexus.py)
- Phrase bank (optional source of sentence templates, loaded at boot):
  - Per‑run: runs/&lt;timestamp&gt;/phrase_bank.json
  - Fallback (packaged): [fum_rt/io/lexicon/phrase_bank_min.json](fum_rt/io/lexicon/phrase_bank_min.json)
- Lexicon (auto‑learned vocabulary from inputs/outputs): runs/&lt;timestamp&gt;/lexicon.json
  - Grows during the run; periodically saved by the runtime

How the macro board populates
- Whenever the runtime emits a macro that is not already registered, it is auto‑registered and persisted to macro_board.json by the UTD.
- This requires no configuration. The file will appear in the active run directory as soon as a new macro key is used.

Example macro_board.json
```json
{
  "status": { "desc": "Emit structured status payload" },
  "say": {
    "desc": "Emit plain text line",
    "templates": [
      "Topology discovery: {keywords}",
      "Observation: {top1}, {top2} (vt={vt_entropy:.2f}, v={valence:.2f})",
      "Emergent structure: {keywords} (b1_z={b1_z:.2f})"
    ]
  }
}
```

Phrase bank (richer sentences)
- The runtime loads optional sentence templates for the “say” macro from either:
  - runs/&lt;timestamp&gt;/phrase_bank.json, or
  - [fum_rt/io/lexicon/phrase_bank_min.json](fum_rt/io/lexicon/phrase_bank_min.json)
- Expected shape:
```json
{
  "say": [
    "Topology discovery: {keywords}",
    "Exploration reveals {top1} linked to {top2} (coverage={vt_coverage:.2f})",
    "Coherent loop near {top1} ↔ {top2} (b1_z={b1_z:.2f})"
  ]
}
```
- Supported placeholders the runtime will fill from current metrics/context:
  - {keywords}, {top1}, {top2}
  - {vt_entropy}, {vt_coverage}, {b1_z}, {connectome_entropy}, {valence}

Lexicon (word bank)
- The runtime maintains runs/&lt;timestamp&gt;/lexicon.json as a simple token frequency store learned from:
  - Inbound UTE text messages (your input stream)
  - Emitted “say” lines
- The lexicon is used to extract keyword summaries and top tokens to slot into templates.
- You can also bootstrap a lexicon from logs using the scanner:
  - Script: [tools/utd_event_scan.py](tools/utd_event_scan.py)
  - Build lexicon JSON from observed “say” macros:
    ```bash
    python tools/utd_event_scan.py runs/2025-08-10_21-00-00 --macro say --emit-lexicon runs/2025-08-10_21-00-00/lexicon.json
    ```

How to get more words and whole sentences
1) Feed more text into the UTE
- Stream domain texts to grow the lexicon automatically (no config needed).
- The more diverse and structured your input, the richer the learned vocabulary.

2) Provide more sentence templates
- Create runs/&lt;timestamp&gt;/phrase_bank.json with many “say” templates (see placeholders above).
- Templates rotate deterministically each emission; you can include longer, multi‑clause sentences.

3) Seed macro board metadata
- Add a “templates” array under the “say” key in macro_board.json (see example above). The runtime will use these at boot.

4) Tune self‑speak gating to allow more emissions
- Lower the valence threshold and tweak spike detector parameters via CLI:
  ```bash
  python -m fum_rt.run_nexus \
    --speak-auto \
    --speak-valence-thresh 0.35 \
    --speak-z 2.0 \
    --speak-hysteresis 0.5
  ```
- Emissions are still gated by topology spikes (B1 proxy) and valence for stability.

Where to see the outputs
- UTD events: runs/&lt;timestamp&gt;/utd_events.jsonl (type: "macro", macro: "say", args.text: "...").
- Optional Nexus logs (gating decisions, e.g., speak_suppressed): runs/&lt;timestamp&gt;/events.jsonl.

Scanner quick start (to audit what the model “tried to say”)
```bash
# Scan a run for “say” macros (NDJSON)
python tools/utd_event_scan.py runs/2025-08-10_21-00-00 --macro say

# Include Nexus speak_suppressed and write CSV
python tools/utd_event_scan.py runs --macro say --include-nexus --format csv --out say_events.csv
```

Operational notes
- Emission path selection: MacroEmitter path priority $UTD_OUT > utd.path > runs/<timestamp>/utd_events.jsonl; ThoughtEmitter path priority $THOUGHT_OUT > runs/<timestamp>/thoughts.ndjson. See [initialize_emitters()](fum_rt/runtime/emitters.py:23).
- Macro names are persisted automatically when first used; no manual step required.
- Phrase bank and macro board are complementary; phrase bank supplies sentence templates, macro board is the registry of macro keys and optional metadata like “templates”.
- The runtime keeps everything compute‑light: deterministic template filling with keywords/tokens from the live lexicon and metrics.

--- 
## Developer utilities (ad hoc; not part of system runtime)

These scripts are standalone developer tools intended to be run manually. They are NOT imported by runtime or core modules, and have no effect on the running system.

- Parity harness: [golden_run_parity.py](tools/golden_run_parity.py:1)
  - Compare two completed runs for behavioral parity (macros and tick metrics)
  - Example:
    - python tools/golden_run_parity.py --run-a runs/2025-08-10_21-00-00 --run-b runs/2025-08-10_22-15-00

- Smoke verifier: [smoke_emissions.py](tools/smoke_emissions.py:1)
  - Sanity-check a run directory for basic emissions (UTD macros, ticks, optional thoughts)
  - Example:
    - python tools/smoke_emissions.py --run runs/2025-08-10_21-00-00

- Geometry bundle automation: [geom_bundle_builder.py](tools/geom_bundle_builder.py:1)
  - Implements the end-to-end VDM geometry capture workflow (prep, provenance, activations, QC, packaging)
  - Example:
    - python tools/geom_bundle_builder.py --config config/geom_config.json --adapter tools.geom_adapter_stub:DeterministicRandomAdapter

Policy:
- No production code imports anything from tools/.
- Tools are safe to modify/remove without impacting runtime execution.
