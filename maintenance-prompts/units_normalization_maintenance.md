**Create/Update `Derivation/UNITS_NORMALIZATION.md` (MathJax-only)**

Search the entire repository (code, tests, notebooks, docs, configs, comments) and compile **the unit systems and nondimensionalization maps actually used**. **Do not invent or infer new scales.** Use only content that exists in the repo.

**Output file:** `Derivation/UNITS_NORMALIZATION.md`
**Canon rule:** This file is the single owner of units & normalization maps. Other docs must link here; do not restate units elsewhere.

**MathJax rules (GitHub-compatible):**

* Inline math: `$ ... $`
* Display math: `$$ ... $$`
* Allowed multi-line alignment: `$$\begin{aligned} ... \end{aligned}$$`
* **Do not use:** `\[` `\]`, `\(` `\)`, `\begin{equation}`, `\begin{align}`, `\tag`, `\label`, numbering, or package-specific macros.

---

### File header (insert verbatim at top)

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Units & Nondimensionalization (Auto-compiled)

**Last updated**: yyyy-mm-dd 
**Last commit**: {latest commit hash here}
**Scope:** Single source of truth for unit systems and nondimensionalization maps used in this repository.  
**Rules:** Other docs link here; do not restate units elsewhere.  
**MathJax:** GitHub-safe `$...$` / `$$...$$` only.  
```

---

### Required sections (populate only with content found in repo)

#### 1) Base Unit Systems

* Enumerate each system explicitly referenced (e.g., “SI”, “LBM units”, “nondimensional”).
* For each, provide a one-line description sourced from nearest comments/docs and **link to sources**.

Template row (repeat):

```markdown
- **System:** <name> • **Scope:** <module/subsystem> • **Source:** `<path>:<lines> • <commit>`
  - **Notes:** lifted from comments or docs (no new text).
```

#### 2) Reference Scales (only those present)

* Collect named reference scales (e.g., `$L$`, `$T$`, `$U$`, `$ \Phi_0 $`, `$D_0$`, `$r_0$`, `$c_s$`) that the repo actually uses.

Table schema:

```markdown
| Symbol | Meaning | Units/System | Source (path:lines • commit) | Notes |
|---|---|---|---|---|
```

#### 3) Nondimensionalization Maps (forward & inverse)

* For each map that exists in code/docs, record the **exact mapping** as MathJax plus sources.
* Include both direction(s) if they appear (dimensional → nondim and/or inverse).

Entry template (repeat per map):

```markdown
##### <Map Name or Module>
**Context:** <path:lines> • <commit>

$$
% paste the exact map as used in repo (add only minimal spacing)
% example:
% x'=\frac{x}{L},\quad t'=\frac{t}{T},\quad \phi'=\frac{\phi}{\Phi_0}
$$

**Inverse (if present):**
$$
% example: x=L\,x',\quad t=T\,t',\quad \phi=\Phi_0\,\phi'
$$

**Related:** link to equations/constants by anchor (no restating math).
```

#### 4) Per-Quantity Units (as used)

* For fields, operators, and diagnostics that have declared units in the repo, list them here.
* Do **not** restate definitions; link to symbols/equations.

Table schema:

```markdown
| Quantity (link to symbol) | Units/System | Where Stated | Notes |
|---|---|---|---|
```

#### 5) Dimensionless Numbers (unit statements only)

* If a file states that a number is dimensionless or gives its normalization context, record that statement **without re-deriving the formula**.
* Link to the defining equation in `EQUATIONS.md`.

Table schema:

```markdown
| Name | Unit Status / Normalization Note | Appears In | Source |
|---|---|---|---|
```

---

### Normalization & linking rules (formatting only)

* Preserve original symbols; do not rename. Normalize style only (`\mathbf{}`, `\boldsymbol{}`, `\mathcal{}`, `\mathrm{}`).
* Use anchors when linking:

  * Symbols: `../Derivation/SYMBOLS.md#sym-...`
  * Equations: `../Derivation/EQUATIONS.md#vdm-e-...`
  * Constants: `../Derivation/CONSTANTS.md#const-...`
* If a map references an undefined symbol/constant, add a **Notes** line: `TODO: link missing <symbol|constant> (see <path>:<line>)`. Do not invent content.

### Ordering

* Within each section, order entries by repository path (lexicographic) of the first source you cite.

### End-of-file blocks (append verbatim)

```markdown
<!-- BEGIN AUTOSECTION: UNITS-INDEX -->
<!-- Tool-maintained list of anchors for quick lookup -->
<!-- END AUTOSECTION: UNITS-INDEX -->

## Change Log
- <date> • updated units/maps • <commit>
```

### Validation

* Confirm all `$...$`/`$$...$$` render on GitHub.
* No re-explanations or re-derivations; only mappings and unit statements that already exist in the repository.
