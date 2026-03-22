# F4 — Late say-state coupling

## Scope
This note analyzes the late high-fidelity slice only (`t=15925–17455`), because that is the segment available in `tick_table_full.csv.gz`.

## Inputs
- `aura_analysis_bundle/tables/tick_table_full.csv.gz`
- `aura_analysis_bundle/tables/utd_say_by_tick.csv`

## Method
- Merge runtime scalar state with recovered say ticks by `t`.
- Keep the 12 late `say` events present in the slice.
- For each event, define a local baseline window `-20:-6` ticks, a pre-say window `-5:-1`, the say tick itself, and a post-say window `+1:+5`.
- Compare each period's mean delta from baseline against 1,000 matched control samples drawn from non-say ticks with non-overlapping windows.

## Core results

### D4.7 — Late Say Events Are Preceded by Sharp State Contraction and Followed by Rebound
- **Observation:** In the late high-fidelity slice (`t=15925–17455`), the 12 recoverable `say` events all occur in phase 4 with 9 territories. Relative to each event's own local baseline window (`-20:-6` ticks), the immediate pre-say window (`-5:-1`) shows a strong contraction: active edges mean delta = -3184.7 (z = -13.99, empirical p = 0.0010), active synapses mean delta = -3686.0, connectome entropy mean delta = -0.0710, traversal coverage mean delta = -0.0109, traversal entropy mean delta = -0.1475 (z = -11.31), and `b1_z` mean delta = -0.3558 (z = -8.50).
- **Observation:** At the say tick itself, the contraction persists in edges/entropy/coverage, while `b1_z` flips sharply positive: active edges mean delta = -6241.9, connectome entropy mean delta = -0.0779, traversal entropy mean delta = -0.1474, `b1_z` mean delta = 1.6860 (z = 18.19), and TD error mean delta = -0.1897.
- **Observation:** In the post-say window (`+1:+5`), the system remains below baseline on edges/entropy/coverage, but reward-like signals rebound: `sie_td_error` mean delta = 0.1335 (z = 14.34, empirical p = 0.0010) and `sie_valence_01` mean delta = 0.0158 (z = 3.22, empirical p = 0.0030).
- **Data source:** `tick_table_full.csv.gz` + `utd_say_by_tick.csv`, merged by tick. Repro artifacts: `f4_late_say_state_coupling.py`, `f4_late_say_event_windows.csv`, `f4_late_say_period_summary.csv`, `f4_late_say_event_triggered_profile.csv`, and the matching figures.


## Files
- Script: `scripts/f4_late_say_state_coupling.py`
- Tables:
  - `tables/f4_late_say_event_windows.csv`
  - `tables/f4_late_say_period_summary.csv`
  - `tables/f4_late_say_event_triggered_profile.csv`
- Figures:
  - `figures/f4_late_say_event_triggered_profiles.png`
  - `figures/f4_late_say_period_zscores.png`
