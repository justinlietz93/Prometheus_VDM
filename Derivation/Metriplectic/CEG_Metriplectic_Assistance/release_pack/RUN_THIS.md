# CEG Metriplectic Assisted-Echo — Quick Reproduce

## Prerequisites
- Python 3.10+
- numpy, matplotlib, scipy (see requirements.txt at repo root)

## One-command reproduce
```bash
cd Derivation/code
python -m physics.metriplectic.assisted_echo_runner --spec ../Metriplectic/CEG_Metriplectic_Assistance/release_pack/data/assisted-echo-t4-prereg-v1c.json --outdir ../Metriplectic/CEG_Metriplectic_Assistance/release_pack/figures
```

## Verify
```bash
bash Derivation/Metriplectic/CEG_Metriplectic_Assistance/release_pack/reproduce.sh
```

## What you should see
- All 4 instrument gates (G1–G4) pass at 100% across 12 seeds
- CEG median at λ=0.5: ≈0.0546 (preregistered threshold: ≥0.05)
- Figures regenerated in figures/

## Key references
- Proposal: ../T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md
- Results: ../T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.md
- Paper (TeX): ../T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex
