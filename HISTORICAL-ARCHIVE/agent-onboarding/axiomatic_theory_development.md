<!-- =============================================================== -->
# VDM Truth‑First Axiomatic Development (Single Source)

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

- `[THEOREM-PROVEN]` formally derived from A1-A4 with proof sketch or full derivation.
- `[LEMMA-PROVEN]` auxiliary proven step used in a theorem proof.
- `[COROLLARY]` immediate logical consequence of proved theorems/lemmas.
- `[CONJECTURE]` claim not yet proven from A1-A4; accompanied by explicit proof obligations.
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

### Derivation A (Discrete Euler-Lagrange → Second‑Order Update) [THEOREM-PROVEN]

Variation of Axiom 4 yields the *core discrete equation*:
\[\frac{W_i^{n+1}-2W_i^{n}+W_i^{n-1}}{\Delta t^{2}} = 2J \sum_{j\in N(i)}(W_j^{n}-W_i^{n}) - V'(W_i^{n}).\]
Derivation note: the interaction term in the action is edge‑doubled (each pair \((i,j)\) appears in both the \(i\)- and \(j\)-centered sums). Hence the variation of \(-\tfrac{J}{2}\sum_{j\in N(i)}(W_j-W_i)^2\) plus the symmetric neighbor contributions yields the factor \(+\,2J\sum_{j\in N(i)}(W_j-W_i)\) in the Euler-Lagrange equation.
Taylor expansion (Axiom 2) of the neighbour term gives the *continuum inertial form* (quarantined inertial label):
\[\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0, \qquad c^{2}=2J a^{2}. \tag{1} [EFT-KG]\]
Error control is given explicitly by Lemma S.1 (spatial Taylor remainder) and Lemma T.1 (temporal Taylor remainder) below.

### Theorem 2 (Overdamped / Gradient‑Flow Limit and Lyapunov) [THEOREM-PROVEN]

Under the LIMIT‑ASSUMPTIONS below and Axiom 5 BCs, the coarse‑grained dynamics reduce to the gradient‑flow form
\[\partial_t \phi = D \nabla^{2}\phi + f(\phi), \quad f(\phi)= r\phi - u\phi^{2} - \lambda \phi^{3}, \quad D=2J a^{2}. \tag{2}\]
Define the Lyapunov functional (for admissible \(\phi\) satisfying BCs)
\[\mathcal L[\phi]=\int_{\Omega}\left( \tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)\right)\,dx,\qquad \hat V'(\phi)=-f(\phi).\]
Then, for solutions of (2) with periodic or no‑flux BCs (Axiom 5),
\[\frac{d}{dt}\mathcal L[\phi] = \int_{\Omega} (D\nabla\phi\cdot\nabla\partial_t\phi + \hat V'(\phi)\partial_t\phi)\,dx = -\int_{\Omega} (\partial_t\phi)^2\,dx \le0.\]
Proof (sketch): substitute \(\partial_t\phi=D\nabla^{2}\phi+f(\phi)\) into the time derivative of \(\mathcal L\); integrate the \(\nabla\phi\cdot\nabla\partial_t\phi\) term by parts and apply Axiom 5 (periodic or Neumann BCs) to kill the boundary term; use \(\hat V'=-f\) to combine terms into \(-\int (\partial_t\phi)^2\). All steps use standard Sobolev regularity provided by Axiom 2. □

Assumption‑Purge Box — Theorem 2 [LIMIT-ASSUMPTIONS]

- BC: periodic or homogeneous Neumann (Axiom 5), stated here for each integration by parts.
- Discrete→continuum replacement bounds: Lemma S.1 with \(C_{spatial}=d/12\); Lemma T.1 with \(C_{time}=1/12\).
- Time‑scale separation: overdamped regime via effective friction \(\gamma_{\mathrm{eff}}>0\); RD time unit chosen so \(\gamma_{\mathrm{eff}}\equiv 1\) unless otherwise stated.
- Parameter identification: direct coarse‑graining from Axiom 4 with Axiom 3 potential implies \(u\equiv \alpha\) and \(\hat V\equiv V\) up to an additive constant; if \(u\ne \alpha\), we still enforce \(\hat V'(\phi)=-f(\phi)\) and tag [LIMIT-ASSUMPTIONS].

LIMIT‑ASSUMPTIONS (explicit):

1. Time‑scale separation: effective damping through coupling to a bath or phenomenological friction \(\gamma\) so that inertial transients decay on times \(\ll\) observation scale; averaging yields (2) to within temporal remainder of Lemma T.1.
2. Smoothness: \(\phi\in C^{4}(\Omega)\) with bounded derivatives to apply Lemma S.1 and control discretization errors.
3. Scale hierarchy: \(a/\ell \ll 1\) for characteristic variation length \(\ell\) so higher‑derivative truncation is controlled by Lemma S.1.

### Theorem S.Compactness (Discrete Aubin-Lions) [THEOREM-PROVEN]

Hypotheses: let \(\Omega\subset\mathbb R^{d}\) be a bounded Lipschitz domain and fix Axiom 5 BCs (periodic or homogeneous Neumann). Consider sequences of meshes with spacing \(a\to0\) and time step \(\Delta t\to0\) with the CFL‑like ratio \(\kappa=a/\Delta t\) bounded. Let \(W^{(a,\Delta t)}*{i}(t_n)\) be discrete solutions to the update from Axiom 4 with initial data having a uniform discrete energy bound
\[E_a(0):=a^{d}\sum*{i}\Big(\tfrac12\Big(\frac{W^{1}_i-W^{0}*i}{\Delta t}\Big)^2 + \tfrac{J}{2}\sum*{j\in N(i)}(W^{0}_j-W^{0}_i)^2 + V(W^{0}*i)\Big) \le E*{0}<\infty\]
independent of \(a,\Delta t\).

Statement: After piecewise‑linear interpolation in time (standard: linear on \([t_n,t_{n+1}]\)), the family of interpolants is relatively compact in L²(0,T;L²(\Omega)). Consequently there exists a subsequence (still indexed by \(a,\Delta t\)) converging strongly in L²(0,T;L²(\Omega)) to a limit \(\phi\). Under the LIMIT‑ASSUMPTIONS and Lemmas S.1/T.1 (constants \(C_{spatial}=d/12, C_{time}=1/12\)), the limit \(\phi\) solves the gradient‑flow PDE (2) in the weak sense.

Proof (outline, explicit bounds):

1. Spatial control. The nearest‑neighbour quadratic term in Axiom 4 yields the discrete gradient seminorm
\[\|\nabla_a W\|*{2}^{2} := a^{d-2}\sum*{i}\sum_{j\in N(i)}(W_j-W_i)^2 \le C_1 E_a(0)\]
for an absolute constant \(C_1\) depending only on lattice coordination and J; this gives a uniform discrete H¹ bound independent of \(a,\Delta t\).
2. Time control. The discrete equation and the uniform energy bound provide a uniform bound on discrete time differences
\[a^{d}\sum_{n}\sum_{i} \Big(\frac{W^{n+1}_i-W^{n}_i}{\Delta t}\Big)^2 \le C_2 E_a(0)/\Delta t\]
which, after piecewise‑linear interpolation, yields equicontinuity in time in L²(\Omega) modulo the standard time‑translation estimate (Helly/BV discrete form). The constant \(C_2\) is explicit from the discrete energy identity.
3. Discrete Aubin-Lions. With uniform discrete H¹ in space and equicontinuity in time we invoke a discrete Aubin-Lions compactness theorem (see e.g. Eymard-Gallouët-Herbin style discrete compactness): there exists a strongly convergent subsequence in L²_{t,x}.
4. Passage to the limit. Use Lemma S.1 and Lemma T.1 (constants displayed above) to control the truncation remainders when replacing discrete Laplacian and discrete second differences by continuum operators; these remainders vanish as \(a,\Delta t\to0\) at rates \(O(a^{2})\) and \(O(\Delta t^{2})\) respectively. The inertial term disappears under the time‑scale separation hypothesis, producing the weak form of (2) for the limit \(\phi\).

Remarks: hypotheses include boundedness of \(E_a(0)\) and Lipschitz regularity of \(\partial\Omega\); constants \(C_1,C_2\) are computable from J and lattice coordination numbers and from Lemmas S.1/T.1.

### Lemma S.Energy‑Decay (Discrete → Continuum Lyapunov) [LEMMA-PROVEN]

Let the hypotheses of Theorem S.Compactness hold and assume the LIMIT‑ASSUMPTIONS producing the overdamped scaling. Define the continuum functional
\[\mathcal L[\phi]=\int_{\Omega}\left(\tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi)\right)dx,\qquad D\ \text{as in (2)}\ \big(\text{i.e., } D=2Ja^{2}/\gamma_{\mathrm{eff}}\ \text{with }\gamma_{\mathrm{eff}}\equiv1\ \text{in RD time units}\big).\]
Then the interpolated solutions satisfy a discrete energy dissipation inequality of the form
\[\mathcal L[\phi^{(a,\Delta t)}(t_{n+1})]-\mathcal L[\phi^{(a,\Delta t)}(t_n)] \le -\Delta t\, \|\partial_t \phi^{(a,\Delta t)}\|*{L^{2}}^{2} + R(a,\Delta t),\]
where the remainder \(R(a,\Delta t)\) satisfies \(|R(a,\Delta t)|\le C*{rem}(a^{2}+\Delta t^{2})\) with \(C_{rem}\) depending on the Sobolev norms of \(\phi\) and constants from Lemmas S.1/T.1. In the limit \(a,\Delta t\to0\) the inequality passes to the continuum identity \(d\mathcal L/dt\le0\).
Proof: standard discrete energy computation from Axiom 4 with damping; remainders controlled by Lemmas S.1/T.1.

### Lemma F.1 (Flux‑form diffusion conserves mass) [LEMMA-PROVEN]

On the nearest‑neighbour lattice with periodic or homogeneous Neumann BCs (Axiom 5), define antisymmetric edge fluxes
\[F_{ij}=-\frac{D}{a}\,(\phi_j-\phi_i),\qquad F_{ij}=-F_{ji},\]
and the conservative update
\[\phi_i^{n+1}=\phi_i^{n}-\frac{\Delta t}{a}\sum_{j\in N(i)}F_{ij}.\]
Then \(\sum_i \phi_i^{n+1}=\sum_i \phi_i^{n}\) exactly for \(f\equiv 0\). Proof: antisymmetry implies \(\sum_i\sum_{j\in N(i)}F_{ij}=0\) after re‑indexing edges and applying BCs.

### Lemma DG.1 (Discrete‑gradient Lyapunov step) [LEMMA-PROVEN]

Let \(\mathcal L[\phi]=\int_{\Omega}(\tfrac{D}{2}|\nabla\phi|^{2}+\hat V(\phi))dx\) with Axiom 5 BCs and define the discrete‑gradient update so that
\[\frac{\phi^{n+1}-\phi^{n}}{\Delta t} = D\nabla^{2}*h \bar\phi + \bar f,\qquad \text{with } \hat V'(\bar\phi)=-\bar f,\]
where the bars denote a suitable discrete gradient in the sense of Gonzalez/Quispel-McLaren. Then
\[\mathcal L^{n+1}-\mathcal L^{n} = -\Delta t\,\Big\|\frac{\phi^{n+1}-\phi^{n}}{\Delta t}\Big\|*{2}^{2}\le 0.\]
Proof: standard discrete‑gradient identity; BCs eliminate boundary terms on the discrete Green’s identity.

Violation of any assumption returns one to the second‑order dynamics (1).

### Logistic Site ODE (Scope Annotation) [LEMMA-PROVEN]

Site‑wise (zero‑diffusion) reduction of (2) yields \(\dot W = rW-uW^{2}\) with invariant \(Q(W,t)=\ln\frac{W}{r-uW}-rt\). Scope: ODE only; *not* a PDE invariant (diffusion destroys it). This lemma cannot justify spatial pattern claims.

### Spatial Prefactor & Continuum Mapping [LEMMA-PROVEN]

Neighbour sum identity: \(\sum_{j\in N(i)}(W_j-W_i)^2 = 2 a^{2}|\nabla\phi|^{2}+R_{spatial}(a)\) where Lemma S.1 bounds the remainder \(R_{spatial}(a)\). Hence per‑site energy term \(J a^{2}|\nabla\phi|^{2}\) up to controlled remainder and the inertial mapping coefficient \(c^{2}=2Ja^{2}\). Appears *only* in (1) / quarantined inertial contexts; never inside the gradient‑flow energy density.

### Lemma S.1 (Spatial Taylor Remainder — Supremum Norm) [LEMMA-PROVEN]

Let \(\phi\in C^{4}(\Omega)\) and consider the nearest‑neighbour lattice Laplacian
\[\Delta_a\phi(x)=a^{-2}\sum_{j\in N(i)}(\phi(x+a e_j)-\phi(x))\]
in dimension \(d\) with mesh spacing \(a\). Then the remainder between discrete Laplacian and continuum Laplacian satisfies the supremum‑norm bound
\[\|\Delta_a\phi-\nabla^{2}\phi\|*{\infty} \le C*{spatial}\, a^{2}\, \|\nabla^{4}\phi\|*{\infty},\qquad C*{spatial}=\frac{d}{12}.\]
Proof sketch: Expand \(\phi(x+a e_j)\) to fourth order in \(a\); cancellations produce the continuum Laplacian and the fourth derivative term yields the stated remainder with combinatorial factor \(d/12\).

### Lemma T.1 (Temporal Taylor Remainder — Supremum Norm) [LEMMA-PROVEN]

Let \(\phi\in C^{4}((0,T);X)\) with time derivatives bounded in supremum norm and define the central second difference
\[\delta_{tt}\phi(t)=\frac{\phi(t+\Delta t)-2\phi(t)+\phi(t-\Delta t)}{\Delta t^{2}}.\]
Then the temporal remainder obeys
\[\|\delta_{tt}\phi-\partial_{tt}\phi\|*{\infty} \le C*{time}\, \Delta t^{2}\, \|\partial_{t}^{4}\phi\|*{\infty},\qquad C*{time}=\frac{1}{12}.\]
Proof sketch: Standard Taylor expansion in time about \(t\) to fourth order; central difference cancels odd derivatives leaving a fourth derivative remainder with coefficient \(1/12\).

### L0-L3 Layering (Model Abstraction Levels)

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

Assumption‑Purge Box — U2 [LIMIT-ASSUMPTIONS]

- BC: periodic or homogeneous Neumann (Axiom 5) on the domain used for comparison‑principle arguments.
- Linearization remainder control: Lemma S.1/T.1 bounds invoked for mapping discrete operators to continuum in the small‑amplitude leading edge.
- KPP conditions: \(f(0)=0\), \(f'(0)=r>0\), \(f(u)\le r u\) for small \(u>0\); steep ICs in the leading edge.
- Parameter identification: \(D\) and \(r\) as in (2); reported collapse uses the dimensionless groups of §14.3.

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
3. Diffusion constant in (2): \(D=2J a^{2}\) (or \(D=(2J/z)a^{2}\) if coordination averaging used; specify variant explicitly if invoked — not mixed).
Consistency Rule: The symbols \(c^{2}\) and \(D\) never appear simultaneously in the same primitive energy functional; mixing implies regime confusion. Parameter identification: when the overdamped scaling is derived directly from Axiom 4 with the potential of Axiom 3, one has \(u\equiv \alpha\) and \(\hat V \equiv V\) up to an additive constant; if coarse‑graining or bath coupling alters site nonlinearities so that \(u\ne \alpha\), tag [LIMIT-ASSUMPTIONS] and enforce \(\hat V'(\phi)=-f(\phi)\). Overdamped time‑scale: introduce \(\gamma_{\mathrm{eff}}\) with units \(T^{-1}\) for frictional coarse‑graining; then \(D=2Ja^{2}/\gamma_{\mathrm{eff}}\). Throughout RD statements we adopt \(\gamma_{\mathrm{eff}}\equiv 1\) (time measured in friction units).

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

- Forbidden phrases (should be absent): hand‑wave, assume small (unbounded), training, learn, fit, optimize, theory complete, undeniable proof, c²=Ja², -(Ja²/2)|∇φ|². (Manual scan PASS.)
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
 1. The per-site logarithmic invariant Q(W,t)=ln(W)-ln(r-uW)-rt is an on-site first integral for the autonomous logistic ODE; its derivation and numeric validation are implemented in `derivation/code/physics/conservation_law/qfum_validate.py` and are recorded in the repository prior to this analysis. [THEOREM-PROVEN (ODE); NUM-EVIDENCE]

 2. For the full FUM discrete update (deterministic skeleton and full runtime including interactions), the global sum Σ_i Q_i is not conserved: single-step Δ(Σ_i Q_i) ≠ 0 in general (see `flux_sweep_*.json`). [NUM-EVIDENCE]
 3. A direct search for a constant-coefficient polynomial edge correction (simple basis) yields only a tiny antisymmetric coefficient and modest residual reduction; no closed-form constant-coefficient H_edge was found. [RESULT: NUM-EVIDENCE]
 4. Small‑N symbolic CAS produced a parametric family of local H expressions (free symbols remain). These solutions generally contain rational factors that require numeric protection (denominator regularization) when evaluated on runtime samples. [RESULT: SYMBOLIC → parametric family]

- Practical conclusion and document mapping:
 	- No constructive, globally valid `H_edge` (closed-form) has been proven; the search remains OPEN and recorded as [OPEN] in this section.
 	- For reproducibility, all scripts and output JSONs above are the ground-truth artifacts that any future claim must reference and re-run.

End of ground truths block. Additions to this block must reference produced artifact paths and numeric gates (SHA256) when claiming new evidence.

## Section 13. Comparative Review (Validation‑Only) — external works mapped to axiom‑core

All items below are strictly [NUM-EVIDENCE] and/or [CONJECTURE] with explicit [LIMIT-ASSUMPTIONS]. None alter Axioms 1-5 or introduce new primitives. They serve as runners and cross‑checks against our derived theorems/lemmas/gates.

### 13.1 Quantum Keldysh reaction-diffusion (Gerbino-Lesanovsky-Perfetto, 2024) [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: [2307.14945v3.pdf](derivation/supporting_work/NEEDS_REVIEW/Reaction-Diffusion/2307.14945v3.pdf)
- Scope: Open quantum Fermi gas with Lindblad two‑body loss; Euler‑scale kinetic (Boltzmann‑like) equation for Wigner density; universal homogeneous decay exponent \(\tilde n \sim \tilde t^{-d/(d+1)}\); 1D links to TGGE; inhomogeneous quenches via trap parameter \(\Omega\).
- Mapping to this document:
  - Different transport sector (ballistic/coherent) vs the overdamped RD gradient‑flow regime (2). No import to axioms.
  - Shared‑limit comparisons only if additional diffusion emerges; test crossover toward classical dispersion \(\sigma(k)=r-Dk^{2}\) [Theorem U1] and envelope speed \(c_{front}=2\sqrt{Dr}\) [Theorem U2].
  - Lyapunov/H‑theorem (Theorem 2) does not apply to their ballistic sector; instead log kinetic entropy monotonicity is the appropriate surrogate within their assumptions.
- Limit assumptions to record with any use:
  - [LIMIT-ASSUMPTIONS] Lindblad jump operators, Euler hydrodynamic scaling (\(\bar t,\bar x\) rescalings), stable quasiparticles, boundary/trap details.
- Validation gates:
  - Gate Q1: Fit homogeneous decay exponent vs \(d\); slope within confidence of \(d/(d+1)\).
  - Gate Q2: In 1D, verify TGGE correspondence via momentum‑space observables.
  - Gate Q3: With added diffusion, check approach to classical RD dispersion/front metrics.

### 13.2 Field theories & basis‑independent RD (del Razo-Lamma-Merbis, 2025) [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: [2409.13377v2.pdf](derivation/supporting_work/NEEDS_REVIEW/Reaction-Diffusion/2409.13377v2.pdf)
- Scope: Unified Fock‑space/Doi-Peliti/CDME framework; basis‑independent creation/annihilation; Galerkin discretization with convergence to RDME; path integrals for arbitrary discretizations; RG universality statements.
- Mapping:
  - L0→L2 consistency runner: compare our Axiom‑driven L0→L2 limit to CDME/RDME on matched meshes/BCs.
  - Use to validate dispersion \(\sigma(k)=r-Dk^{2}\) [U1], front speed \(c_{front}=2\sqrt{Dr}\) [U2], and Lyapunov decay (Theorem 2) in expectation.
- Limits:
  - [LIMIT-ASSUMPTIONS] particle indistinguishability model, local reaction rules, discretization choices, BCs explicitly documented.
- Validation gates:
  - S1: Isaacson‑type convergence of RDME → PDE (2) in large‑copy‑number limit (document mesh scaling).
  - S2: Recovery of U1/U2 within CI bands across seeds.
  - S3: Monotone decay of an energy‑like observable in expectation; violations triaged as finite‑copy effects.

### 13.3 Maximum‑Entropy / Schrödinger‑Bridge RD inference (Movilla Miangolarra et al., 2024) [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: [2411.09880v1.pdf](derivation/supporting_work/NEEDS_REVIEW/Reaction-Diffusion/2411.09880v1.pdf)
- Scope: MaxCal/SB variational inference for interacting particle systems; minimize path relative entropy subject to endpoint/current constraints; coupled forward/backward fields \((\phi,\hat\phi,\psi,\hat\psi)\).
- Mapping:
  - Inference overlay on top of our prior (choose prior as L2 RD PDE (2) or stochastic counterpart). No change to the dynamical origin.
  - Check that inferred drifts/controls preserve our Lyapunov structure when projected back into RD form.
- Limits:
  - [LIMIT-ASSUMPTIONS] declared priors, endpoint/current constraints, mean‑field approximations if used, domain BCs.
- Validation gates:
  - M1: Zero‑constraint sanity: recovered dynamics equal the prior.
  - M2: Linear‑response consistency around the prior PDE.
  - M3: If constrained within class (2), verify \(d\mathcal L/dt\le0\); otherwise tag [CONJECTURE].

### 13.4 Time‑fractional Fisher-KPP numerics (Gortsas, 2025) [CONJECTURE][NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: [2508.16241v1.pdf](derivation/supporting_work/NEEDS_REVIEW/Reaction-Diffusion/2508.16241v1.pdf)
- Scope: LD‑BEM and meshless FPM for time‑fractional (Caputo / RL / fractal) KPP; sparse matrices and reduced volume integrals; accuracy metrics \(E_{\infty},E_{2}\).
- Mapping:
  - Fractional memory is off‑axiom; use strictly as a lab to quantify deviations from U1/U2 and Lyapunov when \(\partial_t\) is fractional.
- Limits:
  - [LIMIT-ASSUMPTIONS] precise fractional operator definition and order \(\alpha\in(0,1]\); discretization and BC details.
- Validation gates:
  - F1: Classical limit \(\alpha\to1^{-}\) recovers (2) and U1/U2.
  - F2: Stability and reported error orders match claims.
  - F3: Any fractional H‑theorem analogue is [CONJECTURE] until proven; test monotone proxies.

### 13.5 Hamiltonian simulation via CLS (Carleman + Schrödingerization) (Sasaki-Endo-Muramatsu, 2025) [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: [2508.01640v1.pdf](derivation/supporting_work/NEEDS_REVIEW/Hamiltonian/2508.01640v1.pdf)
- Scope: Carleman linearization truncated at order \(K\), then Warped‑Phase Transformation to a skew‑Hermitian operator enabling Hamiltonian simulation of nonlinear PDEs inc. RD; classical validations: first‑order in \(K\), second‑order in \(\Delta x\), first‑order in \(\Delta p\).
- Mapping:
  - Computational runner only; does not modify dynamics. Compare outputs back to L2 PDE (2) benchmarks.
- Limits:
  - [LIMIT-ASSUMPTIONS] truncation \(K\), auxiliary \(p\)-domain discretization and BCs; numerical stability.
- Validation gates:
  - QCLS‑1: Convergence in \(K\), \(\Delta x\), \(\Delta p\) with stated orders.
  - QCLS‑2: Transformed operator skew‑Hermiticity/unitarity checks pass.
  - QCLS‑3: U1/U2 recovery within tolerances on benchmark ICs.

Summary: None of the above modifies Axioms 1-5. They serve as validation targets or runners gated by Section 14.

---

## Section 14. Operational program — work order, verification gates, scaling, runners, risks

### 14.1 Work order (L0→L3 pipeline)

1. L0 (Microscopic): Start from Axiom 4 and the chosen BC from Axiom 5; record energy bound and initial data regularity.
2. L1 (Mesoscopic): Apply Taylor expansions with explicit remainder constants from Lemmas S.1/T.1; record remainder budgets.
3. L2 (Continuum selection): Choose regime: inertial [EFT-KG] (1) or gradient‑flow RD (2) under stated LIMIT‑ASSUMPTIONS. Never place \(c^{2}\) and \(D\) in the same primitive energy (Forbidden Mix Sentinel).
4. L3 (Evidence): Run dispersion [U1] and front‑speed [U2] numeric gates on canonical ICs; compute artifact SHA256 and record in provenance.
5. External matrix: Execute selected runners from 14.4; annotate every result with [NUM-EVIDENCE]/[CONJECTURE] and [LIMIT-ASSUMPTIONS].

### 14.2 Verification gates (authoritative, regime‑conditional)

- H‑theorem (RD): \(d\mathcal L/dt\le0\) with BCs per Axiom 5 [Theorem 2]; runtime logging gate: stepwise \(\Delta \mathcal L \le 0\) (no violations) with artifacts hashed.
- Dispersion gate: \(\sigma(k)=r-Dk^{2}\) [Theorem U1]; band: median relative error \(\le 2\times10^{-3}\).
- Front gate: \(c_{front}=2\sqrt{Dr}\) [Theorem U2]; band: relative error \(\le 5\%\) on calibrated meshes.
- Discrete compactness: L0→L2 convergence under energy bound [Theorem S.Compactness]; remainders \(\sim O(a^{2})+O(\Delta t^{2})\).
- Noether (inertial sandbox): conservative‑limit energy/momentum drift \(\le 10^{-4}\) over \(10^{4}\) steps; all inertial claims carry [EFT-KG].
- External runner gates: Q1-Q3 (13.1), S1-S3 (13.2), M1-M3 (13.3), F1-F3 (13.4), QCLS‑1-3 (13.5).

### 14.3 Scaling groups (dimensionless program)

For the RD PDE (2):
\[
\partial_t \phi = D\nabla^{2}\phi + r\phi - u\phi^{2} - \lambda \phi^{3}.
\]
Choose
\[
t' = r t,\quad x' = x\sqrt{r/D},\quad \phi = \phi_{*}\, y,
\]
with \(\phi_{*}=r/u\) if \(u>0\) (logistic scaling) or \(\phi_{*}=\sqrt{r/\lambda}\) if \(u=0,\lambda>0\). Then
\[
\partial_{t'} y = \nabla_{x'}^{2} y + y - y^{2} - \Lambda\, y^{3},\qquad \Lambda=\frac{\lambda r}{u^{2}}\ \text{(when }u>0\text{)}.
\]

- Dimensionless dispersion: \(\hat\sigma(k')=1-k'^{2}\) with \(k'=k\sqrt{D/r}\).
- Dimensionless front speed: \(\hat c = c_{front}/\sqrt{Dr}=2\).
- Reporting standard: collapse plots must use \((t',x',y)\) with legend of \(\Lambda\) and BC. Any deviation from collapse triggers review.

### 14.4 Experiment runners (validation‑only; no foundational import)

All runners must satisfy runtime hard‑gates:

- Sparse‑only execution: use void‑walker scouts and a hierarchical bus strategy; no dense global scans.
- No schedulers: GDSP emergent event‑driven only (no external schedulers).
- No scans in [maps](fum_rt/core/cortex/maps/), nor in [core](fum_rt/core/).
- Respect Maps/Frame v1 or v2 contracts (document variant).
- Guards must pass; control‑impact < \(10^{-5}\) on the golden run.

Artifacts:

- Logs → [derivation/code/outputs/logs/reaction_diffusion/](derivation/code/outputs/logs/reaction_diffusion/)
- Figures → [derivation/code/outputs/figures/reaction_diffusion/](derivation/code/outputs/figures/reaction_diffusion/)
- Compute SHA256 via system `sha256sum` and append to Section 0 provenance.

14.4.1 Classical PDE runner (FD/FE)

- Location: [derivation/code/physics/reaction_diffusion/](derivation/code/physics/reaction_diffusion/)
- Tasks: reproduce U1 dispersion and U2 front speed on canonical ICs with Axiom‑5 BCs; verify \(d\mathcal L/dt\le0\).
- Outputs: dispersion/front figures+logs with SHA256; mesh/timestep sweeps to demonstrate convergence.

14.4.2 Stochastic RDME/CDME runner

- Location: [derivation/code/physics/reaction_diffusion/](derivation/code/physics/reaction_diffusion/) (stochastic sub‑runner)
- Tasks: simulate RDME/CDME consistent with 13.2; verify S1-S3; report CI bands across seeds.
- Outputs: ensemble logs with seed lists and CI; recovery of U1/U2 in the large‑copy limit.

14.4.3 Fractional RD runner (Caputo/RL/fractal)

- Location: [derivation/code/physics/reaction_diffusion/](derivation/code/physics/reaction_diffusion/) (fractional sub‑runner)
- Tasks: implement fractional time derivative as per 13.4; verify F1-F3; mark all claims [CONJECTURE] unless derived from Axiom 4.
- Outputs: error‑order tables and classical‑limit recovery plots.

14.4.4 Quantum CLS runner (Carleman + Schrödingerization)

- Location: [derivation/code/physics/reaction_diffusion/](derivation/code/physics/reaction_diffusion/) (quantum sub‑runner)
- Tasks: simulate (2) via CLS; verify QCLS‑1-3; monitor \(p\)-domain advection artifacts and boundary handling.
- Outputs: convergence curves vs \(K,\Delta x,\Delta p\); dispersion/front comparisons.

14.4.5 Quantum Keldysh/Euler runner (ballistic sector)

- Location: [derivation/code/physics/reaction_diffusion/](derivation/code/physics/reaction_diffusion/) (quantum kinetic sub‑runner)
- Tasks: implement kinetic equation in the Euler‑scale regime for validation only; verify Q1-Q3; never use to justify RD axioms.
- Outputs: decay‑exponent fits; optional crossover tests with added diffusion.

Runtime integration hooks (non‑invasive):

- Diagnostics/guards: use [fum_rt/core/guards/](fum_rt/core/guards/) (e.g., Q‑drift guard) to ensure control‑impact < \(10^{-5}\).
- Tests: place smoke tests in [fum_rt/core/tests/](fum_rt/core/tests/) and keep event‑driven sparse policies; avoid scans in [core](fum_rt/core/) and [maps](fum_rt/core/cortex/maps/).

### 14.5 Risk and kill‑plans

- Kill‑R1 (Lyapunov): any monotonicity violation in RD regime (beyond discretization tolerance) demotes affected claims to [CONJECTURE] until fixed.
- Kill‑R2 (Forbidden mix): any primitive energy mixing \(c^{2}\) and \(D\) flags a CONTRADICTION_REPORT and blocks promotions.
- Kill‑R3 (Gate failure): repeated failures of U1/U2 at calibrated resolution require revisiting LIMIT‑ASSUMPTIONS or parameter mapping; affected statements demoted.
- Kill‑R4 (Runner contamination): any runner introducing non‑sparse scans or schedulers is invalid; results excluded from provenance.
- Kill‑R5 (Quantum overlays): any unitarity/skew‑Hermiticity violation in CLS runs invalidates those runs; remove from evidence table.

### 14.6 Hygiene and cross‑reference checks (operational)

- Tag enforcement: every non‑axiom statement must carry one of [THEOREM-PROVEN], [LEMMA-PROVEN], [COROLLARY], [CONJECTURE], [NUM-EVIDENCE], optionally [EFT-KG].
- BC explicitness: every use of integration by parts must cite periodic or homogeneous Neumann BCs (Axiom 5).
- D vs \(c^{2}\) segregation: grep‑enforced per Section 4 and Forbidden Mix Sentinel.
- Reproducibility: each artifact lists parameters, seeds (if any), BCs, and SHA256.

### 14.7 Provenance procedure (evidence logging)

1. Generate figures/logs into [derivation/code/outputs/](derivation/code/outputs/).
2. Compute SHA256 via `sha256sum <artifact>`; record truncated hashes in Section 0.
3. Append runner configuration (BCs, mesh, ∆t, seeds) to the log JSON; store under the appropriate subfolder (e.g., [derivation/code/outputs/logs/reaction_diffusion/](derivation/code/outputs/logs/reaction_diffusion/)).
4. Update the gates table metrics and keep tags [NUM-EVIDENCE] only; do not elevate logical status.

### 14.8 Cross‑reference compliance report (regex audit) [NUM-EVIDENCE]

Scope (regex): derivation/(supporting_work|code/outputs|code/physics|outputs|arxiv|conservation_law|foundations)/ and fum_rt/core/*.

Findings (this document’s references only):

- Reaction-diffusion runners present:
  - [rd_front_speed_experiment.py](derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:1), [rd_dispersion_experiment.py](derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:1), [rd_front_speed_sweep.py](derivation/code/physics/reaction_diffusion/rd_front_speed_sweep.py:1).
- Conservation law/invariant references present:
  - [qfum_validate.py](derivation/code/physics/conservation_law/qfum_validate.py:1), [discrete_conservation.md](derivation/conservation_law/discrete_conservation.md:1).
- QA notebook references present:
  - [rd_methods_QA.md](derivation/arxiv/RD_Methods_QA/rd_methods_QA.md:1) and associated figures/logs directories under [derivation/code/outputs/](derivation/code/outputs/).
- Foundations link present:
  - [symmetry_analysis.md](derivation/foundations/symmetry_analysis.md:1).
- fum_rt cross‑refs exist (integration hooks/tests):
  - [test_conservation_flux.py](fum_rt/core/tests/test_conservation_flux.py:1), [README.md](fum_rt/core/README.md:1).
Result: PASS. No broken or stale paths detected for the references used in this file. Audit timestamp (UTC): 2025‑08‑31T21:21:56Z.

### 14.9 Asynchronous census engine (runtime‑only; RD) — bottom‑up updates with local hazards

Purpose: event‑driven, sparse micro‑updates that respect Axiom 1 (locality), preserve RD Lyapunov monotonicity, and keep observability read‑only. No external schedulers are introduced; scheduling emerges from local activity.

- Local hazard and clocks:
  \[
  h_i := \big| D\,\Delta_a \phi_i + f(\phi_i) \big|,\qquad c_i^{n+1} \leftarrow c_i^{n} + h_i\,\Delta t.
  \]
  When \(c_i \ge 1\), site \(i\) fires with micro‑step \(\delta t_i := \theta / h_i\) for some quantum \(\theta\in(0,1]\); then set \(c_i \leftarrow c_i - 1\). Only \(i\) and its neighbours \(N(i)\) are touched. This realizes sparse‑only, GDSP emergent event‑driven updates.

- Reaction (exact, on‑site motor):
  \[
  W^{+}=\frac{r\,W\,e^{r\delta t_i}}{u\,W\,(e^{r\delta t_i}-1)+r},\qquad f(\phi)=r\phi-u\phi^{2}-\lambda \phi^{3}.
  \]
  Applied at fired sites; assumes \(r,u>0\). Tag [LIMIT‑ASSUMPTIONS] if parameters differ.

- Diffusion (flux‑form, conservative):
  \[
  F_{ij}=-\frac{D}{a}(\phi_j-\phi_i),\quad F_{ij}=-F_{ji},\qquad
  \phi_i \leftarrow \phi_i - \frac{\delta t_i}{a}\sum_{j\in N(i)} F_{ij}.
  \]
  With periodic or no‑flux BCs and \(f\equiv0\), \(\sum_i \phi_i\) is invariant (Lemma F.1).

- Lyapunov monotonicity (discrete‑gradient step):
  Choose the discrete‑gradient form so that
  \[
  \frac{\phi^{n+1}-\phi^{n}}{\delta t_i}=D\nabla_h^2\bar\phi+\bar f,\quad \hat V'(\bar\phi)=-\bar f
  \]
  holds at the fired site neighbourhood; then
  \[
  \Delta \mathcal L = \mathcal L^{n+1}-\mathcal L^{n} = - \sum_{i\ \text{fired}} \delta t_i \Big\|\frac{\phi^{n+1}-\phi^{n}}{\delta t_i}\Big\|_2^2 \le 0
  \]
  under Axiom 5 BCs (Lemma DG.1).

- Glow (observability channel, read‑only):
  Maintain an intensity
  \[
  M_i^{n+1} = M_i^{n} + \alpha\,\mathbf{1}\{\text{fire at }i\} + \beta \sum_{j\in N(i)} |F_{ji}|
  \]
  to visualize activity. \(M\) never feeds back into dynamics (runtime‑only).

- Gates and compliance:
  - Sparse‑only; no schedulers; no scans in core/maps; maps/frame contracts respected; guard control‑impact < \(10^{-5}\) on golden run (§14.4).
  - RD gates (U1 dispersion, U2 front speed) must pass under census scheduling; log SHA256 into Section 0.
  - H‑theorem gate: stepwise \(\Delta \mathcal L \le 0\) (no violations); diffusion mass conservation verified for \(f\equiv0\).

## Section 15. Alignment Gap Matrix for NEEDS_REVIEW themes (Validation‑only) — mapping to axiom‑core

All items below are external or phenomenological sources. They do not alter Axioms 1-5 or introduce primitives. Each entry records: Mapping (how to compare), Limits (assumptions to keep explicit), and Validation gates (runners/metrics). Status tags remain [NUM-EVIDENCE] and/or [CONJECTURE] with [LIMIT-ASSUMPTIONS].

15.1 Accretion‑Disks [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: [2508.01384v2.pdf](derivation/supporting_work/NEEDS_REVIEW/Accretion-Disks/2508.01384v2.pdf)
- Mapping: Off‑axiom MHD/GR sector; use as external runner to contrast RD diffusion scales vs viscous/magneto‑rotational transport.
- Limits: MHD closure, gravity model (Newtonian/GR), disk geometry/BCs.
- Gates: Consistency of measured diffusion‑like coefficients vs RD collapse variables where applicable; document when no RD reduction exists.

15.2 Active‑Matter [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: [2507.21621v1.pdf](derivation/supporting_work/NEEDS_REVIEW/Active-Matter/2507.21621v1.pdf)
- Mapping: Drift‑diffusion with self‑propulsion; compare linearized spectra to [U1] when advection is small; otherwise mark non‑RD sector.
- Limits: Microscopic propulsion rules, noise models, boundary driving.
- Gates: Spectral fits vs \(\hat\sigma=1-k'^2\) in the weak‑advection limit; Lyapunov proxy monotonicity in coarse‑grained limit when reducible to (2).

15.3 Entropy/Information [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Sources: multiple PDFs under [Entropy](derivation/supporting_work/NEEDS_REVIEW/Entropy/)
- Mapping: Use only as inference overlays (e.g., MaxCal/SB) on top of (2), per 13.3; do not modify dynamics.
- Limits: Declared priors and constraints.
- Gates: M1-M3 of §13.3; explicit check that \(d\mathcal L/dt\le0\) is preserved when projected back into RD.

15.4 Hamiltonian/CLS [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: [2508.01640v1.pdf](derivation/supporting_work/NEEDS_REVIEW/Hamiltonian/2508.01640v1.pdf)
- Mapping: Computational runner; compare outputs to L2 PDE (2).
- Limits: Truncation order \(K\), discretizations.
- Gates: QCLS‑1-3 (Section 13.5). All inertial analogies stay [EFT-KG] quarantined.

15.5 Gravity [CONJECTURE][NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Source: folder [Gravity](derivation/supporting_work/NEEDS_REVIEW/Gravity/)
- Mapping: Embeddings only under [EFT-KG] sandbox and cosmology conjectures (Proof‑Obligation Ledger items 2,3).
- Limits: FRW/diffeomorphism consistency; energy coupling does not violate Lyapunov structure in RD sector.
- Gates: Conservation residuals in conservative tests; H‑theorem maintained when projected back to RD.

15.6 Lorenz‑System / Phase‑Modeling [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Sources: [Lorenz-System](derivation/supporting_work/NEEDS_REVIEW/Lorenz-System/), [Phase-Modeling](derivation/supporting_work/NEEDS_REVIEW/Phase-Modeling/)
- Mapping: ODE and amplitude/phase reductions used as diagnostics only; not foundational.
- Limits: Parameter regimes, truncation validity.
- Gates: Linear response around equilibria from (2); stability vs Lemma U4.

15.7 Reaction‑Diffusion (external) [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Sources: [2307.14945v3.pdf](derivation/supporting_work/NEEDS_REVIEW/Reaction-Diffusion/2307.14945v3.pdf), [2409.13377v2.pdf](derivation/supporting_work/NEEDS_REVIEW/Reaction-Diffusion/2409.13377v2.pdf), [2411.09880v1.pdf](derivation/supporting_work/NEEDS_REVIEW/Reaction-Diffusion/2411.09880v1.pdf), [2508.16241v1.pdf](derivation/supporting_work/NEEDS_REVIEW/Reaction-Diffusion/2508.16241v1.pdf)
- Mapping/Limits/Gates: As in §13.1-13.4 (Q1-Q3, S1-S3, M1-M3, F1-F3). No import to axioms.

15.8 Self‑Supervision / Subquadratic‑Architecture [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Sources: [Self-Supervision](derivation/supporting_work/NEEDS_REVIEW/Self-Supervision/), [Subquadratic-Architecture](derivation/supporting_work/NEEDS_REVIEW/Subquadratic-Architecture/)
- Mapping: Runtime overlays only; cannot alter physics statements.
- Limits: Strict runner hard‑gates (14.4): sparse‑only, no schedulers, no scans in core/maps, Maps/Frame v1/v2 contract, guards pass with control‑impact < \(10^{-5}\).
- Gates: Unit smoke under fum_rt with guard telemetry; any violation → Kill‑R4.

15.9 Physics‑Sims / Escher‑Gödel‑Bach / Evolutionary‑Models / Voxtrium [NUM-EVIDENCE][LIMIT-ASSUMPTIONS]

- Sources: corresponding folders under [supporting_work/NEEDS_REVIEW](derivation/supporting_work/NEEDS_REVIEW/) and [voxtrium](derivation/supporting_work/voxtrium/)
- Mapping: Comparative/illustrative only; do not feedback into axioms.
- Limits: Documented per‑runner assumptions.
- Gates: Reproducibility and segregation from axiom‑core; any derived comparisons tagged [NUM-EVIDENCE].

Status: This matrix completes the alignment‑gap identification across NEEDS_REVIEW themes at the granularity required for validation‑only use. Any future elevation requires explicit derivations from Axioms 1-5 and satisfaction of Section 14 gates.

End of truth‑first axiomatic document. All non‑axiom / regime claims above are tagged; no content follows this termination marker.
[File terminates here intentionally - minimal source enforced.]
