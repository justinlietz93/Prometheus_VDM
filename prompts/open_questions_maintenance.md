**Create/Update `derivation/OPEN_QUESTIONS.md` (MathJax-friendly, speculation-only, references-required)**

Search the entire repository (code, tests, notebooks, docs, comments, configs, experiment logs, Issues/PRs if mirrored in the repo) and compile **only the questions, hypotheses, uncertainties, and “future work” items that actually exist**. **Do not invent new questions or rewrite meaning.** Use only what’s in the repo.

**Output file:** `derivation/OPEN_QUESTIONS.md`
**Canon rule:** This file is the single owner of **speculative/working questions**. It must **not** redefine symbols, equations, or values-link to the canonical files.

**MathJax on GitHub:**

* Inline: `$ ... $`
* Display (only when quoting an existing snippet): `$$ ... $$`
* **Do not use:** `\[` `\]`, `\(` `\)`, LaTeX environments (`\begin{...}`), `\tag`, labels/numbering, or package-specific macros.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: WORKING-THEORY -->
# VDM Open Questions & Working Hypotheses (Auto-compiled)

**Last updated**: yyyy-mm-dd 
**Last commit**: {latest commit hash here}
**Scope:** Repository-sourced questions, hypotheses, uncertainties, and “future work” items.  
**Rules:** Quote/condense from sources; link to canon (SYMBOLS/EQUATIONS/CONSTANTS/UNITS/ALGORITHMS/BC_IC/VALIDATION). Do not restate math or numbers here.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only when quoting existing math.
```

---

### What to collect (strict evidence)

Include items explicitly marked or phrased as: `OPEN`, `QUESTION`, `HYPOTHESIS`, `CONJECTURE`, `ASSUMPTION (unverified)`, `LIMITATION`, `FUTURE WORK`, `TODO (research)`, “prove/disprove”, “validate”, “we are unsure”, “might/possibly”.
Search in: code comments, markdown/docs, notebooks, experiment notes, embedded logs, and any issue/PR exports present in the repo.

---

### Entry template (repeat for each item found)

*(Populate strictly from repository text; keep names/phrasing used in source.)*

```markdown
#### OQ-### - <Short question/hypothesis as written>  <a id="oq-###"></a>
**Status:** <Open | In progress | Resolved>  •  **Priority:** <P1/P2/P3 if present>  •  **Owner:** <name/handle if present>  
**Context:** <path/to/file>:<line-range> • <short-commit>

> <verbatim one- or two-line quote from source, if available>

**Why it matters (lifted):** <one line copied/condensed from source>  
**Related canon (anchors only):**  
- Equations: `../derivation/EQUATIONS.md#vdm-e-...`  
- Symbols: `../derivation/SYMBOLS.md#sym-...`  
- Constants: `../derivation/CONSTANTS.md#const-...`  
- Units: `../derivation/UNITS_NORMALIZATION.md#...`  
- Algorithms: `../derivation/ALGORITHMS.md#vdm-a-...`  
- BC/IC/Geometry: `../derivation/BC_IC_GEOMETRY.md#...`  
- Metrics: `../derivation/VALIDATION_METRICS.md#kpi-...`

**Evidence so far:** <bullet list of cited files/figures/tests; link to `DATA_PRODUCTS.md#data-...` if applicable>  
**Proposed experiment/proof (if present in repo):** <lifted bullet(s) with links; no new steps>  
**Blockers/Dependencies:** <tools, datasets, theory pieces-lifted>  
**Next action (if stated):** <literal next step from source or TODO line>
```

---

### Sections to populate (only if evidenced; otherwise keep a flat list)

1. **Dynamics & RD/EFT Questions**
2. **Walkers / Control Plane / Plasticity**
3. **Units & Normalization / Scaling**
4. **Validation & Metrics / Safety Guards**
5. **LBM/Fluids / Geometry-Specific**
6. **Engineering & Infra (when it impacts the theory)**

*(If the repo doesn’t categorize, just list entries ordered by path.)*

---

### Index & ordering

* Add an alphabetical **Index** of questions at the top via anchors, or maintain a tool block (below).
* Order entries by repository path (lexicographic) of the first cited source; within a file, preserve source order.

---

### De-duplication & conflicts

* If the **same question** appears in multiple places, keep one entry and list all sources under **Context**.
* If **conflicting statements** exist, note both under **Evidence so far** with sources and add `Notes: CONFLICT - needs resolution`.

---

### End-of-file blocks (append verbatim)

```markdown
<!-- BEGIN AUTOSECTION: OPEN-QUESTIONS-INDEX -->
<!-- Tool-maintained list of [OQ-###](#oq-###) anchors for quick lookup -->
<!-- END AUTOSECTION: OPEN-QUESTIONS-INDEX -->

## Change Log
- <date> • questions updated • <commit>
```

---

### Validation

* Render on GitHub; confirm anchors resolve and any quoted MathJax renders.
* Do **not** paste equations or numeric values-**link** to the canonical files.
* Every entry must cite **Context** with `path:lines • commit`. If a needed anchor is missing in canon, add `TODO: add anchor (see <path>:<line>)`; do not create new canon here.
