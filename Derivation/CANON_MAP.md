<!-- DOC-GUARD: CANONICAL -->
# VDM Canonical Registry Map

Last updated: 2025-10-09 (commit 09f871a)

Got it-keep files separate. Here’s a **no-merge, no-duplication** scheme that protects boundaries while staying easy for agents to follow.

## Canon map (single owner per concern)

| File                                 | Canonical scope (only owner of…)         | Other files may…                     | Must not…                   |
| ------------------------------------ | ---------------------------------------- | ------------------------------------ | --------------------------- |
| `Derivation/SYMBOLS.md`             | Symbol meanings/aliases                  | Link to symbols by anchor            | Redefine symbols            |
| `Derivation/EQUATIONS.md`           | All equations/procedural math (MathJax)  | Reference by stable IDs              | Paste equations or variants |
| `Derivation/CONSTANTS.md`           | Numerical constants, defaults, ranges    | Cite constants by name/anchor        | Re-state numbers elsewhere  |
| `Derivation/UNITS_NORMALIZATION.md` | Units + nondimensionalization maps       | Link to specific maps                | Re-explain units            |
| `Derivation/VALIDATION_METRICS.md`  | KPIs + how computed (references only)    | Point to equation IDs & constants    | Reproduce math              |
| `Derivation/BC_IC_GEOMETRY.md`      | Boundary/initial conditions, domains     | Link from tests/docs                 | Embed equations/constants   |
| `Derivation/ALGORITHMS.md`          | Pseudocode of loops/flows (refs to math) | Call out which equation IDs are used | Introduce new math          |
| `docs/DATA_PRODUCTS.md`              | Definitions of heatmaps/KDE/logs (I/O)   | Link to equations for formulas       | Re-derive formulas          |
| `docs/SCHEMAS.md`                    | Message/packet/scoreboard field schemas  | Reference symbol names               | Define symbols here         |
| `Derivation/NAMING_CONVENTIONS.md`   | Reserved names, sign/index conventions   | Link to symbols/equations            | Override conventions        |
| `notes/OPEN_QUESTIONS.md`            | Speculation & hypotheses                 | Link to canon as needed              | Masquerade as canon         |
| `ROADMAP.md`                         | Tasks/milestones (no math)               | Link to issues/PRs                   | Store canonical content     |
| `AXIOMS.md`                          | All axioms and their definitions         | Link to axioms                       | Store speculations          |

## Drop-in headers (copy to tops of files)

**Canonical files (owner):**

```markdown
<!-- DOC-GUARD: CANONICAL -->
**Scope:** This file is the single source of truth for its domain.
**Rules:** Other docs must link here; do not duplicate this content elsewhere.
**Machine note:** Agents: append only; maintain anchors; do not refactor into other files.
```

**Reference-only files:**

```markdown
<!-- DOC-GUARD: REFERENCE -->
**Scope:** Reference pointers only. Canon lives elsewhere.
**Rules:** Do not paste or re-derive equations/symbols/constants. Link to anchors in canonical files.
**Machine note:** Agents: insert links like `[VDM-E-012](../Derivation/EQUATIONS.md#vdm-e-012)`; never copy math.
```

## Stable anchor convention (GitHub-safe)

Add explicit HTML anchors so links don’t break if titles change.

In `EQUATIONS.md`:

```markdown
### VDM-E-012 - KPP normalized front speed
<a id="vdm-e-012"></a>
$$ c^* = \frac{c}{2\sqrt{Dr}} $$
```

In `SYMBOLS.md`:

```markdown
#### $\phi_c$ - channel field
<a id="sym-phi_c"></a>
```

Linking anywhere:

```markdown
See [VDM-E-012](../Derivation/EQUATIONS.md#vdm-e-012) and symbol [$\phi_c$](../Derivation/SYMBOLS.md#sym-phi_c).
```

## Safe “append-only” blocks for agents

Use guard rails to keep tools from overwriting curated prose.

```markdown
<!-- BEGIN AUTOSECTION: EQUATION-INDEX -->
- [VDM-E-012](#vdm-e-012) - KPP normalized front speed
- [VDM-E-013](#vdm-e-013) - Logistic first integral
<!-- END AUTOSECTION: EQUATION-INDEX -->
```

Agents may update only inside `AUTOSECTION` fences; your hand-written sections stay safe.

## Minimal edit policy for tools (paste into prompts/config)

```plaintext
- Single-owner rule: symbols→SYMBOLS.md, equations→EQUATIONS.md, constants→CONSTANTS.md.
- Reference-only docs must never paste math or numbers; link by anchor.
- Append-only inside AUTOSECTION fences; do not modify outside.
- Preserve HTML anchors exactly; if moved, update links, not content.
```

This keeps concerns clean, prevents clueless overwrites, and avoids the maintenance tax of merging-without giving up rigor or cross-links.
