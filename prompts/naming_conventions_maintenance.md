**Create/Update `derivation/NAMING_CONVENTIONS.md` (canonical notation rules; references-only)**

Search the entire repository (code, tests, notebooks, configs, docs, comments) and compile **the notation and naming conventions actually used** in the project. **Do not invent new rules.** Use only conventions evidenced in the repo.
*(If your repo’s canon map uses `docs/NAMING_CONVENTIONS.md`, write to that path instead.)*

**Output file:** `derivation/NAMING_CONVENTIONS.md`
**Canon rule:** This file is the **single owner** of notation, symbol styling, index orders, coordinate systems, and reserved names. Other docs must link here; do not restate or override conventions elsewhere.

**MathJax on GitHub:**

* Inline math: `$ ... $` • Display only if quoting an existing snippet: `$$ ... $$`
* **Do not use:** `\[` `\]`, `\(` `\)`, LaTeX environments (`\begin{...}`), `\tag`, labels/numbering, or package-only macros.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Naming & Notation Conventions (Auto-compiled)

**Last updated**: yyyy-mm-dd 
**Last commit**: {latest commit hash here}
**Scope:** Single source of truth for mathematical and semantic naming conventions used in this repository.  
**Rules:** Extract from repository evidence only; link to canonical symbols/equations/units/constants. Do not redefine them here.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only when quoting existing snippets.
```

---

### Sections to populate (only with conventions found in the repo)

#### 1) Symbol Styling (typography choices)

Document how symbols are styled **in practice** (bold/blackboard calligraphic, etc.).

**Table schema:**

```markdown
| Category | Convention (MathJax) | Example from repo | Source (path:lines • commit) | Notes |
|---|---|---|---|---|
```

Examples of categories (fill only if present): vectors (`\mathbf{}`), multi-channel fields (`\boldsymbol{}`), sets/spaces (`\mathcal{}`, `\mathbb{}`), operators (`\operatorname{}`, `\mathrm{}`), gates/masks, buses, budgets, policies, indices.

Link examples to `SYMBOLS.md` anchors when possible.

---

#### 2) Reserved Names & Abbreviations

List reserved words/abbreviations and their canonical expansions (as used).

**Table schema:**

```markdown
| Name | Expansion / Meaning | Where used | Source | Notes |
|---|---|---|---|---|
```

Include items like “SIE — Self Improvement Engine”, “ADC — Adaptive Domain Cartographer”, GDSP, etc., **only if present**. Link to `SYMBOLS.md` entries.

---

#### 3) Indices & Ordering

Record **actual** index letters and ordering semantics (space, channel, time, neighbor, objective, etc.).

**Table schema:**

```markdown
| Role | Index letters | Ordering / Semantics | Source | Notes |
|---|---|---|---|---|
```

Examples of roles (use only if evidenced): spatial sites, time steps, channels, objectives `$k$`, neighbors `$\mathrm{nbr}(i)$`, dimensions `$d$`.

---

#### 4) Coordinate Systems & Orientation

Document named coordinate systems/frames and handedness/orientation if stated.

**Entry template:**

```markdown
##### <Frame/System Name>  <a id="frame-<slug>"></a>
**Definition (quoted if present):** <one-liner>  
**Axes / orientation:** <as stated>  
**Units/normalization:** link to `UNITS_NORMALIZATION.md#...`  
**Source:** <path:lines • commit>  
**Notes:** references to equations/symbols
```

---

#### 5) Subscripts, Superscripts, Diacritics (semantics)

Record meanings of subscripts/superscripts/diacritics **as used** (e.g., `$c$ for channel$,, n$ for time step, primes/dots/hats/tilde meanings).

**Table schema:**

```markdown
| Notation | Meaning (as used) | Example link | Source | Notes |
|---|---|---|---|---|
```

Use MathJax for the notation, and link examples to `EQUATIONS.md`/`SYMBOLS.md`.

---

#### 6) Sign Conventions & Inequalities

State sign conventions (e.g., curvature signs, Laplacian, d’Alembertian, “positive is …”), and inequality styles used for thresholds/budgets **only if specified**.

**Table schema:**

```markdown
| Convention | Statement (verbatim or minimal) | Appears in | Source |
|---|---|---|---|
```

---

#### 7) File/Anchor Naming Patterns (for cross-links)

Document anchor and ID patterns used across canon files so tools can link stably.

**Table schema:**

```markdown
| Artifact | Anchor/ID Pattern | Example | Source | Notes |
|---|---|---|---|---|
```

Artifacts include: equation IDs (`vdm-e-###`), algorithms (`vdm-a-###`), symbols (`sym-...`), constants (`const-...`), geometries/BC/IC (`geom-...`, `bc-...`, `ic-...`), data products (`data-...`), schemas (`schema-...`), metrics (`kpi-...`). Record only what exists.

---

### Linking rules (anchors only; no duplication)

* Symbols → `../derivation/SYMBOLS.md#sym-...`
* Equations → `../derivation/EQUATIONS.md#vdm-e-...`
* Units → `../derivation/UNITS_NORMALIZATION.md#...`
* Constants → `../derivation/CONSTANTS.md#const-...`
* Algorithms → `../derivation/ALGORITHMS.md#vdm-a-...`

If a required anchor is missing, add `TODO: missing anchor (see <path>:<line>)`; do not create content here.

### De-duplication & ordering

* If multiple files state the **same** convention, keep one row and list all sources.
* If two conflicting conventions exist, list both with sources and add `Notes: CONFLICT — resolve`.
* Order rows **lexicographically by Category/Role/Notation**, or by repository path if more natural from sources.

### End-of-file blocks (append verbatim)

```markdown
<!-- BEGIN AUTOSECTION: NAMING-INDEX -->
<!-- Tool-maintained list of anchors/slugs for quick lookup -->
<!-- END AUTOSECTION: NAMING-INDEX -->

## Change Log
- <date> • conventions updated • <commit>
```

### Validation

* Render on GitHub; confirm anchors resolve and any quoted MathJax renders.
* Ensure conventions reflect **only** what is evidenced in the repository—no new rules, no overrides of `SYMBOLS.md` or `EQUATIONS.md`.
