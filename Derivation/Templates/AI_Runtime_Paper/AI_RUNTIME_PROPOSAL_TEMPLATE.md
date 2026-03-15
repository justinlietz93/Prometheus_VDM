<!-- AI Runtime Proposal Template

ATTENTION! This template adapts the VDM proposal discipline to runtime / cognition experiments rather than physics-only branch work. It is intended for machine-actionable, whitepaper-grade preregistration and internal review. The language should remain objective and third-person where practical, with the runtime or experiment named as the subject. Use GitHub MathJax syntax for equations where needed.

Core adaptation:
- Physics proposals ask whether nature satisfies a constrained mathematical claim.
- Runtime proposals ask whether the VDM substrate exhibits a constrained organizational behavior under specified inputs, meters, and gates.

This template should be used for runtime experiments that probe:
- invariant extraction
- basin formation
- bridge formation across expressions
- regime changes
- transfer episodes
- phenomenology-class inference
- bounded-observation runtime behavior
- self-organization under staged perturbation

The document should remain concise but complete. Five U.S. letter-sized pages is a good target for internal proposals, but longer is acceptable when necessary to kill ambiguity.

Tier guidance:
- T0: concept seed
- T1: toy runtime formalization
- T2: instrument / meter calibration
- T3: smoke test with no strong cognition claim
- T4+: preregistered runtime claims, robustness, OOS, and external falsification
-->

# 1. {Tier Grade} - {Runtime Proposal Title}

> Created Date:  
> Git Commit:  
> Salted Provenance Hash:  
> Proposer Contact(s):  
> Runtime / Branch Tag(s):  
> License:  
> Short Summary (one sentence TL;DR):  

## 2. Proposers and Roles

List authors, affiliations, and roles (PI, runtime implementer, reviewer, approver).

## 3. Abstract

Provide a brief summary (<200 words) of:
- the runtime behavior being tested,
- why it matters,
- what the staged inputs are,
- what would count as success or contradiction.

## 4. Background and Runtime Rationale

Explain:
- what invariant, behavior, or mechanism is under test,
- why the proposed experiment is the next logical step,
- what prior runtime work, canon documents, or observed behaviors justify the experiment,
- what this experiment can and cannot claim.

Reference relevant canon paths, prior notes, and any required meters.

Questions to resolve:
- What hidden organizer or runtime principle is under test?
- Why should this behavior emerge in VDM rather than a static encoder?
- What confounds could mimic success?
- What failure modes would still be informative?
- What future runtime or physics work would depend on this outcome?

## 5. Intellectual Merit and Runtime Procedure

The merit of a runtime proposal is judged by:
1. importance of the runtime question,
2. clarity of the invariant under test,
3. adequacy of the meters and diagnostics,
4. discipline of pass/fail routing,
5. value of the expected negative result.

## 5.1 Runtime Setup and Diagnostics

Specify:
- runtime build / branch / commit,
- required configuration,
- state initialization policy,
- ingestion schedule,
- observation budget,
- logging budget,
- seeds,
- any bounded-observation restrictions.

List each meter / diagnostic with:
- name,
- purpose,
- expected direction if applicable,
- unit or representation,
- sampling cadence.

Examples:
- basin_count
- bridge_count
- basin_retention
- change_score
- cohesion_components
- vt_unique
- refresh_horizon_ticks
- say/output microstructure
- local motif persistence
- invariant_residual
- contradiction flags

## 5.1.1 Pre-Run Requirements

Required artifacts should be defined before runs that write official results:
- approval manifest
- preregistration metadata
- runtime spec JSON
- schema JSON
- proposal markdown path
- seeded input pack path(s)

Minimum preregistration metadata:

```json
{
  "proposal_title": "<string>",
  "tier_grade": "T0|T1|T2|T3|T4|T5|T6|T7|T8|T9",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["<name> <email>"],
  "runtime_branch_tags": ["<tag>"],
  "hypotheses": [
    { "id": "H1", "statement": "<testable runtime statement>", "direction": "increase|decrease|formation|stability|split|no-change" }
  ],
  "inputs": {
    "families": ["<path1>", "<path2>"],
    "schedule": "<staged ingestion policy>"
  },
  "variables": {
    "independent": ["<var1>", "<var2>"],
    "dependent": ["<response>"],
    "controls": ["<control1>"]
  },
  "pass_fail": [
    { "metric": "<name>", "operator": ">=|<=|==|!=", "threshold": 0, "unit": "<unit>" }
  ],
  "registration_timestamp": "<ISO-8601>"
}
```

## 5.2 Experimental Runplan

Describe:
- exact input order or randomization policy,
- whether expressions are injected one per line / one per event,
- washout or stabilization intervals,
- repeated exposures,
- ablations,
- controls,
- contradiction handling,
- publication policy.

Include the Cartesian product of major independent variables:
- family,
- order policy,
- seed,
- observation budget,
- stabilization ticks,
- runtime mode.

## 5.3 Hypotheses, Nulls, and Gates

State each hypothesis clearly.

For each hypothesis include:
- null hypothesis,
- primary metric(s),
- threshold,
- contradiction rule,
- what result would count as ambiguous rather than pass/fail.

## 5.4 Risks and Confounds

Address:
- order effects,
- superficial syntax pooling,
- meter leakage / god-meter contamination,
- insufficient stabilization time,
- path dependence hiding deep invariants,
- bounded-observation failure,
- apparent basin formation without transfer.

## 6. Personnel

Describe who will:
- prepare inputs,
- execute runs,
- review meters,
- adjudicate contradictions,
- write results.

## 7. Expected Artifacts

List planned outputs:
- proposal markdown,
- prereg JSON,
- config/spec JSON,
- runtime logs,
- per-run CSV/JSON,
- figures,
- results paper path.

## 8. Promotion / Demotion Logic

State what PASS promotes to the next tier and what FAIL produces instead:
- contradiction report,
- meter-repair task,
- representation redesign,
- runtime branch quarantine,
- follow-up T1/T2 proposal.
