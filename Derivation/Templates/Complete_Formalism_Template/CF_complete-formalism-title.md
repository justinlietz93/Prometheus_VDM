# CFx: Complete Formalism — {Complete Formalism Title}

Date: {YYYY-MM-DD}  
Status: Draft | Review | Completed Formalism  
Gap Module: {S# or program location if applicable}  
Proposer: {Your Name}  
License: See LICENSE

---

<!-- Markdown MathJax only: use $...$ and $$...$$ -->

## Governing Rule of This Document

This Complete Formalism (CF) is the root written source of truth for the specific formalism, derivation, or construction developed here.

This document is not a summary, not a bridge memo, not a notebook companion narrative, and not a thin wrapper around external canon. It must contain the actual derivation, definitions, assumptions, theorem statements, proof burden, validation logic, and evidentiary support needed to stand on its own.

All future work on this formalism builds from this CF. That includes CFNs, code, figures, numerical experiments, validation runs, proposal work, and later formal extensions.

### Consequence of this rule

For CF documents, the usual VDM anti-duplication rule is suspended where duplication is necessary for completeness.

That means:

- If an equation is required for understanding or proving the formalism here, it must appear here in full.
- If a definition is required for the derivation, it must appear here in full.
- If a theorem depends on assumptions, those assumptions must appear here in full.
- If a claim requires support, the support must appear here in this document.
- If a validation criterion is part of the argument, it must be stated here, even if it also exists elsewhere in canon.

Canonical anchors, registry references, and cross-links are still useful, but they are supplemental references only. They are not hyperlinks that replace actual derivation or actual support.

A reader must be able to reconstruct the logic of the formalism from this CF alone.

---

## Relationship to Canon and External Documents

Canon registries, prior CFs, specifications, notebooks, and references may be cited for:

- provenance
- alignment
- naming consistency
- cross-checking
- broader program integration
- executable realization
- historical context

They may not be used to outsource core work that belongs in this CF.

In particular:

- Do not replace a needed equation with an anchor.
- Do not replace a needed proof step with a citation.
- Do not replace a needed assumption with a link.
- Do not replace evidentiary support with “see notebook.”
- Do not replace theorem burden with “validated elsewhere.”

If something is essential to the formalism described here, it belongs here.

---

## Relationship to the CFN

The paired CFN is the notebook or executable realization of this same formalism.

Its purpose is to:

- recreate the CF computationally
- instantiate the formal construction in code
- generate computed examples
- produce figures and tables
- numerically witness claims already formalized here
- provide executable traceability for the written derivation

The CFN does **not** introduce new derivations, new theorem burden, or missing justification.

The CF must remain complete without the CFN.

A good rule is:

**The CF proves and defines. The CFN executes and illustrates.**

If the CF depends on the CFN for support, then the CF is incomplete.

---

## Executive Summary

State in 3–7 sentences:

- the physical or mathematical object under study
- the scope of the formalism
- the precise result established here
- what is primitive and what is derived
- what this CF contributes to the broader theory
- what remains outside scope, if anything

Then list the principal deliverables of this CF:

- definitions introduced or fixed here
- equations derived here
- theorems proven here
- algorithms or constructions forced by the derivation
- validation logic required by the formalism
- worked examples or executable witnesses paired in the CFN

---

## Read Me First: Writing Rules for CF Documents

1. This document must be self-contained at the level required to understand, test, and reuse the formalism.
2. Every theorem-bearing section must expose its proof burden directly.
3. No section may hide essential logic behind phrases such as:
   - “by covariance”
   - “by standard arguments”
   - “similarly”
   - “it follows directly”
   - “left to the notebook”
   unless the burden is genuinely trivial and already explicit in nearby text.
4. All dependency order must be honest. No theorem may use objects that have not yet been defined or derived.
5. Distinguish clearly between:
   - canonically established
   - proven in this CF
   - strongly suggested
   - working interpretation
   - speculative extension
6. If a statement is not theorem-grade, label it accordingly.
7. If a section is incomplete, mark the CF incomplete.

---

## 1. Scope, Ontology, and Primitive Commitments

State the true primitive object or objects of the formalism.

For each major object in the document, identify whether it is:

- primitive
- derived
- emergent
- gauge-redundant
- coordinate-dependent
- observable
- auxiliary
- computational only

Also state what is explicitly **not** allowed to be inserted as primitive if it is supposed to be derived.

This section should answer:

- What kind of thing is the theory actually claiming exists?
- What structure is taken as given?
- What structure must be earned by derivation?

---

## 2. Mathematical Setting and Definitions

Provide the full setting needed for the derivation.

Include, as needed:

- spaces, manifolds, bundles, state families, fields, operators
- coordinates and charts
- normalization conditions
- gauge redundancies
- regularity assumptions
- domains and codomains
- symbol definitions
- dimensional assignments and units
- boundary or support assumptions

If a symbol is used later in a proof, define it here or immediately before first use.

Do not rely on external symbol registries as substitutes for definitions required in this document.

---

## 3. Foundational Construction

Develop the formal construction in dependency-clean order.

This section should contain the actual derivation of the core structure from the primitive setup.

Use subsections that reflect real logical order, for example:

### 3.1 Primitive representatives and equivalence structure  
### 3.2 Quotient or reduced structure  
### 3.3 Induced geometric objects  
### 3.4 Metric / symplectic / curvature decomposition  
### 3.5 Derived evolution law  
### 3.6 Constitutive or closure structure  
### 3.7 Support / locality / admissibility structure

Do not state later objects before earlier ones that generate them.

If an object such as $g$ or $\Omega$ is derived from a QGT or related induced structure, then that inducing structure must be fully established before any theorem that depends on $g$ or $\Omega$.

---

## 4. Main Theorems and Proofs

State each principal theorem in full.

For every theorem include:

- exact hypotheses
- exact conclusion
- scope of applicability
- proof
- failure conditions or non-applicability conditions where relevant

Proofs must be explicit enough that the derivation can be audited from this document alone.

If a proof depends on a lemma, include the lemma here unless it is genuinely elementary and already proven in this CF.

If a proof imports a known external theorem, state exactly which part is imported and why its hypotheses apply here.

Do not compress proof-bearing sections into summary prose.

---

## 5. Derived Physical Consequences

Once the main construction is complete, derive the physical consequences that are forced by it.

Examples may include:

- conservation structure
- monotonic quantities
- degeneracy conditions
- constitutive equivalence classes
- gauge-hosting consequences
- locality or support consequences
- admissibility conditions
- observable consequences

Every such consequence must be traceable to the derivation already established above.

No consequence may be introduced as a design choice if it is supposed to be a forced result.

---

## 6. Validation Logic and Evidentiary Support

This section belongs in the CF, not just in the CFN.

State how the formalism is supported, constrained, or falsified.

Include, where applicable:

- mathematical consistency checks
- structural identities
- limiting cases
- invariance checks
- compatibility conditions
- observability map
- measurable quantities
- predicted qualitative behavior
- numerical criteria that would witness the formal result
- conditions under which the formalism would fail

This section must explain what counts as evidence **for** the formalism and what would count as evidence **against** it.

If numerical or computational tests are required, state them here in words and equations. The CFN may implement them, but the CF must define them.

---

## 7. Worked Example or Minimal Realization

Provide at least one worked specification or minimal realization of the formalism.

Include:

- chosen setup
- parameter values or parameter regime
- assumptions
- expected behavior
- what quantities are computed
- what success or failure would look like

This may be analytic, semi-analytic, or computationally specified.

Do not place the worked-example logic only in the CFN.

---

## 8. CFN Pairing and Executable Traceability

Describe how the paired CFN mirrors this document.

The mapping should be 1:1 in structure where possible.

For each major section, state:

- the corresponding notebook segment
- the quantities instantiated there
- the diagnostics emitted there
- the figures or tables generated there
- which claims from this CF are being numerically witnessed

Important rule:

The CFN mirrors this CF.  
It does not repair omissions in this CF.

---

## 9. Assumptions, Limits, and Open Boundaries

List all assumptions clearly.

Separate:

### 9.1 Assumptions used in the derivation  
### 9.2 Limits of applicability  
### 9.3 Claims established here  
### 9.4 Claims not established here  
### 9.5 Open problems or future extensions

If some desired claim is not actually proven, say so plainly.

Do not allow aspirational language to masquerade as closure.

---

## 10. Integration with Broader VDM Theory

Explain how this formalism connects to the broader program.

This section is for:

- theory placement
- relation to other CFs
- relation to canon registries
- relation to broader modules or programs
- downstream implications

This section must not carry proof burden that belongs earlier.

---

## 11. References and Provenance

Include:

- internal canon references
- prior CF references
- external literature
- provenance notes if needed

Internal anchors are welcome here, but they remain references only.

They do not substitute for derivation already required above.

---

## Appendix A. Symbol Table

List symbols used in this CF with meanings, dimensions, and units.

You may align with broader symbol registries, but this appendix must still be sufficient for the reader of this CF.

---

## Appendix B. Dependency Audit

Provide a compact dependency map:

- which objects are primitive
- which are derived
- which theorems depend on which constructions
- where each main conclusion is proven

This appendix is intended to make hidden dependency inversion impossible.

---

## Appendix C. CFN Traceability Table

For each major CF section, record the corresponding CFN realization.

Suggested columns:

- CF section
- CFN segment or tag
- quantities instantiated
- diagnostics emitted
- claims witnessed
- artifacts produced

---

## Acceptance Checklist

A CF is only complete when all of the following are true:

- [ ] The primitive ontology is stated clearly.
- [ ] All derived objects are earned in logical order.
- [ ] All equations needed for understanding the formalism are present in the document.
- [ ] All theorem-bearing claims are stated with explicit hypotheses.
- [ ] All proof-bearing claims have actual proofs or explicitly delimited imported theorems.
- [ ] No essential burden has been outsourced to anchors, canon registries, or the CFN.
- [ ] Validation logic and evidentiary support are stated in the CF itself.
- [ ] The worked example or minimal realization is specified in the CF itself.
- [ ] The role of the CFN is executable realization only.
- [ ] Any non-theorem-grade claim is explicitly labeled.
- [ ] Any incomplete section is marked honestly.
- [ ] A reader could reconstruct the formalism from this CF without needing hidden material elsewhere.

If any box above is false, the CF is not finished.
