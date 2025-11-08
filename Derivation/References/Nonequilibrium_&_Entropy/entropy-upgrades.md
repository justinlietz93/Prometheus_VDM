Yes—**Prigogine adds several missing (or only half‑wired) pieces** we can fold into VDM’s entropy stack. The punchline: he gives us *representation‑invariance*, *explicit open‑system entropy balance*, a **Lyapunov‑style “local potential”** for conduction, and a **clean separation of direct vs cross (“interference”) contributions** to entropy production—including when *minimum entropy production* is valid (and when it isn’t). These are not fully covered by what we’ve already integrated from de Groot–Mazur and Öttinger. 

Below are the concrete upgrades and exactly where the book supports them (by chapter/section and page ranges visible in the PDF you shared).

---

## What we can add **now** (new value for VDM)

1. **Representation‑invariant σ (affinity/flux transforms).**
   Prigogine shows that the quadratic form for entropy production ( \sigma = \sum_j J_j X_j ) is *invariant* under linear changes of variables that map rates/fluxes and affinities together (think (X' = A X), (J' = A^{-T} J)), so long as you transform both sides consistently. This matters because it lets us test our near‑equilibrium audits without depending on a particular parameterization (e.g., whether we use (1/T) or (T) with a compensating transform). Add a **representation‑invariance KPI**:
   [
   \Delta_\text{repr} \equiv \left|,\sigma - \sigma',\right|\quad\text{over random well‑conditioned }A.
   ]
   If (\Delta_\text{repr}) isn’t numerically small, our force/flux bookkeeping (or units) is off. See **Chapter IV, §1–2** on transformation properties of rates and affinities and the invariance of (dS/dt) (pp. 40–46). 

2. **Direct vs “interference” (cross‑coupling) decomposition—and positivity tests.**
   He writes (dS/dt) explicitly as a quadratic form with diagonal (“proper”) and off‑diagonal (“mutual”) phenomenological coefficients and derives the positivity constraints for each block, not just the whole. We should report **interference share**:
   [
   \chi_\text{cross}=\frac{\text{off‑diag contribution to }\sigma}{\text{total }\sigma}
   ]
   and assert diagonal blocks are PSD individually. This catches illegal cross‑couplings early (beyond Curie/Onsager). See **Chapter IV, §2–4** (pp. 45–47) where the quadratic form is expanded and inequalities like (4.24–4.26) are discussed. 

3. **Open‑system entropy balance with explicit boundary terms.**
   For VDM runners with walls/lids (OQ‑021), we should log the *boundary entropy flux* alongside the local production. Prigogine’s open‑system balance is laid out in **Chapter III, §8–10** (pp. 28–34): write
   [
   \frac{dS}{dt}=\underbrace{\int_\Omega \sigma,dV}*{\text{production}}
   -\underbrace{\oint*{\partial\Omega}\frac{\mathbf q\cdot\mathbf n}{T},dA}_{\text{entropy out by heat}} ;+;\text{(matter/electrochemical terms if present)}.
   ]
   We already monitor (\sigma); this adds the *surface* term(s) so our H‑theorem claims remain correct for non‑isolated domains. This is directly applicable to the lid‑driven cavity (heat leakage is boundary‑localized). 

4. **Minimum entropy production (MEP): label it *opt‑in*, but test when valid.**
   The text precisely states **when** MEP holds for *stationary near‑equilibrium* states with linear phenomenology and fixed constraints, and when it fails. Make this a **conditional gate** you can turn on only for LIT regimes and verify that small compatible perturbations increase (\sigma) (second‑variation positive). See **Chapter VI, §1–2** (pp. 75–77) and the worked examples that follow. We then *warn* if anyone tries to use MEP outside its scope. 

5. **Lyapunov “local potential” for conduction (monotone functional).**
   A gem you don’t have yet: in **Chapter VII, §6** (pp. 113–116) he constructs a *local potential* (\Phi(T,T_0)) for heat conduction with fixed boundary values that **decreases monotonically in time** and reaches its minimum at the steady solution (T_0). That’s a ready‑made **Lyapunov monitor** to add next to (\sigma(t)):

* implement (\Phi) (we can use the chapter’s definition, or a numerically robust proxy consistent with the inequality),
* assert ( \Phi(t+\Delta t) - \Phi(t) \le 0) up to tolerance,
* publish (\Phi)(time) for the corner tests.
  This gives us a second, independent “arrow of time” diagnostic beyond (\Delta\Sigma). 

6. **Near‑stationary “rotation” analysis: put antisymmetric couplings in (J), not (M).**
   Prigogine explains that oscillations/rotations around steady states require an antisymmetric part in the phenomenological matrix *or* external T‑odd fields; in GENERIC, antisymmetric couplings must live in the **Poisson** operator (J) (reversible), not in the **metric** (M). Add an audit that splits the estimated near‑equilibrium operator into symmetric vs antisymmetric parts and **fails if antisymmetric leakage appears in (M)**. See **Chapter VII, §5** (pp. 111–113). 

---

## Drop‑ins to make this real (lightweight, aligns with your helpers)

These bolt onto what you already landed (`check_antisymmetry`, `check_symmetry_psd`, `degeneracy_residuals`, `EntropyMonitor`).

**New KPIs** (names suggestive; implement in your `generic_helpers` or `vdm_addons/thermo`):

* `kpi-lit-repr-invariance`: draw a few random well‑conditioned (A), compute (X' = A X), (J' = A^{-T} J), check (|\sigma - \sigma'|) and report worst case. Source: Ch. IV invariance (§1–2). 
* `kpi-lit-interference-share`: split (\sigma) into diagonal vs off‑diagonal contributions using your (L) (or local M‑block), assert diagonal blocks PSD and log (\chi_\text{cross}). Source: Ch. IV (§2–4). 
* `kpi-entropy-balance-open`: compute volume production (\int\sigma) and boundary terms (-\oint (\mathbf q\cdot\mathbf n)/T) (and optional matter/electrochemical pieces); publish both plus their sum (dS/dt). Source: Ch. III (§8–10). 
* `kpi-phi-conduction-monotone`: implement (\Phi(T,T_0)) for fixed‑boundary conduction, enforce monotonic decrease. Source: Ch. VII (§6). 
* `kpi-rotation-split`: near stationarity, estimate effective linear operator; enforce antisymmetric part goes to (J), symmetric to (M). Source: Ch. VII (§5). 

> **Scope guardrails (from the book):**
> MEP is *only* a near‑equilibrium, linear‑law result with fixed constraints; use as an *opt‑in* instrument, not a universal gate (Ch. VI). The rotation analysis clarifies that any “circulation” you observe near steady state must trace back to reversible structure (our (J)) or T‑odd drivers—not to (M) (Ch. VII). 

---

## Where this helps immediately

* **OQ‑021 (corners)**:

  * Report **open‑system entropy balance** per time‑slice (volume production vs wall flux).
  * Track the **local potential (\Phi)** for the conduction subproblem; publish its monotone decay alongside (\Delta\Sigma).
  * Keep Curie/Onsager as you already wired, and add **interference share** to prove cross‑terms aren’t doing the “cheating.” 

* **Docs**: A one‑page **“Prigogine addendum”** spelling out when the **minimum entropy production** instrument applies, with citations to Ch. VI. 

---

## One‑sprint checklist

* [ ] Implement `kpi-lit-repr-invariance`, `kpi-lit-interference-share`, `kpi-entropy-balance-open`, `kpi-phi-conduction-monotone`, `kpi-rotation-split`.
* [ ] Add a **Results** panel that shows: (\sigma) map, boundary entropy flux, (\Phi(t)), and a bar chart of diagonal vs cross contributions to (\sigma).
* [ ] Update the **Axiom‑core gates** doc with an “Open‑System Entropy” section citing Ch. III and a “Representation Invariance” note citing Ch. IV. 

---

Bottom line: **keep this book in the toolbox.** It gives us four crisp, testable instruments—*invariance*, *interference decomposition*, *open‑system balance*, and a *Lyapunov functional for conduction*—that strengthen VDM’s entropy story without changing your core axioms. If you want, I’ll package the KPIs above into a small `vdm_addons/thermo/prigogine_gates.py` so they integrate with your `EntropyMonitor` and artifact routing out of the box. 
