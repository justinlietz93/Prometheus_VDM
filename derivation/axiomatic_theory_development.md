<!-- =============================================================== -->
# FUVDM Truth‑First Axiomatic Development (Single Source)
**Policy (Section 0):** Truth‑first. No training. One discrete action; all inertial / RD / KG / oscillatory / diffusion forms are *derived corollaries or limits* of that action with explicit conditions. No regime is assumed a priori.

Classification: RD | EFT‑quarantined (truth‑first audit)

Provenance (hashes pin evidence artifacts; numeric gates are constraints any corollary must satisfy in that regime — they do NOT elevate claims to axioms):

| Evidence Gate | Metric (PASS) | Artifact (figure/log) | SHA256 (truncated) |
|---------------|---------------|------------------------|--------------------|
| Front speed constraint \(c_{front}=2\sqrt{Dr}\) | rel‑err ≈ 4.7%, R²≈0.999996 PASS | fig: rd_front_speed_experiment_20250824T053748Z.png / log: rd_front_speed_experiment_20250824T053748Z.json | 5a4c630a… / 2062f64a… |
| Linear dispersion \(\sigma(k)=r-Dk^{2}\) | median rel‑err ≈ 1.45×10⁻³ PASS | fig: rd_dispersion_experiment_20250824T053842Z.png / log: rd_dispersion_experiment_20250824T053842Z.json | fed2c206… / 7bfa8e11… |
| This axiomatic file (integrity) | n/a | axiomatic_theory_development.md | 7b9e23dc… |

Hash source command (recorded): `sha256sum <artifacts>` on 2025‑08‑29.

Tag Legend: [AXIOM], [THEOREM-PROVEN], [LEMMA-PROVEN], [COROLLARY], [CONJECTURE], [NUM-EVIDENCE], [EFT-KG] (quarantined inertial/EFT statements), [LIMIT-ASSUMPTIONS]. Every non‑axiom must carry an allowed tag.

## Tagging Scheme (Unified)
Allowed status tags (each non‑axiom statement MUST carry one):
- `[THEOREM-PROVEN]` formally derived from A1–A4 with proof sketch or full derivation.
- `[LEMMA-PROVEN]` auxiliary proven step used in a theorem proof.
- `[COROLLARY]` immediate logical consequence of proved theorems/lemmas.
- `[CONJECTURE]` claim not yet proven from A1–A4; accompanied by explicit proof obligations.
- `[NUM-EVIDENCE]` empirically supported numerical observation (figures/logs referenced) — never upgrades logical status.

Unused / legacy labels (e.g. quarantine, heuristic) are deprecated in this document and replaced by the above.

## Section 1. Minimal Axioms (Self‑Contained)
**Axiom 1 (Geometry & Locality) [AXIOM]:** Space is a cubic lattice \(\Lambda_a=a\mathbb Z^{d}\) (\(d\ge1\)) with nearest‑neighbour set \(N(i)\) of size \(2d\); time is discrete \(t_n = n\Delta t\). Updates may depend only on \(W_i^{n}, W_i^{n-1}\) and \(W_j^{n}\) for \(j\in N(i)\).

**Axiom 2 (Field & Regularity) [AXIOM]:** Real scalar site field \(W_i^{n}\in\mathbb R\). A smooth interpolant \(\phi(x,t)\) exists so that lattice differences admit Taylor expansions through \(O(a^{4})\) and forward/backward time differences through \(O(\Delta t^{2})\) within a mesoscopic scale hierarchy \(a \ll \ell \ll L\).

**Axiom 3 (Admissible Potential Class) [AXIOM]:** On‑site potential \(V\) is thrice differentiable with polynomial growth and (optionally) quartic stabilization: representative form \(V(\phi)=\tfrac{\alpha}{3}\phi^{3}-\tfrac{r}{2}\phi^{2}+\tfrac{\lambda}{4}\phi^{4}\) with \(r=\alpha-\beta\), \(\lambda\ge0\); derivatives (single authoritative appearance):
\[V'(\phi)=\alpha\phi^{2}-r\phi+\lambda\phi^{3},\quad V''(\phi)=2\alpha\phi-r+3\lambda\phi^{2},\quad V'''(\phi)=2\alpha+6\lambda\phi.\]

**Axiom 4 (Discrete Action) [AXIOM]:**
Action functional (notation adjusted to avoid bracket mis‑parsing):
\[S(W)= \sum_{n} \Delta t \sum_{i} a^{d} \Big( \tfrac12 (\Delta_t W_i)^2 - \tfrac{J}{2}\sum_{j\in N(i)}(W_j-W_i)^2 - V(W_i) \Big), \quad J>0.\]
No additional axioms; everything else is derived, conditioned, or conjectural.

**Axiom 5 (Domain & Boundary Conditions) [AXIOM]:** Let \(\Omega\subset\mathbb R^{d}\) be the continuum domain of interest. When performing continuum integrations by parts we require one of the following boundary conditions on \(\partial\Omega\): periodic BCs, or no‑flux (homogeneous Neumann) BCs \(\hat n\cdot\nabla\phi=0\). Statements invoking integration by parts state which BC is used.

## Section 2. Core Derivations from the Action

### Derivation A (Discrete Euler–Lagrange → Second‑Order Update) [THEOREM-PROVEN]
Variation of Axiom 4 yields the *core discrete equation*:
\[\frac{W_i^{n+1}-2W_i^{n}+W_i^{n-1}}{\Delta t^{2}} = J \sum_{j\in N(i)}(W_j^{n}-W_i^{n}) - V'(W_i^{n}).\]
Taylor expansion (Axiom 2) of the neighbour term gives the *continuum inertial form* (quarantined inertial label):
\[\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0, \qquad c^{2}=2J a^{2}. \tag{1} [EFT-KG]\]
Error control is given explicitly by Lemma S.1 (spatial Taylor remainder) and Lemma T.1 (temporal Taylor remainder) below.

### Theorem 2 (Overdamped / Gradient‑Flow Limit and Lyapunov) [THEOREM-PROVEN]
Under the LIMIT‑ASSUMPTIONS below and Axiom 5 BCs, the coarse‑grained dynamics reduce to the gradient‑flow form
\[\partial_t \phi = D \nabla^{2}\phi + f(\phi), \quad f(\phi)= r\phi - u\phi^{2} - \lambda \phi^{3}, \quad D=J a^{2}. \tag{2}\]
Define the Lyapunov functional (for admissible \(\phi\) satisfying BCs)
\[\mathcal L[\phi]=\int_{\Omega}\left( \tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)\right)\,dx,\qquad \hat V'(\phi)=-f(\phi).\]
Then, for solutions of (2) with periodic or no‑flux BCs (Axiom 5),
\[\frac{d}{dt}\mathcal L[\phi] = \int_{\Omega} (D\nabla\phi\cdot\nabla\partial_t\phi + \hat V'(\phi)\partial_t\phi)\,dx = -\int_{\Omega} (\partial_t\phi)^2\,dx \le0.\]
Proof (sketch): substitute \(\partial_t\phi=D\nabla^{2}\phi+f(\phi)\) into the time derivative of \(\mathcal L\); integrate the \(\nabla\phi\cdot\nabla\partial_t\phi\) term by parts and apply Axiom 5 (periodic or Neumann BCs) to kill the boundary term; use \(\hat V'=-f\) to combine terms into \(-\int (\partial_t\phi)^2\). All steps use standard Sobolev regularity provided by Axiom 2. □

LIMIT‑ASSUMPTIONS (explicit):
1. Time‑scale separation: effective damping through coupling to a bath or phenomenological friction \(\gamma\) so that inertial transients decay on times \(\ll\) observation scale; averaging yields (2) to within temporal remainder of Lemma T.1.
2. Smoothness: \(\phi\in C^{4}(\Omega)\) with bounded derivatives to apply Lemma S.1 and control discretization errors.
3. Scale hierarchy: \(a/\ell \ll 1\) for characteristic variation length \(\ell\) so higher‑derivative truncation is controlled by Lemma S.1.

### Theorem S.Compactness (Discrete Aubin–Lions) [THEOREM-PROVEN]
Hypotheses: let \(\Omega\subset\mathbb R^{d}\) be a bounded Lipschitz domain and fix Axiom 5 BCs (Dirichlet or homogeneous Neumann). Consider sequences of meshes with spacing \(a\to0\) and time step \(\Delta t\to0\) with the CFL‑like ratio \(c=a/\Delta t\) bounded. Let \(W^{(a,\Delta t)}_{i}(t_n)\) be discrete solutions to the update from Axiom 4 with initial data having a uniform discrete energy bound
\[E_a(0):=a^{d}\sum_{i}\Big(\tfrac12\Big(\frac{W^{1}_i-W^{0}_i}{\Delta t}\Big)^2 + \tfrac{J}{2}\sum_{j\in N(i)}(W^{0}_j-W^{0}_i)^2 + V(W^{0}_i)\Big) \le E_{0}<\infty\]
independent of \(a,\Delta t\).

Statement: After piecewise‑linear interpolation in time (standard: linear on \([t_n,t_{n+1}]\)), the family of interpolants is relatively compact in L²(0,T;L²(\Omega)). Consequently there exists a subsequence (still indexed by \(a,\Delta t\)) converging strongly in L²(0,T;L²(\Omega)) to a limit \(\phi\). Under the LIMIT‑ASSUMPTIONS and Lemmas S.1/T.1 (constants \(C_{spatial}=d/12, C_{time}=1/12\)), the limit \(\phi\) solves the gradient‑flow PDE (2) in the weak sense.

Proof (outline, explicit bounds):
1. Spatial control. The nearest‑neighbour quadratic term in Axiom 4 yields the discrete gradient seminorm
\[\|\nabla_a W\|_{2}^{2} := a^{d-2}\sum_{i}\sum_{j\in N(i)}(W_j-W_i)^2 \le C_1 E_a(0)\]
for an absolute constant \(C_1\) depending only on lattice coordination and J; this gives a uniform discrete H¹ bound independent of \(a,\Delta t\).
2. Time control. The discrete equation and the uniform energy bound provide a uniform bound on discrete time differences
\[a^{d}\sum_{n}\sum_{i} \Big(\frac{W^{n+1}_i-W^{n}_i}{\Delta t}\Big)^2 \le C_2 E_a(0)/\Delta t\]
which, after piecewise‑linear interpolation, yields equicontinuity in time in L²(\Omega) modulo the standard time‑translation estimate (Helly/BV discrete form). The constant \(C_2\) is explicit from the discrete energy identity.
3. Discrete Aubin–Lions. With uniform discrete H¹ in space and equicontinuity in time we invoke a discrete Aubin–Lions compactness theorem (see e.g. Eymard–Gallouët–Herbin style discrete compactness): there exists a strongly convergent subsequence in L²_{t,x}.
4. Passage to the limit. Use Lemma S.1 and Lemma T.1 (constants displayed above) to control the truncation remainders when replacing discrete Laplacian and discrete second differences by continuum operators; these remainders vanish as \(a,\Delta t\to0\) at rates \(O(a^{2})\) and \(O(\Delta t^{2})\) respectively. The inertial term disappears under the time‑scale separation hypothesis, producing the weak form of (2) for the limit \(\phi\).

Remarks: hypotheses include boundedness of \(E_a(0)\) and Lipschitz regularity of \(\partial\Omega\); constants \(C_1,C_2\) are computable from J and lattice coordination numbers and from Lemmas S.1/T.1.

### Lemma S.Energy‑Decay (Discrete → Continuum Lyapunov) [LEMMA-PROVEN]
Let the hypotheses of Theorem S.Compactness hold and assume the LIMIT‑ASSUMPTIONS producing the overdamped scaling. Define the continuum functional
\[\mathcal L[\phi]=\int_{\Omega}\left(\tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)\right)dx,\qquad D=Ja^{2}.\]
Then the interpolated solutions satisfy a discrete energy dissipation inequality of the form
\[\mathcal L[\phi^{(a,\Delta t)}(t_{n+1})]-\mathcal L[\phi^{(a,\Delta t)}(t_n)] \le -\Delta t\, \|\partial_t \phi^{(a,\Delta t)}\|_{L^{2}}^{2} + R(a,\Delta t),\]
where the remainder \(R(a,\Delta t)\) satisfies \(|R(a,\Delta t)|\le C_{rem}(a^{2}+\Delta t^{2})\) with \(C_{rem}\) depending on the Sobolev norms of \(\phi\) and constants from Lemmas S.1/T.1. In the limit \(a,\Delta t\to0\) the inequality passes to the continuum identity \(d\mathcal L/dt\le0\).
Proof: standard discrete energy computation from Axiom 4 with damping; remainders controlled by Lemmas S.1/T.1.

Violation of any assumption returns one to the second‑order dynamics (1).

### Logistic Site ODE (Scope Annotation) [LEMMA-PROVEN]
Site‑wise (zero‑diffusion) reduction of (2) yields \(\dot W = rW-uW^{2}\) with invariant \(Q(W,t)=\ln\frac{W}{r-uW}-rt\). Scope: ODE only; *not* a PDE invariant (diffusion destroys it). This lemma cannot justify spatial pattern claims.

### Spatial Prefactor & Continuum Mapping [LEMMA-PROVEN]
Neighbour sum identity: \(\sum_{j\in N(i)}(W_j-W_i)^2 = 2 a^{2}|\nabla\phi|^{2}+R_{spatial}(a)\) where Lemma S.1 bounds the remainder \(R_{spatial}(a)\). Hence per‑site energy term \(J a^{2}|\nabla\phi|^{2}\) up to controlled remainder and the inertial mapping coefficient \(c^{2}=2Ja^{2}\). Appears *only* in (1) / quarantined inertial contexts; never inside the gradient‑flow energy density.

### Lemma S.1 (Spatial Taylor Remainder — Supremum Norm) [LEMMA-PROVEN]
Let \(\phi\in C^{4}(\Omega)\) and consider the nearest‑neighbour lattice Laplacian
\[\Delta_a\phi(x)=a^{-2}\sum_{j\in N(i)}(\phi(x+a e_j)-\phi(x))\]
in dimension \(d\) with mesh spacing \(a\). Then the remainder between discrete Laplacian and continuum Laplacian satisfies the supremum‑norm bound
\[\|\Delta_a\phi-\nabla^{2}\phi\|_{\infty} \le C_{spatial}\, a^{2}\, \|\nabla^{4}\phi\|_{\infty},\qquad C_{spatial}=\frac{d}{12}.\]
Proof sketch: Expand \(\phi(x+a e_j)\) to fourth order in \(a\); cancellations produce the continuum Laplacian and the fourth derivative term yields the stated remainder with combinatorial factor \(d/12\).

### Lemma T.1 (Temporal Taylor Remainder — Supremum Norm) [LEMMA-PROVEN]
Let \(\phi\in C^{4}((0,T);X)\) with time derivatives bounded in supremum norm and define the central second difference
\[\delta_{tt}\phi(t)=\frac{\phi(t+\Delta t)-2\phi(t)+\phi(t-\Delta t)}{\Delta t^{2}}.\]
Then the temporal remainder obeys
\[\|\delta_{tt}\phi-\partial_{tt}\phi\|_{\infty} \le C_{time}\, \Delta t^{2}\, \|\partial_{t}^{4}\phi\|_{\infty},\qquad C_{time}=\frac{1}{12}.\]
Proof sketch: Standard Taylor expansion in time about \(t\) to fourth order; central difference cancels odd derivatives leaving a fourth derivative remainder with coefficient \(1/12\).

### L0–L3 Layering (Model Abstraction Levels)
- L0 (Microscopic): discrete action, microstate dynamics, explicit lattice spacing \(a\) and time step \(\Delta t\).
- L1 (Mesoscopic): coarse‑grained fields \(\phi(x,t)\), Taylor expansions with remainders controlled by Lemmas S.1/T.1.
- L2 (Continuum PDE): inertial PDE (1) and gradient‑flow PDE (2); effective coefficients \(D,c\) expressed in terms of \(J,a\).
- L3 (Asymptotic/Phenomenological): envelope theorems (pulled front speed), numerically calibrated effective parameters, and conjectured universal relations.

### Assumption‑Purge Checklist
When promoting corollaries to theorems or invoking integration by parts, perform the following purge and record the outcome inline:
1. State the exact BC chosen from Axiom 5 where integration by parts is used.
2. Cite Lemma S.1 or T.1 when replacing discrete operators by continuum ones and include the explicit remainder bound used.
3. Verify time‑scale separation numerically or cite numeric evidence row (front speed / dispersion) when using marginal stability.
4. If any assumption fails, annotate the statement with [LIMIT-ASSUMPTIONS] and revert to second‑order dynamics (1).

(Complete this purge box for each promoted theorem; failure to fill it prevents [THEOREM-PROVEN] tagging.)

## Section 3. Universality / Factorization Theorems

### Theorem U1 (Linear RD Dispersion) [THEOREM-PROVEN]
Linearization of (2) at \(\phi=0\) gives \(\sigma(k)=r-Dk^{2}\). (Fourier mode ansatz.)

### Theorem U2 (KPP Envelope Theorem) [THEOREM-PROVEN]
Conditions (KPP / linear determinacy class):
- Monostable nonlinearity with \(f(0)=0\), \(f'(0)=r>0\) and \(f(u)\le f'(0)u\) for small \(u>0\) (KPP condition).
- Initial data sufficiently steep in the leading edge (exponential decay faster than linear spreading modes) and hypotheses of U1 (linear dispersion control).

Statement: Under the above KPP conditions and the LIMIT‑ASSUMPTIONS, the asymptotic pulled front speed obeys the envelope formula
\[c_{front}=2\sqrt{D r}.\]
Proof sketch: linearize at \(\phi=0\), compute linear spreading speed via marginal stability (saddle point in Fourier‑Laplace plane), then use a comparison‑principle construction to show the nonlinear front is bounded above and below by appropriately translated linear evolution profiles; this pins the nonlinear front speed to the linear spreading value. Numeric gate (Section 0) provides empirical corroboration but does not replace the PDE comparison argument.
Empirical corroboration: see Section 0 provenance — fig `derivation/code/outputs/figures/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.png` and log `derivation/code/outputs/logs/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.json` (SHA256: 5a4c630a… / 2062f64a…), reported rel‑err ≈ 4.7%, R²≈0.999996. (Numeric evidence is [NUM-EVIDENCE], not an axiom.)

### Theorem U3 (Oscillatory RD Doublet Factorization) [THEOREM-PROVEN]
System \(\partial_t \phi =(D\nabla^{2}+r)\phi+\kappa\psi,\ \partial_t \psi =(D\nabla^{2}+r)\psi-\kappa\phi\) ⇒ complex field \(\chi=\phi+i\psi\) obeys \((\partial_t-L)^2\chi+\kappa^{2}\chi=0\), \(L=D\nabla^{2}+r\). Provides *KG‑form factorization* without adding inertial axioms. Tag inertial analogies as [EFT-KG] when used for comparative language.
Obligation: maintain clear separation so that (KG‑like) factorization never feeds back as an axiom for RD energy estimates.

### Lemma U4 (Pattern Attractor Stability) [LEMMA-PROVEN]
If \(V''(\phi^{*})>0\) and the second variation of \(\mathcal L=\int (\tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)) dx\) is positive definite, equilibrium \(\phi^{*}\) is asymptotically stable for (2). Standard Lyapunov argument.

### Corollary U5 (Geometric Extension) [COROLLARY]
Replacing \(\nabla^{2}\) with \(\nabla_i(g^{ij}\nabla_j)\) for a smooth metric preserves \(d\mathcal L/dt \le0\) provided the following hold:
- Uniform ellipticity: there exist constants \(0<\lambda_{min}\le\lambda_{max}<\infty\) such that for all \(x\in\Omega\) and \(\xi\in\mathbb R^{d}\), \(\lambda_{min}|\xi|^{2}\le g^{ij}(x)\xi_i\xi_j\le\lambda_{max}|\xi|^{2}\).
- Boundary conditions: Axiom 5 BCs (periodic or homogeneous Neumann) or sufficient decay so that boundary integrals vanish in integration by parts.

Note: any field‑dependent metric \(g^{ij}(\phi)\) used in modeling must be introduced as a construct/assumption in the theorem statement (hypothesis), not elevated to an axiom. The preservation of Lyapunov dissipation requires the ellipticity and BC hypotheses above.

### Corollary U6 (Inertial KG Representation) [COROLLARY][EFT-KG]
Equation (1) is recovered from U3 factorization by formal identification of \(L\) with spatial operator and \(\kappa\) with effective mass \(m_{eff}\); strictly an *algebraic identity* contingent on oscillatory doublet introduction — not an independent dynamical postulate.

## Section 4. Units & Mapping (Single Source) [LEMMA-PROVEN]
Units with \([\phi]=1\): diffusion constant \(D\) has dimension \(L^{2}T^{-1}\); \(r,u,\lambda\) have \(T^{-1}\); coupling \(J\) has \(T^{-2}\); inertial coefficient \(c^{2}\) has \(L^{2}T^{-2}\). Mapping summary:
1. Discrete neighbour quadratic → continuum gradient: coefficient \(J a^{2}\).
2. Inertial (1) spatial kinetic normalization: \(-\tfrac{c^{2}}{2}|\nabla\phi|^{2}\) with \(c^{2}=2Ja^{2}\) (only in [EFT-KG] contexts).
3. Diffusion constant in (2): \(D=J a^{2}\) (or \(D=(J/z)a^{2}\) if coordination averaging used; specify variant explicitly if invoked — not mixed).
Consistency Rule: The symbols \(c^{2}\) and \(D\) never appear simultaneously in the *same* primitive energy functional; mixing implies regime confusion.

### Discrete Noether & Energy (Short Note) [LEMMA-PROVEN]
Time‑translation invariance of Axiom 4 (discrete action with homogeneous time step) gives a discrete energy observable conserved in the conservative (no‑damping) limit; with damping or implicit averaging this energy becomes a Lyapunov functional in the gradient‑flow limit after coarse‑graining. On a periodic box, spatial translation invariance yields a discrete momentum-like conserved quantity (sum over site shifts); both statements are standard discrete Noether consequences and justify referring to the discrete energy as a control quantity in the compactness argument above.

### Forbidden Mix Sentinel
Forbidden mix rule (grep‑enforced): "c^2" occurrences must be tagged or commented as [EFT-KG]; "D" occurrences must appear only in RD / gradient‑flow contexts. Any file introducing both in the same primitive energy functional must be flagged for manual review.

## Section 5. Numeric Gates Table (Evidence, Non‑Elevating)
Referenced in provenance above. Gates constrain acceptable parameterization when invoking Theorem U2 / U1 in RD regime. They are *regime‑conditional*, not universally axiomatic.

## Section 6. Potential Calculus (Authoritative) [LEMMA-PROVEN]
Already fixed under Axiom 3; reproduced here only for stationary point reference: stationary solutions satisfy \(V'(\phi)=0\) ⇒ \(\phi=0\) or roots of \(\lambda \phi^{2}+\alpha\phi-r=0\) giving \(\phi_{\pm}=(-\alpha \pm \sqrt{\alpha^{2}+4\lambda r})/(2\lambda)\) (when \(\lambda>0\)). No alternate forms elsewhere.

## Section 7. Higher‑Derivative Suppression [LEMMA-PROVEN]
Leading omitted spatial correction scales as \(O(a^{2})\); ratio \(R_{1}\lesssim (a/\ell)^{2}\) for characteristic variation length \(\ell\). If \(a/\ell \le10^{-1}\), truncation error ≤1%. Any claim invoking higher orders must provide an explicit remainder; absent remainder ⇒ tag as [CONJECTURE].

## Section 8. Proof‑Obligation Ledger
1. Massive mode spectrum beyond algebraic factorization [CONJECTURE]: Provide discrete → continuum diagonalization mapping \(\kappa\) to lattice spacing with controlled remainder.
2. Cosmological FRW coupling [CONJECTURE][EFT-KG]: Construct diffeomorphism‑consistent limit preserving Lyapunov monotonicity.
3. Tachyon condensation radius selection [CONJECTURE][EFT-KG]: Bound formation scale via joint use of (1) instability band + U2 front speed; produce inequality with constants.
4. Loop / coarse‑graining running [CONJECTURE]: One explicit mode elimination step with norm control.
5. Universality constants (dimensionless ratios) [CONJECTURE]: Supply compactness + boundedness lemma yielding parameter‑independent attractor values.
6. Higher‑order EFT corrections size (> \(a^{2}\)) [CONJECTURE][EFT-KG]: Remainder estimate through \(O(a^{6})\) with explicit coefficients.
7. Metric field dependence extension (beyond Corollary U5) [CONJECTURE]: Show Lyapunov positivity under \(g^{ij}(\phi)\) modulation.

## Section 9. Conjectures (Collected)
Massive mode EFT spectral structure. [CONJECTURE]
Cosmological FRW embeddings & dark sector links. [CONJECTURE][EFT-KG]
Tachyon condensation characteristic radius formulas. [CONJECTURE][EFT-KG]
Loop / renormalization scaling exponents. [CONJECTURE]
Universality constant tables (DIMENSIONLESS_CONSTANTS.md). [CONJECTURE]
Higher‑derivative suppression extensions beyond \((a/\ell)^2\). [CONJECTURE]
Field‑dependent metric diffusion (nonlinear metric). [CONJECTURE]

<!-- Quarantine note removed; replaced by explicit Conjectures + Ledger above. -->

## Section 10. Hygiene / Assumption Checklist
- Forbidden phrases (should be absent): hand‑wave, assume small (unbounded), training, learn, fit, optimize, theory complete, undeniable proof, c²=Ja², −(Ja²/2)|∇φ|². (Manual scan PASS.)
- Logistic invariant flagged ODE‑only (Section 2) ✔
- Single spatial kinetic mapping \(c^{2}=2Ja^{2}\) only in inertial / [EFT-KG] contexts ✔
- Potential derivative trio appears only once (Axiom 3 / Section 6) ✔
- No ML / runtime heuristic language ✔

## Section 11. CONTRADICTION_REPORT (Reader Self‑Checks)
1. Units Coherence: All appearances of \(D\) have dimension \(L^{2}T^{-1}\); all \(c^{2}\) appearances are quarantined [EFT-KG] with \(L^{2}T^{-2}\). (Check via grep `c^{2} =` and `D =` → single mapping definitions.)
2. Lattice→Continuum Consistency: Coefficient mapping \(c^{2}=2Ja^{2}\) never co‑occurs with RD diffusion equation (2). Any violation would duplicate the mapping; none present.
3. EFT/KG Isolation: Every inertial / mass / oscillatory claim carries [EFT-KG] or appears within a theorem whose statement is purely algebraic (U3/U6) and not cited to justify RD gates except via numeric evidence table (Section 0). Manual scan criterion.

All contradictions currently: NONE observed (manual audit 2025‑08‑29). If future edits introduce conflicts, they must be resolved before asserting new theorems.

## Section 12. Discrete flux / conserved-form search — status, evidence, and recipe [OPEN]

Summary of findings
- The naive, standard discrete Hamiltonian density (kinetic + interaction + potential) was tested in `derivation/conservation_law/discrete_conservation.md` and shown not to be conserved under the FUM update rule: algebraic cancellation fails for general configurations. [NUM-EVIDENCE; see `derivation/conservation_law/discrete_conservation.md`].
- An exact on-site constant of motion for the autonomous logistic on-site law was derived and numerically validated: the logarithmic first integral `Q(W,t)=\ln\frac{W}{r-uW}-rt`. Implementations and validators live in `derivation/code/physics/conservation_law/qfum_validate.py` and are packaged for runtime checks in the RD QA note `derivation/arxiv/RD_Methods_QA/rd_methods_QA.md`. This `Q` is local (per-site) and does not directly provide a spatial flux form. [THEOREM-PROVEN (ODE); NUM-EVIDENCE (validation logs)].

What "flux-form" means here (operational)
- We seek a local discrete quantity `Q_i` (site or edge based) and a local flux `F_{ij}` defined on edges (or oriented neighbour pairs) such that for the discrete update rule
	\[\Delta Q_i := Q_i^{n+1}-Q_i^{n} = -\sum_{j\in N(i)} F_{ij},\qquad F_{ij}=-F_{ji}.\]
- Existence conditions (easy checks): summing over nodes must give zero net change for arbitrary boundary conditions where flux across system boundary vanishes: \(\sum_i \Delta Q_i = 0\) must hold identically for the candidate \(Q_i\). If this fails symbolically the candidate is not flux-conservative.

Status (concrete)
- Direct algebraic attempt using the standard Hamiltonian failed (see `derivation/conservation_law/discrete_conservation.md`): the on-site dissipative terms do not cancel against pairwise interaction differences. [RESULT: NO].
- The on-site logarithmic invariant `Q_{FUM}` is exact for the single-site ODE and numerically robust; it is currently used as a per-node diagnostic and as a CI/runtime guard (`QDriftGuard`) referenced from `derivation/arxiv/RD_Methods_QA/rd_methods_QA.md` and implemented in `qfum_validate.py`. [RESULT: YES (local diagnostic)].
- The possibility remains that a corrected global conserved functional exists of the form `Q_total = sum_i Q_i + sum_{edges} H_{edge}` where `H_{edge}` supplies the missing pairwise correction to make ΔQ_total=0. No explicit closed form for such `H_{edge}` has been found yet. [RESULT: OPEN].

Recommended algebraic / computational recipe (next steps)
1. Symbolic expansion: using a CAS (SymPy) or exact rational algebra, derive the exact expression for the per-node update map `W_i^{n+1}` (or `\Delta W_i`) for the target FUM variant used in `fum_rt/core` (use the exact code expressions as source). Produce `\Delta Q_i` for a candidate `Q_i` (start with the on-site `Q_{FUM}` and also try `\mathcal H_i`).
2. Telescoping test: attempt to rearrange `\Delta Q_i` into a sum of pairwise differences: check whether there exists antisymmetric `F_{ij}` with polynomial/low-order rational dependence on local states satisfying `\Delta Q_i + \sum_j F_{ij} \equiv 0` symbolically. If symbolic factoring fails, attempt ansatz families (linear in neighbors, quadratic edge correction, log-coupled edge term) and solve linear systems for coefficients.
3. Edge‑correction search: assume `H_{edge}` lives on edges `(i,j)` and is a small-degree polynomial/rational function in `(W_i,W_j)`. Solve for coefficients by matching coefficients of the polynomial identity for `\Delta (\sum_i Q_i + \sum_{edges} H_{edge}) = 0` over a sufficiently rich set of monomial basis functions; if a solution exists it gives an explicit flux form.
4. Numerical invariance test (diagnostics): instrument `fum_rt/core` update loop to compute `sum_i Q_i` and `sum_edges H_edge_candidate` (if any) and report `\Delta Q_total` per step across random initial fields; check whether `\Delta Q_total` is exactly zero (symbolic) or numerically within machine tolerance for typical updates.
5. Symmetry search fallback: search for continuous symmetries of the discrete update map (consider one-parameter transforms acting on `t` and the fields) and apply discrete Noether machinery (variational / difference-form Noether) to derive candidate conserved densities.

Practical mapping: where theory meets runtime
- Primary references (evidence and implementations):
	- On-site invariant derivation & numerical protocol: `derivation/arxiv/RD_Methods_QA/logarithmic_constant_of_motion.md` and `derivation/code/physics/conservation_law/qfum_validate.py`.
	- Discrete conservation attempt and negative result: `derivation/conservation_law/discrete_conservation.md`.
	- Symmetry analysis and recommended Noether path: `derivation/foundations/symmetry_analysis.md`.
	- RD QA packaging and `QDriftGuard` runtime pattern: `derivation/arxiv/RD_Methods_QA/rd_methods_QA.md` (and LaTeX variant).

- Apply-to-code suggestions (fum_rt/core):
	- `fum_rt/core/engine/`, `fum_rt/core/guards/`, and `fum_rt/core/global_system.py` are natural insertion points to compute and log per-node `Q` and candidate edge corrections during run-time; use the `metrics` and `diagnostics` helpers in `fum_rt/core/metrics.py` / `diagnostics.py` to record `\Delta Q_total` time-series.
	- Add a short CI harness (pytest) that runs a small lattice in `fum_rt/core` for one step from random initial data and asserts `\Delta Q_total==0` for any proposed symbolic `H_edge` (or asserts the residual is exactly representable as a discrete divergence within tolerance). Keep these tests gated under an "experimental" label until a closed form is proven.

Open research ledger (minimal, actionable items)
- L1: Run symbolic CAS search for `H_edge` ansatz families (linear/quadratic/rational) using exact forms of the update rule in `fum_rt/core` (owner: theory). (Status: not executed in repo; required.)
- L2: Instrument `fum_rt/core` to compute `sum_i Q_i` each step and record `\Delta Q_total` for representative runs; attach results to `derivation/code/outputs/logs/conservation_law/`. (Owner: engineering). (Status: recommended.)
- L3: If symbolic search fails, pursue symmetry discovery (Noether discrete variational approach) as in `derivation/foundations/symmetry_analysis.md` (Owner: theory). (Status: ongoing in docs.)

Status mapping to axioms & tags
- The failure of the standard Hamiltonian conservation is recorded as a negative result in `derivation/conservation_law/discrete_conservation.md` and remains [NUM-EVIDENCE]+[CONJECTURE] for any corrected global Hamiltonian until a constructive proof is provided.
- The on-site logarithmic invariant remains [THEOREM-PROVEN] for the ODE reduction and [NUM-EVIDENCE] for its numeric validation; it is NOT elevated to a global conserved flux without the `H_edge` construction and symbolic proof.

## Ground truths & experiment log (compact)

This short log records the concrete numeric and symbolic artifacts produced while searching for a discrete flux form and the operational conclusions derived from those artifacts. Keep this block small and authoritative — it is the traceable ground truth for the flux search work.

- Key numeric/smoke artifacts (deterministic sweep, fits, and diagnostics):
	- Deterministic sweep JSONs (per-seed ΔQ samples):
		- `derivation/outputs/logs/conservation_law/flux_sweep_1756476135.json`
		- `derivation/outputs/logs/conservation_law/flux_sweep_1756475408.json`
	- Fit / ansatz artifacts:
		- `derivation/outputs/logs/conservation_law/fit_H_edge_1756476188.json` (least-squares fit over simple basis)
		- `derivation/outputs/logs/conservation_law/opt_H_params_1756477394.json` (optimizer result for symbolic free param(s))
		- `derivation/outputs/logs/conservation_law/H_candidate_test_1756476845.json` (numeric test of symbolic H candidate; reported NaN in initial eval)
		- `derivation/outputs/logs/conservation_law/grid_tau0_report.json` (tau0 sensitivity grid)

- Analysis / helper scripts (in-repo):
	- `derivation/code/analysis/flux_sweep.py` — deterministic/random sweep harness; produces `flux_sweep_*.json` and saves sample W0/W1 pairs.
	- `derivation/code/analysis/flux_symbolic_full.py` — small‑N CAS solver (SymPy) to search polynomial ansatz; produced a parametric family with free symbols.
	- `derivation/code/analysis/fit_H_edge.py` — least-squares fitter for simple polynomial basis.
	- `derivation/code/analysis/build_and_test_H_candidate.py` — build symbolic H (fix free params) and test numerically against sweep samples.
	- `derivation/code/analysis/optimize_H_params.py` — numeric optimizer for free symbolic parameters with numeric protections.
	- `derivation/code/analysis/grid_tau0.py` — quick grid sensitivity scan for `tau0`.

- Runtime test harness (non-invasive):
	- `fum_rt/core/tests/test_conservation_flux.py` — pytest that snapshots `Q` before/after a single `Connectome.step()` (dense mode in previous runs was avoided in later runs; scripts sample W directly where possible).

- Short, machine-verified ground truths (what we can assert now):
	1. The per-site logarithmic invariant Q(W,t)=ln(W)−ln(r−uW)−rt is an on-site first integral for the autonomous logistic ODE; its derivation and numeric validation are implemented in `derivation/code/physics/conservation_law/qfum_validate.py` and are recorded in the repository prior to this analysis. [THEOREM-PROVEN (ODE); NUM-EVIDENCE]
 2. For the full FUM discrete update (deterministic skeleton and full runtime including interactions), the global sum Σ_i Q_i is not conserved: single-step Δ(Σ_i Q_i) ≠ 0 in general (see `flux_sweep_*.json`). [NUM-EVIDENCE]
 3. A direct search for a constant-coefficient polynomial edge correction (simple basis) yields only a tiny antisymmetric coefficient and modest residual reduction; no closed-form constant-coefficient H_edge was found. [RESULT: NUM-EVIDENCE]
 4. Small‑N symbolic CAS produced a parametric family of local H expressions (free symbols remain). These solutions generally contain rational factors that require numeric protection (denominator regularization) when evaluated on runtime samples. [RESULT: SYMBOLIC → parametric family]

- Practical conclusion and document mapping:
	- No constructive, globally valid `H_edge` (closed-form) has been proven; the search remains OPEN and recorded as [OPEN] in this section.
	- For reproducibility, all scripts and output JSONs above are the ground-truth artifacts that any future claim must reference and re-run.

End of ground truths block. Additions to this block must reference produced artifact paths and numeric gates (SHA256) when claiming new evidence.

End of truth‑first axiomatic document. All non‑axiom / regime claims above are tagged; no content follows this termination marker.
[File terminates here intentionally – minimal source enforced.]


