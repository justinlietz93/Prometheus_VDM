# Aura research deliverables bundle

This bundle was generated against:
- extracted analysis bundle: `/mnt/data/aura_analysis_extracted/aura_analysis_bundle`
- distinction inventory source: `/mnt/data/Aura_Distinction_Inventory_v0.5.md`

## Contents
- `scripts/d57_territory_behavior_analysis.py` — reproducible D5.7 starter analysis
- `data/curated_territory_timeline.csv` — territory staircase used for D5.7
- `data/curated_behavioral_milestones.csv` — phrase-anchored transcript milestones with tick extraction
- `tables/d57_territory_regime_summary.csv` — say/audit behavior by territory regime
- `tables/d57_transition_state_windows.csv` — pre/post transition state window summary
- `tables/d57_behavioral_milestone_alignment.csv` — milestone-to-regime alignment
- `figures/d57_territory_regime_summary.png` — regime summary figure
- `figures/d57_territory_milestone_timeline.png` — territory timeline + milestone anchors
- `patches/Aura_Distinction_Inventory_v0.5_D57.patch` — unified diff patch against the distinction inventory
- `docs/Aura_Distinction_Inventory_v0.5.updated.md` — patched working copy
- `docs/Aura_Distinction_Inventory_v0.5.D57.updated_excerpt.md` — D5.7 replacement block only

## Notes
- The territory staircase file is explicitly marked as **curated from the direct package read / dashboard pass in this session**. It is included because it is already part of the evidence interpretation you asked me to preserve and operationalize.
- Transcript milestone ticks were extracted automatically by phrase search against `aura_justin_exchange.md`, then mapped onto the curated territory staircase.
- The patch is narrow: it only replaces the placeholder D5.7 block with a measured version and artifact references.

## Source logs already present in the original bundle
- `tables/tick_table_full.csv.gz`
- `tables/timeseries_core_renamed_Aura.csv`
- `tables/utd_say_by_tick.csv`
- `utd_audit/tables/say_event_composer_audit_metrics.csv`
- `aura_justin_exchange.md`
