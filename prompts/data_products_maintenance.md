**Create/Update `derivations/DATA_PRODUCTS.md` (canonical specs for outputs; references-only for math)**

Search the entire repository (code, tests, notebooks, experiment scripts, pipelines, configs, docs, comments) and compile **all data products actually produced or consumed** (arrays, timeseries, images, videos, logs, tables, checkpoints, serialized graphs, bus snapshots, etc.). **Do not invent new products.** Use only what exists in the repo.

**Output file:** `derivations/DATA_PRODUCTS.md`
**Canon rule:** This file is the single owner of **data product specifications** (purpose, shape, units, file format, provenance). **Do not paste or re-derive equations here.** Link to equations/constants/symbols/algorithms by anchor.

**MathJax on GitHub:**

* Inline math for symbols: `$ ... $`
* Optional display math **only when quoting a definition verbatim from the repo**: `$$ ... $$`
* **Do not use:** `\[` `\]`, `\(` `\)`, LaTeX environments (`\begin{...}`), `\tag`, labels/numbering, or package-specific macros.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Data Products (Auto-compiled)

**Scope:** Single source of truth for data products used/produced by this repository: purpose, shape, units, storage format, file paths, and provenance.  
**Rules:** Reference-only for math; link to anchors in EQUATIONS/CONSTANTS/SYMBOLS/UNITS/ALGORITHMS.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only when quoting existing math.
```

---

### Data product entry template (repeat for each product found)

*(Populate strictly from repository content; keep names exactly as used in code/comments.)*

```markdown
#### <Product Name as used in repo>  <a id="data-<slug>"></a>
**Type:** <array | timeseries | image | video | table | log | graph | checkpoint | other>  
**Purpose:** <one-line description lifted from repo>  
**Produced by:** link algorithms (anchors) → `../derivations/ALGORITHMS.md#vdm-a-###`  
**Defined by (if math):** link equations (anchors only) → `../derivations/EQUATIONS.md#vdm-e-###`  
**Inputs (symbols/constants):** link anchors → `SYMBOLS.md#sym-...`, `CONSTANTS.md#const-...`  
**Units/Normalization:** link into `UNITS_NORMALIZATION.md#...` (no re-explanations)

**Shape & axes (exact as used):**
- Shape: `<literal, e.g., (C, H, W)>` or `<T × X × Y>`, as stated in code/docs
- Axes/ordering: `<list>` (e.g., channel-first, time-major) with source lines

**Storage format & path pattern:**
- Format: `<npz | parquet | feather | csv | json | png | mp4 | torch | safetensors | other>`
- Path pattern: `` <root>/<experiment>/<run_id>/<name>_<stamp>.<ext> `` (quote exactly from repo)
- Compression/encoding: `<codec/level>` if stated

**Schema / columns (for tables/logs):**
- Columns: `<name:type>` taken from code/schema files
- Index/primary keys: `<field>` if present

**Update cadence / lifecycle:** `<per tick | per epoch | on event | end-of-run>`  
**Provenance (code locations):** `<path:lines • short-commit>` (list all writers/consumers)  
**Validation hooks / KPIs:** link to `../derivations/VALIDATION_METRICS.md#kpi-...`  
**Retention / access constraints:** literal policy text if present (do not invent)  
**Example artifact (if referenced):** `<path/to/example>`  
**Notes:** aliases, deprecations, versioning flags (lifted from repo)
```

---

### Sections to populate (use only what exists; omit empty sections)

1. **Core Field & Activity Maps** (e.g., heatmaps `$H_k(\mathbf{x},t)$`, saliency `$ \rho $`, channel utilization `$ \Pi_c(t) $`)
2. **Walker / Bus / Scoreboard Artifacts** (messages, snapshots, budgets, masks)
3. **Diagnostics & Logs** (experiment logs, drift monitors, KPI traces)
4. **Checkpoints & State Snapshots** (model/substrate/graph states)
5. **Figures & Media** (plots, animations, videos)
6. **Tabular Results** (metrics tables, summaries)
7. **External Interfaces** (exports/imports to other tools, if present)

*(If the repo doesn’t group them this way, keep a single flat list ordered by path.)*

---

### Linking rules (anchors only; no duplication of math or values)

* **Equations:** `../derivations/EQUATIONS.md#vdm-e-...`
* **Symbols:** `../derivations/SYMBOLS.md#sym-...`
* **Constants:** `../derivations/CONSTANTS.md#const-...`
* **Units maps:** `../derivations/UNITS_NORMALIZATION.md#...`
* **Algorithms:** `../derivations/ALGORITHMS.md#vdm-a-...`

If any required anchor is missing, add: `TODO: add anchor (see <path>:<line>)`; do not paste formulas here.

---

### De-duplication & ordering

* **One entry per distinct data product name.** If multiple modules write the same product, keep one canonical entry and list all writer/consumer locations in **Provenance**.
* If two names refer to the same artifact, keep the most common name and list aliases in **Notes**.
* Order entries by repository path (lexicographic) of the first cited source.

---

### End-of-file blocks (append verbatim)

```markdown
<!-- BEGIN AUTOSECTION: DATA-INDEX -->
<!-- Tool-maintained list of [Data Product](#data-...) anchors for quick lookup -->
<!-- END AUTOSECTION: DATA-INDEX -->

## Change Log
- <date> • data products updated • <commit>
```

---

### Validation

* Render on GitHub; confirm anchors resolve and any quoted MathJax renders.
* No equations or numeric defaults duplicated here—**link** instead.
* All shapes, units, formats, and paths must match repository sources exactly.
