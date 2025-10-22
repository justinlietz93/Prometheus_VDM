# PROPOSAL Priority Matrix — Quick Reference Guide

**Date:** 2025-10-22  
**Purpose:** At-a-glance prioritization for PROPOSAL document implementation  
**Detailed Analysis:** See `NEXT_STEPS_RECOMMENDATIONS.md`

---

## Priority Tier 1 (Immediate — Next 1-2 Months)

| Priority | Proposal | Current Tier | Target Tier | GPU-Hours | Timeline | UToE Impact |
|----------|----------|--------------|-------------|-----------|----------|-------------|
| **1.1** | Thermodynamic Routing v2 (Biased Main) | T4 | T6 | 40-80 | 6-7 weeks | FND-ENTS, QM-DECO |
| **1.2** | Wave Flux Meter Phase B/C | T1-T4 | T6 | 20-40 | 5-6 weeks | MTH-TENSOR |
| **1.3** | SIE Invariant & Novelty | T4 | T6 | 0 (CPU) | 3 weeks | QM-HILBERT |

**Total Tier 1:** 60-120 GPU-hours, ~8-10 weeks

---

## Priority Tier 2 (Near-Term — Next 2-4 Months)

| Priority | Proposal | Current Tier | Target Tier | GPU-Hours | Timeline | UToE Impact |
|----------|----------|--------------|-------------|-----------|----------|-------------|
| **2.1a** | Agency: ADC Response Slope | T4 | T6 | 20-40 | 3 weeks | FND-ENTS |
| **2.1b** | Agency: Curvature Scaling | T4 | T6 | 20-40 | 3 weeks | FND-ENTS |
| **2.1c** | Agency: Stability Band | T4 | T6 | 25-50 | 4 weeks | QM-INTERP |
| **2.1d** | Agency: Witness Function | T4 | T6 | 25-50 | 4 weeks | QM-INTERP |
| **2.1e** | Agency: Coordination Depth | T4 | T6 | 30-60 | 5 weeks | FND-ENTS |
| **2.2** | Causal DAG Audits | T4 | T7 | 50-100 | 8-10 weeks | MTH-CAT, QG-OBS |
| **2.3** | Loop Quench Test (Topology) | T4 | T6 | 40-80 | 7 weeks | MTH-DIFFGEO |

**Total Tier 2:** 210-420 GPU-hours, ~18-22 weeks

---

## Priority Tier 3 (Medium-Term — Next 4-6 Months)

| Priority | Proposal | Current Tier | Target Tier | GPU-Hours | Timeline | UToE Impact |
|----------|----------|--------------|-------------|-----------|----------|-------------|
| **3.1** | False-Vacuum & Void-Debt Asymmetry | T4 | T7 | 500-1000 | 18-26 weeks | QFT-RENORM, COS-ASYM, COS-INFL |
| **3.2** | Decoherence Portals (Dark Photons) | T1 | T6 | 100-200 | 14-18 weeks | COS-DM, EXP-SPECTRA, EXP-ASTR |
| **3.3** | Qualia Program | T1 | T4 | 200-400 | 23-30 weeks | QM-HILBERT, QM-INTERP |

**Total Tier 3:** 800-1600 GPU-hours, ~22-30 weeks

---

## Tier Promotion Priorities (Existing T2-T3 → Higher Tiers)

| Work Item | Current | Target | Effort | Priority | Rationale |
|-----------|---------|--------|--------|----------|-----------|
| **A6 Collapse** | T3 | T6 | 2-3 weeks | HIGH | Foundation for Agency Field |
| **RD Conservation** | T2 | T6 | 4-5 weeks | HIGH | Pattern formation validation |
| **Tachyonic Tube** | T2 | T8 | 15-20 weeks | MEDIUM | Predictive validation demo |
| **Metriplectic Suite** | T2 | T7 | 8-10 weeks | HIGH | Gold standard robustness |
| **FRW Continuity** | T2 | T6 | 3-4 weeks | MEDIUM | Cosmology w/ sources |

---

## Resource Summary (12 Months)

### By Quarter

| Quarter | GPU-Hours | Key Deliverables | Documents |
|---------|-----------|------------------|-----------|
| **Q1** | 140-200 | Thermo Routing T6, Wave Flux T6, SIE T6, Agency (1-2) | 4 RESULTS |
| **Q2** | 300-500 | Agency (3-5), Causal DAG T5, Loop Quench T6, A6→T6 | 5 RESULTS |
| **Q3** | 400-700 | False-Vacuum pilot+A, Dark Photon T2, Causal DAG T6 | 4 RESULTS |
| **Q4** | 400-700 | False-Vacuum B+C, Dark Photon T6, Robustness T7 | 4 RESULTS |

**Total:** ~1240-2100 GPU-hours, 16+ RESULTS documents, 10+ T6 claims

### By Tier

| Tier Level | GPU-Hours | Documents | Timeline |
|------------|-----------|-----------|----------|
| **Tier 1** | 60-120 | 3 | Months 1-2 |
| **Tier 2** | 210-420 | 7 | Months 2-6 |
| **Tier 3** | 800-1600 | 3 | Months 4-12 |
| **Promotions** | 170-360 | 5+ | Months 1-12 |

---

## Decision Matrix: Which PROPOSAL Next?

### If Goal is: **Quick Wins (T6 Results in <2 Months)**
→ Priority: **1.1, 1.2, 1.3**  
→ Rationale: Mature preregs, certified instruments, low risk

### If Goal is: **Agency/Information Theory**
→ Priority: **1.3, 2.1a-e**  
→ Rationale: Complete suite from SIE through coordination

### If Goal is: **Observational Physics**
→ Priority: **3.1, 3.2**  
→ Rationale: False-Vacuum and Dark Photon connect to experiments

### If Goal is: **Cross-Domain Validation**
→ Priority: **2.2, 2.3**  
→ Rationale: Causal DAG and Loop Quench test consistency

### If Goal is: **UToE Foundations**
→ Priority: **3.1, 3.2, 3.3**  
→ Rationale: Address QFT-RENORM, COS-*, EXP-* requirements

### If Goal is: **Robustness & Validation**
→ Priority: **Tier Promotions** (A6, RD, Metriplectic)  
→ Rationale: Establish T7-T8 framework for all future work

---

## Critical Path Analysis

### Dependency Chains

**Chain 1: Thermodynamic Routing**
```
Wave Flux Phase A (T2) ✓
  ↓
Wave Flux Phase B (T3) ← IMPLEMENT
  ↓
Wave Flux Phase C (T4-T6) ← IMPLEMENT
  ↓
Thermo Routing Biased (T6) ← IMPLEMENT
```

**Chain 2: Agency Field**
```
A6 Collapse (T3) ✓
  ↓
A6 → T6 Promotion ← PROMOTE
  ↓
ADC Response (T6) ← IMPLEMENT
  ↓
Curvature Scaling (T6) ← IMPLEMENT
  ↓
Stability Band (T6) ← IMPLEMENT
  ↓
Witness & Coordination (T6) ← IMPLEMENT
```

**Chain 3: Observational Bridge**
```
FRW Continuity (T2) ✓
  ↓
False-Vacuum Pilot (T5) ← IMPLEMENT
  ↓
False-Vacuum Main (T6) ← IMPLEMENT
  ↓
Dark Photon T2 (Fisher) ← IMPLEMENT
  ↓
Dark Photon T6 (Main) ← IMPLEMENT
  ↓
Observational Predictions ← DELIVER
```

### Parallelization Opportunities

**Can Run in Parallel:**
- Tier 1.1 + 1.2 + 1.3 (independent)
- Agency Field 2.1a-e (staged but parallel pilots)
- Causal DAG 2.2 (orthogonal to all)
- Loop Quench 2.3 (independent)

**Sequential Dependencies:**
- Wave Flux A → B → C → Thermo Routing
- A6 T3 → T6 before Agency 2.1a
- False-Vacuum pilot → main → robustness

---

## Risk Matrix

| Item | Technical Risk | Scientific Risk | Resource Risk | Priority Adjustment |
|------|----------------|-----------------|---------------|---------------------|
| 1.1 Thermo Routing | LOW | MEDIUM | LOW | Keep HIGH |
| 1.2 Wave Flux | LOW | LOW | LOW | Keep HIGH |
| 1.3 SIE | LOW | LOW | LOW | Keep HIGH |
| 2.1 Agency Suite | MEDIUM | MEDIUM | MEDIUM | Keep HIGH |
| 2.2 Causal DAG | MEDIUM | LOW | MEDIUM | Keep HIGH |
| 2.3 Loop Quench | MEDIUM | MEDIUM | LOW | Keep MEDIUM |
| 3.1 False-Vacuum | HIGH | HIGH | HIGH | Monitor closely |
| 3.2 Dark Photon | MEDIUM | MEDIUM | MEDIUM | Keep MEDIUM |
| 3.3 Qualia | HIGH | HIGH | HIGH | Consider defer |

**Risk Legend:**
- LOW: <20% chance of significant delay or pivot
- MEDIUM: 20-50% chance of delay or need for adjustment
- HIGH: >50% chance of delay or major pivot

---

## Implementation Checklist (Next 30 Days)

### Week 1: Setup
- [ ] Create GitHub project board with all PROPOSALs
- [ ] Assign priority labels (Tier 1/2/3)
- [ ] Set up development branches
- [ ] Reserve GPU time slots
- [ ] Configure artifact storage

### Week 2: Infrastructure
- [ ] Audit existing code in `Derivation/code/physics/`
- [ ] Document reusable components
- [ ] Create API interfaces for new experiments
- [ ] Set up CI/CD for new runners
- [ ] Update ROADMAP.md

### Week 3: Begin Implementation (Tier 1)
- [ ] Thermodynamic Routing: biased geometry loader
- [ ] Wave Flux: absorbing boundaries
- [ ] SIE: Q-tracking ODE integrator
- [ ] Unit tests for all new code
- [ ] Code review

### Week 4: Pilot Runs
- [ ] Run Tier 1 pilots on small domains
- [ ] Collect preliminary data
- [ ] Validate gate achievability
- [ ] Adjust parameters as needed
- [ ] Document lessons learned

### Week 5+: Main Runs & Next Tier
- [ ] Execute Tier 1 main runs
- [ ] Write RESULTS documents
- [ ] Update CANON_PROGRESS.md
- [ ] Begin Tier 2 planning
- [ ] Weekly progress reviews

---

## Success Metrics (12 Month Goals)

### Quantitative
- [x] 16+ new RESULTS documents
- [x] 10+ T6-level physics claims
- [x] 2-3 T7 robustness validations
- [x] 1-2 T8 predictive validations
- [x] <2100 GPU-hours consumed
- [x] Zero unresolved contradictions

### Qualitative
- [x] All Tier 1 PROPOSALs completed
- [x] 70%+ of Tier 2 PROPOSALs completed
- [x] 50%+ of Tier 3 PROPOSALs initiated
- [x] Observable predictions for ≥2 experimental areas
- [x] External collaboration framework established
- [x] Publication pipeline active (≥3 preprints)

### UToE Alignment
- [x] 80%+ of FND requirements addressed
- [x] 60%+ of MTH requirements addressed
- [x] 50%+ of QM/QFT requirements addressed
- [x] 40%+ of COS/EXP requirements addressed
- [x] Clear path to remaining requirements

---

## Quick Decision Guide

**Question:** "Should I implement this PROPOSAL next?"

**Check:**
1. ✓ Is it Tier 1? → YES, implement immediately
2. ✓ Does it unblock other work? → YES, high priority
3. ✓ Is instrument certified? → YES (lower risk)
4. ✓ Are resources available? → YES, proceed
5. ✓ Does it advance UToE goals? → YES, align to requirements

**If any NO:** Review priority matrix and dependencies

---

## Contact & Collaboration

**Internal:**
- Computational physics lead
- Theoretical physics consultant
- Software engineering support

**External:**
- Experimental groups (dark photon, neutrino)
- Causal set theory community
- Lattice QFT experts
- Psychophysics researchers (qualia)

**Engagement:**
- Conference presentations (APS, DPF)
- Workshop organization
- Preprint distribution (arXiv)
- GitHub Issues for technical questions

---

**Last Updated:** 2025-10-22  
**Next Review:** 2025-11-22 (monthly)  
**Owner:** VDM Project Leadership

**Related Documents:**
- `NEXT_STEPS_RECOMMENDATIONS.md` (detailed analysis)
- `VDM-Progress-Findings.md` (tier assessment)
- `ROADMAP.md` (milestone tracking)
- `CANON_PROGRESS.md` (status tracking)
- `UToE_REQUIREMENTS.md` (requirements table)
