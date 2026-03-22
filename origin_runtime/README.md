# origin_runtime

Structured project layout for the primitive-origin runtime.

## What is already here

- `src/core/BInv.c` — primitive bifurcation kernel
- `src/core/OriginStep.c` — same-class articulation step around `BInv`
- `src/core/origin_runner.c` — fixed-duration observed runner
- `src/observe/origin_observer.c` — append-only NDJSON event writer
- `src/observe/origin_main.c` — CLI entrypoint
- `include/*.h` — observer/runner headers
- `docs/run_notes.md` — original runner notes

## What is still a placeholder

- `src/witnesses/your_witnesses.c` — your canon-faithful witness semantics
- `docs/canon_notes.md` — place to pin which papers ground which witness
- `docs/event_schema.md` — event meanings for replay/rendering
- `scripts/run.sh` — convenience launcher
- `scripts/plot.py` — later visualization entrypoint
- `tests/*` — harnesses

## Build

`make`

## Run

`./origin_run <steps> runs/logs/out.ndjson`
