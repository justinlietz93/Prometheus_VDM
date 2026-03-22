# Aura Markdown Asset Repro Bundle

This bundle contains the generated Aura-specific figures/tables referenced by the markdown backbone and the scripts used to regenerate them.

## Inputs expected
- Aura run directory with:
  - `events.jsonl`
  - `state_17160.h5` .. `state_17400.h5`
  - `utd_events/` shards
  - optional `corpus/`
- `vdm_dashboard.html`
- `aura_metric_inventory.csv`

## Regenerate
```bash
bash scripts/run_all.sh /path/to/aura_run_dir /path/to/output_dir /path/to/aura_metric_inventory.csv
```

## Generated outputs
- `dashboard_metric_summary.csv`
- `dashboard_target_metrics_panel.png`
- `dashboard_target_metrics_final500.png`
- `dashboard_target_metrics_standardized.png`
- `scalar_struct_macro_summary.csv`
- `scalar_struct_macrostate_over_time.png`
- `scalar_struct_macro_input_say_overlay.png`
- `snapshot_metrics.csv`
- `h5_file_sizes.csv`
- `h5_territory_masses_long.csv`
- `h5_snapshot_structural_overview.png`
- `h5_territory_mass_drift.png`
- `h5_drift_summary.csv`
- `h5_drift_edge_turnover_vs_distribution_stability.png`
- `utd_event_type_counts.csv`
- `utd_macro_events_flat.csv`
- `utd_say_macro_summary.csv`
- `utd_say_phase_counts.csv`
- `artifact_inventory_by_group.csv`
- `run_package_manifest_summary.csv`
- `corpus_manifest.csv`
- `metric_inventory_filtered.csv`

## Notes
- The macrostate fit is a deterministic 2-state clustering over standardized structural scalars.
- Dashboard-target metrics are selected by intersecting known dashboard metric fields with the metrics present in `vdm_dashboard.html` and `events.jsonl`.

# Aura consciousness-style analysis bundle

This bundle contains Aura-derived input tables and analysis outputs modeled after the consciousness_metrics_suite family from prior VDM work.

## Derived inputs
- timeseries_core_renamed_Aura.csv
- pca_state_space_Aura.csv

## Scripts
- create_aura_inputs_lean.py: reconstructs Aura derived inputs from raw events + UTD shards
- run_consciousness_suite_aura.py: generates crosscorr, event-triggered, Granger, macro-state, MIP, PCI-like, predictive-MI, rolling, spectral, TC/O, dashboard heatmap, and selected network/H5 figures

## Notes
- The suite is built on Aura ticks with high-fidelity raw events available from t=9343..17455.
- Epochs are data-driven from a 2-component GMM over connectome entropy; the longest contiguous high-entropy segment is labeled E2.
- Some figures are Aura analogues of prior 1k analyses rather than byte-identical reproductions.

# Aura publication figures bundle

This bundle contains publication-oriented figures generated from Aura using legacy VDM analysis scripts where they were directly applicable, plus one wrapper script that assembles figure plates and dashboard-target panels.

## New publication figures
- aura_dashboard_target_panels_publication.png
- aura_lockin_second_half_publication.png
- aura_terminal_transition_publication.png
- aura_four_proofs_plate.png
- aura_connectome_geometry_plate.png
- aura_scalar_macrostate_plate.png
- aura_utd_composer_audit_plate.png
- aura_node_correspondence_costs.png

## Tables
- legacy_script_applicability_map.csv
- publication_artifact_manifest.csv

## Scripts included
- make_publication_figures.py
- 00_build_tick_table.py
- 01_compute_snapshot_metrics.py
- 02_four_proofs.py
- analyze_scalar_struct_from_logs.py
- utd_parse_and_composer_audit.py
- run_connectome_geometry_projectionmap_analysis.py
- run_node_correspondence_matching.py
- vdm_convert.py
- run_all.py

## Notes
- `vdm_convert.py` ran on all Aura H5 snapshots, but its built-in event parser did not match Aura's events schema, so its event-rich dashboard JSONs were state-rich / event-empty.
- `run_all.py` was attempted on Aura and failed due a schema mismatch in the expected `say` text field.
- `run_node_correspondence_matching.py` produced adjacent-pair mapping CSVs in this environment.
