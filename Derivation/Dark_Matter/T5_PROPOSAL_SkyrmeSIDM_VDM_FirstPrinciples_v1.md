<!-- Derive Voxtrium’s Skyrme‑SIDM curve from first principles (starting at the Lagrangian, solving the hedgehog profile, computing phase shifts and the transfer factor (C_T(k))), **not** to assume his numbers.

> **Where to put this file (paths)**
>
> * **Proposal file (this document):**
>   `Derivation/Proposals/T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md`
>
> * **Domain (code/artifacts namespace):**
>   `Derivation/code/physics/dm/sidm_soliton/`
>
> * **Schema:**
>   `Derivation/code/physics/dm/sidm_soliton/schemas/SIDM_SKYRME.schema.json`
>
> * **Spec (pre‑reg run config):**
>   `Derivation/code/physics/dm/sidm_soliton/specs/sidmskyrme.v1.json`
>
> * **Approval manifest:**
>   `Derivation/code/physics/dm/sidm_soliton/APPROVALS.json`
-->

# 1. T5 (Pilot) — First‑Principles Skyrme‑SIDM × VDM Micro‑to‑Macro Bridge

> **Created Date:** 2025-11-10  
> **Provenance commit:** `{git rev-parse HEAD}`  
> **Salted provenance:** base_sha256=`{...}` | salt_hex=`{...}` | salted_sha256=`{...}`  
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)  
> **License:** See `LICENSE` at repo root  
> **Short summary:** From the $SU(2)$ Skyrme EFT, derive the hedgehog profile, shape constants and scattering amplitude, then produce a **parameter‑free** prediction of $(\sigma\_T/m(v))$ after one dwarf‑scale anchor $({m,(\sigma_T/m)_0})$. Couple the micro scales to VDM’s metriplectic boundary meters and publish pass/fail gates.  

***Practical provenance pattern*** (pre‑run): create and push a signed prereg tag; include salted hashes here and in §5.1.1. The run must record the tag in artifacts (per template).  

---

## 2. List of proposers and associated institutions/companies

* **Justin K. Lietz** — PI; theory, numerics, prereg author and approver.

---

## 3. Abstract

Proposed is a first‑principles derivation of a **self‑interacting dark matter (SIDM)** scattering law based on [Voxtrium's](https://doi.org/10.5281/zenodo.16857209) **SU(2) Skyrme effective field theory**: solve a single hedgehog soliton, compute **dimensionless shape constants** $((c\_m,c\_R,c\_\sigma))$, obtain the **mass–size** and **$low‑(v)$** normalization, and fold in **effective‑range** plus a **profile‑derived transfer factor** $(C_T(k))$. With one dwarf‑scale anchor $({m,(\sigma_T/m)_0})$ we algebraically determine $((K_s,e))$ and then **predict** $(\sigma\_T/m(v))$ across dwarfs→clusters **without per‑halo retuning**. These micro scales are then wired into VDM’s **A8 hierarchy** / boundary meters and **finite‑time A8‑T** gates to test consistency with codimension‑1 energy concentration and pulled fronts. The proposal registers **unitarity/analyticity** hygiene, **refinement** gates on the solved profile, and **optical‑theorem** checks of the amplitude. Results are published with reproducible manifests and salted provenance.

---

## 4. Background & Scientific Rationale

**Skyrme SIDM microphysics.** In Voxtrium’s notes, dark matter $(DM)$ is a **topological soliton** of an $SU(2)$ Skyrme EFT; solving one hedgehog locks three **dimensionless profile integrals** $((c_m,c_R,c_\sigma))$. These in turn lock the mass–size relation, the **low‑velocity** $((\sigma_T/m)_0)$ normalization, and a **finite‑size suppression scale** that drives the turnover of $(\sigma\_T/m(v))$. After anchoring $({m,(\sigma\_T/m)\_0})$, the EFT couplings $((K_s,e))$ are fixed **algebraically** and the full velocity dependence follows from **effective range** (s‑wave) times a **profile‑derived transfer factor** $(C\_T(k))$ (no extra mediators). This pipeline is recorded succinctly in the “Skyrme SIDM Pocket Reference.”  

**Core equations (micro):** with  

$$(U\in SU(2)), (L\_\mu=U^\dagger\partial\_\mu U)$$

$$[
\mathcal{L}=\frac{F^2}{16}\mathrm{Tr}(L_\mu L^\mu)+\frac{1}{32e^2}\mathrm{Tr}([L_\mu,L_\nu]^2),\quad K_s\equiv \tfrac{F}{2},\ X\equiv eK_s.
]$$

Hedgehog  

$$
(U(r)=\cos f(r)+i(\hat r\cdot\tau)\sin f(r)), (x\equiv X r);  
$$

$$
energy (E=(K\_s/e),4\pi\int\epsilon(x),dx)
$$  

yielding **shape constants**  

$$
(c\_m,c\_R,c\_\sigma=\pi c\_R^2/c_m)
$$

Calibrate by  

$$
({m,(\sigma\_T/m)*0}\Rightarrow (K\_s,e)\Rightarrow R*\ast=c\_R/X)
$$

then **predict** $(\sigma\_T/m(v))$ using s‑wave ERE and $(C\_T(k))$.

**Hygiene and unitarity.** The construction uses **partial‑wave unitarity** (ERE), a **profile transfer** bounded by unity, standard **forward‑limit analyticity**, and asymptotics well below Froissart–Martin bounds (UV behavior improved by finite size).

**VDM context.** VDM’s A8 (candidate) asserts that in metriplectic, tachyonic pulled‑front systems, finite excess energy on large domains **forces hierarchical scale breaks** with boundary‑law energy on codimension‑1 sets; the finite‑time variant A8‑T supplies operational coverage bounds and $(\delta^2)$ receipts from tail truncation. This proposal bridges the **micro** Skyrme scales into VDM’s **boundary meters** so that the same calibrated $((K\_s,e))$ that predict $(\sigma\_T/m(v))$ also **predict boundary observables** that A8/A8‑T can grade.

---

## 5. Intellectual Merit and Procedure

**Questions.** (Q1) Can the Skyrme EFT’s **first‑principles** derivation (not imported numbers) reproduce the hedgehog constants and produce a **unitary, predictive** $(\sigma\_T/m(v))$ from a single dwarf‑scale anchor? (Q2) Do the implied micro scales $((X,R\_\ast))$ and the predicted **finite‑size turnover** align with VDM’s **boundary‑law** and **pulled‑front** meters (A8/A8‑T), without extra knobs?

**Impact.** A parameter‑disciplined, unitary micro model tied by prereg meters to macro **boundary phenomenology** raises the bar beyond flexible mediator models. It also furnishes a testable micro→macro **causal spine** for VDM.

**Approach.** A strict, reproducible pipeline:

1. **Profile solve (from scratch).** Solve the hedgehog ODE to obtain $(f(x))$; compute $((c\_m,c\_R,c\_\sigma))$. Demonstrate **grid‑refinement stability** and independence of bookkeeping choices (e.g., whether $(x^2)$ sits “inside $(\epsilon)$” or in the measure).  

2. **Algebraic calibration.** Given $({m,(\sigma\_T/m)\*0})$ at dwarfs, compute $((K\_s,e))$, then $(X)$ and $(R*\ast)$. Keep **all units** consistent ($cm(^2)/g$ to $GeV(^{-3})$).

3. **Amplitude & unitarity.** Build the s‑wave ERE amplitude, attach the **profile transfer**:

$$[
\frac{\sigma_T}{m}(v)=\left(\frac{\sigma_T}{m}\right)*0 \frac{1}{\big[1-\tfrac12 a r_e k^2\big]^2+(a k)^2}\times C_T(k),\quad C_T(k)=\frac{1}{4\pi}!\int d\Omega,(1-\cos\theta),|F*{\rm prof}(q)|^2,
]$$

   with $(k=\mu v)$ and $(F\_{\rm prof})$ determined by $(\epsilon(x))$. Check **optical theorem** residuals and **forward analyticity** positivity.

4. **One‑curve prediction.** Hold a single global $(r\_e=\xi R\_\ast)$ $((\xi=\mathcal{O}(1)))$ and **do not** add per‑halo knobs. (Optional breathing mode off for baseline.)

5. **VDM overlay.** Feed $(R\_\ast)$ and turnover $(v\_{R\_\ast})$ into the VDM boundary meters: boundary‑law $(\to)$ **codimension‑1** energy fraction, DSI probes, and A8‑T coverage pressure.  

---

## 5.1 Experimental Setup and Diagnostics

**Parameters (inputs).**

* Dwarf anchors: $(m)$ $[GeV]$, $((\sigma_T/m)_0)$ $[cm(^2)/g]$.
* ERE choice: $(\xi)$ for $(r\_e=\xi R\_\ast)$ (single global in ($\[0.5,1.0]$\)).
* Numerics: ODE tolerances; quadrature tolerances for $(F\_{\rm prof}(q))$; $(k)$ grid.

**Diagnostics (micro).**

* Profile integrals $((c\_m,c\_R,c\_\sigma))$ vs grid refinement.
* **Unit conversions** check $(cm(^2)/g (\leftrightarrow) GeV(^{-3}))$.
* **Optical theorem** residual $(|\text{Im},M - 2k\sqrt{s},\sigma\_{\rm tot}|)$.
* **Forward‑limit** dispersion convexity test; partial‑wave unitarity bound.
* $(C_T(k))$ reproducibility across two independent quadrature schemes.

**Diagnostics (VDM overlay).**

* Boundary‑law fraction $(\alpha)$ and info fraction $(\alpha\_\mathcal{I})$ on tubes; DSI ripple check; A8‑T coverage $(N(L,T))$ vs $(c\_\star)$ bound. 

---

## 5.1.1 Pre‑Run Config Requirements

* **APPROVALS.json** (required; block below)
* **Schemas** under `schemas/` and **specs** under `specs/` (blocks below)
* **PRE‑REGISTRATION.json** per template (same directory; not shown here for brevity)

**APPROVALS.json**

```json
{
  "preflight_name": "skyrme_sidm_preflight",
  "description": "Approval manifest for first-principles Skyrme SIDM pilot.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Real runs require this proposal and matching salted provenance.",
  "pre_registered": true,
  "proposal": "Derivation/Proposals/T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md",
  "allowed_tags": ["sidm-skyrme-v1"],
  "schema_dir": "Derivation/code/physics/dm/sidm_soliton/schemas",
  "approvals": {
    "sidm-skyrme-v1": {
      "schema": "Derivation/code/physics/dm/sidm_soliton/schemas/SIDM_SKYRME.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto timestamp",
      "approval_key": "auto hashed key"
    }
  }
}
```

(Conforms to the proposal template’s approvals and prereg flow.)  

**Schema** — `SIDM_SKYRME.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vdm.sidm.skyrme.v1",
  "title": "First-principles Skyrme SIDM run schema",
  "type": "object",
  "properties": {
    "m_GeV": {"type": "number", "minimum": 0.1},
    "sigmaT_over_m_cgs": {"type": "number", "minimum": 0.0},
    "xi_re_over_Rstar": {"type": "number", "minimum": 0.2, "maximum": 2.0},
    "ode_abs_tol": {"type": "number"},
    "ode_rel_tol": {"type": "number"},
    "quad_tol": {"type": "number"},
    "k_grid_spec": {"type": "array", "items": {"type": "number"}}
  },
  "required": ["m_GeV", "sigmaT_over_m_cgs", "xi_re_over_Rstar", "ode_abs_tol", "ode_rel_tol", "quad_tol"]
}
```

**Spec** — `sidmskyrme.v1.json`

```json
{
  "run_name": "sidm_skyrme_first_principles",
  "version": "1.0.0",
  "tag": "sidm-skyrme-v1",
  "schema_ref": "Derivation/code/physics/dm/sidm_soliton/schemas/SIDM_SKYRME.schema.json",
  "parameters": {
    "m_GeV": 6.283,
    "sigmaT_over_m_cgs": 0.10,
    "xi_re_over_Rstar": 0.6667,
    "ode_abs_tol": 1e-12,
    "ode_rel_tol": 1e-10,
    "quad_tol": 1e-10,
    "k_grid_spec": [1e-6, 1e-4, 1e-3, 1e-2, 5e-2, 1e-1]
  },
  "seeds": [0]
}
```

**Units helper** ($cm^2/g$ $(\leftrightarrow)$ $GeV^{-3}$) is documented in the cheat‑sheet; include those constants in code.

---

## 5.2 Experimental runplan

1) **Solve hedgehog ODE** with rigorous tolerances; compute $\((c\_m,c\_R,c\_\sigma)\)$ and **repeat** under (i) doubled resolution; (ii) alternative bookkeeping $(\(x^2\) inside vs. outside \(\epsilon\)$. Require convergence and invariance (see gates).  
2) **Calibrate** $$\((K\_s,e)\)$$ from the dwarf anchor $\(\{m,(\sigma\_T/m)\_0\}\)$; compute $\(X=eK\_s\)$, $\(R\_\ast=c_R/X\)$, $\(v\_{R\_\ast}=1/(\mu R\_\ast)\)$.  
3) **Build amplitude** $\(f\_{\rm ERE}(k)\)$ and **profile transfer** $\(C_T(k)\)$ from the solved $\(\epsilon(x)\)$; produce $\(\sigma\_T/m(v)\)$ on a velocity grid (dwarfs→clusters). Validate **unitarity/optical‑theorem** and **forward‑limit** positivity.  
4) **One‑knob discipline:** hold a **single** global $\(\xi\)$ in $\(r\_e=\xi R\_\ast\)$ (band \(0.5\!\le\!\xi\!\le\!1.0\)); keep optional internal mode **off** in baseline to maximize falsifiability.  
5) **VDM overlay:** ingest $\(R\_\ast, v\_{R\_\ast}\)$ as “micro‑implied scales” into the RD/KG runners; run A8/A8‑T meters (boundary fraction, DSI, coverage). (A8 candidate & A8‑T notes for placement and gates are already in the repo.) 

**Results publication:** white‑paper grade T5_RESULTS_* with figures, logs, salted hashes; same laddered provenance the template prescribes.  

---

## 6. Personnel

- **Justin K. Lietz** — implements, validates numerics, signs prereg, authors results.

---

## 7. References

- **Skyrme SIDM micro→macro**: hedgehog Lagrangian, profile integrals, algebraic calibration, ER + $\(C\_T(k)\)$ pipeline.   
- **Hygiene (unitarity/analyticity/UV):** optical theorem, forward‑limit dispersion, finite‑size suppression, Froissart–Martin behavior.  
- **Cheatsheet constants & anchors:** locked $\((c\_m,c\_R,c\_\sigma)\)$, conversions, calibration example; “one‑curve” logic.   
- **VDM A8/A8‑T context and placement guidance.** 

---

## Pass/Fail **Gates** (pre‑registered)

**G‑P1 (Profile stability).** The computed $\((c\_m,c\_R,c\_\sigma)\)$ change by **\< 0.5%** under 2× grid refinement and are **invariant** (within 0.2%) to the “ $\(x^2\)$ inside $\(\epsilon\)$ ” bookkeeping choice.  

**G‑P2 (Calibration reproducibility).** $\((K\_s,e)\)$, $\(X\)$, $\(R\_\ast\)$ recovered from the dwarf anchor **match algebraic solutions** to **$\< 10^{-8}$** relative error; $\(v\_{R\_\ast}\)$ consistent on two unit systems to **$\< 10^{-8}$**.  

**G‑A1 (Unitarity & optical theorem).** On the velocity grid, $\(|\text{Im}\,M(s,0)-2k\sqrt{s}\,\sigma\_{\rm tot}|\!/(\text{scale}) < 10^{-6}\)$ everywhere; the partial‑wave bound is never exceeded.  

**G‑A2 (Forward analyticity).** Second \(s\)‑derivative of the forward real part is **non‑negative** below threshold across the scan.  

**G‑T1 (One‑curve discipline).** With a **single** global $\(\xi\in[0.5,1.0]\)$, $\(\sigma\_T/m(v)\)$ is **monotonic** from dwarfs to clusters and displays a turnover set by $\(kR\_\ast\sim 1\)$; optional internal mode **off**.  

**G‑X1 (Transfer reproducibility).** $\(C\_T(k)\)$ computed by two independent quadratures agree within **0.5%** across $\(kR\_\ast\in[10^{-3},10]\)$.  

**G‑VDM1 (Boundary‑law overlay).** With the micro‑implied $\(R\_\ast\)$, the VDM run shows codimension‑1 energy fraction $\(\alpha>0.5\)$ and information fraction $\(\alpha\_\mathcal{I}>0.5\)$ on interface tubes at nominal resolution. (Same meters used in A8.)  

**G‑VDM2 (Finite‑time coverage).** For fixed $\(c\_\star=2\sqrt{Dr}\)$ the measured $\(N(L,T)\)$ satisfies $\(N \ge \lceil L/(c\_\star T)\rceil - 1\)$ on $\(\ge 90\%\)$ of seeds (A8‑T coverage pressure).  

**Ablations.**  
- **Profile‑off null:** replace $\(C\_T(k)\to 1\)$ (pointlike); turnover disappears—**must** fail G‑T1.  
- **ERE‑scramble:** randomize $\(r\_e\)$ per‑velocity (same mean); optical theorem residual rises—**must** fail G‑A1.  
- **Per‑halo tuning trial:** Allow per‑halo $\(\xi\)$; marks **OUT‑OF‑SCOPE** (violates one‑curve discipline).

---

## Failure modes → Interpretation

- **G‑P1 fails:** ODE/quad tolerances too loose or boundary conditions mis‑set; revisit solver & check near‑origin series.  
- **G‑A1/A2 fail:** ERE implementation bug or normalization of transfer kernel; verify $\(C\_0(k)\)$ normalization and forward limit.  
- **G‑T1 fails:** Either $\(\xi\)$ not $\(\mathcal{O}(1)\)$ or profile $\(F\_{\rm prof}\)$ wrong; re‑derive $\(F\_{\rm prof}(q)\)$ from $\(\epsilon(x)\)$.  
- **G‑VDM gates weak:** Micro scales inconsistent with boundary meters at current settings; report as tension with A8 overlay, keep micro result standalone.

---

## What we answer

> **“Do we import, or write a proposal experiment?”**  
> We write **this** T5 proposal and run it. It stands alone and does **not** assume Voxtrium’s numbers; it re‑derives them.

> **“Which two anchors?”**  
> The dwarf‑scale pair $\(\{m,(\sigma_T/m)\_0\}\)$. These determine $\((K\_s,e)\)$ $\(\Rightarrow\)$ $\(X\)$, $\(R\_\ast\)$ and then the **entire** $\(\sigma\_T/m(v)\)$ through $ERE\(\times C\_T(k)\)$. No per‑halo retuning. 

> **“Why compatible with my theory?”**  
> Because the A8/A8‑T machinery tests **where** energy/information live (interfaces, finite‑time coverage) and the Skyrme microphysics predicts a **finite size** $\(R\_\ast\)$ and a **turnover** $\(v\_{R\_\ast}\)$ that can be **independently** compared against the boundary meters. The two stories meet at **codimension‑1 structure** with a micro‑derived scale.  

---

### Appendix — Equations/definitions we will compute in‑house (first principles)

- **Hedgehog ODE** and constants:

$$[
E=(K_s/e)4\pi\!\int_0^\infty\!\!\epsilon(x)\,dx,\quad
c_m=4\pi\!\int\epsilon\,dx,\ 
c_R=\Big(\tfrac{\int x^2\epsilon\,dx}{\int \epsilon\,dx}\Big)^{1/2},\ 
c_\sigma=\pi c_R^2/c_m.
\]
$$
  
  (Bookkeeping choices like “\(x^2\) inside \(\epsilon\)” are benign; invariants must agree.)  

- **Calibration from anchors:**

$$[
K_s^2=\frac{c_m c_\sigma}{m\,(\sigma_T/m)_{\rm nat}},\quad e=\frac{c_m K_s}{m},\quad X=eK_s,\quad R_\ast=\frac{c_R}{X}.
\]$$
  
  ***(Unit conversions per cheatsheet.)*** 

- **ERE + profile transfer:**

$$[
k\cot\delta_0=-\frac{1}{a}+\frac{r_e}{2}k^2,\quad
\frac{\sigma_T}{m}(v)=\Big(\frac{\sigma_T}{m}\Big)_0 \frac{1}{[1-\tfrac12 a r_e k^2]^2+(ak)^2}\times C_T(k),
\]
$$

$$
\[
C_T(k)=\frac{1}{4\pi}\!\int d\Omega\,(1-\cos\theta)\,|F_{\rm prof}(q)|^2,\ 
F_{\rm prof}(q)=\frac{\int_0^\infty\epsilon(x)\,j_0((q/X)x)\,dx}{\int_0^\infty\epsilon(x)\,dx}.
\]$$

---

### Notes

- Commit this file at `Derivation/Dark_Matter/T5_PROPOSAL_SkyrmeSIDM_VDM_FirstPrinciples_v1.md`.  
- Add `APPROVALS.json`, schema, and spec at the paths listed above (per §5.1.1).  
- When publishing results, reference the existing A8 candidate and A8‑T notes (placement guidance already spelled out there).
- **Skyrme EFT & one‑curve pipeline** (hedgehog → $\((c_m,c_R,c_\sigma)\)$ → calibration → $\(\sigma\_T/m(v)\)$ with ERE × $\(C\_T\))$ comes from Voxtrium’s “Microphysics” and “SuperCheatsheet” documents; I used his **equations**, not his **numbers**, to set the derivation targets and pass/fail gates.   
- **Unitarity/analyticity hygiene** and forward‑limit checks are codified in his amplitude note; I turned those into **gates G‑A1/A2**.  
- **VDM A8/A8‑T** statements and placement guidance were taken from the proposal text; these are the boundary meters the micro result will face. 

---

### References

* J. K. Lietz. 2025. The Lietz Infinity Resolution Conjecture: Hierarchical Scale-Breaking in Tachyonic Metriplectic Systems (v0.1). Zenodo. https://doi.org/10.5281/zenodo.17503344  
* J. K. Lietz. 2025. Agency field evolution in metriplectic systems. VDM Canonical Documentation, https://github.com/justinlietz93/Prometheus_VDM/Derivation/AGENCY_FIELD.md.  
* J. K. Lietz. 2025. Causality-enhanced guidance in the Void Dynamics Model. VDM Internal Report, https://github.com/justinlietz93/Prometheus_VDM/Derivation/.  
* Voxtrium. 2025. Voxtrium/GR-DM-Interaction-Theory: SU2-Skyrme-SIDM-Microphysics (v1.0). Zenodo. https://doi.org/10.5281/zenodo.16857209  
