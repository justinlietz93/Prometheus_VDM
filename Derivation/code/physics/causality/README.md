# Causality DAG Audit

Order-only audit over event logs to estimate local causal dimension and interval scaling.

## Inputs

- events: `events.jsonl` or a directory of shards (`*.jsonl`, optionally `*.jsonl.gz`)
- utd events (optional): `utd_events.jsonl` or directory
- JSONL row fields accepted: `id|event_id`, `t|time|timestamp`, optional `parents|parent_ids|sources` (list)

Notes:

- For runtime logs written by `fum_rt`:
  - `events.jsonl` rows look like `{ ts, level, msg, ... }` with per-tick metrics nested under `extra`. The audit treats `t` (tick index) as a valid event ID and accepts `ts` as time when provided via `--time-key ts --time-scale 1`.
  - `utd_events.jsonl` rows look like `{ type, payload:{ t, ... }, score }`. The audit falls back to nested `payload.t` and related time aliases automatically.
- If rows lack an explicit `id`, you can synthesize IDs by using `--id-key t` (tick as ID) or rely on the default that includes `t` as an accepted alias.
- For neuron-indexed events with keys like `neuron` and `i|idx|index`, the audit composes a stable ID `"<neuron>:<i>"` automatically.

## Run

```bash
python Derivation/code/physics/causality/run_causality_dag_audit.py \
  --events Derivation/code/physics/causality/data/events.jsonl \
  --utd-events Derivation/code/physics/causality/data/utd_events.jsonl \
  --tag v1
```

Quick start for a Nexus run directory (runtime logs):

```bash
python Derivation/code/physics/causality/run_causality_dag_audit.py \
  --events runs/<timestamp>/events.jsonl \
  --utd-events runs/<timestamp>/utd_events.jsonl \
  --time-key ts --time-scale 1 \
  --infer-by-time \
  --tag v1
```

Flags:

- `--allow-unapproved` (AVOID this) to quarantine artifacts when proposal/tag is not yet approved
- `--infer-by-time` to add precedence edges by time order when explicit parents are missing
- `--streams events,utd` to include multiple streams
- Use `--max-events 200000` to cap ingest for large logs during exploration.
- For UTD-only analysis, point `--events` to the UTD file and add `--time-key payload.t` or `payload.ts` as appropriate.

## Outputs

- Figure: `Derivation/code/outputs/figures/causality/<timestamp>_dag_audit_v1.png`
- Log JSON: `Derivation/code/outputs/logs/causality/<timestamp>_dag_audit_v1.json`

Artifacts route to `failed_runs/` unless the tag is approved per `APPROVAL.json` and the approvals DB.
