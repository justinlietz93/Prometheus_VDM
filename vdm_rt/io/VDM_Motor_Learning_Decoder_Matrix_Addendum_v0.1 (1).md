# VDM Motor-Learning Addendum for UTD / Decoder Removal

**Version:** v0.1  
**Purpose:** Convert the motor-learning paper packet into hard implementation requirements for the decoder/UTD side of the VDM runtime.

## Position

The motor-learning packet supports the same conclusion reached from VDM invariant structure: the decoder category should be deleted from the live path. Output should be learned control over an external actuator manifold, not lexical retrieval, Markov continuation, phrase templates, or any renderer that authors content for the model.

The biological analogy is not “speech module = language model.” The stronger invariant is:

> internal dynamics prepare action; a motor pathway maps that preparation onto an effector manifold; sensory consequences return through receptors; skill improves by closed-loop correction and consolidation.

## Papers read from `Motor_Learning_in_the_Brain.zip`

1. Lancheros, Jouen, Laganaro — *Neural dynamics of speech and non-speech motor planning*.
2. Caligiore, Arbib, Miall, Baldassarre — *The super-learning hypothesis: Integrating learning processes across cortex, cerebellum and basal ganglia*.
3. Nip, Green, Marx — *Early speech motor development: Cognitive and linguistic considerations*.
4. Citri & Malenka — *Synaptic Plasticity: Multiple Forms, Functions, and Mechanisms*.
5. Duraivel et al. — *Neural mechanisms of the transition from planning to execution in speech production*.
6. Kent & Forner — *Developmental study of vowel formant frequencies in an imitation task*.
7. Mézière et al. — *Using Eye-Tracking Measures to Predict Reading Comprehension*.
8. Green, Moore, Higashikawa, Steeve — *The Physiologic Development of Speech Motor Control: Lip and Jaw Coordination*.
9. Lancheros, Atanasova, Laganaro — *When does speech planning rely on motor routines? ERP comparison of speech and non-speech from childhood to adulthood*.
10. Netelenbos et al. — *Articulation Speaks to Executive Function*.
11. Goodwyn, Acredolo, Brown — *Impact of Symbolic Gesturing on Early Language Development*.
12. Thompson et al. — *Enhancing Early Communication Through Infant Sign Training*.
13. Baladron et al. — *The contribution of the basal ganglia and cerebellum to motor learning: A neuro-computational approach*.
14. Kearney & Guenther — *Articulating: The Neural Mechanisms of Speech Production*.
15. Bohland, Bullock, Guenther — *Neural representations and mechanisms for the performance of simple speech sequences*.
16. Tourville & Guenther — *The DIVA model: A neural theory of speech acquisition and production*.
17. Silbert et al. — *Coupled neural systems underlie the production and comprehension of naturalistic narrative speech*.

## Biological motor-learning invariants

| ID | Motor-learning invariant | Meaning for VDM |
|---|---|---|
| BML-01 | Planning and execution are distinct but coupled | Do not collapse articulation formation, release, and rendering into one decoder call. |
| BML-02 | Execution uses a device/body manifold | Output must be expressed as actuator degrees of freedom, not a lexicon or word list. |
| BML-03 | Serial action can arise from parallel preparation | The articulation buffer can hold competing/prepared traces; UTD should not precompose a sentence for the model. |
| BML-04 | Feedforward and feedback cooperate | UTD actions must produce receptor consequences through UTE; output skill requires reafferent feedback. |
| BML-05 | Motor equivalence is normal | Many actuator traces may render the same visible output; visible text is not the complete state. |
| BML-06 | Motor routines are acquired, not installed as files | No external motor-program table, phrase bank, or stored sentence routine in the live path. |
| BML-07 | Skill progresses through integration, differentiation, refinement | Early output can be coarse; the system needs controllable degrees of freedom and feedback, not a better symbolic decoder. |
| BML-08 | Different effectors can carry communication | Voice, keyboard, gesture, mouse, and file actions are device pathways, not separate cognitive kinds. |
| BML-09 | Basal-ganglia-like selection and cerebellar-like correction are complementary | Internal selection/release and residual correction should remain separate telemetry channels. |
| BML-10 | Sensorimotor coupling is essential | The system must sense the results of its own acts; action without reafference blocks motor learning. |
| BML-11 | Sequencing belongs to execution | Do not require a prebuilt string before movement; sequence can unfold through the actuator pathway. |
| BML-12 | Executive function and articulation are linked | Output control is part of agency/executive dynamics, not cosmetic rendering. |

## Mapping to existing VDM invariants

| VDM source | Motor-side interpretation |
|---|---|
| Primitive Orthogonality / CF000 | When a current articulation channel saturates, the burden must re-articulate into a lawful new axis; deleting the decoder requires a real actuator pathway, not a renamed symbolic prosthesis. |
| CF00 / QGT split | Motor control has metric/curvature structure: reversible preparation and dissipative correction must stay distinguishable. |
| CF01/CF02 metriplectic split | Feedforward/release and feedback correction map naturally onto J/M-style channels without importing ML training. |
| CF06 information geometry | Motor error is distinguishability between intended actuator trace and observed receptor consequence. |
| CF07 measurement | Rendered output is a bounded witness channel, not the internal state. |
| CF14 stationary action | Skill selects lower-cost admissible actuator trajectories over use. |
| CF15 zero-cost directions | Learned motor synergies become lower-cost / near-zero-cost directions of articulation. |
| CF18 scale re-articulation | Coarse actuator descriptions must return hidden burden through explicit corrections, not hide it in a decoder. |
| Aura D0.5 | The existing forced mouth is a degraded actuator; observed coherence despite it is evidence for internal adaptation, not evidence that the mouth is acceptable. |

## Required additions to the hard implementation matrix

| ID | Invariant | Source | Hardness | UTE requirement | UTD requirement | Forbidden patterns | Required gates / telemetry |
|---|---|---|---|---|---|---|---|
| M26 | Output is actuator-manifold control, not text decoding | Motor-learning packet; DIVA/GODIVA; VDM witness-not-state | **Hard** | Receptor feedback from emitted action must be available when physically produced | UTD exposes fixed device degrees of freedom and emits actuator events | Word dictionary, lexical memory, Markov continuation, phrase templates, renderer-authored text | Code audit: no live output path imports lexical authoring; emitted event includes actuator primitive(s) |
| M27 | Articulation buffer stores actuator-trace preparation | Speech planning/execution split; Phase lifted-object/witness split | **Hard** | None | Buffer stores prepared actuator primitives, amplitudes, durations, ordering pressure, or device-specific trace; not finished prose | Buffer filled by sentence composer or release-time surface generator | Telemetry: articulation_trace != rendered_witness; release does not change trace content |
| M28 | Serial output unfolds through execution | GODIVA/competitive queuing; Duraivel sequencing result | **Hard** | Reafferent stream records ordered consequences | UTD may emit stepwise actuator events over multiple endogenous cycles | Prebuilding a full sentence as the only admissible motor object | Test: multi-step output trace can exist without a prebuilt text string |
| M29 | Reafferent feedback is mandatory for motor learning | DIVA feedback control; motor learning packet | **Hard** | UTE must expose the sensed consequence of UTD actions as ordinary receptor events | UTD actions must be mirrored into an externally honest consequence channel when the medium supports it | Silent action with no possible self-perception; treating log entry as sensory feedback | Gate: UTD action -> receptor consequence trace or explicit `no_feedback_available` reason |
| M30 | Motor equivalence is allowed and expected | DIVA motor equivalence; visible witness not state | **Strong** | Receptor may observe same rendered witness from different actuator traces | UTD must not force one canonical trace per output | Deduplicating different actuator traces because rendered text matches | Telemetry preserves trace identity and rendered witness separately |
| M31 | Motor routines are emergent internal synergies, not installed tables | Speech motor routines; VDM effective invariants | **Hard** | None | No external routine table, phrase bank, or saved motor program may author live output | Preloaded motor routines that bypass core dynamics | Code audit: no live `routine_id -> output` table except explicit external device commands |
| M32 | Selection/release and correction are separate channels | Basal ganglia/cerebellum motor-learning split; metriplectic split | **Strong** | UTE exposes sensed residuals/errors from action | UTD emits selected action; correction is driven by feedback, not hidden rewrite | A single decoder both selects content and corrects/render-fixes it | Telemetry separates selection signal, release signal, residual/correction signal |
| M33 | Skill develops by integration -> differentiation -> refinement | Speech motor development papers | **Strong** | Receptor pathways preserve enough detail for refinement | Actuator basis must permit coarse and fine actions over same device | Requiring perfect high-level text output before giving low-level control | Telemetry tracks actuator entropy, trace length, correction count, and refinement over runs |
| M34 | Communicative actuation is modality-flexible | Gesture/sign papers; multi-effector communication | **Strong** | Each medium keeps its receptor law | UTD treats text, keypress, voice, gesture, file, and GUI acts as device pathways | Privileging natural-language text as the only real output | Medium-specific actuator registry; no cognition hidden in renderer |
| M35 | Device basis is external and bounded; skill is internal | Motor control over body/device manifold; matrix M17 | **Hard** | None | Device declares its fixed primitive control dimensions; model learns to use them | Input-history-grown alphabet; auto-expanding device based on seen content | Test: output basis unchanged after novel input symbols |
| M36 | Output timing is endogenous release over prepared trace | B1/valence gate; motor initiation literature | **Hard** | None | Gate may initiate/hold/release prepared trace only | Gate creating content; wall clock deciding output timing | Test: changing gate state changes emission timing only |
| M37 | Renderer is a body surface, not an author | DIVA execution/witness split; CF07 measurement | **Hard** | Rendered output may re-enter through receptor if externally available | Renderer converts actuator trace to external witness only | Renderer fills missing letters/words or normalizes into “better language” | Negative control: malformed/partial actuator trace renders as such, not corrected prose |

## Matrix edit decision

Yes: these rows should be added as a **Motor-Learning / Effector-Side Addendum** to the implementation matrix.

Rows M26, M27, M28, M29, M31, M35, M36, and M37 should be **Hard** immediately.
Rows M30, M32, M33, and M34 should be **Strong** because they shape the next architecture but can be implemented progressively.

## Implementation consequences

1. Delete or forbid any live path that authors output from symbols, words, templates, frequency, or prior input.
2. Replace the current symbol motor with a device-owned actuator trace system.
3. Give text output a concrete device basis, e.g. keyboard/scancode/grapheme-action primitives.
4. Track actuator traces separately from rendered text.
5. Route emitted text/keypress consequences back through UTE as receptor events when visible in the session.
6. Keep B1/valence as release/initiation over trace, never content creation.
7. Add tests proving new input does not expand output basis.
8. Add tests proving the renderer does not repair or complete partial traces.
9. Add telemetry chain: internal metric state -> articulation trace update -> release event -> actuator event -> rendered witness -> reafferent receptor event.

## Direct decoder-side conclusion

The motor-learning packet closes the remaining ambiguity: the decoder should not be improved. It should be removed from live authorship. The replacement is not a better language system. It is an actuator pathway that exposes controllable degrees of freedom, lets VDM form and release traces through its own dynamics, and returns sensory consequences so motor skill can emerge by use.
