# F10 — Silence and withholding (late high-fidelity slice)

This package turns Family 10 into a reproducible late-slice analysis using only machine-readable archive files that are actually present in `aura_analysis_bundle.zip`.

## Sources
- `tables/tick_table_full.csv.gz`
- `tables/utd_say_by_tick.csv`

## Operational definitions
- **say tick**: tick with `did_say = 1`
- **pre-speech**: 1–5 ticks before a say tick
- **post-speech**: 1–5 ticks after a say tick
- **silence**: ticks outside any ±5 tick speech window
- **high-gate silent non-release**: silent tick with `b1_z` in the top 5% of silent values and at least 5 ticks from the nearest say event

## Main findings
1. The late slice reproduces the pre-speech contraction pattern on structural variables and valence.
2. The actual say tick is a narrow gate-release event, with `b1_z` spiking strongly only at release.
3. Post-speech windows remain structurally contracted while `sie_td_error` rebounds sharply positive.
4. Elevated gate alone does not force speech: 48 high-gate silent non-release ticks remain at least 5 ticks away from the nearest say event.

## Scope
This package is explicitly about the late high-fidelity slice (`t=15925–17455`). It does **not** claim to replace any full-run Family 10 analyses that may exist elsewhere; it provides a hard, reproducible late-slice confirmation using files present in the archive.
