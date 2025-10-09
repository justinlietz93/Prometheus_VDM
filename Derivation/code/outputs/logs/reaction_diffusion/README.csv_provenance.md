# CSV Sidecar Provenance (reaction_diffusion)

This directory contains CSV sidecars derived from existing JSON logs to satisfy the canon rule: runner + CSV/JSON + figure.

Files derived in this pass:

- rd_front_speed_experiment_20250824T053748Z.csv
  - Source JSON: rd_front_speed_experiment_20250824T053748Z.json
  - Fields: run parameters, fit metrics (c_meas, rel_err, R^2, etc.), acceptance thresholds, pass flag, timestamp.
- rd_dispersion_experiment_20250824T053842Z.csv
  - Source JSON: rd_dispersion_experiment_20250824T053842Z.json
  - Fields: run parameters, med_rel_err, r2_array, elapsed_sec, timestamp.

Notes:

- No values were altered; the CSVs are faithful tabular extracts of the JSON logs to improve auditability and allow spreadsheet tooling.
- When runners are updated to emit CSV natively, these derived CSVs can be superseded by runner-emitted sidecars.
- Contact: Justin K. Lietz (VDM Project)
