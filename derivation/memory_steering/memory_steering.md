# Steering by Memory: A Dimensionless Law and Its Graph Discretization

Author: Justin K. Lietz  
Date: August 9, 2025

---

## 1. Objective

Establish a rigorous, minimal theory of how slowly stored structure (“memory”) imposes energy/information gradients that **steer** trajectories, and integrate it with the existing FUM scalar EFT. The result is a compact, falsifiable set of dimensionless laws that:
- Adds a slow “memory” field to bias routing (orthogonal to the fast φ‑propagation already derived).
- Produces scaling collapses (logistic junction choice, curvature) and a stability band.
- Admits a clean graph discretization aligned with our runtime.

Cross‑refs:
- Continuum φ‑EOM, vacuum, mass: [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:121-128)
- Kinetic normalization from a discrete action: [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:121-128)
- Units/FRW/action embedding and retarded kernels: [derivation/fum_voxtrium_mapping.md](derivation/fum_voxtrium_mapping.md:106-121)
- Source note (steering framework): [derivation/voxtrium/voxtrium_message.txt](derivation/voxtrium/voxtrium_message.txt:1)

---

## 2. Steering by a Memory‑Induced Refractive Index

Let \( M(x,t) \) be a slow “memory potential” (dimensionful). Define a local index
\[
n(x,t)\;=\;\exp\!\big[\eta\,M(x,t)\big],
\]
with coupling \( \eta \) (inverse units of \( M \) so that \( \eta M \) is dimensionless).

In the high‑frequency (ray/eikonal) limit (Fermat’s principle, geometric optics), the ray curvature obeys
\[
\mathbf r''\;=\;\nabla_\perp \ln n\;=\;\eta\,\nabla_\perp M,
\]
where \( \nabla_\perp \) denotes the gradient transverse to the local propagation direction. Interpretation:
- \( \eta>0 \): trajectories bend toward increasing \( M \) (attraction).
- \( \eta<0 \): trajectories bend away (dispersion).

This **steering law** is geometric and independent of the φ‑sector’s kinetic normalization; it acts as a slow, external bias on routing, while φ governs fast propagation.

---

## 3. Memory Dynamics (Write–Decay–Spread)

We posit a minimal, testable PDE for memory evolution:
\[
\partial_t M\;=\;\gamma\,R(x,t)\;-\;\delta\,M\;+\;\kappa\,\nabla^2 M,
\]
with:
- \( R(x,t) \): local usage/co‑activation rate (Hebbian driver; externally measurable, e.g. STDP proxy).
- \( \gamma \): write gain, \( \delta \): decay rate, \( \kappa \): consolidation/spread.

This is the simplest linear, causal model that creates, forgets, and spatially smooths memory.

---

## 4. Non‑Dimensionalization and Dimensionless Groups

Choose characteristic scales: length \( L \), time \( T \), memory \( M_0 \), usage \( R_0 \).
Define
\[
m\equiv \frac{M}{M_0},\quad \tilde t\equiv \frac{t}{T},\quad \tilde x\equiv \frac{x}{L},\quad \rho\equiv \frac{R}{R_0}.
\]

Steering law:
\[
\mathbf r''\;=\;\Theta\,\nabla_\perp m,\qquad \Theta\;\equiv\;\eta\,M_0.
\]

Memory PDE:
\[
\partial_{\tilde t}m\;=\;D_a\,\rho\;-\;\Lambda\,m\;+\;\Gamma\,\nabla^2 m,
\]
with the **dimensionless groups**:
\[
D_a=\frac{\gamma R_0 T}{M_0},\qquad \Lambda=\delta T,\qquad \Gamma=\frac{\kappa T}{L^2}.
\]

- \( \Theta \): memory–coupling strength (steering curvature per normalized gradient).
- \( D_a \): write rate relative to observation time.
- \( \Lambda \): forgetting over \( T \).
- \( \Gamma \): smoothing relative to system size.

Optional “thermo” knob (for stochastic settings): \( \Xi\equiv \Delta E_{\rm mem}/(k_B T_{\rm eff}) \). For \( \Xi\ll 1 \), gradients are too noisy to steer; for \( \Xi\gg 1 \), paths lock in.

---

## 5. Predictions (Dimensionless, Falsifiable)

1) Junction (fork) choice law. For a two‑branch junction with memory difference \( \Delta m \):
\[
P(\mathrm{choose\ A})\;\approx\;\sigma\!\big(\Theta\,\Delta m\big).
\]
Hence data from different sizes/speeds collapse vs. \( \Theta\Delta m \).

2) Curvature scaling. Local path curvature scales with normalized gradient:
\[
\kappa_{\rm path}\;\propto\;\Theta\,\big|\nabla_\perp m\big|.
\]
Plot curvature vs. \( \Theta|\nabla m| \); curves overlay across preparations if the law holds.

3) Stability band for retention. Robust memory requires \( D_a\gtrsim \Lambda \). Excessive \( \Gamma \) washes out memory; too little \( \Gamma \) yields brittle attractors. Expect a “band” in \( (D_a,\Lambda,\Gamma) \) with high fidelity.

---

## 6. Separation of Time Scales and Consistency with φ‑EFT

- φ‑sector (fast dynamics; canonical RD model):
  \[
  \partial_t \phi \;=\; D\,\nabla^2 \phi \;+\; r\,\phi \;-\; u\,\phi^2 \;\;[\;-\;\lambda\,\phi^3\;\text{optional}\;],\qquad \phi_\star = r/u\ \text{(or stabilized solution if }\lambda>0\text{)}.
  \]
  Note: EFT/KG formulations and \(m_{\rm eff}\) belong to [derivation/effective_field_theory_approach.md](effective_field_theory_approach.md:1) and should be used only in EFT contexts.

- M‑sector (slow routing bias): steering law and memory PDE as above.

These sectors are orthogonal: M biases routing geometry; φ determines propagation and excitations. Embedding in FRW bookkeeping with covariant conservation and retarded kernels remains consistent (see [derivation/fum_voxtrium_mapping.md](derivation/fum_voxtrium_mapping.md:106-121)).

---

## 7. Graph Discretization for the Runtime

Let the runtime graph have adjacency \( A \), degree \( D \), Laplacian \( L=D-A \). Define node‑wise vectors \( \mathbf m, \mathbf r \).

Memory update (forward Euler per tick \( \Delta t \)):
\[
\dot{\mathbf m}=\gamma\,\mathbf r\;-\;\delta\,\mathbf m\;-\;\kappa\,L\,\mathbf m,\qquad
\mathbf m \leftarrow \mathbf m + \Delta t\,\dot{\mathbf m}.
\]
Notes:
- \( \mathbf r \) is an independently measured usage/co‑activation rate (e.g., STDP proxy over a short window). Avoid circularity by not deriving \( \mathbf r \) from the choice probabilities.

Steering (transition softmax):
- At node \( i \), define index \( n_i=\exp(\eta m_i) \).
- For neighbors \( j\in N(i) \), set:
\[
P(i\to j)\;=\;\frac{\exp(\Theta\,m_j)}{\sum_{k\in N(i)}\exp(\Theta\,m_k)},\qquad \Theta=\eta M_0.
\]
At a 2‑branch fork, this reduces exactly to \( P(A)=\sigma(\Theta\,\Delta m) \).

Curvature on graphs:
- Approximate discrete curvature along a polyline/path by the turning angle \( \theta_k \) at node \( k \) over arc length \( \ell \):
\[
\kappa_{\rm path}\;\approx\;\frac{2\sin(\theta_k/2)}{\ell}.
\]
Regress \( \kappa_{\rm path} \) vs. \( \Theta\,|\nabla m| \), estimating \( |\nabla m| \) by neighbor differences around the path.

---

## 8. Units and Mapping to the Existing GeV Scaffold

Adopt the same \( (L,T)=(a,\tau) \) rulers as the φ‑map in [derivation/fum_voxtrium_mapping.md](derivation/fum_voxtrium_mapping.md:44-80). Choose \( M_0 \) as a characteristic memory change (e.g., an STDP weight shift) and \( R_0 \) as a characteristic co‑activation rate so that:
\[
\Theta=\eta M_0,\quad D_a=\frac{\gamma R_0 \tau}{M_0},\quad \Lambda=\delta \tau,\quad \Gamma=\frac{\kappa \tau}{a^2}.
\]
This preserves unit discipline alongside φ’s \( m^2=(\alpha-\beta)/\tau^2 \) and \( c^2=2Ja^2 \).

---

## 9. Avoiding Circularity

To test the theory properly:
- Measure \( m \) (or a proxy) independently (e.g., weight change from a predefined STDP protocol).
- Predict routing/curvature from \( m \). Do not back‑infer \( m \) from the very routing data being tested.

---

## 10. Experimental Protocols and Acceptance Criteria

1) Junction logistic collapse
- Prepare a Y‑junction; write a controlled \( \Delta m \) on branch A; hold \( \Theta \) fixed.
- Sweep \( \Delta m \); record \( P(A) \) vs. \( \Theta\,\Delta m \) across sizes/latencies.
- Accept if curves overlay and fit a logistic with slope within ±10% across conditions.

2) Curvature scaling
- Create a smooth gradient in \( m \); emit narrow pulses in φ (propagating at \( c^2=2Ja^2 \)).
- Accept if \( \kappa_{\rm path} \) vs. \( \Theta|\nabla m| \) collapses to a line ( \( R^2 \ge 0.9 \) ) across \( \Theta \).

3) Stability band
- Sweep \( (\gamma,\delta,\kappa) \); compute \( (D_a,\Lambda,\Gamma) \) and retention/fidelity.
- Accept if robust memory primarily appears for \( D_a\gtrsim \Lambda \) at intermediate \( \Gamma \).

---

## 11. Integration With Existing Derivations

- φ‑sector (canonical RD): \(\partial_t \phi = D\nabla^2\phi + r\phi - u\phi^2\) [optional \(-\lambda\phi^3\) stabilization]. Homogeneous fixed point: \(\phi_\star = r/u\) (or stabilized root if \(\lambda>0\)).
- EFT context (future work only): if using second‑order dynamics, \(\Box\phi + \alpha\phi^2 - (\alpha-\beta)\phi=0\) with \(v=1-\beta/\alpha\), \(m_{\rm eff}^2=\alpha-\beta\). Use these only within [derivation/effective_field_theory/effective_field_theory_approach.md](Prometheus_FUVDM/derivation/effective_field_theory/effective_field_theory_approach.md:1).
- Do not back‑solve \((\alpha,\beta)\) from \((v,m_{\rm eff})\) in the RD narrative. For EFT use, the relation \(\alpha={m_{\rm eff}^2}/{v}\), \(\beta={(1-v)}{m_{\rm eff}^2}/{v}\) may be referenced in that file.
- Memory \( M \) augments routing only; it does not modify the on‑site ODE used to derive \( Q_{\rm FUM} \), the on‑site invariant in [derivation/foundations/symmetry_analysis.md](Prometheus_FUVDM/derivation/foundations/symmetry_analysis.md:141-148).

---

## 12. Implementation Stubs (Runtime)

To support immediate testing, we provide separate modules (so the main φ loop remains unchanged):

- Memory PDE and steering API: [fum_rt/core/memory_steering.py](fum_rt/core/memory_steering.py:1)
  - `update_memory(m, r, L, gamma, delta, kappa, dt)` — Euler step for \( \dot m=\gamma r-\delta m-\kappa L m \).
  - `transition_probs(i, neighbors, m, theta)` — softmax steering \( P(i\to j)\propto e^{\Theta m_j} \).
  - Utilities to collect junction/curvature datasets for the acceptance tests.

- Diagnostics (already present): [fum_rt/core/diagnostics.py](fum_rt/core/diagnostics.py:1)
  - Mass gap via two‑point (\( m_{\rm eff}=1/\xi \)), pulse speed ( \( v_g \) ) for \( c^2\approx 2Ja^2 \).

---

## 13. Remarks on Scope and Claims

This appendix adds a **routing** layer governed by stored structure. It does not alter the previously derived φ‑EFT, kinetic normalization, nor the units/FRW embedding. It supplies pre‑registered, falsifiable **scaling collapses** to test across graph sizes and conditions, addressing “hand‑coded vs emergent” by measurement rather than assertion.

---

## 14. Provenance and Citations

- Steering & memory PDE (source): [supporting_work/voxtrium/20250809_voxtrium_message_2.md](Prometheus_FUVDM/derivation/supporting_work/voxtrium/20250809_voxtrium_message_2.md:1)
- φ‑EFT continuum, vacuum, mass invariants:
  [derivation/foundations/discrete_to_continuum.md](Prometheus_FUVDM/derivation/foundations/discrete_to_continuum.md:121-128)
- Kinetic/action derivation ( \( c^2=2Ja^2 \) ):
  [derivation/effective_field_theory/kinetic_term_derivation.md](Prometheus_FUVDM/derivation/effective_field_theory/kinetic_term_derivation.md:121-128)
- Units/FRW/retarded kernels:
  [derivation/effective_field_theory/fum_voxtrium_mapping.md](Prometheus_FUVDM/derivation/effective_field_theory/fum_voxtrium_mapping.md:106-121)
