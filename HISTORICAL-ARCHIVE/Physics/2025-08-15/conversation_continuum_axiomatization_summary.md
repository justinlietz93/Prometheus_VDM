# Continuum Axiomatization Conversation Summary

Date: 2025-08-29
Repository Target: Prometheus_FUVDM (branch: jlietz/dashboard_fixes).

Purpose
Comprehensive, self-contained recap of all discussion related to axiomatizing and upgrading the discrete-to-continuum theory (legacy T1 theorem and associated assumptions) in this chat session. Excludes unrelated strategic / ASI / tooling conversations. Enables a new contributor to reconstruct rationale, derivations, and planned file/axiom changes without raw chat logs.

------------------------------------------------------------------
High-Level Trajectory
1. Goal: Upgrade legacy continuum limit theorem (T1) so prior strong convergence / regularity assumptions (in old A6) become derived results, not axioms.
2. Strategy: Introduce a new authoritative T1_upgraded.md; retain legacy file with a supersession banner for traceability.
3. New Derived Components: Discrete Stability (DS), Compactness (CT), Quantitative Remainders (QR), Weak Form Derivation (WF), Regularity Bootstrap (RB). These replace monolithic pieces of old A6.
4. Axiom Reduction: A6 shrinks to a single uniform initial energy bound; convergence & high-regularity are now conclusions.
5. Error Control: Establish O(a^2) residual in H^{-2} norm; conditional classical convergence under higher Sobolev data.
6. Documentation Plan: Dependency graph updates, derivation roadmap, acceptance / verification tests, and legacy notice.

------------------------------------------------------------------
Legacy Situation (Pre-Upgrade)
- Old A6 bundled: (i) uniform energy, (ii) assumed convergence of interpolants, (iii) implicit high regularity of limit.
- Legacy T1 relied directly on these strong assumptions rather than proving them from discrete dynamics.
- Problem: Over-axiomatization reduces falsifiability and obscures which properties stem from the lattice equations.

------------------------------------------------------------------
Upgraded Theorem (T1_upgraded) - Core Claim (Condensed)
Given lattice solutions W^{(k)} on grids with spacing a_k→0 and Δt_k = a_k/c, periodic BCs, and uniform initial energy E_{a_k}^0 ≤ E_*, the interpolants φ^{(k)} possess a subsequence converging strongly in C^0_t L^2_x and L^2_t H^1_x to φ solving ∂_t^2 φ - c^2 Δφ + V'(φ)=0 weakly. Residual (in H^{-2}) is O(a_k^2). With higher initial Sobolev regularity (s>1+d/2), φ is classical and test-function residual pairing is second-order.

Key Clauses
1. Convergence: Strong L^2-based convergence + weak-* H^1 bounds.
2. PDE Identification: Via discrete weak form passage (WF provides detailed summation-by-parts and approximation control).
3. Quantitative Residual: ||Res^{(k)}||_{L^2_t H^{-2}_x} ≤ C a_k^2 (1 + M + M^2), M = sup_t ||φ^{(k)}||_{H^1}.
4. Regularity Upgrade: With high-order initial data, classical solution & O(a^2) weak-form error against H^2 tests.
5. Explicit Dependencies: DS, CT, QR, WF, RB replace prior axiom fragments.

------------------------------------------------------------------
Derived Components (Definitions / Roles)
DS (Discrete Stability): Provides uniform energy and H^1 bounds from discrete energy conservation / coercivity.
CT (Compactness): Uses Aubin-Lions (bounded in L^∞ H^1; time differences bounded in L^2 L^2) to extract strong convergence subsequence.
QR (Quantitative Remainders): Local truncation expansions for temporal second difference and spatial Laplacian plus interpolation error of nonlinearity → O(a^2) in H^{-2}.
WF (Weak Form Derivation): Standalone discrete summation-by-parts showing lattice EL ⇒ weak PDE with explicit remainder; term-by-term continuum limit justification.
RB (Regularity Bootstrap): Energy hierarchy on spatial derivatives (using H^s algebra for s > d/2, d ≤ 3) to upgrade weak to classical solution and control higher norms.

------------------------------------------------------------------
Supporting / Modified Files (Planned)
1. proofs/T1_upgraded.md (new authoritative theorem).
2. proofs/regularity_bootstrap.md (RB content: energy induction, Grönwall bounds).
3. proofs/weak_form_derivation.md (WF: detailed discrete → continuum weak form derivation, O(a^2) residual estimate).
4. proofs/T1_continuum_limit.md (legacy) - prepend deprecation / supersession notice.
5. core_axioms.md - revise A6 to minimal uniform initial energy bound.
6. dependency_graph.md - add WF and RB nodes; edges: DS → CT → T1_upgraded; WF & QR → T1_upgraded; RB → T1_upgraded (classical clause). Remove direct convergence assumptions from A6.
7. README - add Derivation Roadmap + acceptance test overview.

------------------------------------------------------------------
Proof Architecture Flow
Discrete EL: δ_t^2 W_i^n - κ Δ_a W_i^n + V'(W_i^n)=0.
→ Interpolate & apply discrete summation-by-parts (WF).
→ Obtain weak form with residual r_a.
→ Apply DS (bounds) + QR (local truncation) ⇒ ||r_a||_{L^2 H^{-2}} ≤ C a^2.
→ Use CT to extract φ limit.
→ Residual → 0 ⇒ φ satisfies weak PDE.
→ Apply RB (if high-regularity data) for classical solution and refined error statements.

------------------------------------------------------------------
Residual Decomposition Detail
Res^{(k)} = (δ_t^2 - ∂_t^2)φ^{(k)} - c^2 (Δ_a - Δ) φ^{(k)} + [V'(φ^{(k)}) - I(V'(W^{(k)}))].
Each piece bounded via Taylor expansion & stability-controlled norms. Nonlinear interpolation error uses local Lipschitz of V' plus Sobolev embeddings (H^1 ↪ L^p, p ≤ 6 for d ≤ 3).

------------------------------------------------------------------
Regularity Bootstrap Steps
1. Differentiate equation with D^m (|m| ≤ s).
2. Define energy E_m = 0.5 ||∂_t D^m φ||_2^2 + 0.5 c^2 ||∇D^m φ||_2^2 + potential interaction terms.
3. Use H^s algebra (s > d/2) to bound nonlinear commutators.
4. Sum energies ⇒ d/dt Σ_{|m|≤s} E_m ≤ C Σ E_m.
5. Grönwall ⇒ uniform high-order control; continuity yields classical solution.

------------------------------------------------------------------
Dimension / Nonlinearity Notes
- Focus d ≤ 3: cubic / polynomial potentials are subcritical; embeddings supply needed product estimates.
- Extension to d=4 possible with adjusted critical exponent handling.

------------------------------------------------------------------
Acceptance / Verification Tests (Proposed)
1. Manufactured Solution: Impose analytic φ, compute discrete weak residual; verify log-log slope ≈ 2.
2. Energy Stability: Track discrete energy E^n; deviations diagnose DS issues.
3. Weak Form Random Test: Sample smooth ψ; discrete residual norm scales O(a^2).
4. High-Order Data Persistence: Monitor spectral tail for spurious growth (validates RB numerically).

------------------------------------------------------------------
Axiom Simplification Outcome
Old A6: (Energy bound + assumed convergence + implicit high regularity).
New A6: Only uniform initial energy bound. All former convergence/regularity claims become theorem outputs with explicit dependency references.

------------------------------------------------------------------
Planned Next Steps
- Implement roadmap section in README.
- Materialize DS, CT, QR as explicit documents if not already separate (improves modular review).
- Extend RB to higher dimensions with refined estimates.
- Outline mechanized (Lean/Coq) verification strategy for discrete summation identities.

------------------------------------------------------------------
Integration Checklist
[ ] Add new proof files (T1_upgraded, regularity_bootstrap, weak_form_derivation).
[ ] Deprecate legacy T1 file with banner.
[ ] Reduce A6 in core_axioms.md.
[ ] Update dependency_graph.md with new nodes & edges.
[ ] README derivation roadmap.
[ ] Acceptance tests doc (tests/ or docs/tests.md).
[ ] Tag commit (e.g., v0.2-theory-upgrade).

------------------------------------------------------------------
Onboarding Path
1. Read minimal A6 in core_axioms.md.
2. Study T1_upgraded.md (main theorem & dependencies).
3. Consult weak_form_derivation.md for lattice → weak PDE passage.
4. Review regularity_bootstrap.md for high-regularity enhancements.
5. Run acceptance tests to empirically validate discrete scheme.

------------------------------------------------------------------
Rationale & Benefits
- Auditability: Each analytical transformation isolated.
- Flexibility: Changing potential V or BCs localizes required modifications (primarily QR & RB).
- Extensibility: Additional quantitative error results can attach cleanly to existing dependency nodes.
- Empirical Alignment: Test suite directly maps to theoretical guarantees.

------------------------------------------------------------------
End of Summary