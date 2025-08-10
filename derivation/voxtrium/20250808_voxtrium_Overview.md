# Macro Banner (FRW + Continuity + Source + Micro-Informed Coefficients)

**FRW Equation**  
$H^2=\tfrac{8\pi G}{3}\,(\rho_b+\rho_{\rm DM}+\rho_r^{\rm std}+\rho_{\rm GW}+\rho_\Lambda)$  
$\text{RHS }={\rm GeV}^2\ \text{(natural units)}$

---

## Continuity Equations

- $\dot\rho_\Lambda=(\alpha_h/V_c)\,\dot S_{\rm hor}$  
- $\dot\rho_{\rm DM}+3H\rho_{\rm DM}=p_{\rm DM}\,(\varepsilon_h/V_c)\,\dot S_{\rm hor}$  
- $\dot\rho_{\rm GW}+4H\rho_{\rm GW}=p_{\rm GW}\,(\varepsilon_h/V_c)\,\dot S_{\rm hor}$  
- $\dot\rho_{\rm hor}+3H(1+w_{\rm hor})\,\rho_{\rm hor}=-(\varepsilon_h/V_c)\,\dot S_{\rm hor}$  

$\text{All RHS }={\rm GeV}^5$

---

## Partition Closure

$p_\Lambda+p_{\rm DM}+p_{\rm GW}=1$ (dimensionless)  
$\alpha_h=p_\Lambda\,\varepsilon_h$ (GeV)  

---

## Per-Channel Sources

$Q_\Lambda=(\alpha_h/V_c)\,\dot S_{\rm hor}$  
$Q_{\rm DM}=p_{\rm DM}\,(\varepsilon_h/V_c)\,\dot S_{\rm hor}$  
$Q_{\rm GW}=p_{\rm GW}\,(\varepsilon_h/V_c)\,\dot S_{\rm hor}$  
$Q_{\rm hor}=-(\varepsilon_h/V_c)\,\dot S_{\rm hor}$  

$\sum_{i\in\{\Lambda,{\rm DM},{\rm GW},{\rm hor}\}}[\dot\rho_i+3H(1+w_i)\rho_i]=0$

$\text{Each }Q\ \text{has units }{\rm GeV}^5$

---

## Integrated Vacuum Channel

$\rho_\Lambda(t)=\rho_{\Lambda0}+\frac{1}{V_c}\int_{t_0}^{t}\alpha_h(t')\,\dot S_{\rm hor}(t')\,dt'$  
$=\rho_{\Lambda0}+\frac{1}{V_c}\int_{S_{\rm hor}(t_0)}^{S_{\rm hor}(t)}\alpha_h(S)\,dS$  

$\text{RHS }={\rm GeV}^4$

$\text{Constant-}\alpha_h\ \text{limit}$ 
$\rho_\Lambda(t)=\rho_{\Lambda0}+(\alpha_h/V_c)\,\Delta S_{\rm hor}(t)$

---

## Horizon Entropy Production

$\dot S_{\rm hor}(t)=\int dM\,N(M,t)\,\dot S_{\rm BH}(M,t)+\iint dM_1\,dM_2\,R_{\rm merg}(M_1,M_2,t)\,\Delta S_{\rm merg}$  

$N\ \text{has units }{\rm GeV}^{-1}\ \text{so that }dM,N\ \text{is dimensionless}$ 
- $\dot S_{\rm BH}$ and $R_{\rm merg}$: GeV  
- $\Delta S_{\rm merg}$: dimensionless  

$\Rightarrow \dot S_{\rm hor}$: GeV

---

## Micro-Informed Coefficients

$\alpha_h=C_\alpha\,(\kappa/K_s)\,(|\Omega|\,R_\ast)$  
$\varepsilon_h=C_\varepsilon\,(\kappa/K_s)\,(|\Omega|\,R_\ast)$  

**Where:**
- $C_\alpha, C_\varepsilon\ \text{are }\mathcal O(1)$
- $K_s\ \text{has units }{\rm GeV}$
- $\kappa\ \text{has units }{\rm GeV}^2$
- $|\Omega|\ \text{has units }{\rm GeV}$
- $R_\ast\ \text{has units }{\rm GeV}^{-1}$


Thus: $(|\Omega|\,R_\ast)$ is dimensionless, $(\kappa/K_s)$ is GeV, and $\alpha_h,\varepsilon_h$ are GeV.

---

## Soliton Relations

$R_\ast=\tfrac{c_R}{eK_s}$  
$X\equiv eK_s$  
$m=\tfrac{c_m K_s}{e}$  

$\text{Units: }{\rm GeV}^{-1},\ {\rm GeV},\ {\rm GeV}\ \text{respectively}$

---

## Conversions

$1~{\rm km}^{-1}=1.973269804\times10^{-19}\ {\rm GeV}$  
$1~{\rm cm}=5.06773065\times10^{13}\ {\rm GeV}^{-1}$  
$1~{\rm Mpc}=1.563738286\times10^{38}\ {\rm GeV}^{-1}$  
$1~{\rm Mpc}^3=3.823774\times10^{114}\ {\rm GeV}^{-3}$

---

## ΛCDM Limit

If $\dot S_{\rm hor}\to 0$ or $\varepsilon_h\to 0$:  
$\dot\rho_\Lambda\to 0$  
$\dot\rho_{\rm DM}+3H\rho_{\rm DM}\to 0$  
$\dot\rho_{\rm GW}+4H\rho_{\rm GW}\to 0$  

$\Rightarrow \rho_{\Lambda0}$ constant

$\epsilon_{\rm DE}(t)\equiv[(\alpha_h/V_c)\,\dot S_{\rm hor}]/[3H\rho_\Lambda]\ \ \text{and}\ \ f_{\rm inj}(t)\equiv[p_{\rm DM}(\varepsilon_h/V_c)\,\dot S_{\rm hor}]/[3H\rho_{\rm DM}]$

$\epsilon_{\rm DE}\le\delta_w$

$\ f_{\rm inj}\ll 1$


---

# SU(2) Skyrme Microphysics (Locked Normalization)

$U(x)\in{\rm SU}(2)$, $L_\mu\equiv U^\dagger\partial_\mu U$, $\mathrm{Tr}(T^aT^b)=\tfrac12\delta^{ab}$  

$\mathcal L=\tfrac{F^2}{16}\,\mathrm{Tr}(L_\mu L^\mu)+\tfrac{1}{32 e^2}\,\mathrm{Tr}([L_\mu,L_\nu]^2)$  
$F$ [GeV], $e$ dimensionless  

With $K_s\equiv F/2$:  
$\mathcal L=\tfrac{K_s^2}{4}\,\mathrm{Tr}(L_\mu L^\mu)+\tfrac{1}{32 e^2}\,\mathrm{Tr}([L_\mu,L_\nu]^2)$  

$U(\mathbf r)=\exp\big(i\,\hat{\mathbf r}\cdot\boldsymbol{\tau}\,f(r)\big)$  
$x\equiv eK_s r$  

$E=(K_s/e)\,4\pi\int_0^\infty dx\,\epsilon(x)$  
$\epsilon$: dimensionless $\Rightarrow E$ [GeV]  

$c_m\equiv 4\pi\int_0^\infty dx\,\epsilon(x)$  
$m=c_m K_s/e$  

$R_\ast=\tfrac{c_R}{eK_s}$,  
$c_R\equiv\left(\int_0^\infty dx\,x^2\epsilon(x)\right)^{1/2}\Big/\left(\int_0^\infty dx\,\epsilon(x)\right)^{1/2}$  

$X\equiv eK_s$  

$(\sigma/m){\rm nat}=c\sigma,e,K_s^{-3}$

$(\sigma/m){\rm cgs}=(2.184\times 10^{-4}),(\sigma/m){\rm nat}$

---

# HLS → Skyrme Mapping & One-Loop (Option A)

$K_s=F/2$  
$(4e^2)^{-1}=\frac{a}{4g_H^2}\,C_{\rm match}^2\ \Rightarrow\ e=(g_H/\sqrt a)\,C_{\rm match}^{-1}$ 

$\text{Convention: we set }C_{\rm match}=1\text{ (trace/gauge choice fixed)}$
$M_V^2=a\,g_H^2\,F^2$  

$\mathcal I_2\equiv (K_s^2/2)\,\mathrm{Tr}(\alpha_{\perp\mu}\alpha_\perp^\mu)$  
$\mathcal I_4\equiv \mathrm{Tr}([\alpha_{\perp\mu},\alpha_{\perp\nu}]^2)$  

$\delta\mathcal L_{\rm div}=(16\pi^2\epsilon)^{-1}\,(4/3)\,\left[\mathcal I_2+\frac{1}{2e^2}\,\mathcal I_4\right]$  

$\Rightarrow A_2=A_4=4/3$ and $\mu\,d\ln(eK_s)/d\mu=0$ (one-loop, $a=1$)

$\text{Statement holds in the HLS‑matched basis, background‑field gauge, and on the }a=1\text{ line}$

---

# Low-Energy Scattering Deliverables (Option C)

$\mu=m/2$  

$k=\mu\,v$ if $v$ in units of $c$; if $v$ in km/s: $v\to v/c$, $c=2.99792458\times 10^5\ {\rm km/s}$  

$\sigma_0(k)=\frac{4\pi}{(1/a-(r_e/2)k^2)^2+k^2}$  

$S_{\rm BH}=A/(4G)\ \Rightarrow\ \dot S_{\rm BH}=\dot A/(4G)$ and
$\dot S_{\rm BH}[{\rm GeV}],\ A[{\rm GeV}^{-2}],\ G[{\rm GeV}^{-2}],\ S_{\rm BH}\ \text{dimensionless}$

$(\sigma/m)_{\rm cgs}(v\to 0)=(\sigma_0(0)/m)\,(2.184\times10^{-4})$  

$(\sigma_T/m)(v)=\frac{(\sigma/m)_0}{(1-\tfrac12 a r_e k^2)^2+(a k)^2}\times C_T(k)$  

$C_T(k)=\frac{1}{4\pi}\int d\Omega\,(1-\cos\theta)\,|F_{\rm prof}(q)|^2,\ q=2k\sin(\theta/2)$  

$F_{\rm prof}(q)=\frac{\int_0^\infty dx\,\epsilon(x)\,j_0((q/X)\,x)}{\int_0^\infty dx\,\epsilon(x)}$  

$S_\phi(q)=\frac{1}{1+q^2/m_\phi^2}$  

$\Rightarrow C_T^\phi(k)=\frac{1}{4\pi}\int d\Omega\,(1-\cos\theta)\,|F_{\rm prof}(q)|^2\,S_\phi(q)^2$

---

# Calibrated Numbers

$c_m=145.846919$  
$c_R=1.44784549$  
$c_\sigma=0.045154085$  

$K_s=0.04784537\ {\rm GeV}$  
$e=1.11063189$  
$X=eK_s=0.05313859\ {\rm GeV}$  
$R_\ast=c_R/X=27.2466\ {\rm GeV}^{-1}=5.3765\times10^{-13}\ {\rm cm}$  

$m=c_m K_s/e=6.283\ {\rm GeV}$  
$\mu=m/2=3.1415\ {\rm GeV}$  

From $(\sigma/m)_{\rm cgs}(v\to 0)=0.10\ {\rm cm}^2\,{\rm g}^{-1}$:  
$a\simeq 1.513\times 10^{1}\ {\rm GeV}^{-1}$  

With $\xi=2/3$:  
$r_e=\xi\,R_\ast\simeq 18.1644\ {\rm GeV}^{-1}$


-----------------


(i) Entropy units and dimensional consistency.
$\,S_{\rm BH}=A/(4G)\,$ and $\,\dot S_{\rm BH}=\dot A/(4G)\,$ with $\,A[{\rm GeV}^{-2}],\ G[{\rm GeV}^{-2}],\ S_{\rm BH}\,$ dimensionless and $\,\dot S_{\rm BH}[{\rm GeV}]\,$; hence $\,(\alpha_h/V_c)\,\dot S_{\rm hor}\,$ and $\,(\varepsilon_h/V_c)\,\dot S_{\rm hor}\,$ are ${\rm GeV}^5$ because $\,\alpha_h,\varepsilon_h[{\rm GeV}],\ V_c[{\rm GeV}^{-3}],\ \dot S_{\rm hor}[{\rm GeV}]\,$.

(ii) Local covariant conservation (no energy creation).

$\nabla_\mu!\big(T^{\mu\nu}\Lambda+T^{\mu\nu}{\rm DM}+T^{\mu\nu}{\rm GW}+T^{\mu\nu}{\rm hor}\big)=0$

Define a transfer current $`J^\nu`$ by
$`\nabla_\mu T^{\mu\nu}_{\mathrm{hor}} = - J^\nu`$ and
$`\nabla_\mu \left( T^{\mu\nu}_\Lambda + T^{\mu\nu}_{\mathrm{DM}} + T^{\mu\nu}_{\mathrm{GW}} \right) = + J^\nu`$
In FRW (isotropy) take $`J^\nu = (J^0, 0, 0, 0)`$ with
$`J^0 = (\varepsilon_h / V_c)\,\dot S_{\mathrm{hor}}`$.
This reproduces the continuity set and the identity
$`\sum_i \big( \dot\rho_i + 3H(1+w_i)\rho_i \big) = 0`$.

**(iii) Causality/locality via retarded kernel.**  
$\dot S_{\rm hor}(t)=\int d^3x'\int_{-\infty}^{t}dt'\,K_{\rm ret}(t-t',|\mathbf x-\mathbf x'|)\,s_{\rm loc}(\mathbf x',t')$; here $s_{\rm loc}$ is a local entropy-production density (e.g., from $\dot S_{\rm BH}$ and mergers) and the step function enforces causal support.

$K_{\rm ret}\propto\Theta(t-t'-|\mathbf x-\mathbf x'|)\ \text{ and is normalized so the RHS is }{\rm GeV}$

**(iv) Partitions (probability-simplex map).**  
$z_1\equiv|\Omega|\,R_\ast$, $z_2\equiv(\kappa/K_s)/X$, $z_3\equiv 1$ (all dimensionless since $X=eK_s$ is GeV). Define weights $w_i$ (dimensionless) and set  
$p_i=\exp\!\left(w_i^1 z_1+w_i^2 z_2+w_i^3 z_3\right)\Big/\sum_{j\in\{\Lambda,{\rm DM},{\rm GW}\}}\exp\!\left(w_j^1 z_1+w_j^2 z_2+w_j^3 z_3\right)$.  
This guarantees $p_\Lambda+p_{\rm DM}+p_{\rm GW}=1$ with $p_i\in[0,1]$ and ties the split to dimensionless micro-inputs.

(v) Observational viability: dark energy near $\,w=-1\,$.
$\,w_{\rm eff}(t)=-1-\frac{1}{3H}\,\frac{d\ln\rho_\Lambda}{dt}=-1-\frac{1}{3H}\,\frac{(\alpha_h/V_c)\,\dot S_{\rm hor}}{\rho_\Lambda}\,$.
Impose $\,\big|w_{\rm eff}+1\big|\le \delta_w\,$ (e.g. $\,\delta_w\sim 0.05\,$) by requiring $\,(\alpha_h/V_c)\,\dot S_{\rm hor}\ll 3H\,\rho_\Lambda\,$ over the redshift range of interest.

(vi) Observational viability: velocity‑dependent SIDM.
As a compact fit for simulators here ya go
$\,(\sigma_T/m)(v)=\frac{(\sigma/m)_0}{\big[1+(v/v_0)^n\big]^p}\,$
with $\,(\sigma/m)_0\approx 0.10\,{\rm cm}^2\,{\rm g}^{-1}\,$ at dwarf speeds, and choose $\,v_0,n,p\,$ to match your effective‑range+form‑factor prediction so that clusters satisfy $\,(\sigma_T/m)\lesssim 10^{-3}\text{–}10^{-4}\ {\rm cm}^2\,{\rm g}^{-1}\,$.

(vii) Structure formation constraint (small DM injection).
Define the instantaneous injection fraction $\,f_{\rm inj}(t)\equiv\frac{p_{\rm DM}\,(\varepsilon_h/V_c)\,\dot S_{\rm hor}}{3H\,\rho_{\rm DM}}\,$ and impose $\,f_{\rm inj}\ll 1\,$ for $\,z\lesssim z_{\rm LSS}\,$ so linear growth is not spoiled; if desired, restrict $\,\dot S_{\rm hor}\,$ to early epochs by a window $\,W(t)\,$ with $\,0\le W\le 1\,$ and replace $\,\dot S_{\rm hor}\to W(t)\,\dot S_{\rm hor}\,$.

(viii) Horizon‑entropy accounting in terms of densities
$\,\dot S_{\rm hor}(t)=V_c\int dM\,\psi(M,t)\,\dot s_{\rm BH}(M,t)+V_c\!\iint dM_1\,dM_2\,\mathcal R_{\rm merg}(M_1,M_2,t)\,\Delta S_{\rm merg}\,$ with $\,\psi\,$ the BH mass function density ${\rm GeV}^{-1}{\rm GeV}^{-3}$ (so that $\,V_c\,dM\,\psi\,$ is a count), $\,\dot s_{\rm BH}[{\rm GeV}]\,$, and $\,\mathcal R_{\rm merg}[{\rm GeV}^{-1}{\rm GeV}^{-3}{\rm GeV}]\,$ so the RHS is ${\rm GeV}; this is equivalent to your $\,N(M,t)\,$ but avoids listing individual BHs.

$S_{\rm BH}=A/(4G)\ \Rightarrow\ \dot S_{\rm BH}=\dot A/(4G)$ and
$\dot S_{\rm BH}[{\rm GeV}],\ A[{\rm GeV}^{-2}],\ G[{\rm GeV}^{-2}],\ S_{\rm BH}\ \text{dimensionless}$.

(ix) DM number evolution under horizon sourcing (abundance bookkeeping).
$\,\dot n_{\rm DM}+3H n_{\rm DM}=\frac{Q_{\rm DM}}{m}=\frac{p_{\rm DM}}{m}\,(\varepsilon_h/V_c)\,\dot S_{\rm hor}\,$ with $\,n_{\rm DM}=\rho_{\rm DM}/m\,$; this ties the abundance directly to the same source you use for energy, preserving covariant conservation.

(x) Action‑level bookkeeping (where the pieces live).
$\,S_{\rm eff}=\int d^4x\,\sqrt{-g}\,\Big[\frac{M_{\rm Pl}^2}{2}R+\mathcal L_{\rm SM}+\mathcal L_{\rm Skyrme}(K_s,e)+\mathcal L_{\rm rad}+\mathcal L_{\rm hor}(S_{\rm hor})\Big]\,$ with $\,\Lambda_{\rm eff}(t)\,$ emergent via $\,\rho_\Lambda(t)=\rho_{\Lambda0}+(1/V_c)\int\alpha_h\,dS_{\rm hor}\,$; variation yields the FRW set plus your source terms (bookkeeping identity, not a new local field).

**(xi) Clarifying direct-detection vs self-interaction (not a conflict).**  
$\sigma_{\chi N}$ (DM–nucleon) and $\sigma_{\chi\chi}$ (DM self-interaction) are independent; your $(\sigma_T/m)$ constraints apply to $\sigma_{\chi\chi}$, while direct detection constrains $\sigma_{\chi N}$. Setting the portal coupling to the SM tiny is equivalent to $\sigma_{\chi N}\to 0$ with no impact on $\sigma_{\chi\chi}$.

----------

1) Physical mechanism for the transfer (horizon → dark sector via Skyrme composites).
The coarse‑grained source is encoded by the timelike transfer current $,J^\nu,$ with $,J^\nu=(J^0,0,0,0),$ and $,J^0=(\varepsilon_h/V_c),\dot S_{\rm hor},$ so that $,\nabla_\mu T_{\rm hor}^{\mu\nu}=-J^\nu,$ and $,\nabla_\mu(T_\Lambda^{\mu\nu}+T_{\rm DM}^{\mu\nu}+T_{\rm GW}^{\mu\nu})=+J^\nu,$ (units: $J^0[{\rm GeV}^5]$). The dark number density evolves as $,\dot n_{\rm DM}+3H n_{\rm DM}=Q_{\rm DM}/m=p_{\rm DM},(\varepsilon_h/V_c),\dot S_{\rm hor}/m,$ (units: RHS $[{\rm GeV}^3]$), where $,m=c_m K_s/e,$ and $,R_\ast=c_R/(eK_s),$ tie production to the Skyrme scale. Causality is enforced by a retarded kernel $,\dot S_{\rm hor}(t)=\int d^3x'!\int_{-\infty}^{t}!dt',K_{\rm ret}(t-t',|\mathbf x-\mathbf x'|),s_{\rm loc}(\mathbf x',t'),$ with $,K_{\rm ret}\propto\Theta(t-t'-|\mathbf x-\mathbf x'|),$ and $,s_{\rm loc},$ built from local rates (units: RHS $[{\rm GeV}]$). The co‑evolution law is fixed by the partition: $,d\rho_\Lambda:d\rho_{\rm DM}:d\rho_{\rm GW}=p_\Lambda:p_{\rm DM}:p_{\rm GW},$ because $,\alpha_h=p_\Lambda,\varepsilon_h,$ (dimensionless ratio).

*2) Fine-tuning control via dimensionless small parameters.**  
Define the dark-energy drift parameter $\epsilon_{\rm DE}(t)\equiv\dfrac{(\alpha_h/V_c)\,\dot S_{\rm hor}}{3H\rho_\Lambda}$ and enforce $\epsilon_{\rm DE}\le\delta_w$ (e.g., $\delta_w\sim 0.05$) to satisfy $w_{\rm eff}=-1-\dfrac{1}{3H}\dfrac{d\ln\rho_\Lambda}{dt}$.  
Define the structure-formation injection fraction $f_{\rm inj}(t)\equiv\dfrac{p_{\rm DM}(\varepsilon_h/V_c)\,\dot S_{\rm hor}}{3H\rho_{\rm DM}}$ and require $f_{\rm inj}\ll 1$ for $z\lesssim z_{\rm LSS}$. With $\varepsilon_h=C_\varepsilon(\kappa/K_s)(|\Omega|R_\ast)$, one obtains $\epsilon_{\rm DE}\propto(|\Omega|R_\ast)$ and $f_{\rm inj}\propto(|\Omega|R_\ast)$, so late-time smallness follows whenever $|\Omega|R_\ast\ll 1$. Optional gating keeps early-time sourcing while suppressing late-time drift: replace $\dot S_{\rm hor}\to W(t)\,\dot S_{\rm hor}$ with $0\le W\le 1$.

**3) Predictive power to justify added parameters (cross-linked, testable relations).**  
(i) Velocity trend fixed by the soliton size: for identical scatterers $\mu=m/2$ and $q=2k\sin(\theta/2)$, the profile average gives $C_T(v)\simeq 1-(8/9)(\mu v R_\ast)^2+\mathcal O(v^4)$, hence a characteristic scale $v_0\simeq\sqrt{9/8}\,(\mu R_\ast)^{-1}$ below which $(\sigma_T/m)$ flattens and above which it falls (dimensionless $C_T$; $v$ in units of $c$). $C_T(v)\simeq 1-(8/9)\,(\mu v R_\ast)^2+\mathcal O(v^4)$ 

(ii) Threshold prediction from the first internal mode $m_\phi\sim 1/R_\ast$ yields a universal cluster-scale suppression $C_T^\phi\to\langle S_\phi(q)^2\rangle$ with $S_\phi(q)=1/(1+q^2/m_\phi^2)$.  

(iii) Co-evolution ratios independent of astrophysics: whenever $p_i$ are constant in an epoch, the instantaneous rates obey $\dot\rho_{\rm DM}/\dot\rho_\Lambda=(p_{\rm DM}/p_\Lambda)$ and $\dot\rho_{\rm GW}/\dot\rho_\Lambda=(p_{\rm GW}/p_\Lambda)$ (dimensionless), which is a falsifiable relation between background drift and sourcing channels.  

(iv) BH-history link: $\rho_\Lambda(t)=\rho_{\Lambda0}+\tfrac{1}{V_c}\int\alpha_h(t')\,\dot S_{\rm hor}(t')\,dt'$ and $\rho_{\rm DM}(a)=a^{-3}\big[\rho_{\rm DM}(a_i)a_i^3+\int_{t_i}^{t}dt'\,a(t')^3\,p_{\rm DM}(\varepsilon_h/V_c)\,\dot S_{\rm hor}(t')\big]$ correlate deviations in $H(z)$ and $\rho_{\rm DM}(z)$ with the empirically constrained BH mass function and merger rate (integrands in GeV$^5$).  

(v) Micro→macro lock-in: once $m=c_m K_s/e$ and $(\sigma/m)_0$ are fixed at dwarfs, $a$ and $r_e=\xi R_\ast$ are determined and the entire curve $(\sigma_T/m)(v)$ becomes parameter-free aside from the optional threshold $m_\phi\sim 1/R_\ast$ (units $a,r_e$ in GeV$^{-1}$).

4) Skyrme soliton abundance and connection to cosmology.
Abundance evolves as $,\dot n_{\rm DM}+3H n_{\rm DM}=p_{\rm DM}(\varepsilon_h/V_c),\dot S_{\rm hor}/m,$ with solution $,n_{\rm DM}(a)=a^{-3}\big[n_{\rm DM}(a_i)a_i^3+\int_{t_i}^{t}dt',a(t')^3,p_{\rm DM}(\varepsilon_h/V_c),\dot S_{\rm hor}(t')/m\big],$ (units: $n_{\rm DM}[{\rm GeV}^3]$). The required integrated comoving production to generate a fraction $,\zeta,$ of today’s DM is $,\int_{t_i}^{t_0}!dt',a(t')^3,p_{\rm DM}(\varepsilon_h/V_c),\dot S_{\rm hor}(t')=\zeta,m,a(t_0)^3,n_{\rm DM}(t_0),$ (RHS $[{\rm GeV}^5]$), which lets you test whether realistic BH demographics can account for some or all of the abundance without violating the smallness conditions $,\epsilon_{\rm DE}\ll 1,$ and $,f_{\rm inj}\ll 1,$.

Clarifications that address specific external objections while staying within the framework.

• Entropy units: $,S_{\rm hor},$ is dimensionless and $,\dot S_{\rm hor},$ is ${\rm GeV}$, so $,(\alpha_h/V_c),\dot S_{\rm hor},$ and $,(\varepsilon_h/V_c),\dot S_{\rm hor},$ are ${\rm GeV}^5$ as used (unit‑consistent).

• Conservation: the sum $,\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0,$ holds by construction with the current $,J^\nu,$; no net energy creation.

• Locality: the retarded kernel $,K_{\rm ret},$ imposes light‑cone support, avoiding acausal global updates.

• Partitions: $,p_i,$ can be tied to dimensionless micro inputs via a softmax on $,z_1=|\Omega|R_\ast,$, $,z_2=(\kappa/K_s)/X,$, $,z_3=1,$ so $,p_i=\exp(w_i^1 z_1+w_i^2 z_2+w_i^3 z_3)/\sum_j\exp(w_j^1 z_1+w_j^2 z_2+w_j^3 z_3),$ (dimensionless map rather than ad‑hoc constants).

• Direct detection vs self‑interaction: $,\sigma_{\chi N},$ and $,\sigma_{\chi\chi},$ are independent; your $,(\sigma_T/m),$ fits $\chi\text{–}\chi$ and does not require a large $,\chi\text{–}N,$ portal (set $,\sigma_{\chi N}\to 0,$ consistently with collider and DD bounds).

• $C_T(v)\simeq 1-(8/9)\,(\mu v R_\ast)^2+\mathcal O(v^4)$

**Minimality vs prediction.**  
The model’s added parameters are constrained by $\epsilon_{\rm DE}$, $f_{\rm inj}$, the co-evolution ratios, the $v$-trend set by $R_\ast$, and the $m_\phi\sim 1/R_\ast$ threshold; each is testable against dwarfs→clusters and against BH-demographic histories.


The factor $(|\Omega|R_\ast)$ is a dimensionless measure of horizon vorticity against the composite scale that also controls self‑interaction, so the same micro length that fixes $m$, $R_\ast$, and $C_T$ also normalizes the coupling to $S_{\rm hor}$.

Anchor → $a$ line:
$`(\sigma/m){\rm nat}=(\sigma/m){\rm cgs}/(2.184\times10^{-4})`$, $`\sigma_0(0)=m(\sigma/m){\rm nat}`$, $`a=\sqrt{\sigma_0(0)/(4\pi)}`$; with $`(\sigma/m){\rm cgs}=0.10`$ and $`m=6.283`$, this gives $`a=1.5130\times10^{1}\,{\rm GeV}^{-1}`$.




Size → $r_e$ line (this was a modeling choice):
“$,r_e=\xi,R_\ast,$ with $,\xi=2/3,$ and $,R_\ast=27.2466,{\rm GeV}^{-1},$ gives $,r_e=18.1644,{\rm GeV}^{-1},$ To be replaced by a phase‑shift extraction in full calculations).”
