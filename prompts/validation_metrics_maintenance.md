**Create/Update `derivation/VALIDATION_METRICS.md` (MathJax-friendly, references-only)**

Search the entire repository (code, tests, notebooks, configs, experiment logs, docs, comments) and compile **all validation metrics/KPIs that are actually used** to assess VDM behavior. **Do not invent new metrics.** Use only what exists in the repo.

**Output file:** `derivation/VALIDATION_METRICS.md`
**Canon rule:** This file is the single owner of *metric specs* (names, purposes, thresholds, and links). **Do not paste or re-derive equations here.** Link to equations/constants/symbols by anchor.

**MathJax on GitHub:**

* Inline math only where needed for metric names/symbols: `$ ... $`
* Optional display math **only if quoting an existing line verbatim from the repo**: `$$ ... $$`
* **Do not use:** `\[` `\]`, `\(` `\)`, `\begin{equation}`, `\begin{align}`, `\tag`, labels/numbering, or package-specific macros.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Validation Metrics & KPIs (Auto-compiled)

**Last updated**: yyyy-mm-dd 
**Last commit**: {latest commit hash here}
**Scope:** Single source of truth for validation metrics used in this repository: names, purposes, thresholds/bands, and references to their definitions and implementations.  
**Rules:** Reference-only. Link to equations/constants/symbols/scripts; do not restate formulas here.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only when quoting existing math.
```

---

### Metric entry template (repeat for every metric you find)

*Populate strictly from repository content; no new text beyond brief summaries lifted from nearby comments/docs.*

```markdown
#### <Metric Name as used in repo>  <a id="kpi-<slug>"></a>
**Symbol (if any):** `$ <symbol> $`  
**Purpose:** <one-line purpose lifted from repo>  
**Defined by:** <link to equation anchor in `EQUATIONS.md` (e.g., `../derivation/EQUATIONS.md#vdm-e-###`)>  
**Inputs:** link symbols/constants used (e.g., `SYMBOLS.md#sym-...`, `CONSTANTS.md#const-...`)  
**Computation implemented at:** `<path/to/file>:<lines> • <short-commit>` (list all locations if multiple)  
**Pass band / thresholds:** literal values with links to constants (no formulas). Example: `[a, b]` → `CONSTANTS.md#const-...`  
**Units / normalization:** link into `UNITS_NORMALIZATION.md` (no re-explanations)  
**Typical datasets / experiments:** `<path>` or brief label found in repo  
**Primary figure/artifact (if referenced):** `<path/to/png|ipynb|md>`  
**Notes:** aliases, deprecations, or cross-links (lifted from repo text)
```

> **Important:** If a metric is described *only* in prose (no equation anchor yet), include the entry with `Defined by: TODO → add equation anchor` and cite the exact source lines. Do not invent the equation.

---

### Sections to populate (use only what exists; omit empty sections)

1. **Macro Banner (Headline KPIs)**

   * Collect metrics explicitly marked in repo as “banner”, “headline”, “key result”, or similar.
   * Present a short bullet list of links to those metric entries (no formulas).

2. **Core Dynamics Metrics**

   * All metrics tied to field dynamics, walkers, gating/scoreboard, plasticity, etc. (by whatever names appear in the repo).

3. **Stability & Safety Guards**

   * Thresholds, budget checks, drift monitors, CFL-type guards-link to implementations and constants.

4. **Performance / Efficiency Metrics**

   * Throughput, sparsity, utilization, memory retention, etc., as named in the repo.

5. **Domain-Specific Metrics**

   * RD, LBM/fluids, EFT/field-theory, tube/cylinder modes-whatever categories are evidenced by file paths or comments.

*(Order sections by repository evidence; do not invent categories. It’s OK to have a single flat list if the repo doesn’t group them.)*

---

### Index & de-duplication rules

* **One entry per distinct metric name.** If identical metrics are computed in multiple places, keep one canonical entry and list all code locations under **Computation implemented at**.
* If two names refer to the **same metric**, keep the most common name and list the alias in **Notes** with sources.
* Sort entries **lexicographically by metric name** within each section.

---

### Linking rules (anchors only; no restating math)

* Equations: `../derivation/EQUATIONS.md#vdm-e-###`
* Symbols: `../derivation/SYMBOLS.md#sym-...`
* Constants: `../derivation/CONSTANTS.md#const-...`
* Units maps: `../derivation/UNITS_NORMALIZATION.md#...`

If a required anchor is missing, add `TODO` in the entry and cite the repo lines; do not create content here.

---

### End-of-file blocks (append verbatim)

```markdown
<!-- BEGIN AUTOSECTION: METRICS-INDEX -->
<!-- Tool-maintained list of [Metric](#kpi-...) anchors for quick lookup -->
<!-- END AUTOSECTION: METRICS-INDEX -->

## Change Log
- <date> • metrics updated • <commit>
```

---

### Validation

* Ensure no formulas are copied into this file; *definitions must be links*.
* All thresholds and bands must point to `CONSTANTS.md` (do not restate numbers).
* Render on GitHub preview; confirm all anchors resolve and MathJax (if any) renders.
