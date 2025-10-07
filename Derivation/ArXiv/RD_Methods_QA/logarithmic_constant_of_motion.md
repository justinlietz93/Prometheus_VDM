# A Logarithmic First Integral for the Logistic On‑Site Law in Void Dynamics

Author: Justin K. Lietz  
Date: 2025‑08‑26  
Keywords: logistic law; invariant; first integral; reaction–diffusion; dissipative systems; conservation

Abstract
I prove a closed‑form constant of motion for the autonomous on‑site law
\[
\dot W \;=\; r\,W \;-\; u\,W^2,
\]
which underpins the Reaction–Diffusion (RD) baseline of Void Dynamics. Defining
\[
Q(W,t)\;=\;\ln\!\frac{W}{\,r-uW\,}\;-\;r\,t,
\]
I show that \(\tfrac{d}{dt}Q=0\) along solutions on domains where the expression is defined (e.g., \(0<W<r/u\)). I relate \(Q\) to the standard logistic solution, establish domains/branches and limiting behaviors, and explain why a naïve “kinetic\(+\)potential” energy is not conserved for this first‑order dissipative flow. Finally, I include a minimal, self‑contained numerical protocol that verifies machine‑precision constancy of \(Q\) and exhibits convergence consistent with the time‑stepper’s order. The note is self‑contained and implementation‑agnostic.

1. Introduction and main statement
I consider the one‑degree‑of‑freedom, autonomous ordinary differential equation (ODE)
\[
\dot W \;=\; F(W)\;=\; r\,W - u\,W^2,\qquad r,u\in\mathbb{R},
\]
and assume \(u\neq 0\). (In many RD parameterizations one writes \(r=\alpha-\beta\), \(u=\alpha\); I do not need that mapping here.) Because the ODE is autonomous, time‑translation symmetry implies the existence of an implicit first integral. The following explicit invariant holds.

Proposition (logarithmic invariant). For any interval on which the expression is defined (e.g., \(0<W<r/u\) when \(r/u>0\)),
\[
Q(W,t)\;\equiv\;\ln\!\frac{W}{\,r-uW\,}\;-\;r\,t
\]
is constant along any trajectory of \(\dot W=rW-uW^2\).

2. Proof (time‑translation constant for an autonomous ODE)
For an autonomous ODE \(\dot W=F(W)\), one has \(dt=\tfrac{dW}{F(W)}\). Here
\[
\frac{dW}{F(W)} \;=\; \frac{dW}{W(r-uW)} \;=\; \frac{1}{r}\left(\frac{1}{W}+\frac{u}{\,r-uW\,}\right)dW.
\]
Integrating both sides gives
\[
t + C \;=\; \frac{1}{r}\Big(\ln|W|-\ln|r-uW|\Big),
\]
or equivalently,
\[
\ln\!\frac{W}{\,r-uW\,}\;-\;r\,t \;=\; \text{const}.
\]
Defining \(Q(W,t) \equiv \ln\!\big(\tfrac{W}{r-uW}\big) - r t\) yields \(\tfrac{d}{dt}Q=0\) along solutions. This proves the claim.  
Remark. The proof is valid on any interval avoiding the simple poles at \(W=0\) and \(W=r/u\), with a consistent logarithm branch chosen on that interval.

3. Relation to the logistic closed‑form solution
Separation of variables yields the well‑known logistic solution
\[
W(t)\;=\;\frac{r}{u}\,\frac{1}{1+C\,e^{-r t}},\qquad
C\;=\;\frac{r-uW_0}{W_0},
\]
for an initial condition \(W(0)=W_0\) that avoids the poles. Substituting into the invariant gives
\[
Q\big(W(t),t\big)
=\ln\!\left(\frac{\tfrac{r}{u}\,\tfrac{1}{1+C e^{-rt}}}{\,r-\tfrac{r}{1+C e^{-rt}}\,}\right)-rt
=\ln\!\left(\frac{1}{u}\cdot\frac{1}{C}\right),
\]
which is constant in time. Thus \(Q\) encodes the integration constant (\(1/C\)) up to an additive constant \(-\ln u\); different branches correspond to the standard piecewise structure induced by the poles.

4. Properties, domains, units, and limits
- Poles and branches. \(Q\) has simple poles at \(W=0\) and \(W=r/u\). On any open interval avoiding these poles, one may select a consistent logarithm branch and obtain a constant \(Q\). Natural intervals are: (i) \((0,r/u)\) when \(r/u>0\), and (ii) \((r/u,\infty)\) when \(r/u>0\). Similar partitions apply when \(r/u<0\).
- Units. If \(W\) is dimensionless and \(r,u\) have units of inverse time, then \(\ln\!\frac{W}{r-uW}\) is dimensionless while \(rt\) is dimensionless, so \(Q\) is dimensionless. If one alternatively assigns a scale to \(W\), the same conclusion holds once a reference scale is absorbed.
- Limiting forms.
  - As \(W\to 0^\pm\): \(Q\sim \ln|W|-\ln|r| - r t\).
  - As \(W\to (r/u)^\mp\): \(Q\sim -\ln\big|r-uW\big| - r t + \text{const}\).
- Monotonicity of \(W\). On \((0,r/u)\) with \(r,u>0\), \(W\) grows monotonically to \(r/u\); on \((r/u,\infty)\), \(W\) decays monotonically to \(r/u\). The invariant remains constant on each interval separately.

5. Numerical verification (self‑contained protocol)
Objective. Verify that the numerical drift \(\Delta Q \equiv \max_{0\le n\le N} |Q(W_n,t_n)-Q(W_0,0)|\) is limited by discretization/round‑off and exhibits the expected step‑order convergence.

Protocol.
- Time‑stepper: fixed‑step RK4 (or Dormand–Prince with tight tolerances).
- Parameters: e.g., \(r=0.15\), \(u=0.25\).
- Initial conditions: sample \(W_0\in(10^{-3},\, r/u-10^{-3})\) and \(W_0\in(r/u+10^{-3},\, 1-10^{-3})\) to test both sides of the middle pole.
- Time step and horizon: \(dt=10^{-3}\), \(N=10^5\) steps (double precision).

Acceptance gates.
- Double precision: \(\Delta Q \le 10^{-10}\) (RK45 with tight tolerances) or \(\Delta Q \le 10^{-8}\) (RK4 with \(dt\approx 10^{-3}\)).
- Single precision: \(\Delta Q \le 10^{-5}\).
- Convergence: halving \(dt\) reduces \(\Delta Q\) by a factor consistent with the order \(p\) of the scheme; a log–log fit of \(\Delta Q\) vs \(dt\) yields slope \(p\pm 0.2\).

Pseudocode (language‑agnostic)
1) define F(W) = r·W − u·W²  
2) initialize t=0, W=W0, Q0 = ln(W/(r−uW)) − r·t  
3) for n in 1..N: advance (W,t) one step by RK4 with step dt  
4) compute Qn = ln(W/(r−uW)) − r·t and track max |Qn−Q0|  
5) report ΔQ and, if running a step‑refinement, the observed convergence slope

Numerical notes. Trap underflow/overflow near the poles; reject steps that cross the singularity. The test is most transparent on \((0,r/u)\) for \(r,u>0\).

6. Why there is no naïve conserved “energy” here
If one guesses a per‑site energy \(H(W,\dot W)=\tfrac12 \dot W^2 + V(W)\), then
\[
\frac{dH}{dt}=\dot W\big(\ddot W + V'(W)\big).
\]
In a first‑order flow \(\dot W=F(W)\), \(\ddot W=F'(W)\dot W\). Hence
\[
\frac{dH}{dt}=\dot W\big(F'(W)\dot W + V'(W)\big),
\]
which is not generically zero unless \(\dot W\equiv 0\) or \(V'\) is tuned to cancel \(F'(W)\dot W\) pointwise in time—impossible for a potential that depends only on \(W\). Thus a time‑independent Hamiltonian of this simple form is not conserved. The correct conserved quantity is the logarithmic first integral \(Q\) arising from autonomy/time‑translation symmetry.

7. Discussion and scope
- The invariant \(Q\) is local (on‑site). In spatially extended or coupled systems, \(Q\) is generally not conserved site‑wise; instead, it serves as a per‑node diagnostic for deviations induced by coupling/diffusion.
- The result is independent of implementation or discretization; it relies only on autonomy of the on‑site law and standard calculus.

Acknowledgments
I thank Voxtrium for providing his theory to me and giving me confidence when I saw that it mapped to his work and strengthened my own.

References
- S. H. Strogatz, Nonlinear Dynamics and Chaos, 2nd ed., Westview (2015).  
- C. H. Edwards, D. E. Penney, Differential Equations and Boundary Value Problems, Pearson.  
- J. D. Murray, Mathematical Biology I: An Introduction, 3rd ed., Springer (2002).
