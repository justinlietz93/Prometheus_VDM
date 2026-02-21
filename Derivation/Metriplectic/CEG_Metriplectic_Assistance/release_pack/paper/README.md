# Paper Source Files

The paper source files live at:

- **TeX source**: `../../T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex`
- **Markdown**: `../../T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.md`
- **Proposal**: `../../T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md`
- **Bibliography**: `../../references.bib`
- **PDF (pre-built)**: `../../T4_RESULTS_CEG_AssistedECHO.pdf`

## Compile Instructions

```bash
cd Derivation/Metriplectic/CEG_Metriplectic_Assistance
pdflatex T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex
bibtex T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment
pdflatex T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex
pdflatex T4_RESULTS_CEG_Metriplectic_Assisted-Echo_Experiment.tex
```

Requires a standard LaTeX distribution (TeX Live, MiKTeX) with the `amsmath`,
`amssymb`, `hyperref`, and `natbib` packages.
