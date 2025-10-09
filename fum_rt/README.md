
# FUM Real‑Time Runtime (Scaffold v3)

This is a **minimal, production‑oriented** runtime that matches your Nexus ⇄ UTE/UTD vision.
It runs continuously, ingests input, updates the connectome with your *void equations* if
present (`Void_Equations.py`), logs metrics, and renders dashboards and connectome images.

> Entry point: `python -m fum_rt.run_nexus`

## Quick start

```bash
pip install -r requirements.txt
export PYTHONPATH=.
python -m fum_rt.run_nexus --neurons 800 --hz 10 --domain biology_consciousness --viz-every 5
```

Artifacts land in `runs/<timestamp>/`:
- `events.jsonl`   - structured logs
- `dashboard.png`  - metrics (updated)
- `connectome.png` - graph snapshot (updated)
- `state_<step>.h5` (or `.npz` fallback) - checkpointed engram state (see `--checkpoint-every`, `--checkpoint-keep`)

### Where to put your functions
If your repo already contains `Void_Equations.py` and `Void_Debt_Modulation.py` on `PYTHONPATH`,
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

- `fum_rt/run_nexus.py` - CLI entrypoint.
- `fum_rt/nexus.py` - the real‑time orchestrator.
- `fum_rt/core/void_dynamics_adapter.py` - loads your void functions or a minimal stub.
- `fum_rt/core/connectome.py` - kNN‑ish graph + vectorized update step.
- `fum_rt/core/metrics.py` - sparsity/cohesion/complexity metrics.
- `fum_rt/core/visualizer.py` - dashboard & graph rendering (matplotlib).
- `fum_rt/core/memory.py` - engram snapshots (.npz).
- `fum_rt/io/ute.py` - Universal Temporal Encoder (stdin & synthetic tick sources).
- `fum_rt/io/utd.py` - Universal Transduction Decoder (stdout & file sink).
- `fum_rt/utils/logging_setup.py` - structured logger helper.
- `requirements.txt` - only `numpy`, `networkx`, `matplotlib`.

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
  2) `fum_rt/io/lexicon/macro_board_min.json` (fallback).
- This allows new macro keys (e.g., `say`, `status`) to accumulate across runs without additional configuration.



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
  - Fallback: [fum_rt/io/lexicon/phrase_bank_min.json](fum_rt/io/lexicon/phrase_bank_min.json)
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
- Macro names are persisted automatically when first used; no manual step required.
- Phrase bank and macro board are complementary; phrase bank supplies sentence templates, macro board is the registry of macro keys and optional metadata like “templates”.
- The runtime keeps everything compute‑light: deterministic template filling with keywords/tokens from the live lexicon and metrics.


---

## Domain, Phase Control, and Cycles (Topology Complexity)

This section explains three runtime concepts that appear in profiles and logs: domain, phase control, and the “cycles” metric.

### Domain

- Purpose: Selects a modulation factor for the void equations, scaling both the growth and decay elemental deltas before each tick. The value is computed by [get_domain_modulation()](fum_rt/core/void_dynamics_adapter.py:46), and is passed into both Δα and Δω inside the adapter.
- How it works:
  - If you provide your own Void_Debt_Modulation on PYTHONPATH (class with get_universal_domain_modulation), the adapter uses it to obtain domain_modulation.
  - Otherwise, a safe fallback mapping is used internally and the modulation is computed from built‑in targets and the ALPHA/BETA ratio of the void equations.
- Supported presets (fallback path) include: quantum, standard_model, dark_matter, biology_consciousness, cosmogenesis, higgs. Any unknown string (e.g., "math_physics") resolves to a baseline default in the fallback path unless your module overrides it.
- Where it is applied: The scalar is fed into the void equations through the adapter and then consumed by the Connectome during step() each tick.

Examples
- CLI:
  python -m fum_rt.run_nexus --domain biology_consciousness
- Profile JSON (run_profiles/*.json):
  "domain": "math_physics"

To customize the mapping:
- Add a Python module on PYTHONPATH that exposes a class VoidDebtModulation with get_universal_domain_modulation(domain) → {"domain_modulation": float}. See the adapter’s import logic in [get_domain_modulation()](fum_rt/core/void_dynamics_adapter.py:46) for how it is discovered. A reference template for domain modulation also exists in [computational_proofs/Void_Debt_Modulation.py](computational_proofs/Void_Debt_Modulation.py).

---

### Phase control

- Purpose: A simple, file‑driven control plane that lets you switch between pre‑tuned “profiles” at runtime without restarting. It adjusts:
  - Speak gates (z threshold, hysteresis, cooldown, valence threshold)
  - Connectome traversal/homeostasis parameters (walkers, hops, bundle_size, prune_factor)
  - Optional structural knobs (threshold, lambda_omega, candidates)
- Where: See default profile definitions in [Nexus._default_phase_profiles()](fum_rt/nexus.py:339).
- How it’s applied:
  - The runtime polls runs/<timestamp>/phase.json each tick via [Nexus._poll_control()](fum_rt/nexus.py:403).
  - When the file exists and its mtime changes, the profile is merged and applied immediately. The path is set at startup in [Nexus.__init__ → phase_file](fum_rt/nexus.py:183).
- On vs Off:
  - OFF: If runs/<timestamp>/phase.json does not exist, no phase control is applied (runtime uses current CLI values and defaults).
  - ON: Create runs/<timestamp>/phase.json and write a profile (see example below). Edits to the file are picked up live.

Example phase.json
{
  "phase": 1,
  "speak": {
    "speak_z": 2.5,
    "speak_hysteresis": 0.8,
    "speak_cooldown_ticks": 10,
    "speak_valence_thresh": 0.35
  },
  "connectome": {
    "walkers": 384,
    "hops": 4,
    "bundle_size": 3,
    "prune_factor": 0.10,
    "threshold": 0.15,
    "lambda_omega": 0.10,
    "candidates": 64
  }
}

Notes
- Simple toggle: Create the file to enable; remove/rename to disable.
- Merging: If you only specify {"phase": n}, the defaults for that phase are loaded; any extra fields you include override those defaults.
- Safety: All updates are range‑checked and applied only if a matching attribute exists on the current connectome.

---

### “Cycles” metric (complexity_cycles)

- Definition: A topology‑only proxy for the number of simple cycles in the active subgraph. It is computed from the active graph induced by W[i]*W[j] > threshold. The proxy is the cyclomatic complexity formula:
  cycles = E_active - N + C_active
  where E_active is the number of active edges, N is the number of nodes, and C_active is the number of connected components over the active nodes.
- Implementations:
  - Dense backend: [Connectome.cyclomatic_complexity()](fum_rt/core/connectome.py:375)
  - Sparse backend: [SparseConnectome.cyclomatic_complexity()](fum_rt/core/sparse_connectome.py:393)
- How it’s used:
  - The Nexus uses complexity_cycles each tick as a “B1 proxy” input to a streaming z‑score detector. See the B1 update inside [Nexus.run()](fum_rt/nexus.py:442) where b1_value is taken from m["complexity_cycles"] and fed to the z‑spike detector to gate speaking.
  - It can be augmented with additional cycle signals from the traversal/ADC subsystem; the Nexus folds such findings into the metric before gating.

Why it matters
- Phase control does not “only affect cycles.” It adjusts traversal/homeostasis/speak gates that indirectly influence many structure‑and‑dynamics metrics (coverage, entropy, cohesion components, active edges, density, and thus cycles). Cycles is highlighted because it’s an effective, void‑native trigger for salient topology events and is used to gate autonomous speaking.

Toggle summary
- Domain: CLI/profile string selecting void‑equation modulation; fallback mapping is internal unless you provide your own implemention. See [get_domain_modulation()](fum_rt/core/void_dynamics_adapter.py:46).
- Phase control: Enabled when runs/<timestamp>/phase.json exists; disabled when it doesn’t. Profiles are defined in [Nexus._default_phase_profiles()](fum_rt/nexus.py:339), polled by [Nexus._poll_control()](fum_rt/nexus.py:403), and applied live.
- Cycles: Topology‑only cycle count proxy computed each tick (dense/sparse backends above). Used by the streaming detector to gate “say” macro emissions.
