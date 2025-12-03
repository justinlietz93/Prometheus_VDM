## 1. What Future-Justin should open first (from my own work)

**Eisenhower Quadrant Score for this topic:** **Q2 = Important + Not Urgent → schedule it immediately.** (This is explicitly your “1c” item in `Current_TODO`.)

1. `Derivation/z.CANONICAL_Roadmap/Current_TODO.md`

   * **Why:** tells you *where this belongs* (1c), what it depends on (1b + SIE definition), and what deliverables you promised (T3 RESULTS + T4 PROPOSAL).

2. `Derivation/z.CANONICAL_Roadmap/Backlog/Q2-Important-Not-Urgent/2025-12-02/Mode-resolved-entropy-echoes-via-OTOC.md`

   * **Why:** this is the canonical “home note” for the project **and it’s currently empty** (0 bytes) → fill it first so you don’t re-forget.

3. `Derivation/z.CANONICAL_Roadmap/Backlog/Q1-Important-Urgent/2025-12-02/Deriving-Linblad-from-Lie-geometry.md`

   * **Why:** this is your **SU(2) Lindblad metriplectic exemplar (1b)**; 1c is built on top of it, not adjacent to it. 

4. `Derivation/z.CANONICAL_Roadmap/Backlog/Q1-Important-Urgent/2025-12-03/SciLean-Lean4-toolkit-for-PDEs-and-gradient-flows.md`

   * **Why:** this is where you pinned the **OTOC spectroscopy paper** as the next limb after the SU(2) exemplar. 

5. `Derivation/Entropy/Self-Information/T3_PROPOSAL_Agency_Entropy_Echo_Measurement_v1.md`

   * **Why:** gives your canonical **entropy-echo** object + normalization (what “echo” means in your stack). 

6. `Derivation/Metriplectic/CEG_Metric_Definition/T2_PROPOSAL_CEG_Metric_Definition_v1.md`

   * **Why:** your canonical normalization for “echo improvement” (useful if you add an assisted/unassisted comparison in 1c). 

7. `Derivation/Complete-Formalisms/CF01_QGT_to_Metriplectic_Brackets.md` (+ `Derivation/Complete-Formalisms/CF01_QGT_to_Metriplectic_Brackets.ipynb`)

   * **Why:** this is your *constitution* for the **J⊕M** split; 1c must reuse its symbols and degeneracy checks.

8. `AXIOMS.md` + `Derivation/z.CANONICAL_Equations/00_EQUATIONS.md` + `Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md`

   * **Why:** where A4/A5/A7 and the meter/KPI naming live (you cite these, not re-explain them).

9. Code you will copy patterns from:

   * `Derivation/code/physics/metriplectic/assisted_echo.py` (echo protocol pattern) 
   * `Derivation/code/physics/metriplectic/echo_metrics.py` (metric plumbing / serialization hooks) 
   * `Derivation/code/common/instrument_helpers/generic_helpers.py` (antisymmetry/PSD/degeneracy check helpers)

---

## 2. Canonical equations and objects to reuse (not reinvent)

Use these as “imports” and **do not re-derive** them in 1c:

1. **Metriplectic split**: `J ⊕ M` evolution

   * **Use for:** separating “reversible scrambling generator” vs “irreversible entropy production” in the SU(2) exemplar and in the echo protocol.
   * **Do not re-derive:** the split itself; cite A4/VDM-E anchors via canon. (The SU(2) exemplar doc explicitly frames this reuse.) 

2. **GKSL/Lindblad generator**

   * **Use for:** ground-truth open-system evolution on SU(2) (your 1b engine that 1c meters sit on).
   * **Do not re-derive:** GKSL properties; treat it as the reference form to match. 

3. **Bloch-ball state representation**: `ρ = ½(I + r·σ)`

   * **Use for:** *everything numerical* (fast stepping, echo comparison, operator evolution in Pauli basis).
   * **Do not re-derive:** conversion identities; just implement utilities once. 

4. **SIE / entropy-echo definition**

   * Canon object: `E_echo(δ,T) := D_KL( μ0 || μ_rew,δ,T )`, with optional normalization by an information flux `R_VW` into the dimensionless agency index `𝒜 = E_echo / (R_VW T)`.
   * **Use for:** the “echo axis” you compare the OTOC spectrum against.
   * **Do not re-derive:** use the exact symbol names and definition. 

5. **OTOC meter object (choose one and freeze it):**

   * Either `F(t)=Tr(ρ W(t) V W(t) V)` OR commutator-growth `C(t) = -Tr(ρ [W(t),V]^2)`; pick one and keep it fixed across the results/proposal.
   * **Use for:** the “scrambling axis” you Fourier analyze into a **mode-resolved scrambling spectrum** `S(ω)=|FFT(C(t))|`.

6. **CEG (optional but recommended if you add “assisted rewind”):**

   * Canon: `CEG = (E_baseline − E_assisted)/E_baseline`.
   * **Use for:** turning “echo got better” into a dimensionless headline number. 

### Papers you must treat as external anchors (and what they’re for)

* **Colombo et al. (2025)**, *“Euler–Poincaré dynamics on adjoint-coupled semidirect products and the geometric origin of Lindblad generators”* (arXiv:2511.21967).

  * **Use for:** the 1b claim that “Lindblad on Bloch ball comes from geometry (ACSP + metric/contortion/torsion)” which your SU(2) engine implements.  

* **Fujii et al. (2025)**, *“Out-of-Time-Order Correlator Spectroscopy”* (arXiv:2511.22654).

  * **Use for:** the motivation and framing of “mode-resolved OTOC / spectroscopy” as a meter, i.e. “extract spectral structure of scrambling from OTOCs.”

* **GKSL originals (ground truth form):**

  * **Use for:** canonical Lindblad/GKSL structure (only as background reference; your repo already treats GKSL form as standard). (You cite these only if you need to justify a property externally.)

---

## 3. Concrete extraction / implementation procedure

This is written as if you’re building code + artifacts *now*, in your existing meter style.

### A. Preconditions (do not skip)

1. **Confirm 1b exists and passes basic gates**

   * You need a working SU(2) open-system stepper (J-step, M-step, Strang/JMJ composition) *before* you bolt on OTOC.
   * Minimal gates you must already have: `Tr ρ≈1`, `ρ ⪰ 0`, and a stable JMJ step size regime. (This is the whole point of 1b.) 

2. **Create the “home spec” for 1c**

   * Fill `Mode-resolved-entropy-echoes-via-OTOC.md` (it’s empty) with: (i) definition choices for OTOC + E_echo, (ii) parameter ranges, (iii) file paths you’re about to create, (iv) expected plots.

### B. Implement the OTOC spectrum meter on SU(2)

3. **Pick a fixed operator choice and state choice** (freeze these in both RESULTS and PROPOSAL)

   * Use Pauli operators: `V = σ_z`, `W = σ_x` (or any fixed pair; just don’t change later).
   * Use **infinite-temperature state** `ρ∞ = I/2` for the OTOC trace unless you have a strong reason otherwise.

4. **Compute Heisenberg evolution for W(t) using your SU(2) Liouvillian adjoint**

   * Implement: `W(t) = exp(t 𝓛†) W(0)` in the Pauli basis.
   * Practical implementation (fast path): represent any traceless operator as a 3-vector of Pauli coefficients; evolve it linearly.

5. **Define the OTOC time series** (use commutator form; it’s numerically clean on SU(2))

   * `C(t) := -Tr(ρ∞ [W(t), V]^2)`
   * For Pauli operators at ρ∞, you can reduce to a pure vector expression (no heavy matrix ops): `[W,V]` is proportional to a cross product of Pauli coefficient vectors → `C(t)` becomes a simple norm of that cross product.
   * Output: `C(t_n)` for `t_n = n Δt, n=0..N`.

6. **Build the mode-resolved spectrum**

   * Choose a time window `T_spec` and sampling `Δt`.
   * Compute `S(ω_k) = |FFT(C(t) - mean(C))|` and store:

     * peak frequencies,
     * peak heights,
     * integrated high-frequency weight above a cutoff (your “scrambling hardness” scalar).

### C. Implement the entropy-echo metric on the same SU(2) engine

7. **Define the echo protocol on SU(2) (forward → kick → rewind)**
   Use an explicit, reproducible protocol:

   * Sample an ensemble `{ρ0^m}` (e.g., random Bloch vectors inside the ball, or a fixed spherical design).
   * Forward evolve for time `T_echo` with your JMJ stepper: `ρT^m`.
   * Apply a **kick** controlled by δ, e.g. `ρT,kick^m = U(δ) ρT^m U(δ)†` with `U(δ)=exp(-i δ V)` (reuse the same `V` as OTOC).
   * Rewind for time `T_echo` using **J reversed** (`H→-H`) while keeping **M forward** (because you can’t time-reverse dissipation). This mirrors your existing “assisted echo” philosophy.

8. **Compute the SIE echo metric in your canon form**

   * Build empirical distributions: `μ0` from `{ρ0^m}` and `μ_rew` from `{ρ_rew^m}` via coarse-graining (e.g., histogram on Bloch ball bins).
   * Compute `E_echo(δ,T) = D_KL( μ0 || μ_rew,δ,T )` exactly as canon. 
   * Optional (nice-to-have): also compute per-trajectory **quantum relative entropy** `S(ρ0^m || ρrew^m)` and average it; keep the histogram-KL as the *canonical* reported value.

### D. Compare “scrambling spectrum” vs “echo”

9. **Make the comparison objects you will report**
   For each parameter set θ (Lindblad type, rates, |ω|, δ):

   * `scramble_scalar(θ)` = (peak frequency, peak height, high-ω weight, early-time slope)
   * `E_echo(θ)` from step 8

10. **Metrics + plots (minimum viable non-embarrassing)**

* Plot 1: `C(t)` curves for 2–3 parameter slices (e.g. dephasing vs depolarizing).
* Plot 2: corresponding `S(ω)` spectra with peaks labeled.
* Plot 3: `E_echo(δ)` vs δ for those same slices.
* Plot 4: scatter `E_echo` vs high-ω weight (and report correlation coefficient + CI via bootstrap over the initial-state ensemble).

11. **Instrument QC gates you must log**

* State validity: `|Tr ρ - 1|`, min eigenvalue of ρ, and stability under `Δt → Δt/2`.
* OTOC sanity: `C(0)=0` (within tol), and “two implementations match” (Heisenberg-evolved operator vs brute-force 2×2 matrices) on a small sample.

12. **Artifact routing (match your existing style)**

* Write CSV/JSON/PNG under a single output root (pattern-copy from `assisted_echo.py` + `echo_metrics.py`).  
* Store: config JSON, time series CSV, spectrum CSV, KPI JSON, and figures.

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in my style

These filenames are **already implied by your Current_TODO item 1c**: deliver a T3 RESULTS doc + a T4 PROPOSAL doc.

### A) `Derivation/Quantum_Echos/T3_RESULTS_OTOC_SIE_Echo_SU2_v1.md`

**Required sections**

1. Scope banner (“T3 smoke test; no novelty claim; meter shaking”).
2. System definition (SU(2) Lindblad family, operator choices V/W, state choice ρ∞).
3. Meter definitions (exact `C(t)` choice + `S(ω)` construction + canonical `E_echo`).
4. QC gates & pass/fail table (trace/positivity, dt-halving stability, OTOC sanity).
5. Experiments (parameter grid).
6. Results (the 4 minimum plots listed in step 10 + a small KPI table).
7. Artifacts (paths + hashes/checksums if you’re being extra disciplined).
8. Next steps (promote to T4 prereg protocol).

**Minimum experiments/figures for “non-embarrassing T3”**

* Two Lindblad families (e.g. dephasing + depolarizing).
* At least 3 values of γ and 3 of |ω|.
* Ensemble size large enough that `E_echo` is stable under bootstrap (you can show CI widths).
* The 4 plots + a QC table.

### B) `Derivation/Quantum_Echos/T4_PROPOSAL_OTOC_SIE_Echo_Meter_v1.md`

**Required sections**

1. Hypotheses + nulls

   * e.g. “High-frequency OTOC spectral weight predicts larger `E_echo` at fixed δ,T” (or state what you *actually* want).
2. Locked protocol

   * fixed V/W choice, Δt, T_spec, T_echo, ensemble sampling rule, histogram binning rule.
3. Locked analysis

   * exact FFT method, peak picking rule, which scalar “scramble” quantity you will correlate, CI method.
4. Gates / contradiction routing

   * what constitutes PASS/FAIL for meter stability and correlation strength.
5. Ablations you promise (at least: different δ, different ensemble seed strategy, dt-halving).

**Minimum experiments/figures for “non-embarrassing T4”**

* A preregistered grid you can run in <1 day.
* Explicit numeric thresholds (not vibes).
* A locked artifact schema (filenames + fields in JSON).

---

## 5. How this plugs back into the larger VDM story

This is **Current_TODO item 1c**: “Mode-resolved entropy echoes via OTOC (SIE-echo meter),” explicitly dependent on (1b) the SU(2) ACSP→Lindblad exemplar and (2) the SIE entropy-echo definition, with deliverables `T3_RESULTS_OTOC_SIE_Echo_SU2_v1.md` and `T4_PROPOSAL_OTOC_SIE_Echo_Meter_v1.md`.  Conceptually, it welds **A4 (J⊕M split)** to **A7 (measurable meters)** by making “scrambling” (OTOC spectrum) and “memory recovery” (entropy echo `E_echo`) into a *single calibrated instrument chain* sitting on top of your boring-but-legit SU(2) Lindblad testbed. That’s valuable because it creates a cross-branch bridge: the **KG+RD metriplectic engine** teaches you how to build and certify `J`/`M` numerically, and the **SIE/agency/echo** documents tell you what “echo” must mean in your own language (`E_echo = D_KL(μ0||μ_rew)`), so 1c becomes your first “scrambling meter” that can later be ported back onto classical fields (KG/RD) and eventually into your cosmology-facing instruments (interface/void meters) as a universal diagnostic of “how irreversible is the run, and in what modes.”
