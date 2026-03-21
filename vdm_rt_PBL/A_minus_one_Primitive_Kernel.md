# A(-1) Primitive Kernel Specification

## Status
Draft specification for implementation. This document is **not** a CF and does not introduce new formal derivations. It is an implementation-specification constrained by the already-written canon. The kernel described here must not smuggle in objects that the CF stack says are derived.

## Purpose
Build the smallest executable engine whose **physics core** is only the A(-1) law and the root CF000 articulation logic. The engine must not begin from a lattice, graph, field, particle, metric, gauge group, external stimulus, or pre-given serialization axis. It must begin from a single unresolved origin and admit later structure only if that structure is forced by continued invariant-bearing under non-discharge.

The target is not “a small simulator.” The target is an origin-kernel whose repeated lawful execution can be inspected for the emergence of:

1. serial distinguishability,
2. proto-number / repeat-count structure,
3. orthogonal re-articulation,
4. 2D ORS completion,
5. the half-turn/opening condition and the first appearance of \(\pi\),
6. later carrier/adjacency structure,
7. later effective physics only after the earlier structures are actually present.

---

## Governing Rule
The engine may implement **only** the primitive contradictory-origin law in executable form:

- unresolved two-pole opposition is borne in one admissible origin,
- discharge into either isolated pole is forbidden,
- same-class continuation is allowed only while the invariant remains borne,
- when genuinely new invariant-bearing articulation in the current class is exhausted while unresolved burden remains, the minimum additional lawful structure must be admitted,
- the first irreducible such admission is orthogonal re-articulation.

That is the whole physics core.

No later physical object may appear in the kernel as a primitive. If a later object appears in code, it must appear only in a **diagnostic** or **extraction** layer outside the core update law.

---

## Canon Anchors This Specification Must Obey

### A(-1) / CF000 root licenses
Use the following as hard implementation constraints:

- The primitive law is unresolved two-pole opposition under non-discharge; same-domain saturation forces orthogonal re-articulation. fileciteturn48file1
- Same-domain saturation is logical exhaustion of genuinely new invariant-bearing articulation within the present admitted class, not merely temporal delay. fileciteturn46file5turn46file3
- Minimum protection forbids importing more structure than is required to keep the invariant borne. fileciteturn46file4turn46file5
- Boundary hosting is the correct behavior when bulk/same-class hosting saturates while unresolved burden remains; CF08 is a later explicit witness that saturation forces boundary-hosted modes. fileciteturn47file0

### CF00 / CF13 anchors
The kernel must respect the downstream order already fixed by canon:

- CF00 licenses \(\pi\) as the **unique least-positive ORS half-turn parameter**, not as an imported primitive constant. fileciteturn48file0
- CF13 closes that \(\pi\) is not imported, but is the first exact half-turn constant of the ORS orbit; chirality comes from the oriented non-equivalence of the two half-turn completions. fileciteturn47file3turn48file0

### CF14 anchor
The kernel must respect the general continuation law already extracted in temporal form:

- CF14 states that stationary action is the temporal effective invariant of **minimum admissible orthogonal articulation**. This is not a different law; it is the same root law on an admitted temporal path domain. fileciteturn46file3turn46file4

### CF-document discipline
The implementation spec must follow the same discipline as the CF documents:

- define primitive vs derived vs computational-only objects explicitly,
- do not state later objects before earlier ones that generate them,
- do not hide theorem-bearing logic behind convenience phrases,
- do not outsource essential ontology to code convenience. fileciteturn47file4turn47file5turn47file7

---

## Scope Lock
This kernel is responsible only for the **primitive-to-early-structural** regime:

- origin,
- serial articulation emergence,
- proto-number emergence,
- orthogonal re-articulation,
- early ORS/2D closure diagnostics.

This kernel does **not** primitively include:

- carrier geometry,
- differentiable fields,
- J/M split,
- gauge sectors,
- particle species,
- gravity,
- thermodynamics,
- electroweak / confinement / radiative corrections.

Those may appear only later as extracted effective structure if and when the primitive kernel earns the prerequisites.

---

## Ontology Table

### Primitive
These are the only ontic primitives the kernel may assume:

- **Origin**: one admissible bearer of unresolved two-pole opposition.
- **Pole opposition**: irreducible internal two-pole non-coincidence.
- **Non-discharge**: the bearer may not collapse into either isolated pole.
- **Bearing status**: whether the current articulation still lawfully bears the invariant.
- **Representability status**: whether the current articulation class can still express genuinely new invariant-bearing structure.

### Derived / emergent
These must **not** be inserted as primitives:

- serialization / successor order,
- 1D chain structure,
- number / count / magnitude classes,
- orthogonality as a named geometric object,
- 2D carrier,
- ORS orbit,
- \(\pi\),
- adjacency,
- lattice,
- fields,
- gauge, charge, mass, metric, force.

### Computational only
These may exist in implementation but are not ontic:

- memory indices,
- array order,
- loop counter,
- deterministic seed,
- storage containers,
- logging timestamps,
- debug labels.

A loop counter is **not** physical time. An array position is **not** a serialized articulation. A storage group is **not** a neighborhood.

---

## Forbidden Primitive Imports
The kernel core must not name or use, as ontic primitives:

- node
- edge
- graph
- lattice
- coordinate
- metric
- field
- particle
- stimulus
- observation event
- Laplacian
- boundary condition on a pre-existing space
- neighborhood or stencil
- force or potential
- gauge group
- mass
- energy functional
- entropy functional

If any of these appear, they belong in downstream extraction/diagnostic code, not in the core law.

---

## Computational Substrate Rule
The computational substrate may be extremely low level (Python + NumPy + Numba, or an even thinner binary kernel), but the execution substrate must not be confused with the ontic substrate.

Practical consequence:

- binary voltage states are allowed as **hardware support**,
- but the primitive origin is **not** a programmer bit,
- and implementation indexing must not stand in for emergent serialization.

The kernel may use the smallest computational structures available, but it must not let their convenience become ontology.

---

## Core Conceptual Distinction: Bearing vs Execution
The kernel needs two layers kept sharply separate.

### Ontic law
What the simulated world is actually allowed to do:

1. bear unresolved opposition,
2. continue while same-class bearing remains possible,
3. saturate when no genuinely new same-class invariant-bearing articulation remains,
4. force minimum additional structure only when same-class bearing fails while unresolved burden remains.

### Computational execution
What the computer must do to run the ontic law:

- inspect state,
- test admissibility predicates,
- update storage,
- record transitions.

A computational iteration is not itself a physical “step.” Physical succession must be extracted later from persistent lawful same-class continuation.

---

## Formal Objects Required by the Kernel

### 1. Primitive origin record \(\Omega\)
The engine begins with exactly one primitive record \(\Omega\) carrying unresolved two-pole opposition.

Minimum required primitive fields:

- `bearing`: whether unresolved opposition is still borne,
- `unresolved`: whether contradiction remains non-discharged,
- `class_id`: identifier of the current articulation class (primitive origin starts in the root class),
- `representability`: whether the current class still admits genuinely new invariant-bearing articulation,
- `extension_budget`: not a numeric energy, but an ordering marker used only to compare whether a candidate continuation adds no new structure, minimal new structure, or more-than-minimal new structure.

No geometric fields, coordinates, or adjacency fields are allowed here.

### 2. Articulation class \(R_n\)
An articulation class is an equivalence class of lawful invariant-bearing expressions that use the same kind of structure.

Examples by role only:

- root contradictory origin,
- serial articulation class,
- orthogonalized continuation class,
- later ORS-completion class.

The kernel must not predefine the full list. It may only track the currently admitted class and the minimal extension relation between classes.

### 3. Bearing predicate \(\mathsf{Bear}(x)\)
Returns true iff state \(x\) still bears both poles without discharge.

This is the most primitive admissibility test in the kernel. Any continuation that destroys unresolved opposition fails.

### 4. Same-class representability predicate \(\mathsf{Rep}_{R_n}(x)\)
Returns true iff the current articulation class still supports a genuinely new invariant-bearing continuation of \(x\) without adding a new irreducible structural mode.

This is the formal notion of “same-domain continuation.” It is not a coordinate step.

### 5. Saturation predicate \(\mathsf{Sat}_{R_n}(x)\)
The current class is saturated at \(x\) iff:

- unresolved burden remains borne,
- but there is no genuinely new same-class continuation left.

Equivalently:

\[
\mathsf{Sat}_{R_n}(x) \iff \mathsf{Bear}(x) = \text{true} \;\wedge\; \mathsf{Rep}_{R_n}(x) = \text{false}.
\]

This definition is the executable counterpart of canon’s “same-domain saturation”: logical exhaustion of genuinely new invariant-bearing articulation in the present class. fileciteturn46file5turn46file3

### 6. Least-extension selector \(\mathsf{LeastExt}(x)\)
When same-class representation fails, the kernel must admit the **least additional structure** that restores invariant-bearing. This is the executable form of minimum protection. fileciteturn46file4turn46file5

This selector does **not** minimize CPU cost, code size, or syntax length. It minimizes added ontic structure.

### 7. Orthogonal re-articulation relation \(x \rightsquigarrow x'\)
A new state \(x'\) is an orthogonal re-articulation of \(x\) iff:

1. \(x\) is saturated in its present class,
2. \(x'\) still bears the invariant,
3. \(x'\) cannot be represented inside the old class,
4. \(x'\) is the least extension satisfying 2 and 3.

This must be treated as a **new irreducible articulation class**, not merely another element in the old class.

---

## The Kernel Law in Executable Form

For any current state \(x\):

1. **Bearing check**
   - If \(\mathsf{Bear}(x)\) is false, the state is invalid. The kernel must treat this as contradiction/discharge and halt or quarantine.

2. **Same-class continuation test**
   - Determine whether there exists a continuation \(x'\) in the current articulation class \(R_n\) such that:
     - \(\mathsf{Bear}(x')\) is true,
     - \(x'\) is genuinely new relative to the already-realized same-class expressions,
     - no new irreducible structure has been imported.

3. **Least same-class continuation**
   - If one or more such continuations exist, choose the one with least additional ontic structure.
   - This repeated persistence is what later becomes serial articulation when stable ordered continuation is first extractable.

4. **Saturation detection**
   - If unresolved burden remains but no same-class genuinely new continuation exists, the class is saturated.

5. **Boundary-hosting transition**
   - When saturation occurs, unresolved burden is carried at the limit/interface of the current class rather than disappearing.
   - The kernel must mark this as a boundary-hosting event, not as annihilation. This follows the same constitutional logic later witnessed explicitly in CF08. fileciteturn47file0

6. **Least orthogonal extension**
   - Admit the minimal new articulation class that restores invariant-bearing.
   - This is the first orthogonal re-articulation.

7. **Repeat**
   - Continue applying the same law, without adding new physics rules.

This seven-part law is the complete kernel logic.

---

## How Serialization Must Emerge
Serialization is not allowed to be primitive. It emerges only when repeated same-class continuations stabilize into an irreversible dependence order.

### Necessary condition for first serialization
Serialization may be declared emergent only if the following hold:

1. there is a repeatable lawful continuation mode within one articulation class,
2. later continuation depends on earlier continuation being already borne,
3. the continuation sequence is not freely commutative,
4. the sequence can be recognized as an ordered chain of distinguishable invariant-bearing realizations.

This is the first true 1D substrate.

### Important warning
Implementation memory order, list position, or loop count may not be used as evidence that serialization has emerged. Serialization must be detected from the invariant-bearing relation itself.

---

## How Proto-Number Must Emerge
Number is not primitive. It emerges only after stable serialization exists.

### Proto-number criterion
Proto-number may be declared only if:

1. a lawful serialized chain already exists,
2. repeated equivalent articulation segments can be recognized as belonging to the same repetition class,
3. those repetition classes are stable under repeated realizations,
4. count is an external abstraction over those repetitions, not an inserted ontic primitive.

In other words, numbers are readouts of repeated serialized articulation, not the substrate that makes serialization possible.

---

## How Orthogonal Re-Articulation Must Be Understood Mechanistically
Orthogonal re-articulation is not “branch now” or “spawn child now.” It is what happens when same-class representability fails while bearing remains mandatory.

Mechanistically:

1. unresolved opposition persists,
2. same-class continuation has been exhausted,
3. discharge is forbidden,
4. therefore a new irreducible class must appear,
5. because it cannot be represented inside the old class, the new class is orthogonal in the relevant structural sense.

This is how a new axis of freedom first appears. Orthogonality is therefore a **forced minimal new expressivity**, not a geometric angle assumed in advance.

---

## How ORS and \(\pi\) Must Be Allowed to Emerge
The kernel must not program \(\pi\), quarter-turns, half-turns, circles, or trigonometric structure.

What it may do is permit the repeated orthogonal re-articulation process to generate a stable two-axis completion process. Only when such a completion process exists may the diagnostics ask whether an ORS-like orbit has emerged.

### ORS emergence criterion
An ORS-like structure may be declared only if:

1. two irreducible articulation axes have been earned,
2. there exists a lawful completion process between them,
3. repeated completion traces a stable closure/opening pattern,
4. there is a unique least-positive completion parameter for the first exact half-turn/opening condition.

Only then may the diagnostics identify that least-positive half-turn parameter with the canonically derived \(\pi\)-role. CF00/CF13 say that this quantity is not imported, but the first exact half-turn constant of the ORS orbit. fileciteturn48file0turn47file3

### Irrationality mechanism
The kernel does not directly “compute irrationality.” Instead, irrationality must emerge as the inability of the half-turn/opening relation to be finitely exhausted by any same-class finite capture mechanism once the continuous ORS closure process is present. That is the executable shadow of the CF13 result that \(\pi\) is not algebraically captured as a primitive finite closure but appears as the exact half-turn constant of an orbit completion process. fileciteturn47file3

---

## Diagnostic Layer (External to the Core)
All of the following belong outside the kernel core:

- logging,
- visualization,
- UI,
- serialization to disk,
- extraction of emergent chains,
- extraction of repetition classes,
- ORS detection,
- adjacency or carrier extraction,
- later field or graph fitting.

The kernel must be able to run without any of these. The diagnostics may observe the kernel, but must not feed back ontic structure into it.

This separation follows the same discipline as the CF/CFN split: the core formalism proves and defines; the executable/diagnostic layer witnesses and illustrates. fileciteturn47file4turn48file3

---

## Suggested Minimal Implementation Layers

### Layer A — kernel core
Only:

- primitive state container,
- bearing predicate,
- same-class representability predicate,
- least-extension selector,
- orthogonal re-articulation trigger,
- boundary-hosting marker.

### Layer B — trace buffer
Only:

- append-only record of kernel events,
- no interpretation beyond event identity and parent relation.

### Layer C — diagnostics
Separate module(s) that infer:

- serialization,
- proto-number,
- orthogonal class count,
- ORS-like closure,
- emergent adjacency / carrier.

No Layer C code may be called from Layer A.

---

## Implementation Constraints

1. The kernel should use the thinnest practical substrate available.
2. Classical binary execution is acceptable as hardware support, but binary values are not the ontic law.
3. NumPy/Numba are acceptable only as storage and execution aids, not as ontological shortcuts.
4. No graph, PDE, physics, mesh, or CA library is allowed in the core.
5. No predeclared constants from later physics are allowed in the core.
6. No explicit “step law” may be mistaken for physical time.
7. No explicit “bifurcate()” primitive may exist as ontology; orthogonal re-articulation must be the consequence of saturation under non-discharge.

---

## Minimum Deliverables for the First Engine
A first acceptable kernel implementation must provide:

1. one primitive origin state,
2. one explicit bearing predicate,
3. one explicit same-class representability test,
4. one explicit saturation criterion matching canon,
5. one explicit least-extension rule,
6. one explicit orthogonal re-articulation transition defined as a consequence of 3–5,
7. zero imported later physics objects,
8. a raw trace of events for external diagnostics.

If any later object is primitive, the engine is invalid.

---

## Validation Gates for the Kernel Specification

### G1 — Ontology purity
The core implementation contains no primitive lattice, graph, field, geometry, gauge, particle, or external-stimulus objects.

### G2 — Bearing discipline
Every state transition preserves the invariant-bearing condition or is rejected/quarantined as discharge.

### G3 — Saturation discipline
Orthogonal re-articulation occurs only when same-class genuinely new continuation is exhausted while unresolved burden remains.

### G4 — Minimality discipline
When extension occurs, the admitted new structure is the least extension that restores bearing.

### G5 — Serialization honesty
Any claim that serialization has emerged is based on extracted continuation order, not on storage order or loop count.

### G6 — ORS/\(\pi\) honesty
Any claim that ORS-like completion or \(\pi\)-role structure has emerged is made only after a two-axis completion process has actually been detected.

---

## Non-Negotiable Red-Team Checklist
Before accepting the kernel, ask:

- Did we secretly assume a successor relation?
- Did we secretly assume adjacency?
- Did we secretly assume time by equating iteration count with physical order?
- Did we secretly assume number by using integer labels as ontic count?
- Did we secretly assume bifurcation by naming a spawn operation instead of deriving re-articulation from saturation?
- Did we secretly assume a 2D closure or ORS orbit before two irreducible axes were earned?
- Did we secretly assume \(\pi\) instead of detecting a least-positive half-turn/opening parameter?
- Did we use implementation convenience as physical law?

If the answer to any of these is yes, the kernel is contaminated and must be rewritten.

---

## Practical Next Step
Write the first implementation against this spec with:

- one tiny kernel module,
- one append-only raw trace buffer,
- no diagnostics in the core,
- no reuse of the v9 runtime,
- no imported late-stack objects.

Then build external diagnostics to ask whether the kernel has actually earned:

1. serialization,
2. proto-number,
3. orthogonal re-articulation,
4. ORS-like closure,
5. the half-turn/opening constant role.

Until those are detected, the runtime has not yet earned later physics.
