**Create/Update `derivation/SYMBOLS.md` (MathJax-only)**

Search the entire repository (code, tests, notebooks, docs, comments, configs) and extract **every symbol actually used in the repo’s math**. **Do not invent new symbols or meanings.** Use only what exists.

**Output file:** `derivation/SYMBOLS.md`

**MathJax rules (GitHub-compatible):**

* Inline math: `$ ... $`
* Display math (rare here): `$$ ... $$`
* Allowed multi-line alignment: `$$\begin{aligned} ... \end{aligned}$$`
* **Do not use:** `\[` `\]`, `\(` `\)`, `\begin{equation}`, `\begin{align}`, `\tag`, `\label`, numbering, or package-specific macros.

**Scope (what to include as a “symbol”):**

* Scalars, vectors, matrices/tensors, fields, functions, operators, sets/spaces, indices, dimensionless numbers, gates/masks, buses, budgets, policies—**if they appear in equations or procedural math**.
* Include notational variants that occur in the codebase (e.g., `$ \mathbf{x} $`, `$ x_w $`, `$ \mathcal{B}_\ell $`).
* **Do not** include numeric defaults or values here (those live in `CONSTANTS.md`). Cross-link instead.

**Normalization (formatting only, not meaning):**

* Keep existing names; don’t rename variables. Normalize styling only: vectors `\mathbf{}`, multi-channel stacks `\boldsymbol{}`, sets `\mathcal{}`, number sets `\mathbb{}`, operators `\operatorname{}`/`\mathrm{}`.
* Use `\lVert\cdot\rVert`, `\lvert\cdot\rvert`. Escape underscores in prose with `\_` when needed.
* Expand acronyms in prose once per entry when they are part of names: *Self Improvement Engine (SIE)*, *Adaptive Domain Cartographer (ADC)*.

**File top matter (insert verbatim at top):**

```markdown
<!-- DOC-GUARD: CANONICAL -->
# VDM Symbols (Auto-compiled)

**Last updated**: yyyy-mm-dd 
**Last commit**: {latest commit hash here}
**Scope:** Single source of truth for meanings and roles of all mathematical symbols present in this repository.  
**Rules:** Other docs must link here; do not duplicate definitions elsewhere.  
**MathJax:** GitHub-safe `$...$` / `$$...$$` only.  
```

**Row template (use exactly this table header; append rows):**

```markdown
| Symbol | Meaning | Type | Domain/Codomain | Units | Appears In | Source (path:lines • commit) | Notes |
|---|---|---|---|---|---|---|---|
```

**Field guidance:**

* **Symbol:** MathJax form (e.g., `$ \phi_c $`, `$ \mathbf{x} $`, `$ \mathcal{B}_\ell $`). Prepend an HTML anchor for deep links, e.g. `<a id="sym-phi_c"></a>`.
* **Meaning:** One concise phrase lifted from nearby comments/docs (no new theory).
* **Type:** `scalar | vector | matrix | tensor | field | function | operator | set | index | dimensionless | mask/gate | policy | bus | budget | other`.
* **Domain/Codomain:** MathJax like `$ \mathbb{R}^d \to \mathbb{R}^C $` or `$ \{0,1\} $` if discrete; leave blank if not stated.
* **Units:** “nondimensional”, “LBM units”, or link to `UNITS_NORMALIZATION.md` anchor; leave blank if unspecified.
* **Appears In:** comma-separated links to equation IDs from `EQUATIONS.md` (e.g., `[VDM-E-012](../derivation/EQUATIONS.md#vdm-e-012)`).
* **Source:** `path:line-start-line-end • <short-commit>` where the symbol & meaning are evidenced.
* **Notes:** aliases (e.g., “also written `$ \varphi $` in `<path>`”), or pointers like “default in `CONSTANTS.md#const-alpha_plast`”.

**Aliases & collisions:**

* If multiple notations refer to the **same concept**, keep **one primary row** and list alternates in **Notes** (`Aliases: $ \varphi \equiv \phi $ in <paths>`).
* If a symbol is used with **different meanings** in different modules, create **scoped rows** labeled in **Notes** (e.g., “module: memory” vs “module: fluids”) and list distinct sources.

**Ordering:**

* Sort rows by the **normalized LaTeX token** of `Symbol` (case-sensitive). Keep ordering stable across runs.
* Grouping/headings are not required; a single table is fine. If the list grows large, insert alphabetical subheaders (`A-C`, `D-F`, …) without changing the table schema.

**Coverage & cross-check:**

* Ensure **every symbol referenced by any entry in `EQUATIONS.md`** has a row here; otherwise append a row with **Meaning** pulled from its nearest source, or add a minimal placeholder with `Notes: TODO clarify meaning (see <path>:<line>)`.
* Do not add numerical values here; link to `CONSTANTS.md` for defaults/ranges.

**End-of-file tool block (append verbatim):**

```markdown
<!-- BEGIN AUTOSECTION: SYMBOLS-INDEX -->
<!-- Tool-maintained list of [Symbol](#sym-...) anchors for quick lookup -->
<!-- END AUTOSECTION: SYMBOLS-INDEX -->
```

**Change Log (append section at end):**

```markdown
## Change Log
- <date> • added/updated symbols • <commit>
```

**Validation:**

* Render on GitHub to confirm all `$...$` inline math displays correctly.
* No content beyond what exists in the repository; all meanings and aliases must be sourced.
