# VDM Documentation Index (rapidly evolving)

**Author:** Justin K. Lietz  
**Contact:** <justin@neuroca.ai>  
**Zenodo Community:** [Void Dynamics Model](https://zenodo.org/communities/void-dynamics-model/records?q=&l=list&p=1&s=10&sort=newest)  
**ORCID:** [0009-0008-9028-1366](https://orcid.org/0009-0008-9028-1366)  
**Created:** Saturday, November 8, 2025  

> NOTE — repository velocity:
> This repository is growing and evolving rapidly. If this page’s “last updated” timestamp (or the file’s Git commit date) is older than a few days, the content here may be incomplete or stale. For the authoritative, current state, use the single‑source‑of‑truth pointers below.

## Single source of truth

The canon lives in Derivation/ with anchors and KPIs:

- Canon change log and attestations: [CHRONICLES.md](../Derivation/CHRONICLES.md)
- Axioms (A0–A7) and cross‑links to gates: [AXIOMS.md](../Derivation/AXIOMS.md)
- Equations registry (anchors, no duplication): [EQUATIONS.md](../Derivation/EQUATIONS.md)
- Validation metrics (KPIs/gates, thresholds): [VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md)
- Results authoring standards: [RESULTS_PAPER_STANDARDS.md](../Derivation/Templates/RESULTS_PAPER_STANDARDS.md)
- IO policy (figures/logs/json routing): [python.io_paths](../Derivation/code/common/io_paths.py:1)

## Freshness checklist (quick)

- Check the canon attestation: [CHRONICLES.md](../Derivation/CHRONICLES.md) has the latest “Change Attestation” entries with exact file paths, anchors, and dates.
- Prefer anchors over prose. If a page text conflicts with an anchor in [EQUATIONS.md](../Derivation/EQUATIONS.md) or [VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md), the anchor is authoritative.
- Verify proposal/result pointers:
  - Proposals live under Derivation by domain (e.g., [Derivation/Nonequilibrium/…](../Derivation/Nonequilibrium)).
  - Code instruments live under Derivation/code/… (snake_case).
- If in doubt, read the relevant KPI and its thresholds in [VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md) and the referenced anchor in [EQUATIONS.md](../Derivation/EQUATIONS.md).

## How we keep this consistent

- No duplication: reference anchors like `[VDM-E-###]` in prose; keep numbers/equations in canon files only.
- Every canon‑impacting change adds an entry in [CHRONICLES.md](../Derivation/CHRONICLES.md) with:
  - Paths changed
  - Anchors added/updated
  - Dependencies reviewed
  - Approval/PR status

## Where to start

- Background and standards: [VDM_Project_Standards_Technical_Summary.md](./VDM_Project_Standards_Technical_Summary.md)
- Active axioms and scale program: [AXIOMS.md](../Derivation/AXIOMS.md) and [VALIDATION_METRICS.md](../Derivation/VALIDATION_METRICS.md)
- Algorithms/pseudocode adapters: [ALGORITHMS.md](../Derivation/ALGORITHMS.md)
- Open questions / roadmap: [OPEN_QUESTIONS.md](../Derivation/OPEN_QUESTIONS.md) and [ROADMAP.md](../Derivation/ROADMAP.md)

## Provenance discipline (for contributors)

When updating any document under docs/:

- Link to canon by anchor instead of repeating equations or constants.
- If the change reflects or depends on canon movement, add the corresponding attestation block in [CHRONICLES.md](../Derivation/CHRONICLES.md) and reference it here only by path/anchor.
- Route all artifacts via [python.io_paths](../Derivation/code/common/io_paths.py:1) and follow RESULTS standards.
