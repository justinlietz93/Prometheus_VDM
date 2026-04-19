# VDM Hard Implementation Matrix v0.1

## Purpose

This matrix converts the cross-paper invariants from:
- the VDM formal stack,
- the Aura distinction inventory,
- and the human learning / reading packet,

into **non-negotiable implementation requirements** for the UTE / UTD rewrite.

This is a **hard boundary document**. If an implementation violates a row marked **Hard**, it is rejected.

---

## Governing Law

**External stays external. Internal stays internal. Everything crosses only through the corresponding interface.**

Corollaries:
1. The core system does not touch the world directly.
2. The world does not touch the core system directly.
3. UTE is receptor transduction only.
4. UTD is actuator transduction only.
5. No live decoder is allowed to author output for the model.
6. No hidden persistence pockets are allowed in the interfaces.
7. The model's endogenous clock is sovereign for cognition.
8. External time may exist in the environment and logs, but may never silently drive model cognition.

---

## Interpretation of Column Labels

- **Invariant source**: the cross-paper reason this rule exists.
- **Hardness**: `Hard` means break = reject. `Strong` means may defer but may not contradict. `Future` means target architecture, not blocker for first pass.
- **UTE requirement**: what the receptor interface must do.
- **UTD requirement**: what the effector interface must do.
- **Forbidden patterns**: concrete things that must not appear in the implementation.
- **Required gates / telemetry**: concrete observables or tests required to verify compliance.

---

## Core Matrix

| ID | Invariant | Invariant source | Hardness | UTE requirement | UTD requirement | Forbidden patterns | Required gates / telemetry |
|---|---|---|---|---|---|---|---|
| M01 | Interface-only coupling | Primitive/effective distinction; measurement as bounded channel | **Hard** | All world→model transfer must pass through receptor transduction only | All model→world transfer must pass through actuator transduction only | Any direct world object mutation from core; any direct model-state mutation from environment | Static audit: no core module imports hardware/UI transport directly |
| M02 | Visible witness is not state | Phase Calculus lifted object vs witness | **Hard** | UTE may expose only sensed structure, not interpreted cognition | UTD may emit only rendered witness traces of model activity | Treating output text/audio as model state itself | Telemetry separates internal articulation state from emitted witness |
| M03 | No completion-branch authorship in live path | Shadow/Phase Calculus; Aura crude forced decoder finding | **Hard** | No semantic completion machinery on perception boundary | No lexicon / Markov / phrase template / macro composer in live outbound path | `lexicon.json`, n-grams, phrase templates, summary fallbacks, sentence macros in live articulation path | Code audit: live path contains zero lexical authoring modules |
| M04 | Endogenous cognitive time is sovereign | VDM endogenous clock / oscillatory physiology | **Hard** | UTE may not inject wall-clock cadence into cognition | UTD may not use wall time to decide model output timing | Passing elapsed wall time into connectome state-update as cognitive driver | Telemetry shows internal phase / SIE path as timing basis; no hidden wall-time driver inputs |
| M05 | Wall clock may appear only as sensed content or provenance | Boundary law + explicit time query exception | **Hard** | Time-of-day/calendar may only enter as explicit receptor content or external metadata | Same | Hidden scheduler time, arrival timestamps, or elapsed seconds influencing cognitive update | Distinct telemetry fields for provenance time vs model time |
| M06 | No hidden pockets | External/internal separation | **Hard** | Continuous media may not be re-perceived after passing unless externally paused/captured/recorded | Same | Secret interface caches, replay limbo, private revisit buffers masquerading as external availability | Gate: once source advances and no save/pause occurred, direct re-access must fail |
| M07 | Memory is not persistence | Human learning packet + VDM boundary law | **Hard** | If an external object disappears, only memory remains unless an external save existed | Same | Treating remembered content as externally re-openable without actuation | Telemetry distinguishes `memory_recall` from `external_reacquire` |
| M08 | Saving is an actuation, not an internal wish | Device externality | **Hard** | None | Saving/capturing/archiving must be real actuator events creating real external objects | Implicit save, hidden autosave as cognitive side effect | Every persistent object must have an explicit creation event |
| M09 | Reopening is reacquisition, not introspection | Device externality | **Hard** | Re-read of archived content must re-enter through receptor path | Same | Accessing archived content from internal memory channel | Every reopen produces a new receptor event trace |
| M10 | Continuous media is world-timed, model-sampled | Human perception of continuous streams; embodiment constraint | **Hard** | Streams advance externally regardless of model attention; model samples current signal on endogenous cadence | UTD may pause/record/seek only via explicit controls if device supports them | Freezing the live stream internally; revisiting vanished frames without external save/pause | Gate: stream progresses while model ruminates; revisit unavailable absent external record |
| M11 | Static/session artifacts are externally scoped objects | Mailbox/session semantics | **Hard** | Session object is perceivable only while externally present in chat/session/view | Same | Treating vanished session content as still externally openable | Gate: close session -> direct re-open fails unless externally persisted |
| M12 | Text intake must preserve full order and repetition | Human reading / low-level factorization | **Hard** | Ordered text stream must preserve every unit in sequence, including repeats | None directly | Unique-character collapse, set-unioned stimulation, whole-line semantic dump | Tests: `sassafrass`, `tintinnabulation`, combining marks preserve sequence |
| M13 | Text is sequentially sampled, not whole-line dumped | Reading research / eye-movement-like uptake | **Hard** | UTE exposes ordered slices, not one-shot whole-line injection | None directly | Entire line hitting connectome at once as one stimulation event | Telemetry: receptor slices are sequential and ordered |
| M14 | Receptor aperture may vary, but structure must remain ordered | Human reading packet | **Strong** | Slice width may adapt by internal dynamics (graphemes, subword spans, words, phrases), but must remain sequential and repetition-preserving | None directly | Hard-coding only one grapheme forever; or jumping to token semantics at boundary | Telemetry records slice width per engagement cycle |
| M15 | Boundary representation should stay low-level and medium-native | Infant phonetics / Dehaene reading / supramodal convergence downstream | **Hard** | UTE exposes receptor-native low-level structure first | UTD consumes actuator-native low-level structure first | Boundary tokenization as primary cognitive object; prepackaged semantic meaning injection | Audit: boundary types are medium-native, not LM-token-native |
| M16 | Downstream convergence, not boundary flattening | Modality-specific entry, supramodal downstream integration | **Strong** | Different media keep different entry laws | Different actuators keep different output laws | Forcing text, image, audio, and video into the same boundary object prematurely | Type audit of medium-specific transducers |
| M17 | Actuator basis belongs to the device, not to input history | Learned motor control over a device manifold | **Hard** | None | Output basis must be fixed by external device/transducer capabilities | Growing output alphabet from seen input symbols; soft lexicon reintroduction | Code audit: no input-history-dependent output basis growth |
| M18 | Articulation must be model-authored before release | Thought/execution split; Aura workaround evidence | **Hard** | None | Maintain an internal articulation buffer / actuator trace before emission | Release-time composition, release-time sentence generation | Telemetry chain: internal change → articulation formation → release → actuator trace |
| M19 | Release gate is release-only | Existing B1/valence agreement | **Hard** | None | Gate may allow/block emission timing only; it may not author the content | `if gate open: compose sentence now` | Test: identical buffer + different gate state changes only release, not authored content |
| M20 | Actuator traces may be rendered, but rendering is downstream witness only | Witness-not-state invariant | **Hard** | None | Rendered text/audio is produced from actuator trace | Rendering stage deciding content or filling missing content | Telemetry: actuator trace stored separately from rendered witness |
| M21 | Session engagement is optional and endogenous | Executive agency / endogenous timing | **Strong** | Model may ignore, defer, or engage with an offered session object | Same | Forced intake because object exists | Telemetry includes offered-but-unengaged objects |
| M22 | Rumination and external engagement must remain separable | Internal thought is internal | **Hard** | UTE must not keep making old external states present just because model is still thinking | Same | Hidden interface persistence during rumination | Gate: rumination with no save/capture cannot reacquire vanished external content |
| M23 | Interface objects are bookkeeping, not cognition | External encoder/receiver mechanism only | **Hard** | Object ids/cursors/session state live outside the model only | Same | Treating mailbox ids, file ids, offsets, cursors as model-internal semantic primitives | Review: interface metadata never enters core as ontology |
| M24 | Provenance and dashboard transport are not cognition | Logging externality | **Hard** | Live UI feed and archival logging are separate from receptor semantics | Same | Dashboard file tailing or archive format influencing cognition | Architecture split: in-memory/live feed separate from audit log |
| M25 | Tools/devices are external technologies, not internalized capacities | Device externality | **Future** | None | Screenshot, recorder, archive, pause, seek, etc. must exist as external controls/devices | Magical internal save, internal screenshot, implicit external control | Device actions always emit explicit actuator events |

---

## Medium-Specific Semantics Matrix

| Medium class | External persistence law | Lawful model interaction | Unlawful shortcut |
|---|---|---|---|
| Continuous stream (camera/mic/live video) | Source advances on world time regardless of attention | Sample current signal; think about memory trace; explicitly actuate pause/capture/record if device supports it | Freeze old stream state internally; revisit vanished stream content without external save/pause |
| Session artifact (chat message/image in active session) | Exists only while session/view still presents it externally | Engage now; ignore; return while session still exists; explicitly archive if supported | Treat closed/disappeared session object as still directly available |
| Durable artifact (file, archived image, saved clip, saved text) | Persists externally by virtue of real storage | Open/reopen through receptors after explicit save/archive or prior external existence | Access durable object through memory path alone |
| Interactive source (player, GUI, terminal, webpage) | Source evolves externally but may be changed by actuation | Pause, scroll, seek, save, reopen only by explicit control events | Internal control over external source without actuator event |

---

## Specific Kill-Switch Anti-Patterns

Any implementation containing one of these is rejected.

1. **Live decoder authorship**
   - lexicon lookup
   - Markov n-grams
   - phrase macros/templates
   - sentence fallback summaries
   - release-time sentence assembly

2. **Input-history-grown output basis**
   - "things the model has seen can enlarge the live articulation alphabet"

3. **Whole-line cognitive injection**
   - entire text line stimulates the connectome in one simultaneous semantic event

4. **Unique-symbol collapse**
   - repeated characters or repeated low-level units removed before receptor transduction

5. **Hidden replay pocket**
   - old live stream states remain directly accessible after they have passed externally without real external recording/pause/save

6. **Session limbo persistence**
   - closed/disappeared chat content remains directly openable through UTE

7. **Clock hijack**
   - wall clock or arrival timestamps silently influence cognition

8. **Save-by-thinking**
   - internal state alone creates external persistence without actuator event

9. **Render-authorship leak**
   - renderer fills in missing content or invents structure not present in articulation trace

---

## Minimum Acceptance Tests for First Rewrite

| Test ID | Required behavior |
|---|---|
| T01 | `Sassafrass` is transduced as full ordered repeated units, not collapsed unique symbols |
| T02 | `Tintinnabulation` preserves repeated letters and full sequence |
| T03 | Combining-mark text keeps base+mark ordering intact |
| T04 | A line of text is not delivered as one simultaneous stimulation blob |
| T05 | Output path contains no live lexicon / Markov / template authorship |
| T06 | Output basis is device-defined and fixed, not input-history-grown |
| T07 | Gate releases buffered articulation only; gate does not author it |
| T08 | Live stream cannot be revisited after it has passed unless the model externally paused/captured/recorded it |
| T09 | Closed/disappeared session content is unavailable unless externally archived/saved |
| T10 | Any saved external object has an explicit actuator creation event |
| T11 | Reopening a saved object creates a fresh receptor event |
| T12 | Provenance time and model time are logged separately |

---

## Implementation Priority Order

| Priority | Work item | Reason |
|---|---|---|
| P1 | Delete all live decoder-category authorship | Largest conceptual violation |
| P2 | Replace text whole-line injection with sequential ordered receptor slicing | Biggest receptor violation |
| P3 | Remove input-history-dependent output-basis growth | Prevents soft-lexicon regression |
| P4 | Preserve articulation buffer + release-only gate | Good structural split already identified |
| P5 | Make medium-specific semantics explicit in UTE | Prevent future category leakage |
| P6 | Split live dashboard transport from archival logging | Stops UI/log path from dictating architecture |
| P7 | Add explicit external devices (pause, capture, archive, reopen) | Enables lawful world interaction without hidden pockets |

---

## Final Design Reading

The correct architecture is not:

`world -> parser/decoder junk -> model -> sentence generator -> world`

The correct architecture is:

`world -> receptor transducer (UTE) -> core dynamics -> articulation formation -> release gate -> actuator transducer (UTD) -> rendered witness in world`

All richer structure must emerge **inside** that boundary discipline or remain explicitly external as a tool/device.

---

# Motor-Learning / Effector-Side Addendum v0.1

This addendum incorporates the motor-learning paper packet into the UTD/decoder side of the matrix. It is governed by the same boundary law: external stays external, internal stays internal, and all coupling crosses only through receptor/actuator interfaces.

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
