**Create/Update `Derivation/RESULTS.md` (canonical index of experimental results; references-only for math/values)**

Search the entire repository (all `Derivation/` domain folders and subfolders) and compile **all RESULTS_*.md files that actually exist**. **Do not invent or infer content.** Use only what exists in the repo.

**Output file:** `Derivation/RESULTS.md`
**Canon rule:** This file is the single owner of the *results index*. **Do not paste equations, code, or raw data here.** Link to results documents and reference canonical files by anchor. Each results entry must document: run configurations, specs, schemas, methods, gates, outcomes, and artifacts.

**MathJax on GitHub:**

* Inline math only where needed for brief context or gate expressions: `$ ... $`
* Optional display math **only if quoting an existing line verbatim from a results file**: `$$ ... $$`
* **Do not use:** `\[` `\]`, `\(` `\)`, `\begin{equation}`, `\begin{align}`, `\tag`, labels/numbering, or package-specific macros.

---

### File header (insert verbatim at top)

```markdown
# RESULTS: Overview of Experimental Results

This document provides a comprehensive overview of all experimental results in the Void Dynamics Model (VDM) repository. Each results document follows whitepaper-grade standards with full narrative, MathJax-rendered equations, numeric figure captions tied to actual artifacts, explicit thresholds with pass/fail gates, and provenance. Results are organized by domain.

**Total Results Documents: {count}**

> Last Updated: {yyyy-mm-dd}  
> Template: `Templates/RESULTS_PAPER_STANDARDS.md`  
> Standards: All results must follow comprehensive documentation standards  
> Authorization: All experiments require approved PROPOSAL_ documents

---
```

---

### Results entry template (repeat for every RESULTS_*.md file found)

*Populate strictly from repository content; extract details from the actual results documents.*

```markdown
## {Domain Name} ({count} result{s})

### {Subdomain/} (if applicable)
- **{RESULTS_filename.md}**  
  Path: `{Domain}/{Subdomain/}{RESULTS_filename.md}`  
  *{Title from results document}*
  - **Run Configuration**: {brief extraction from Methods/Procedure section}
  - **Specs**: {key parameters from Variables/Equipment section}
  - **Schema**: {link to data products schema if documented, or describe artifact structure}
  - **Methods**: {brief summary from Methods/Procedure section}
  - **Gate{s}**: {explicit gate expressions with thresholds}
  - **Outcome**: {PASS/FAIL with measured values}
  - **Artifact{s}**: `{path to figures/logs/csvs with timestamps}`
  - **Summary**: {TL;DR or introduction one-liner lifted from document}
```

**Per-entry requirements:**
* **Run Configuration**: Extract computational setup: grid size (N), time steps (Δt), seeds, tolerances, integrator choices, composition schemes (e.g., Strang JMJ), numerical methods (Störmer-Verlet, discrete-gradient), boundary conditions
* **Specs**: List key dimensional/dimensionless parameters, control variables from the Variables section
* **Schema**: Document the structure of output artifacts (JSON logs, CSV columns, figure types). Link to `SCHEMAS.md#schema-...` if formalized
* **Methods**: Summarize the experimental procedure: what was measured, how gates were computed, instrument model
* **Gate{s}**: List all explicit pass/fail gates with their mathematical expressions and threshold values. Link thresholds to `CONSTANTS.md#const-...` where applicable
* **Outcome**: State PASS/FAIL and report measured values vs thresholds
* **Artifact{s}**: List all pinned artifacts (figures, CSVs, JSONs) with full paths and timestamps from the results document

---

### Sections to populate (organize by domain folders as found in repo)

Scan `Derivation/` for all domain folders containing RESULTS_*.md files. Group results by domain following the existing folder structure:
* Agency_Field/
* Causality/
* Collapse/
* Conservation_Law/
* Cosmology/
* Dark_Photons/
* Information/
* Intelligence_Model/
* Metriplectic/ (with subsections for subfolders)
* Qualia/
* Quantum_Gravity/
* Tachyon_Condensation/
* Thermodynamic_Routing/ (with subsections for subfolders)
* Topology/
* (any other domains found)

Within each domain, list results in alphabetical order by filename.

---

### Cross-reference requirements

For each results entry, verify and document:
* **Corresponding proposal**: Link to the PROPOSAL_*.md file that authorized the experiment (should be cited in results document)
* **Canonical references**: Ensure results reference canonical files where applicable:
  - Equations → `EQUATIONS.md#vdm-e-...`
  - Symbols → `SYMBOLS.md#sym-...`
  - Constants → `CONSTANTS.md#const-...`
  - Units → `UNITS_NORMALIZATION.md#...`
  - Algorithms → `ALGORITHMS.md#vdm-a-...`
  - Schemas → `SCHEMAS.md#schema-...`
* **Code locations**: Document the experiment runner path (e.g., `code/physics/{domain}/run_{experiment}.py`)

---

### Summary statistics table (append after all domain sections)

```markdown
---

## Summary Statistics by Domain

| Domain | Results Count | Key Focus |
|--------|--------------|-----------|
| {Domain} | {count} | {brief focus from entries} |
...

---
```

---

### End-of-file notes block (append verbatim)

```markdown
## Notes

- All results follow the standards at `Templates/RESULTS_PAPER_STANDARDS.md`
- Every result includes: TL;DR with artifact path, explicit gates, pass/fail outcomes, and full provenance
- Results must cite corresponding PROPOSAL_ document
- All artifacts (figures, CSVs, JSONs) are pinned with timestamps and tags for reproducibility
- Failed gates trigger contradiction reports and artifact quarantine

<!-- BEGIN AUTOSECTION: RESULTS-INDEX -->
<!-- Tool-maintained list of results by domain -->
<!-- END AUTOSECTION: RESULTS-INDEX -->

## Change Log
- {date} • results index updated • {commit}
```

---

### Validation checklist

Before finalizing the update:
* [ ] Every RESULTS_*.md file in the repository is listed exactly once
* [ ] Each entry extracts run configuration, specs, schema, methods, gates, outcomes, and artifacts
* [ ] All artifact paths are validated against actual file locations
* [ ] Domain organization matches the repository folder structure
* [ ] Summary statistics table matches the actual counts
* [ ] Total results count in header is accurate
* [ ] All MathJax renders correctly on GitHub preview
* [ ] No equations, code blocks, or raw data duplicated from source files-use links/brief summaries only
* [ ] Every result cites its corresponding PROPOSAL_ document
* [ ] Schema documentation describes artifact structure (JSON fields, CSV columns, figure types)

---

### De-duplication and consistency

* One entry per RESULTS_*.md file; do not create multiple entries for the same file
* If a results file covers multiple experiments/phases, keep one entry and document all configurations, gates, and outcomes in that single entry
* Results file path must be exact and relative to `Derivation/` root
* Maintain consistent formatting across all entries
* Use the document's own title and summary; do not paraphrase unnecessarily
