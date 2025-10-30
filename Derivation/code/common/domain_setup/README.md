# Domain Setup Tools

This allows the user or an agent to run a single command to scaffold a template domain for experiments. Doing so creates these directories:

## Pre-Run Config Requirements

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

## README.md

This should be automatically created from a template skeleton to include blank sections that would be manually filled out with important, interesting, or domain specific details like equations, constants, symbols, or other items used that might also be documented in the global "all-caps" files at the root of Prometheus_VDM/Derivations/ (EQUATIONS.md for example).

Any items that this experiment would (or will) be referencing, updating, adding, or removing from a global canon file in the liste below should include a direct link in the README.md.

[](Derivation/ALGORITHMS.md)
[](Derivation/AXIOMS.md)
[](Derivation/BC_IC_GEOMETRY.md)
[](Derivation/CANON_MAP.md)
[](Derivation/CANON_PROGRESS.md)
[](Derivation/CHRONICLES.md)
[](Derivation/CONSTANTS.md)
[](Derivation/DATA_PRODUCTS.md)
[](Derivation/DIMENSIONLESS_CONSTANTS.md)
[](Derivation/EQUATIONS.md)
[](Derivation/NAMING_CONVENTIONS.md)
[](Derivation/OPEN_QUESTIONS.md)
[](Derivation/ROADMAP.md)
[](Derivation/SCHEMAS.md)
[](Derivation/SYMBOLS.md)
[](Derivation/TIER_STANDARDS.md)
[](Derivation/UNITS_NORMALIZATION.md)
[](Derivation/UToE_REQUIREMENTS.md)
[](Derivation/VALIDATION_METRICS.md)
