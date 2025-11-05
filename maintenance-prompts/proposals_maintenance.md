**Create/Update `Derivation/PROPOSALS.md` (canonical index of research proposals; references-only for math/values)**

Search the entire repository (all `Derivation/` domain folders and subfolders) and compile **all PROPOSAL_*.md files that actually exist**. **Do not invent or infer content.** Use only what exists in the repo.

**Output file:** `Derivation/PROPOSALS.md`
**Canon rule:** This file is the single owner of the *proposals index*. **Do not paste equations, code, or implementation details here.** Link to proposal documents and reference canonical files by anchor. Each proposal entry must document: experimental setup, diagnostics, parameters, gates, methods, maturity tier, and provenance at similar rigor to results.

**MathJax on GitHub:**

* Inline math only where needed for brief context or key expressions: `$ ... $`
* Optional display math **only if quoting an existing line verbatim from a proposal file**: `$$ ... $$`
* **Do not use:** `\[` `\]`, `\(` `\)`, `\begin{equation}`, `\begin{align}`, `\tag`, labels/numbering, or package-specific macros.

---

### File header (insert verbatim at top)

```markdown
# PROPOSALS: Overview of Research Proposals

This document provides a comprehensive overview of all research proposals in the Void Dynamics Model (VDM) repository. Each proposal follows the whitepaper-grade template standards and includes explicit gates, MathJax-rendered equations, and full provenance. Proposals are organized by domain and follow the T0-T9 maturity ladder.

**Total Proposals: {count}**

> Last Updated: {yyyy-mm-dd}  
> Template: `Templates/PROPOSAL_PAPER_TEMPLATE.md`  
> Standards: All proposals must be approved before experiments can run  
> Authorization: See `code/common/authorization/README.md`

---
```

---

### Proposal entry template (repeat for every PROPOSAL_*.md file found)

*Populate strictly from repository content; extract details from the actual proposal documents.*

```markdown
## {Domain Name} ({count} proposal{s})

### {Subdomain/} (if applicable)
- **{PROPOSAL_filename.md}**  
  Path: `{Domain}/{Subdomain/}{PROPOSAL_filename.md}`  
  *{Title or Abstract one-liner from proposal}*
  - **Tier**: {T0-T9 maturity level if documented}
  - **Research Question{s}**: {key questions from Background/Rationale section}
  - **Experimental Setup**: {protocol, parameters, trial configuration from section 5.1}
  - **Diagnostics**: {measurements, metrics, gate computations}
  - **Gate{s}**: {explicit gate expressions with thresholds and pass criteria}
  - **Variables**: {independent, dependent, and control variables from Variables section}
  - **Methods/Protocol**: {procedure steps, numerical methods, integrators, composition schemes}
  - **Schema/Artifacts**: {planned output structure: figure types, CSV columns, JSON fields, artifact tags}
  - **Equipment/Software**: {runner scripts, environment, dependencies}
  - **Risk Assessment**: {identified risks and mitigation strategies}
  - **Personnel**: {proposers, roles, institutions}
  - **References**: {citations to derivation notes, canonical files, prior work}
  - **Summary**: {abstract or background rationale lifted from document}
```

**Per-entry requirements:**

* **Tier**: Document the maturity level (T0-T9) if specified; reference TIER_STANDARDS.md for ladder definition
* **Research Question{s}**: Extract the core scientific questions from Background/Rationale section
* **Experimental Setup**: Detail the protocol - parameter ranges (e.g., Θ ∈ {1.5, 2.5, 3.5}, Δm ∈ [-2, 2]), sampling strategy, trial counts, computational configuration (grid size, time steps, boundary conditions)
* **Diagnostics**: Document how measurements will be taken, what metrics will be computed, instrument models
* **Gate{s}**: List all explicit pass/fail gates with mathematical expressions and threshold values. Link thresholds to `CONSTANTS.md#const-...` where applicable
* **Variables**: Extract the complete variable table: independent variables, dependent variables, control variables with rationales
* **Methods/Protocol**: Summarize the procedure: numerical methods (e.g., Störmer-Verlet, discrete-gradient, Strang composition), algorithmic steps, risk assessment
* **Schema/Artifacts**: Document the planned artifact structure - figure specifications, CSV column definitions, JSON log fields, artifact naming/tagging convention
* **Equipment/Software**: List runner script paths, software dependencies, Git commit references for reproducibility
* **Risk Assessment**: Document identified risks (methodological, computational, safety) and mitigation strategies
* **Personnel**: List proposers, roles, and institutions
* **References**: Extract citations to derivation notes, equations, prior proposals/results
* **Summary**: One-paragraph abstract or scientific rationale lifted from the proposal

---

### Sections to populate (organize by domain folders as found in repo)

Scan `Derivation/` for all domain folders containing PROPOSAL_*.md files. Group proposals by domain following the existing folder structure:

* Agency_Field/ (with subsections for subfolders like Coordination_Depth/, Witness/)
* Causality/
* Collapse/
* Conservation_Law/
* Cosmology/
* Dark_Photons/
* Information/
* Intelligence_Model/
* Metriplectic/ (with subsections for subfolders like Thermal_Landscape_Quench/, Self_Model_Assisted_Echo/, etc.)
* Qualia/
* Quantum_Gravity/
* Tachyon_Condensation/
* Thermodynamic_Routing/ (with subsections for Passive_Thermodynamic_Routing/, Wave_Flux_Meter/, etc.)
* Topology/
* (any other domains found)

Within each domain, list proposals in alphabetical order by filename.

---

### Cross-reference requirements

For each proposal entry, verify and document:

* **Maturity tier**: If higher-tier proposals (T4+) reference supporting work, document those dependencies
* **Canonical references**: Ensure proposals reference canonical files where applicable:
  * Equations → `EQUATIONS.md#vdm-e-...`
  * Symbols → `SYMBOLS.md#sym-...`
  * Constants → `CONSTANTS.md#const-...`
  * Units → `UNITS_NORMALIZATION.md#...`
  * Algorithms → `ALGORITHMS.md#vdm-a-...`
  * Schemas → `SCHEMAS.md#schema-...`
* **Downstream results**: If a corresponding RESULTS_*.md file exists, note it (for tracking proposal → execution → results lineage)
* **Code locations**: Document planned experiment runner paths (e.g., `code/physics/{domain}/run_{experiment}.py`)
* **Authorization status**: Note if proposal has been approved for execution (reference authorization README)

---

### End-of-file notes block (append verbatim)

```markdown
---

## Notes

- All proposals must follow the template at `Templates/PROPOSAL_PAPER_TEMPLATE.md`
- Proposals are graded T0-T9 according to maturity ladder (see TIER_STANDARDS.md)
- Each proposal requires approval before experiments can run
- Proposals must include: explicit gates, provenance, equations, and artifact paths
- Higher-tier proposals (T4+) must reference supporting work from lower tiers
- Experimental setup, diagnostics, variables, methods, and schema documentation must be comprehensive and rigorous
- All gates must have explicit pass/fail thresholds with units and normalization specified

<!-- BEGIN AUTOSECTION: PROPOSALS-INDEX -->
<!-- Tool-maintained list of proposals by domain -->
<!-- END AUTOSECTION: PROPOSALS-INDEX -->

## Change Log
- {date} • proposals index updated • {commit}
```

---

### Validation checklist

Before finalizing the update:

* [ ] Every PROPOSAL_*.md file in the repository is listed exactly once
* [ ] Each entry extracts: tier, research questions, experimental setup, diagnostics, gates, variables, methods, schema, equipment, risks, personnel, references, summary
* [ ] Experimental setup includes parameter ranges, sampling strategy, trial configuration
* [ ] Diagnostics describe measurement instruments and metric computation
* [ ] All gates are explicitly documented with thresholds and pass criteria
* [ ] Variables section documents independent, dependent, and control variables with rationales
* [ ] Methods/Protocol section details numerical methods, integrators, and algorithmic steps
* [ ] Schema documentation specifies planned artifact structure (figures, CSVs, JSONs)
* [ ] Equipment/Software lists runner scripts and dependencies
* [ ] Risk assessment documents identified risks and mitigations
* [ ] Domain organization matches the repository folder structure
* [ ] Total proposals count in header is accurate
* [ ] All MathJax renders correctly on GitHub preview
* [ ] No equations, code blocks, or detailed math duplicated from source files-use links/brief summaries only
* [ ] Maturity tier documented (T0-T9) when specified
* [ ] Authorization status noted where applicable
* [ ] Links to corresponding RESULTS_*.md files when they exist

---

### De-duplication and consistency

* One entry per PROPOSAL_*.md file; do not create multiple entries for the same file
* If a proposal covers multiple phases or variations, keep one entry and document all configurations and gates in that single entry
* Proposal file path must be exact and relative to `Derivation/` root
* Maintain consistent formatting across all entries
* Use the document's own title, abstract, and key questions; do not paraphrase unnecessarily
* Ensure rigor level matches results documentation: comprehensive extraction of setup, diagnostics, methods, and schemas
