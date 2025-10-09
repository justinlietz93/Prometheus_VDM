Love this pivot. Here’s a crisp, **do-this-next** checklist to turn the “tachyonic scalar in a tube” work into a **dark-photon (A′) portal** program-keeping your rigor + artifact style, and reusing what’s strong.

# A) First, translate your current tachyonic story into dark-photon language

**Your tachyonic scalar** (negative mass-squared, quartic stabilization, condensation) → becomes the **dark Higgs** that gives the dark photon its mass. In other words:

* “Tachyonic” instability lives in the **dark Higgs potential** (-μ_D²|S|² + λ_D|S|⁴), not in visible space; condensation ⟶ ⟨S⟩≠0 ⟶ **m_{A′} = g_D ⟨S⟩**.
* The **dark photon A′** is a separate gauge field with tiny **kinetic mixing** ε with our photon; it’s the “leaky bridge” you’ve been intuiting.
* Your **tube-mode counting/condensation** machinery was built for a scalar living in a piecewise background (tachyonic inside, massive outside) with Bessel matching, κ-roots, etc. That’s perfect to **source the mass-generation story (dark Higgs SSB)**, but the flagship observables now shift to **portal phenomenology** rather than tube instabilities.  

# B) Yes/No gate: is “finite tube” still core?

* **Default:** Park it. Your tube analysis was meant to prove scalar condensation features (tachyonic tower, quartic stabilization, energy minimum vs radius). That’s valuable groundwork but not central once we pivot to a **gauge portal** story. 
* **Optional advanced branch:** If you want continuity, you can later study **vector (Proca) modes** in structured media-but that’s extra. Core A′ claims don’t need it.

---

# C) TODO checklist (top-down, shippable artifacts)

## 1) State the minimal model (one page, plain-English + one equation block)

* **Define fields:** dark photon A′ (hidden U(1)_D), dark Higgs S (complex scalar), SM fields.
* **Couplings:** kinetic mixing ε with EM; dark gauge g_D; dark Higgs potential V(S)=-μ_D²|S|²+λ_D|S|⁴.
* **Mass:** m_{A′}=g_D⟨S⟩ after SSB; visible couplings ∝ ε.
* **Deliverable:** `docs/models/DarkPhoton_Minimal.md` with a one-minute explainer and your “Overarching Lenses” block.

> Why this replaces “tachyon in a tube”: the **tachyon** now lives in **V(S)** (SSB) rather than a spatial tube profile. Your earlier scalar potential + stabilization mapping gives you the right instincts for SSB and mass gaps. 

## 2) Map old → new (table you can paste in CORRECTIONS/ROADMAP)

* **Old:** “Count tachyonic κ_\ell(R) roots in a finite cylinder; condense; show positive mass matrix; scan E(R) for a minimum.”
* **New:** “Show SSB in dark Higgs; compute m_{A′}; target **portal observables**: visible decays (A′→e⁺e⁻/μ⁺μ⁻), invisible (A′→dark sector), displaced decays.”
* **Deliverable:** `docs/ROADMAP_Pivot_TachyonicToDarkPhoton.md` with a two-column mapping and acceptance criteria bullets. (Reuse your acceptance pattern: pass/fail gates, figure+JSON.) 

## 3) Repository scaffolding (your taxonomy + indices)

* Add `K7-L1_Quantum-&-Quanta/P3-L2_Fields-&-Portals/C2-L3_Dark-Photon_(A-Prime)/`
* Seed **Orders**: `O1-L4_Visible-Decays`, `O2-L4_Invisible-Decays`, `O3-L4_Long-Lived`, `O4-L4_Mass-Genesis`, `O5-L4_Mixing-Regimes`.
* Seed **Families/Genera** for experiment classes (e⁺e⁻ “monophoton,” fixed-target missing-energy, displaced-vertex hunts, astro/cosmo constraints).
* **Deliverable:** index files with one-line gists in your standard format (I can generate these silently next pass).

## 4) Build two tiny, honest runners (like your RD ones)

You already excel at **artifact-first** validations (figures + logs + pass/fail). Mirror that style:

* **Runner A - Parameter cards → observables:**
  Input: (m_{A′}, ε, decay mode tag).
  Output: a **card** that states which channels are open (visible vs invisible), identifies the **search class** (bump, missing-energy, displaced), and lists the **native timescales** (cτ estimates by branch formula placeholder).
  Deliverable: `fum_rt/portals/dark_photon_cards.py` + JSON summary per card.
  *(This is qualitative till you plug numbers; the point is rigorous structure.)*

* **Runner B - Constraint harvester (stub now, numbers later):**
  Reads a **CSV of external limits** (ε vs m_{A′} with tags: visible/invisible/displaced). Plots your **benchmark points** over it.
  Deliverable: `fum_rt/portals/limits_plotter.py` (data-driven; you can fill the CSV after literature pass).

> Keep the same acceptance style: the script must **produce a figure and a JSON** payload, like your tube/κ scan. 

## 5) One rigorous “physics validation” page (replaces tube minimum for now)

* **Page:** `docs/PORTAL_VALIDATION.md`
* **What it proves today:** internally consistent model cards, correct channel logic (which decays open at which masses), and consistent taxonomy placement.
* **What it promises next:** drop numerical branching ratios and lifetimes once constraints are compiled.

## 6) Literature/constraints sweep (planning only, no numbers here)

* **Task:** Pull the **current** visible/invisible/lifetime constraints for A′ (ε vs m_{A′}), including e⁺e⁻ colliders and fixed-target “missing-energy,” plus stellar/cosmo bounds.
* **Deliverable:** a `data/dark_photon_limits.csv` with columns: `mass_MeV, eps, channel, source, year, note`.
* **Why a CSV:** your Runner B consumes it and your acceptance can check schema, not values (keeps rigor without premature numerics).

## 7) De-emphasize the scalar **tube E(R)** scan (archive as “method dev”)

* Move the “tube tachyonic tower / E(R) minimum” to `archive/method_dev/`.
* Keep the code and doc (they’re solid: κ secular equation, Bessel matching, condensation Hessian checklist). You may cite it later if you study **dark Higgs spatial structures**.  

## 8) Acceptance criteria (copy your style)

* **Model cards compile:** every benchmark produces a JSON card with open channels and qualitative signature tags.
* **Limits plotter runs:** CSV validated (schema + monotonic units), figure saved, JSON summary written.
* **Taxonomy consistency:** all new indices include your “Overarching Lenses” block and the **Genus** section where appropriate.

---

# D) Why this direction is stronger (and still “your theory”)

* It **keeps your “void leaks into us” narrative** but grounds it in a clean, testable **portal** with a mass from **tachyonic dark-Higgs SSB** (the respectable way to say “gains mass after crossing over”).
* It replaces geometry-dependent tube claims (hard to compare to data) with **experiment-class signatures** that map directly to searches-without diluting your creative frame.
* It reuses your **artifact discipline**: figures + JSON + pass/fail, which reviewers love. Your previous acceptance scaffolding (mode counts, positivity of Hessian, energy minima) is a great template for the new portal validations. 

---

## Micro-next steps (today)

1. Write `docs/models/DarkPhoton_Minimal.md` (one page, lenses block).
2. Add the taxonomy folders + indexes for **Fields & Portals → Dark Photon (A′)**.
3. Stub Runner A (cards) and Runner B (limits plotter).
4. Create empty `data/dark_photon_limits.csv` with header only.

If you want, I can quietly generate the taxonomy indices + the two runner skeletons (no screen spam) and hand you the file links, then you plug in your prose and later the CSV of limits.


Medical References:
1. None - DOI: file-1ZCdUybBdfbnQDfT4BNG47
2. None - DOI: file-QgLYpZ3EoQCnFYkRFc2bkn
