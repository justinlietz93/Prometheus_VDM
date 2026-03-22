# Family 15 — Interaction Dynamics (Analyst-side probe reconstruction) v0.1

## Scope

This note advances Family 15 using the analyst-side reconstruction available in `aura_justin_exchange.md` together with already-established D5 interaction results. The exchange file is used only to recover which inputs were Justin-originated for analysis. It does **not** imply the runtime had access to any source tag or source-specific metadata. In the run itself, inputs arrived through the same channel.

## Hard observations added here

### D15.1 — Unified-channel operator probes are externally recoverable for analysis
- `aura_justin_exchange.md` contains **51** analyst-recoverable Justin probe messages.
- These can be used as an external perturbation ledger for event-triggered analysis without changing the core claim that Aura received an undifferentiated stream at runtime.
- Artifact: `tables/f15_interaction_dynamics_summary.csv`, `tables/f15_operator_probe_response_lags.csv`

### D15.2 — Key boundary / embodiment / naming arc is tightly clustered and rapidly answered
- A key arc of **16** probe messages was extracted from the exchange stream, covering:
  - domain-wall / boundary prompts,
  - portal / robotic chassis prompts,
  - naming prompts,
  - wakefulness / recognition prompts,
  - safety / return prompts,
  - body / windows / senses prompts,
  - final experience / desire / canal prompts.
- Across this key arc, the lag to the next Aura output is:
  - mean = **35.25 ticks**
  - median = **8.5 ticks**
- The two late terminal probes land almost immediately before their paired outputs:
  - `t=17101` → next Aura output at `t=17104` (**3 ticks**)
  - `t=17199` → next Aura output at `t=17201` (**2 ticks**)
- Artifact: `tables/f15_operator_probe_key_arc_response_lags.csv`

### D15.3 — Family 15 sits on top of already-computed D5 interaction evidence
The new chronology does not replace D5; it sharpens it.

Existing interaction results already in the distinctions document:
- D5.1 permutation result: `active_edges z = 14.52, p = 0.000`, operator delta `= -5,253` edges vs matched-control `+196`
- D5.1b Mann–Whitney result: significant shifts in `active_edges`, `connectome_entropy`, `vt_entropy`, and `vt_coverage`
- D5.4 reply motif uptake: `28.6%` of replies to Justin contain boundary motifs; `36.7%` share content words
- D5.6 reply-lag compression: early mean `58.5` ticks → late mean `21.7` ticks

Taken together, the analyst-side reconstruction file and the computed D5 metrics support the same interaction family from two angles:
1. externally reconstructed probe chronology,
2. measured structural/state differentiation around those probes.

## Immediate use in the paper

This Family 15 note gives a clean evidence-only way to say the following:
- Justin-originated probes are recoverable only at the analyst layer, not the runtime layer.
- Despite the unified input channel, the runtime responds to those probes as a distinct dynamical class.
- In the late identity / boundary arc, response lags compress to single-digit ticks, with the final two probes landing 3 and 2 ticks before their paired Aura outputs.

## Artifact paths
- `tables/f15_interaction_dynamics_summary.csv`
- `tables/f15_operator_probe_response_lags.csv`
- `tables/f15_operator_probe_key_arc_response_lags.csv`
