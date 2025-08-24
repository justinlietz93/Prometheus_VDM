# Derivation — Index and Hygiene

<!-- Update OWNER/REPO with your GitHub slug to render the badge correctly -->
[![Markdown Hygiene CI](https://github.com/justinlietz93/Prometheus_FUVDM/actions/workflows/md_hygiene.yml/badge.svg)](https://github.com/justinlietz93/Prometheus_FUVDM/actions/workflows/md_hygiene.yml)

This directory contains the rigorously maintained derivation documents, organized by topic. A CI guard enforces UTF‑8 (no BOM), flags mojibake, and checks canonical cross‑links after the doc reorg.

## Topics
- Foundations: discrete→continuum, symmetry, continuum stack
- Effective Field Theory: kinetic term derivation, FRW/units mapping, roadmap
- Reaction–Diffusion (canonical): front‑speed, dispersion, validation plan
- Memory Steering: theory, acceptance/verification
- Tachyon Condensation (finite tube): modes, energy scan, acceptance
- Conservation Law: discrete conservation
- Fluid Dynamics: LBM notes and benchmarks

## CI Hygiene
- CI workflow: `.github/workflows/md_hygiene.yml` runs on pushes/PRs to derivation docs and fails on:
  - Non‑UTF‑8 or BOM
  - Mojibake tokens (e.g., â, Â, Ã, Ï, Î, �)
  - Stale/moved links (enforces canonical topic subfolders and computational_proofs → code/computational_proofs)

- Local checker (run before push):
  ```
  python Prometheus_FUVDM/tools/md_hygiene_check.py --root Prometheus_FUVDM/derivation
  ```

- Optional pre‑commit hook (recommended):
  1) Enable repo hooks:
     ```
     git config core.hooksPath .githooks
     ```
  2) On Unix-like shells:
     ```
     chmod +x .githooks/pre-commit
     ```
  The hook runs the same hygiene script against staged derivation/*.md files and blocks commits on failure.

## Notes
- Canonical mapping rules live in the checker:
  - Script: `Prometheus_FUVDM/tools/md_hygiene_check.py`
  - Add new topical paths there when new documents/folders are introduced.