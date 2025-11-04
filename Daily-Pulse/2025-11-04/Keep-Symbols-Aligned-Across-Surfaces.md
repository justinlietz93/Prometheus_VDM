Here’s a quick, practical guide to make your symbols consistent across your **deskmat**, **EQUATIONS.md**, and **GUI labels** so reasoning feels “snappy” and unambiguous.

---

# Visual‑semantic coherence audit (fast pass)

**Goal:** one symbol ↔ one meaning ↔ one unit ↔ one GUI label.

## 1) Canonical source of truth

* Pick one file as canonical: `Derivation/EQUATIONS.md` (or `SYMBOLS.md` if you keep both).
* Every other surface (deskmat art, GUI, code tooltips) must mirror this exactly.

## 2) Minimal symbol registry (single table)

Create/extend `Derivation/SYMBOLS.md` with a single table (copy/paste):

| ID   | Symbol     | Name (short) | Meaning (1‑liner)                   | Units                  | Domain | Allowed Aliases | GUI Label         | Notes                    |
| ---- | ---------- | ------------ | ----------------------------------- | ---------------------- | ------ | --------------- | ----------------- | ------------------------ |
| S001 | ( \phi )   | order field  | primary state variable              | dimensionless (or set) | RD     | none            | “Field φ”         | links to eqn IDs         |
| S002 | ( J )      | Poisson op.  | antisymmetric (Hamiltonian) bracket | —                      | MP     | none            | “J (Hamiltonian)” | …                        |
| S003 | ( M )      | metric op.   | symmetric, PSD (dissipative)        | —                      | MP     | none            | “M (Dissipative)” | …                        |
| S004 | ( \Sigma ) | entropy      | Lyapunov/entropy functional         | J/K (or set)           | MP     | “S” (if legacy) | “Entropy Σ”       | alias must be deprecated |
| S005 | ( F )      | free energy  | free‑energy functional              | J                      | MP     | none            | “Free energy F”   | clarify sign conventions |
| S006 | ( D )      | diffusivity  | scalar/tensor diffusion             | m²/s                   | RD     | none            | “Diffusivity D”   | …                        |
| S007 | ( r )      | growth rate  | linear growth in FKPP               | s⁻¹                    | RD     | none            | “Growth r”        | …                        |
| …    | …          | …            | …                                   | …                      | …      | …               | …                 | …                        |

**Rules:**

* One row per symbol. No duplicates.
* If you keep an alias (legacy papers), mark it in **Allowed Aliases** and **ban** it in new text/UI.

## 3) EQUATIONS.md ↔ registry cross‑links

In `EQUATIONS.md`, add equation IDs and cross‑link to symbol rows:

* **Eq. E101 (FKPP):** (\partial_t \phi = D,\Delta \phi + r,\phi(1-\phi))
  *Uses:* S001, S006, S007.

* **Eq. E201 (Metriplectic split):** (\dot{z} = J(z)\nabla H(z) + M(z)\nabla \Sigma(z))
  *Uses:* S002, S003, S004.

This makes diffs obvious when something drifts.

## 4) GUI alignment (labels & tooltips)

Mirror the registry verbatim in the GUI:

* Slider label: **“Diffusivity D”**, tooltip: `Symbol: D — diffusivity (m²/s). See S006.`
* No Unicode drift: use the exact glyphs (e.g., **Σ** not plain **S**).

## 5) Deskmat check (the physical artifact)

* Print out the registry and lay it next to the deskmat.
* For each printed symbol on the mat: confirm **glyph**, **name**, **units**, **direction of arrows**, **signs** match the registry.
* If the mat abbreviates, add a tiny QR to `SYMBOLS.md` (can be a sticker) to keep parity without clutter.

## 6) Code comments & config keys

* In code, adopt comments like: `# Symbol S006 (D): diffusivity, m^2/s — see Derivation/SYMBOLS.md`.
* For config/JSON specs, prefer keys that map to GUI labels, e.g., `"diffusivity_D"` not `"diff"`.

## 7) Sign‑convention gate (save headaches)

Add a tiny boxed note in both `EQUATIONS.md` and `SYMBOLS.md`:

* **Sign policy:** (M \succeq 0). **Dissipative limb increases (\Sigma)** (or decreases (F)).
* State explicitly which Lyapunov you monitor and keep this invariant across docs, UI, and code.

## 8) Quick audit checklist (copy to `Derivation/CHECKS/SYMBOLS_CHECKLIST.md`)

* [ ] Each symbol on deskmat exists in `SYMBOLS.md` (same glyph).
* [ ] Each symbol in GUI exists in `SYMBOLS.md` (same label/tooltip).
* [ ] Every equation lists the symbol IDs it uses.
* [ ] No alias appears in new materials.
* [ ] Units present for all dimensional symbols.
* [ ] Sign‑convention box present in both files.
* [ ] Last pass date recorded and signed.

## 9) Tiny helper snippet (optional)

If you keep specs in JSON, add a lint step that diff‑checks GUI labels against the registry. For example, keep a canonical `symbols_registry.json` (generated from the table) and run a pre‑commit that fails on mismatches. (I won’t include code here unless you want it.)

---

If you want, I can draft `SYMBOLS.md` and a matching `SYMBOLS_CHECKLIST.md` from your current variables—just say the word, and I’ll produce the files in your exact folder layout.

