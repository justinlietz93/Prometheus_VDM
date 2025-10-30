<!-- White Paper Proposal Template

ATTENTION! The proposal documents you create MUST BE whitepaper-grade documents with full structure, full narrative, MathJax-rendered equations (Meaning use Github MathJax syntax, $ ... $ and $$ ... $$ instead of other syntax), numeric figure captions tied to actual artifacts if using any for background, explicit thresholds with pass/fail gates, and provenance. You need to imagine if the document will be getting submitted for proposal at the most highly respected and quality Physics journals on Earth. These templates are engineering-grade and intended to be machine-actionable.

This template is the canonical authoring scaffold for VDM proposals (T0–T9 ladder). It is MANDATORY and IMPORTANT to include the substance of the outlined topics. The
length of the proposal should not exceed five U.S. letter-sized pages (including figures and references). Language and phrasing in this document should be objective and third perspective, placing the VDM as the subject. When describing methods the focus should be on what is predicted, planned, and what will be done rather than using perspective based verbiage (example: "We/I/They propose a metriplectic..." would be wrong. Instead, do this "Proposed in this document is a metriplectic..." or even "VDM proposes a metriplectic...")

# Tier Grades

This MUST included the grade of proposal this is. The grade of the proposal should be the same as the grade of the RESULTS_* if the runs pass.

Shown in a table below is the T0–T9 maturity ladder. This ladder distinguishes between:

- **Meters/instruments** (T2): Proven testing measurement apparatus
- **Phenomena** (T3+): Making physics claims with those proven meters
- **Preregistered claims** (T4-T6): Formal hypothesis testing
- **Robustness & validation** (T7-T8): Out-of-sample prediction
- **Reproduction** (T9): External verification

- **T0 (Concept)**
- **T1 (Proto-model)**
- **T2 (Instrument)**
- **T3 (Smoke)**
- **T4 (Prereg)**
- **T5 (Pilot)**
- **T6 (Main Result)**
- **T7 (Out-of-sample prediction)**
- **T8 (Robustness validation and parameter sweeps**
- **T9 (External verification/reproduction)** 

Additionally, if this PROPOSAL document is graded above T0, there should be existing supporting work referenced for each tier in sequence. For example, if a T4 experiment is proposed there must be a T0, T1, T2, and T3 that exists within the repository referenced with paths for any existing PROPOSAL and RESULTS documents listed. The figures and logs can also be referenced from each of those prior work items. There should be at a minimum of one for each, but no max limit.

In order for any experiment to run or pass, PROPOSAL_ documents MUST be created. Reference some brief approval standards here C:\git\Prometheus_VDM\derivation\code\common\authorization\README.md -->

# 1. {Tier Grade} - {Proposal Title}

> Created Date:  
> {git rev-parse HEAD} and put the latest commit here for provenance.
> Additionally, reate a hash salted with the commit and put it here.
> Proposer contact(s):  (<justin@neuroca.ai>)
> License: (Link to LICENSE file)
> Short summary (one sentence TL;DR):  

## 2. List of proposers and associated institutions/companies

List authors (Justin K. Lietz), affiliations, and roles (PI, implementer, approver).

## 3. Abstract

Include a very brief ( <200 words max ) summary of your proposal’s purpose, motivation, and anticipated goals.

## 4. Background & Scientific Rationale

Context, previous T0–T9 work (cite repository paths and prior PROPOSAL/RESULTS documents). Include information sufficient for someone with a background in physics, math, or engineering,
but not necessarily an expert in your subfield, to understand your proposal. Explain the maturity ladder and provenance. Any prerequisite experiments must be referenced here for clarity and completeness. Why this experiment is the next logical step, and why the prerequisites and gates are valid.

## Some questions to consider

- How novel is this experiment/project?
- Why does the experiment need to be done?
- Are there target findings that would be requisite for future work?
- What specific area of physics (quantum, gravity, electromagnetic, etc.) will this work impact?
- What fundamental question or problem will it address?
- What criticisms might there be of this approach? Should you re-think the proposal based on the answers to this question?
- What are the potential seen or unseen gaps, and what is being done to address them if any?

## 5. Intellectual Merit and Procedure

White paper proposals will be reviewed based on the Intellectual Merit and Broader Impacts of
the proposal. The Intellectual Merit will be judged based on:

**(1)** Importance of the scientific questions addressed.
**(2)** Potential broader impacts of the experiment.
**(3)** Clarity and reasonableness of the experimental approach.
**(4)** Planned level of rigor, and discipline.

## 5.1 Experimental Setup and Diagnostics

- What are the known, required parameters involved in the experiment?
- What diagnostics are needed (list and count) and how they are measured?
  - Include the number of each required.
- Might there be other unplanned equipment needed?
- Is there any new equipment, tools, or scripts required to be fabricated by the proposer?
  - (paths where created)
- Required parameters and defaults (list keys and units).

## 5.1.1 Pre-Run Config Requirements

- Required config and metadata:
  - Derivation/code/physics/{domain}/APPROVAL.json
  - Derivation/code/physics/{domain}/schemas/
    - {tag name}.schema.json
  - Derivation/code/physics/{domain}/specs/
    - {run name}.{version}.json

### APPROVALS.json

```json
{
  "preflight_name": "preflight runner name",
  "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must be created at Derivation/{domain}/ explicit review."
},
{
  "pre_registered": true,
  "proposal": "Derivation/{domain}/{Tier grade}_PROPOSAL_{Experiment Name}.md",
  "allowed_tags": [
    "{tag name}-{version number}"
  ],
  "schema_dir": "Derivation/code/physics/{domain}/schemas",
  "approvals": {
    "{tag name}-{version number}": {
      "schema": "Derivation/code/physics/{domain}/schemas/{tag name}.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto generated timestamp",
      "approval_key": "auto generated hashed key"
    }
  }
}
```

### PRE-REGISTRATION.json

- Required metadata:
  - Derivation/code/physics/{domain}/PRE-REGISTRATION.json
  - Domain and runner specific, but must include at minimum the following keys.

<!-- Minimum required keys only; values are placeholders. It is recommended to add more if there are any additional. -->
```json
{
  "proposal_title": "<string>",
  "tier_grade": "T0|T1|T2|T3|T4|T5|T6|T7|T8|T9",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["<name> <email>"] ,
  "hypotheses": [
    { "id": "H1", "statement": "<testable statement>", "direction": "increase|decrease|no-change" }
  ],
  "variables": {
    "independent": ["<var1>", "<var2>"] ,
    "dependent": ["<response>"] ,
    "controls": ["<control1>"]
  },
  "pass_fail": [
    { "metric": "<name>", "operator": ">=|<=|==|!=", "threshold": 0, "unit": "<unit>" }
  ],
  "spec_refs": ["<relative-path-to-spec>"] ,
  "registration_timestamp": "<ISO-8601>"
}
```

### Specs

- Required metadata:
  - Derivation/code/physics/{domain}/{run name}.{version}.json
  - Domain and runner specific, but must include at minimum the following keys.

<!-- Minimum required keys only; values are placeholders. It is recommended to add more if there are any additional. -->
```json
{
  "run_name": "<string>",
  "version": "<semver>",
  "tag": "<tag-identifier>",
  "schema_ref": "<path-or-uri-to-schema>",
  "parameters": {},
  "seeds": [0]
}
```

### Schemas

- Required metadata:
  - Derivation/code/physics/{domain}/schemas/{tag name}.schema.json
  - Domain and runner specific, but must include at minimum the following keys.

<!-- Minimum JSON Schema draft; extend per use-case. It is recommended to add more if there are any additional. -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "<schema-id>",
  "title": "<schema-title>",
  "type": "object",
  "properties": {},
  "required": []
}
```

## 5.2 Experimental runplan

- Describe how the resources in section 5.1 will be employed to answer the proposed scientific question(s).
- What is the estimated amount of runtime required to carry out the proposed plan?
- What is the plan of action for a successful experiment?
- What is the plan of action for a failed experiment?
- How will the results be published / displayed? (Review the Derivation/Templates/RESULTS_PAPER_STANDARDS.md document for Whitepaper grade format)
- Exact Cartesian product of independent variables (specify N, Δt, splits, λ, seeds).
- Estimated runtime per run and total estimated compute budget.
- Success and failure actions (contradiction handling, quarantine, publication policy).

## 6. Personnel

Describe the roles of the proposer (Justin K. Lietz) and what will be done by the proposer do to execute the goals of the project.

## 7. References

---

End of template. Authors should fill each numbered section and include machine-readable spec and schema files when submitting PRs.
