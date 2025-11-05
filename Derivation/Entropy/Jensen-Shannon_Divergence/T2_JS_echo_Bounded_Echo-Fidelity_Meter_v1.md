# T2 — **JS_echo: A Bounded Echo-Fidelity Meter for Forward→Rewind Experiments (VDM Instrument Proposal)**

> **Created Date:** 2025‑11‑05
> **Provenance (to be auto-populated by preflight script):**
> • `commit_sha`: `<git rev-parse HEAD>`
> • `base_sha256`: `<sha256(commit_sha)>`
> • `salt_hex`: `<32–64 hex chars>`
> • `salted_sha256`: `<sha256(commit_sha || salt_hex)>`
> **Proposer contacts:** Justin K. Lietz (PI), implementers TBD  <[justin@neuroca.ai](mailto:justin@neuroca.ai)>
> **License:** MIT (see `LICENSE`)
> **One‑sentence TL;DR:** Proposed herein is a rigorously qualified, bounded, symmetric **echo meter**—**JS_echo**—that scores the quality of a rewind (“comeback”) by comparing **cluster occupancy** distributions from forward vs. rewind states using the Jensen–Shannon divergence.

This document follows the required VDM white‑paper scaffold and preregistration/provenance procedures.  

---

## 2. Proposers and affiliations

* **Justin K. Lietz**, Neuroca AI — **PI / approver**
* **TBD**, Neuroca AI — **implementer**
* **TBD**, Collaborating Lab — **implementer**

---

## 3. Abstract (≤200 words)

A general, portable metric is needed to quantify the fidelity of “rewind” operations across forward→rewind experiments (agency/echo studies, reversible dynamics, control pulses). **JS_echo** scores echo quality at time index $\tau$ as
$$
\mathrm{JS_echo}(\tau) \equiv 1 - D_{\mathrm{JS}}!\big(P_{\text{fwd}}(\tau), P_{\text{rev}}(\tau)\big)\in[0,1],
$$
where $P_{\text{fwd}}$ and $P_{\text{rev}}$ are **cluster occupancy** distributions induced by a fixed state‑space partition. With base‑2 logarithms, $D_{\mathrm{JS}}\in[0,1]$ bits, ensuring intuitive normalization (1 = perfect comeback, 0 = none). This proposal (Tier **T2: Instrument**) specifies the meter, diagnostic suite, datasets, and preregistered **pass/fail gates** to qualify the meter for subsequent physics claims (T3+) and preregistered tests (T4–T6). The plan includes analytical reversibility baselines, controlled noise injections, partition‑robustness sweeps, bootstrap CIs, and cross‑metric comparisons (EMD/MMD). Deliverables include an audited implementation, schemas/specs, and machine‑actionable artifacts suitable for CI.

---

## 4. Background & Scientific Rationale

**Context.** Forward→rewind experiments arise in reversible dynamics, control/compensation, and “agency/echo” protocols where a system is driven forward under flows with dissipation and subsequently “rewound” by engineered operations. A robust, **display‑level** scalar score is needed to compare rewind states against forward references while tolerating microscopic jitter and remaining strictly bounded and symmetric.

**Prior work (VDM ladder).** This document is a **T2 (Instrument)** proposal. Supporting artifacts (T0–T1) are referenced for continuity and will be linked in the repository:

* **T0 (Concept):** `Derivation/agency/T0_PROPOSAL_js_echo_concept.md` and `RESULTS_T0/…`
* **T1 (Proto‑model):** `Derivation/agency/T1_PROPOSAL_js_echo_protomodel.md` and `RESULTS_T1/…`

**Why Jensen–Shannon on occupancies?**

* **Symmetric & bounded.** With base‑2 logs, $D_{\mathrm{JS}}\in[0,1]$ supports direct mapping to a fidelity‑like score $1-D_{\mathrm{JS}}$.
* **Well‑behaved with zeros.** Mixture smoothing avoids infinite divergences.
* **Coarse‑grained robustness.** Occupancy in a **fixed, frozen partition** filters micro‑scale chaos while preserving macro‑state comparisons.
* **Interpretability.** “Where the system spends time” is operationally tangible across domains.

**Criticisms & mitigations.**

* **Partition dependence:** mitigated via **DIP** (Discretization Invariance Protocol) sweeps across $k$ and grid bins with preregistered robustness gates.
* **State aliasing:** checked via ablations that vary embedding choices and evaluate stability gates.
* **Temporal windowing bias:** normalized sampling windows and preregistered $N_\tau$ per time index.

---

## 5. Intellectual Merit and Procedure

**(1) Importance.** A validated, domain‑agnostic echo meter enables rigorous comparisons of rewind protocols, a prerequisite for causal claims about control quality and dissipation recovery.

**(2) Broader impacts.** The instrument underpins preregistered physics tests (T4–T6) and robustness (T7–T8) across simulation/control labs; outputs are CI‑ready and reproducible.

**(3) Clarity & approach.** The meter, data pathway, and acceptance gates are fully specified with schemas and pass/fail thresholds.

**(4) Rigor & discipline.** Provenance (salts, tags, signed prereg), partition freezes, seeds, and power targets are mandated in 5.1.1.

---

## 5.1 Experimental Setup and Diagnostics

### 5.1.1 Meter definition

Let $\mathcal{X}$ be state space, $\Phi:\mathcal{X}!\to!{1,\dots,K}$ a **fixed** partition (e.g., $k$‑means on frozen embeddings or axis‑aligned grid). For a set of samples at time index $\tau$:
[
P_i(\tau)=\frac{1}{N_\tau}\sum_{n=1}^{N_\tau}\mathbf{1}{\Phi(x^{\text{fwd}}*{n,\tau})=i},\quad
Q_i(\tau)=\frac{1}{N*\tau}\sum_{n=1}^{N_\tau}\mathbf{1}{\Phi(x^{\text{rev}}*{n,\tau})=i}.
]
With $M=\tfrac12(P+Q)$ and base‑2 logs,
[
D*{\mathrm{JS}}(P,Q)=\tfrac12 D_{\mathrm{KL}}(P|M)+\tfrac12 D_{\mathrm{KL}}(Q|M),\quad
D_{\mathrm{KL}}(A|B)=\sum_i A_i\log_2\frac{A_i}{B_i}.
]
Define the **echo score**:
[
\boxed{;\mathrm{JS_echo}(\tau)=1-D_{\mathrm{JS}}(P(\tau),Q(\tau))\in[0,1];}
]
**Smoothing.** Add $\varepsilon$ prior: $\tilde{P}=(P+\varepsilon)!/!|\cdot|_1$ and similarly $\tilde{Q}$, with $\varepsilon=10^{-9}$ unless overridden.

### 5.1.2 Required parameters (defaults)

* **Partition type & size:** $K\in{32,64,128}$ (primary default $K=64$); grid alternatives: ${16!\times!16,32!\times!32}$.
* **Embedding/feature map:** $\psi(x)$ (frozen if learned).
* **Smoothing:** $\varepsilon=10^{-9}$.
* **Time indices:** $\tau\in{0,\dots,T}$; report per‑$\tau$ and terminal $\tau=T$.
* **Samples per $\tau$:** $N_\tau\ge 1000$ (power target in §5.4).
* **Bootstraps:** $B=1000$ per $\tau$ for CIs.
* **Seeds:** `seeds=[0,1,2,3,4]` minimum.

### 5.1.3 Diagnostics (counts & purpose)

* **D1:** Partition robustness (DIP) sweeps: 5 partitions × 3 $K$ levels (15 instruments).
* **D2:** Bootstrap CI per $\tau$ (95%).
* **D3:** Cross‑metric checks vs. EMD ($W_1$) and MMD (RBF).
* **D4:** Sensitivity curves under controlled noise $\sigma$.
* **D5:** Temporal alignment offsets $\Delta\tau$ tests.
* **D6:** Reversibility baselines: analytic oscillator (Hamiltonian), and Langevin double‑well (with/without noise).

---

## 5.1.1 Pre‑Run Config Requirements (machine‑actionable)

**Approval manifests and schema locations (domain `agency`)** must exist and be signed before runs that write artifacts.

#### APPROVALS.json

```json
{
  "preflight_name": "vdm.preflight.agency",
  "description": "Approval manifest for JS_echo instrument runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Only preflight tests may run without approval. Artifact-writing runs require a compliant PROPOSAL_* at Derivation/agency/.",
  "pre_registered": true,
  "proposal": "Derivation/agency/T2_PROPOSAL_JS_echo.md",
  "allowed_tags": ["js-echo-1.0"],
  "schema_dir": "Derivation/code/physics/agency/schemas",
  "approvals": {
    "js-echo-1.0": {
      "schema": "Derivation/code/physics/agency/schemas/js-echo.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "<auto timestamp>",
      "approval_key": "<auto hashed key>"
    }
  }
}
```

#### PRE-REGISTRATION.json

```json
{
  "proposal_title": "JS_echo: Echo-Fidelity Instrument",
  "tier_grade": "T2",
  "commit": "<git-sha>",
  "salted_provenance": "<salted_sha256>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "On a numerically reversible integrator, terminal JS_echo >= 0.985.", "direction": "increase" },
    { "id": "H2", "statement": "JS_echo decreases monotonically with noise amplitude sigma.", "direction": "decrease" },
    { "id": "H3", "statement": "JS_echo decreases with absolute misalignment |Δτ|.", "direction": "decrease" },
    { "id": "H4", "statement": "Partition sweeps yield MAD(JS_echo)<=0.03 at each τ.", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["partition_type", "K", "sigma", "Δτ"],
    "dependent": ["JS_echo(τ)", "JS_echo(T)"],
    "controls": ["N_τ", "ε", "seeds", "embedding ψ"]
  },
  "pass_fail": [
    { "metric": "reversible_terminal", "operator": ">=", "threshold": 0.985, "unit": "1" },
    { "metric": "noise_monotonicity_spearman", "operator": "<=", "threshold": -0.95, "unit": "ρ" },
    { "metric": "offset_monotonicity_spearman", "operator": "<=", "threshold": -0.90, "unit": "ρ" },
    { "metric": "partition_mad_max", "operator": "<=", "threshold": 0.03, "unit": "1" },
    { "metric": "bootstrap_ci_width_max", "operator": "<=", "threshold": 0.06, "unit": "1" },
    { "metric": "mismatch_baseline", "operator": "<=", "threshold": 0.20, "unit": "1" }
  ],
  "spec_refs": ["Derivation/code/physics/agency/js-echo.1.0.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

#### Specs (run‑time)

```json
{
  "run_name": "js-echo.qual.1",
  "version": "1.0.0",
  "tag": "js-echo-1.0",
  "schema_ref": "Derivation/code/physics/agency/schemas/js-echo.schema.json",
  "parameters": {
    "K": 64,
    "partition_type": "kmeans",
    "embedding": "frozen:psi_v1",
    "epsilon": 1e-9,
    "taus": [0,1,2,3,4,5,10,20,50,100],
    "N_tau": 2000,
    "bootstraps": 1000,
    "seeds": [0,1,2,3,4],
    "comparators": ["EMD", "MMD"],
    "noise_levels": [0.0,0.1,0.2,0.3],
    "offsets": [0,1,2,3,5,8]
  },
  "seeds": [0,1,2,3,4]
}
```

#### Schemas (excerpt)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "js-echo.schema",
  "type": "object",
  "properties": {
    "K": {"type": "integer", "minimum": 8, "maximum": 4096},
    "partition_type": {"type": "string", "enum": ["kmeans","grid"]},
    "embedding": {"type": "string"},
    "epsilon": {"type": "number", "minimum": 0},
    "taus": {"type": "array", "items": {"type": "integer", "minimum": 0}},
    "N_tau": {"type": "integer", "minimum": 100},
    "bootstraps": {"type": "integer", "minimum": 100},
    "seeds": {"type": "array", "items": {"type": "integer"}}
  },
  "required": ["K","partition_type","embedding","epsilon","taus","N_tau","bootstraps","seeds"]
}
```

---

## 5.2 Qualification protocol & acceptance gates

**Benchmarks.**

* **B1: Reversible oscillator.** Symplectic integrator; round‑trip without dissipation. **Gate:** $\mathrm{JS_echo}(T)\ge 0.985$ and 95% CI lower bound $\ge 0.97$.
* **B2: Mismatch baseline.** Randomly permute rewind samples per $\tau$. **Gate:** median $\mathrm{JS_echo}(T)\le 0.10$ and 95% upper CI $\le 0.20$.
* **B3: Noise sensitivity.** Add i.i.d. perturbations with $\sigma\in{0,0.1,0.2,0.3}$. **Gate:** Spearman $\rho(\sigma,\mathrm{JS_echo}(T))\le -0.95$.
* **B4: Temporal misalignment.** Shift rewind snapshots by $\Delta\tau$. **Gate:** Spearman $\rho(|\Delta\tau|,\mathrm{JS_echo}(T))\le -0.90$.
* **B5: Partition robustness (DIP).** Across $K\in{32,64,128}$ and 5 seeds of partitions, **Gate:** per‑$\tau$ $\operatorname{MAD}\le 0.03$.
* **B6: Precision/stability.** Bootstrap 95% CI width $\le 0.06$ for all reported $\tau$.

**Cross‑metric sanity.** For B1–B4, **EMD/MMD** must agree in directionality of change ($\ge95%$ agreement across settings). **Gate:** pass/fail boolean.

---

## 5.3 Implementation & auditing notes

* **Partition freezing.** If $k$‑means is used, centroids are fit **once** on a reference corpus and committed as artifacts; subsequent runs only assign.
* **Label semantics.** No label permutation is allowed post‑freeze; centroids are the invariant reference.
* **Smoothing.** $\varepsilon$ added component‑wise before normalization.
* **Numerical base.** All logs are base‑2 to bound $D_{\mathrm{JS}}\le1$ and make the range intuitive.
* **CIs.** Nonparametric bootstrap over samples within each $\tau$.
* **Reproducibility.** Seeds, centroids, embeddings, and transforms are versioned in the manifest.

**Reference implementation (auditable, language‑agnostic).**

```plaintext
function JS_divergence(p, q):
    m = 0.5*(p+q)
    return 0.5*KL(p, m) + 0.5*KL(q, m)   # log base-2

function JS_echo(p_fwd, p_rev):
    return 1.0 - JS_divergence(p_fwd, p_rev)
```

---

## 5.4 Statistical design & power

For multinomial occupancy with $K\in[32,128]$ and uniform‑ish mass, the variance of plug‑in $D_{\mathrm{JS}}$ shrinks as $\mathcal{O}(1/N_\tau)$. Pilot calculations (not shown) indicate that **$N_\tau\ge 1000$** yields typical standard errors $\lesssim 0.02$ for moderate $K$, making the **CI‑width ≤0.06** gate feasible with $B=1000$ bootstraps. The preregistered **seeds ≥5** ensure stability estimates for partitions and samplers.

---

## 6. Broader impacts

A bounded fidelity score that is **portable** across domains (simulators, bench setups, agent rollouts) advances testable claims about reversibility, control, and dissipation. The meter’s discipline (frozen partitions, prereg CIs, taggable artifacts) promotes **reproducible physics** and seamless CI integration.

---

## 7. Risks, limitations, and mitigations

* **Partition bias / aliasing.** Addressed via DIP sweeps and **MAD ≤ 0.03** gate.
* **Embedding drift.** Embeddings are **frozen**; any update revs the instrument tag and re‑qualifies.
* **Temporal window mismatch.** Uniform sampling windows preregistered per $\tau$; offsets are explicitly stress‑tested.
* **Domain mismatch.** Cross‑metric checks (EMD/MMD) guard against degenerate occupancy matches.

---

## 8. Deliverables & artifacts

1. **Code & CLI:** `Derivation/code/physics/agency/js_echo/` (reference impl, tests).
2. **Schemas & specs:** as in §5.1.1.
3. **Prereg tag:** `prereg.js-echo.v1.YYYYMMDDThhmmZ` including salts and commit.
4. **Qualification report:** auto‑generated PDFs/JSON logs with B1–B6 outcomes, CIs, and DIP sweep tables.
5. **RESULTS_T2:** Signed result bundle with pass/fail gates and reproducibility manifest.

---

## 9. References (minimal)

* Lin, J. “Divergence Measures Based on the Shannon Entropy.” *IEEE Trans. Inf. Theory*, 37(1):145–151, 1991.
* Endres, D. M., & Schindelin, J. E. “A New Metric for Probability Distributions.” *IEEE Trans. Inf. Theory*, 49(7):1858–1860, 2003.
* (VDM template and ladder as mandated in repository documentation.) 

---

## Appendix A — Procedural details (machine‑readable summary)

**A.1 Algorithmic contract**

1. **Input:** Frozen partition $\Phi$, samples ${x^{\text{fwd}}*{n,\tau}}$ and ${x^{\text{rev}}*{n,\tau}}$.
2. **Occupancy:** Compute $P(\tau),Q(\tau)$ with $\varepsilon$ smoothing; normalize.
3. **Score:** $\mathrm{JS_echo}(\tau)=1-D_{\mathrm{JS}}(P(\tau),Q(\tau))$ (base‑2).
4. **Uncertainty:** Bootstrap $B=1000$ for CIs, report per‑$\tau$ and terminal $T$.
5. **Robustness:** Repeat across DIP partitions; compute per‑$\tau$ MAD.

**A.2 Comparator metrics**

* **EMD ($W_1$)** on the same partition grid (grid mode) or via centroid distances (cluster mode).
* **MMD (RBF)** on embeddings $\psi(x)$; kernel bandwidth via median heuristic on reference set.
* **Directionality agreement:** fraction of settings where comparator’s change sign equals that of $\mathrm{JS_echo}$ w.r.t. perturbation (σ or $|\Delta\tau|$).

**A.3 Pass/fail gates (concise)**

| Gate                  | Criterion             | Threshold                            |
| --------------------- | --------------------- | ------------------------------------ |
| Reversible (B1)       | $\mathrm{JS_echo}(T)$ | $\ge 0.985$ (CI LB $\ge 0.97$)       |
| Mismatch (B2)         | $\mathrm{JS_echo}(T)$ | median $\le 0.10$, 95% UB $\le 0.20$ |
| Noise mono. (B3)      | Spearman $\rho$       | $\le -0.95$                          |
| Offset mono. (B4)     | Spearman $\rho$       | $\le -0.90$                          |
| Partition robust (B5) | MAD per‑$\tau$        | $\le 0.03$                           |
| Precision (B6)        | CI width per‑$\tau$   | $\le 0.06$                           |
| Comparator agree      | Direction match       | $\ge 95%$                            |

---

## Tier Grade Justification and Lineage

**Tier:** **T2 (Instrument)**. The present document qualifies a **meter** with quantitative gates, without yet making physics claims about systems under study (T3+). Upon passing B1–B6 with preregistration satisfied, **RESULTS_T2** will carry the identical tier grade. Future documents will reference this instrument for **T3 (Phenomenon smoke tests)** and **T4–T6 (Preregistered hypotheses)**, as mandated by the VDM ladder.  

---

### Practical provenance checklist (must pass before artifact runs)

* Compute salted hashes (base_sha256, salt_hex, salted_sha256) and store in prereg; sign and push tag `prereg.js-echo.v1.YYYYMMDDThhmmZ`.
* Ensure `APPROVALS.json`, `PRE-REGISTRATION.json`, schema, and spec paths exist and validate.
* Freeze $\Phi$ (partition centroids or grid), $\psi$ (embedding), and `seeds`.
* CI gate: refuse artifact‑writing runs if proposal hashes or tags are missing/mismatched.  

---

**End of proposal.**
