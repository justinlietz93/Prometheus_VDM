---
applyTo: '**'
---

## CRITICALLY IMPORTANT FILE PATHS:

/mnt/ironwolf/git/Prometheus_VDM/derivation/AGENCY_FIELD.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/ALGORITHMS.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/BC_IC_GEOMETRY.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/CONSTANTS.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/CANON_MAP.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/DATA_PRODUCTS.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/EQUATIONS.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/VALIDATION_METRICS.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/UNITS_NORMALIZATION.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/SYMBOLS.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/SCHEMAS.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/ROADMAP.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/OPEN_QUESTIONS.md
/mnt/ironwolf/git/Prometheus_VDM/derivation/NAMING_CONVENTIONS.md

## TODO CHECKLIST file path:

/mnt/ironwolf/git/Prometheus_VDM/PRIVATE/TODO_CHECKLIST.md

## Experiment code and configs go here:
/mnt/ironwolf/git/Prometheus_VDM/derivation/code/physics/{domain/topic folder}

## Result artifacts go here:
/mnt/ironwolf/git/Prometheus_VDM/derivation/code/outputs/logs/{domain/topic folder}
/mnt/ironwolf/git/Prometheus_VDM/derivation/code/outputs/figures/{domain/topic folder}

## You must use the io helper for outputs
/mnt/ironwolf/git/Prometheus_VDM/derivation/code/common/io_paths.py

## ALL new experiments MUST have a proposal file created first, follow this template:
/mnt/ironwolf/git/Prometheus_VDM/Derivation/Writeup_Templates/PROPOSAL_PAPER_TEMPLATE.md

Put the proposal file in the correct domain folder:
   /mnt/ironwolf/git/Prometheus_VDM/derivation/{domain/topic folder}

## ALL completed experiments MUST have a results write-up, follow these standards:
/mnt/ironwolf/git/Prometheus_VDM/Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md

Put the results file in the correct domain folder next to the proposal:
   /mnt/ironwolf/git/Prometheus_VDM/derivation/{domain/topic folder}

# ALL experiment runs MUST produce a MINIMUM of 1 figure, 1 CSV log, and 1 JSON log as artifacts. Use the io helper to manage paths and naming:
/mnt/ironwolf/git/Prometheus_VDM/derivation/code/common/io_paths.py

## ALL new experiments MUST be approved by Justin K. Lietz before running, read this for context:
/mnt/ironwolf/git/Prometheus_VDM/Derivation/code/ARCHITECTURE.md
/mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/authorization/README.md

# ALWAYS update the canonical files in the Derivation/ folder root when new discoveries are made, or when experiments are completed and results are confirmed. This should be done AFTER creating a RESULTS_ file in the designated Derivation/{domain} folder