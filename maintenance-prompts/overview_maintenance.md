**Create/Update `Derivation/VDM_OVERVIEW.md` (reference-only; link to canon; no new theory)**

Search the entire repository (docs, canon registries, RESULTS/PROPOSAL papers, audits under `audits/`, domain READMEs, code comments near instruments) and compile a high-level overview that reflects the current, accepted state of the VDM project. Use only content that already exists. Do not invent new claims or numbers. All statements must be backed by in-repo sources via anchors or explicit paths.

**Output file:** `Derivation/VDM_OVERVIEW.md`

**Canon rule:** This file is reference-only. Do not restate equations, symbol meanings, constants, units, or algorithms. Link to them by anchor. When a concise phrase is needed, lift it verbatim (or minimally condensed) from source text and cite that path/anchor.

**MathJax on GitHub:**

- Inline only when quoting names/symbols: `$ ... $`
- No display math or LaTeX environments here.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: REFERENCE -->
# VDM Overview (Compiled from Repository Evidence)

**Last updated**: yyyy-mm-dd  
**Last commit**: {latest commit hash here}  
**Scope:** High-level overview synced to canon files and proven instruments; all claims trace to in-repo sources by anchor.  
**Rules:** Reference-only. Link to canonical math/specs (SYMBOLS/EQUATIONS/CONSTANTS/UNITS/ALGORITHMS/BC_IC/VALIDATION/DATA_PRODUCTS/SCHEMAS). Do not duplicate canon here.
```

---

### Sections to populate (reference-only; anchors required)

1) **Canonical Model Banner**  
Summarize the currently accepted canonical branch and scoped branches with anchors only. No new numbers or equations; link to canon.

```markdown
## Canonical Model Banner
- **Canonical branch:** Reaction–Diffusion (RD) • Evidence: `EQUATIONS.md#vdm-e-015`, `EQUATIONS.md#vdm-e-016`, `EQUATIONS.md#vdm-e-017`, `EQUATIONS.md#vdm-e-018`
- **Scoped branches:** EFT/KG (J-only), Metriplectic J⊕M composition • Evidence: `EQUATIONS.md#vdm-e-014`, `EQUATIONS.md#vdm-e-042`, `EQUATIONS.md#vdm-e-091` (composition diagnostics)
- **Discrete → continuum mapping (links only):** `EQUATIONS.md#vdm-e-011`, `EQUATIONS.md#vdm-e-012`, CHRONICLES notes (mapping lines)
- **Validation gates overview:** link to `VALIDATION_METRICS.md#...` anchors (no thresholds pasted)
- **Proven instruments (examples):** link to RESULTS entries (e.g., KG Noether, RD front speed, RD dispersion, metriplectic JMJ structure)
- **RB-Gate (fluids onset) as meter:** link `EQUATIONS.md#vdm-e-121`–`#vdm-e-124`
- **Causality meters:** link telegraph speed and locality/dispersion meters (`EQUATIONS.md#vdm-e-105`, KG meters in RESULTS)
```

2) **Branches (scoped summaries with anchors)**  
Provide one entry per branch present in the repo evidence. Use this template for each branch you find explicitly described.

```markdown
## Branch: {Name}  <a id="branch-{slug}"></a>
**Scope:** <one‑line excerpt lifted from repo, with path/anchor>  
**Primary equations:** `EQUATIONS.md#vdm-e-...`, `EQUATIONS.md#vdm-e-...`  
**Proven instruments (links):** RESULTS entries related to this branch  
**Status:** reference to CHRONICLES entry (link) or explicit status tag in source (e.g., T2 meter, scoped future work)  
**Notes:** brief evidence pointer (paths/anchors only; no numbers)
```

3) **Domains (overview; group by existing folders)**  
Summarize each scientific domain represented in `Derivation/` with links to PROPOSALS/RESULTS where present.

```markdown
## Domain: {Domain Name}  <a id="dom-{slug}"></a>
- **Summary (1–2 lines):** lifted verbatim or minimally condensed from domain README or top-of-file context with `path:lines`  
- **Key proposals:** link to `PROPOSALS.md` section and/or explicit `Derivation/{Domain}/PROPOSAL_*.md`  
- **Key results:** link to `RESULTS.md` section and/or explicit `Derivation/{Domain}/RESULTS_*.md`  
- **Canon references (anchors only):** symbols → `SYMBOLS.md#sym-...`, equations → `EQUATIONS.md#vdm-e-...`, constants → `CONSTANTS.md#const-...`, units → `UNITS_NORMALIZATION.md#...`, algorithms → `ALGORITHMS.md#vdm-a-...`, metrics → `VALIDATION_METRICS.md#kpi-...`
```

4) **Instruments and KPIs (links only, no formulas)**  
Summarize meters and acceptance gates by linking to canonical metrics anchors and RESULTS writeups.

```markdown
## Instruments and KPIs
- Meter: <name> • RESULTS link • KPIs: `VALIDATION_METRICS.md#kpi-...` (no thresholds pasted)
- Meter: <name> • RESULTS link • KPIs: `VALIDATION_METRICS.md#kpi-...`
```

5) **Artifacts & IO Policy (links only)**  
Route to IO helper and standards; do not restate details.

```markdown
## Artifacts & IO Policy
- IO helper paths: `code/common/io_paths.py` (link by path)  
- Standards / templates: `Templates/PROPOSAL_PAPER_TEMPLATE.md`, `Templates/RESULTS_PAPER_STANDARDS.md`  
- Quarantine / approvals: `code/common/authorization/README.md`
```

6) **Tier Status Snapshot (links only)**  
Report counts and statuses by linking to indices and CHRONICLES entries; do not restate numbers in this template (tools can fill later).

```markdown
## Tier Status Snapshot
- Proposals index: `PROPOSALS.md` • Results index: `RESULTS.md` • CHRONICLES: `Derivation/CHRONICLES.md`
- Notes: If tiers (T0–T9) are summarized elsewhere, link those summaries (no duplication here).
```

---

### Cross-reference requirements

For every bullet/claim in the overview:

- Provide at least one anchor to a canonical file or to a PROPOSAL/RESULTS document in Derivation.
- Prefer anchors:  
  - Symbols → `../Derivation/SYMBOLS.md#sym-...`  
  - Equations → `../Derivation/EQUATIONS.md#vdm-e-...`  
  - Constants → `../Derivation/CONSTANTS.md#const-...`  
  - Units → `../Derivation/UNITS_NORMALIZATION.md#...`  
  - Algorithms → `../Derivation/ALGORITHMS.md#vdm-a-...`  
  - BC/IC/Geometry → `../Derivation/BC_IC_GEOMETRY.md#...`  
  - Validation metrics → `../Derivation/VALIDATION_METRICS.md#kpi-...`  
  - Data products → `../Derivation/DATA_PRODUCTS.md#data-...`  
  - Schemas → `../Derivation/SCHEMAS.md#schema-...`  
- If a needed anchor is missing, write: `TODO: add anchor (see <path>:<line>)`. Do not paste canon content.

---

### Entry templates (repeat as needed)

1) Branch entry (scoped):

```markdown
### {Branch Name}  <a id="branch-{slug}"></a>
**Scope:** <one line from source> (`<path>:<lines>`)  
**Primary equations:** `EQUATIONS.md#vdm-e-...`  
**Meters:** link to RESULTS entries  
**Status:** link to CHRONICLES or explicit status tag in source
```

2) Domain entry:

```markdown
### {Domain}  <a id="dom-{slug}"></a>
- **Summary:** <one–two lines lifted> (`<path>:<lines>`)  
- **Proposals:** `PROPOSALS.md#...` (+ direct file links if helpful)  
- **Results:** `RESULTS.md#...` (+ direct file links if helpful)  
- **Canon refs:** symbols/equations/constants/units/algorithms/metrics anchors
```

3) Instrument/KPI listing:

```markdown
- Meter: <name> • RESULTS: `<path>` • KPIs: `VALIDATION_METRICS.md#kpi-...`
```

---

### De-duplication & ordering

- **One branch entry per branch name.** If multiple sources discuss the same branch, keep one entry and list all sources inline as `(path:lines)`.
- **One domain entry per domain folder name.** If subdomains exist, add subsections under the domain using the same template.
- **Order:**  
  - Branches: canonical first, then scoped branches by repository path (lexicographic) of first cited source.  
  - Domains: by repository path (lexicographic).  
  - Instruments: by RESULTS path (lexicographic).

---

### Indices & blocks (append verbatim)

```markdown
<!-- BEGIN AUTOSECTION: OVERVIEW-INDEX -->
<!-- Tool-maintained list of overview anchors (branches/domains/instruments) -->
<!-- END AUTOSECTION: OVERVIEW-INDEX -->

**Change Log (ADD THIS TO CHRONICLES.md):**

```markdown
## Change Log
- <date> • overview synced to canon • <commit>
```

---

### Validation checklist

Before finalizing the update:

- [ ] Every overview statement is backed by an in-repo path and/or anchor
- [ ] No equations or numeric thresholds pasted here (links only)
- [ ] All anchors resolve in GitHub preview
- [ ] Branch/domain/instrument ordering follows the rules above
- [ ] DOC-GUARD header present and accurate (date/commit filled)
- [ ] Any missing anchors are marked with `TODO: add anchor (see <path>:<line>)`

---

### Notes

- This maintenance guide enforces canon discipline: OVERVIEW is a navigational surface, not a source of equations or values.  
- Keep language minimal and sourced; prefer one-liners pointing to the canonical owners.  
- If CHRONICLES indicates policy clarifications affecting the overview, link those entries rather than paraphrasing.
