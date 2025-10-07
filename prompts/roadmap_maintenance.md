
**Create/Update `derivation/ROADMAP.md` (planning-only; references to canon, no new content)**

Search the entire repository (docs, code comments, TODO blocks, notebooks, experiment logs, exported Issues/PRs if present, CONFIG/README notes) and compile **the roadmap items already captured**: milestones, tasks, dependencies, risks, and acceptance criteria. **Do not invent new work.** Use only what exists in the repo.

**Output file:** `derivation/ROADMAP.md`

**Canon rule:** This file is **planning-only**. Do **not** restate symbols, equations, constants, units, or algorithms. Link to them by anchor.

**MathJax on GitHub:**

* Inline math only when quoting names/symbols: `$ ... $`
* No display math or LaTeX environments here.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: REFERENCE -->
# VDM Roadmap (Compiled from Repository Evidence)

**Scope:** Milestones and tasks already recorded in this repository (docs, comments, logs, exported issues).  
**Rules:** Planning-only. Link to canonical math/specs (SYMBOLS/EQUATIONS/CONSTANTS/UNITS/ALGORITHMS/BC_IC/VALIDATION/DATA_PRODUCTS/SCHEMAS). Do not duplicate canon here.
```

---

### Milestone entry template (repeat for each milestone found)

*(Populate strictly from repository text; keep names exactly as written in source.)*

```markdown
## <Milestone Title as in repo>  <a id="ms-<slug>"></a>
**Status:** <Planned | In progress | Blocked | Done> • **Priority:** <P1/P2/P3 if present>  
**Source:** <path/to/file>:<line-range> • <short-commit>  (list all if multiple)

**Goal (verbatim/condensed from source):** <one-three lines>

**Acceptance criteria (links only, no formulas):**
- Metrics/KPIs: `VALIDATION_METRICS.md#kpi-...`
- Equations referenced: `EQUATIONS.md#vdm-e-...`
- Data products to produce: `DATA_PRODUCTS.md#data-...`
- Units/normalization context: `UNITS_NORMALIZATION.md#...`

**Dependencies:** link to other milestones/tasks (`#ms-...`, `#task-...`) and external artifacts if cited  
**Risks/Constraints:** brief bullets lifted from source  
**Deliverables:** filenames or artifacts explicitly mentioned (figures, tables, checkpoints)  
**Target timeframe (if stated):** literal dates or “next sprint/phase” as written
```

---

### Task entry template (repeat for tasks under a milestone)

```markdown
### <Task Title as in repo>  <a id="task-<slug>"></a>
**Source:** <path:lines> • <short-commit>  
**Description:** <one-two lines lifted>  
**Linked canon:** symbols → `SYMBOLS.md#sym-...`, equations → `EQUATIONS.md#vdm-e-...`, constants → `CONSTANTS.md#const-...`, algorithms → `ALGORITHMS.md#vdm-a-...`  
**Exit criteria:** reference KPIs/figures/artifacts by anchor/path (no formulas)  
**Owner (if present):** <name/handle> • **Status:** <…>
```

---

### Sections to populate (only if evidenced; omit otherwise)

1. **Near-Term Milestones** (next sprint/phase)
2. **Mid-Term Milestones**
3. **Long-Term / Research Threads**
4. **Engineering/Infra Tasks that impact theory**
5. **Blocked/On-Hold** (with cited blockers)

*(If the repo doesn’t group them, keep a single list ordered by path.)*

---

### Linking rules (anchors only; no duplication)

* Symbols → `../derivation/SYMBOLS.md#sym-...`
* Equations → `../derivation/EQUATIONS.md#vdm-e-...`
* Constants → `../derivation/CONSTANTS.md#const-...`
* Units → `../derivation/UNITS_NORMALIZATION.md#...`
* Algorithms → `../derivation/ALGORITHMS.md#vdm-a-...`
* BC/IC/Geometry → `../derivation/BC_IC_GEOMETRY.md#...`
* Validation metrics → `../derivation/VALIDATION_METRICS.md#kpi-...`
* Data products → `../derivation/DATA_PRODUCTS.md#data-...`
* Schemas → `../derivation/SCHEMAS.md#schema-...`

If a needed anchor is missing, write: `TODO: add anchor (see <path>:<line>)`. Do not paste canon here.

---

### De-duplication & ordering

* **One milestone entry per distinct title.** If the same milestone appears in multiple places, keep one entry and list all sources under **Source**.
* If two names refer to the same milestone, keep the most common name and list the alias in **Notes** with sources.
* Order milestones by **priority** if stated; otherwise by repository path (lexicographic) of the first cited source.

---

### Indices & blocks (append verbatim)

```markdown
<!-- BEGIN AUTOSECTION: ROADMAP-INDEX -->
<!-- Tool-maintained list of [Milestone](#ms-...) and [Task](#task-...) anchors -->
<!-- END AUTOSECTION: ROADMAP-INDEX -->

## Change Log
- <date> • roadmap updated • <commit>
```

---

### Validation

* Render on GitHub; ensure anchors resolve.
* Planning text must be sourced from the repo (docs/comments/issues in-repo). No new tasks or dates.
* All acceptance criteria should **link to** canonical metrics/equations/data—no formulas or numbers pasted here.
