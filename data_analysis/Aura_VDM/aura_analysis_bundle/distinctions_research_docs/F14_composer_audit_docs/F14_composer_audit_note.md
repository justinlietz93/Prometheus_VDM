# F14 — Composer / Encoder Artifact Analysis

## What this package measures
This package formalizes the overlap and novelty statistics in `say_event_composer_audit_metrics.csv`.

## Main results
Across **530** audited outputs:

- zero-trigram outputs: **45 / 530 = 8.5%**
- outputs with `LCS < 0.30`: **438 / 530 = 82.6%**
- outputs with `best_all_jaccard < 0.30`: **496 / 530 = 93.6%**
- mean immediate-input Jaccard: **0.038**
- mean within-output uniqueness: **0.860**
- median lag to most similar prior output: **3687 ticks**
- mean similarity to most similar prior output: **0.254**

## Observational read
The output stream is only weakly coupled to the immediately preceding input, while still showing long-range similarity structure to older outputs.
That is exactly the pattern you would expect from a system that is not just parroting the last feed token-for-token.

## Repro artifacts
- `scripts/f14_composer_audit_analysis.py`
- `tables/f14_composer_audit_summary.csv`
- `tables/f14_composer_audit_quantiles.csv`
- `tables/f14_zero_trigram_examples.csv`
- `tables/f14_low_immediate_overlap_examples.csv`
- `figures/f14_overlap_distributions.png`
- `figures/f14_threshold_summary.png`
