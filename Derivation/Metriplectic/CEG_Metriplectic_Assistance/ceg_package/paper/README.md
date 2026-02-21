# Paper

The full paper describing this instrument and its theoretical foundations is:

**T4: CEG Metriplectic Assisted-Echo Experiment**

**Author:** Justin K. Lietz — Neuroca, Inc.  
**ORCID:** [0009-0008-9028-1366](https://orcid.org/0009-0008-9028-1366)

## Location in Repository

The paper source files are located at:

```
Derivation/Metriplectic/CEG_Metriplectic_Assistance/
├── T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex   # LaTeX source
├── T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.md    # Markdown version
├── T4_RESULTS_CEG_AssistedECHO.pdf                            # Compiled PDF
└── references.bib                                             # Bibliography
```

## How to Compile

```bash
cd Derivation/Metriplectic/CEG_Metriplectic_Assistance/
pdflatex T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex
bibtex T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment
pdflatex T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex
pdflatex T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex
```

## Abstract

This paper presents the CEG (Counterfactual Echo Gain) instrument — a gate-certified
observable that quantifies whether a model-aware time-reversal improves state recovery
versus a model-blind baseline. The physics is a metriplectic split (Klein-Gordon J-limb
+ reaction-diffusion M-limb) via Strang splitting. Five instrument gates certify each
run. Published result (2025-11-04): 12 seeds × 5 λ values, all gates pass, with
median CEG > 0 at λ > 0.
