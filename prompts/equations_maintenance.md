**Create/Update `derivation/EQUATIONS.md` (MathJax-only)**

Search the entire repository (code, tests, notebooks, docs, comments) and extract **all formulas, equations, and procedural math that are currently used as defining parts of the VDM theory**. **Only use content that already exists in the repo.** Do not infer, extrapolate, or add new material.

**Output file:** `derivation/EQUATIONS.md`

**MathJax rules (GitHub-compatible):**

* Inline math: `$ ... $`
* Display math: `$$ ... $$`
* Allowed multi-line alignment: `$$\begin{aligned} ... \end{aligned}$$`
* **Do not use:** `\[` `\]`, `\(` `\)`, `\begin{equation}`, `\begin{align}`, `\tag`, `\label`, numbering, or package-specific macros.

**Normalization (formatting only, not content):**

* Preserve original symbols and notation; don’t rename variables.
* Ensure consistent LaTeX casing: `\boldsymbol{}`, `\mathbf{}`, `\mathrm{}`, `\operatorname{}` as in source (normalize only if inconsistent).
* Use `\lVert \cdot \rVert`, `\lvert \cdot \rvert`; insert thin spaces `\,` only where needed for readability.
* Fix obvious Markdown escaping issues (e.g., `_` in text → `\_`).

**Entry template (repeat for every equation found):**

```markdown
#### VDM-E-### — <short name taken from nearby comment or file>
**Context:** <path/to/file>:<line-range> • Commit: <short-hash> • Last Updated: <datetime>

$$
% paste the exact equation from the source, minimally normalized for MathJax if needed
$$

**Notes:** one line on where/how it’s used (lifted from code/comments).
```

**Compilation rules:**

* One entry per **distinct** equation. If the same equation appears in multiple places, keep one entry and list additional locations under **Notes**.
* Order entries by repository path (lexicographic). Do not add your own categories.
* Do not add symbol definitions here. If an equation references a symbol not present in `derivation/SYMBOLS.md`, add a line in **Notes**: `TODO: add <symbol> to SYMBOLS.md (see <path>:<line>)`.
* Maintain exact project naming where it appears (e.g., “Self Improvement Engine (SIE)”, “Adaptive Domain Cartographer (ADC)”).

**File top matter (insert verbatim at top):**

```markdown
# VDM Canonical Equations & Procedural Math (Auto-compiled)
*Defining equations and procedural math currently present in this repository.*

- Source of truth: extracted from repository files; do not edit equations here without updating their sources.
- MathJax only: use `$...$` and `$$...$$`; no numbering/tags/environments not supported by GitHub.
- Labels: entries are headed by `VDM-E-###` (header anchors); no equation tags inside MathJax.
```

**Change log (append at end):**

```
## Change Log
- VDM-E-### • <commit> • <path> added/updated
```

**Validation:**

* Ensure all math blocks render on GitHub.
* No content beyond what exists in the repository.
