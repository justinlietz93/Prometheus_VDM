# F15 reproducibility note

This folder contains machine-generated F15 interaction outputs built from:
- `aura_analysis_extracted/aura_analysis_bundle/aura_justin_exchange.md`
- `aura_analysis_extracted/aura_analysis_bundle/scalar_struct/tables/tick_table_full.csv.gz` (late-run merge where available)

Main command:
`python f15_interaction_analysis.py`

Outputs:
- parsed exchange events
- Justin→next-Aura lag table
- key-arc subset table
- summary metrics
- lag histogram figure
- interaction-window state figure