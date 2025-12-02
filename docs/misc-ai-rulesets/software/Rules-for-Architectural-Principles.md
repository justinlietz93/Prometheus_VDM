# Rules for Architectural Principles

**Generated on:** October 27, 2025 at 4:40 PM CDT

This document synthesizes technical rules, syntax requirements, and architectural constraints across various segments of a larger document, providing a single, cohesive, and de-duplicated master list of commandments.

---

## I. Architectural Principles & Design

1. **Abstraction & Simplicity:** Architectures must be abstractions to manage complexity, simplifying system understanding by suppressing unnecessary detail and focusing on public element details, excluding private implementation.
2. **Decision Identification:** Architects must identify all decisions that comprise the architecture.
3. **Reasoning Support:** Architectural structures must support reasoning about the system and its properties, particularly attributes important to stakeholders.
4. **Conceptual Integrity:** The architecture must possess conceptual integrity and technical consistency, ensuring the same approach is applied consistently across the system for similar concerns (e.g., error handling, logging, user interaction).
5. **Module Design:** Architecture must feature well-defined modules with functional responsibilities assigned based on information hiding and separation of concerns.
6. **Information Hiding:** Information-hiding modules must encapsulate volatile elements to insulate software from changes, exposing only a well-defined interface.
7. **Modifiability:** Design decomposition structures to localize changes within a few (preferably small) modules to enhance system modifiability.
8. **Independence:** Design module interfaces to enable development teams to work largely independently.
9. **Data Flow Separation:** Separate modules that produce data from modules that consume data.
10. **Consistent Interaction:** The architecture must feature a small number of simple, consistent component interaction patterns throughout the system.
11. **Resource Contention:** Define and clearly specify a small, specific set of resource contention areas and their resolution within the architecture.
12. **Constraint Adherence:** Software architecture must adhere to all system and enterprise constraints.
13. **Technology Independence:** Architecture must not depend on a particular version of a commercial product or tool. If such a dependency is unavoidable, structure the architecture for straightforward and inexpensive version changes.
14. **Quality Attributes Integration:** Design solutions for quality attribute requirements (e.g., security, high performance, safety) into the system’s architecture from the beginning; they cannot be "bolted on" late in development.
15. **Tradeoffs:** Make appropriate tradeoffs when designing to satisfy conflicting quality attribute requirements; do not attempt to achieve quality attributes in isolation.
16. **Pattern & Tactic Usage:** Achieve quality attributes using well-known architectural patterns and tactics, unless requirements are unprecedented; refine design tactics as they are applied to system design.

## II. Architectural Structures & Views

1. **Module Elements:** Module structure elements must be conceptual modules (e.g., classes, packages, layers, functional divisions).
2. **Module Relations:** Module structure relations must include uses, generalization ("is-a"), and "is part of."
3. **Layered Systems:** In strictly layered systems, a layer is permitted to use only a single other layer, and upward usages are prohibited.
4. **Uses Relation:** Define the 'uses' relation between software units based on correctness requiring a correctly functioning version (not a stub) of the used unit.
5. **Component-and-Connector (C&C) Relations:** C&C structure relations must be 'attachment', indicating component-connector connections.
6. **C&C Attachment Rules:** Components can only be attached to connectors, and connectors can only be attached to components. Attachments must only be made between compatible components and connectors. Connectors cannot appear in isolation; a connector must be attached to a component.
7. **Module View Constraints:** Module views may impose topological constraints, such as limitations on visibility between modules.
8. **Allocation View Purpose:** The primary goal of an allocation view is to compare the properties required by the software element with the properties provided by the environmental elements to determine if the allocation will be successful.
9. **View Management:** Architects must manage how architectural structures are associated. In an overlay view, elements and relations must retain the types defined in their constituent views.
10. **Element Design Principles:** Elements should have high cohesion, be defined by a narrow set of responsibilities, and demonstrate low coupling.

## III. Architectural Process & Governance

1. **Leadership:** Software architecture must be the product of a single architect or a small group with an identified technical leader.
2. **Stakeholder Engagement:** Maintain a strong connection between architects and the development team to avoid impractical designs. Architects must identify their real stakeholders and their needs, continuously basing the architecture on prioritized, well-specified quality attribute requirements.
3. **ASR Identification:** Architects must identify architecturally significant requirements (ASRs), which must have a profound impact on the architecture and high business or mission value. ASRs should be recorded in one place for review, reference, justification, and periodic revisit, and evaluated against business value and technical risk, with high-risk ASRs receiving the most attention.
4. **Design Iteration:** Design architectures to support incremental implementation. Each design iteration must focus on achieving a particular goal, typically satisfying a subset of the architectural drivers. Establish a goal before starting each iteration.
5. **Architectural Drivers:** Architects must "own" the architectural drivers, checking for overlooked stakeholders or changed business conditions. Primary functionality and quality attribute (QA) scenarios should be prioritized, ideally by key stakeholders.
6. **Design Backlog:** Architectural drivers become part of an architectural design backlog, and a design round is completed when all items in the backlog are accounted for by design decisions.
7. **Progress Tracking:** Use backlogs and Kanban boards to track design progress. Establish clear criteria for moving drivers between "Not Yet Addressed," "Partially Addressed," and "Completely Addressed" columns. A design round is terminated when a majority of drivers (or at least the highest priority ones) are in the "Completely Addressed" column.
8. **Element Refinement:** Satisfying drivers requires architectural design decisions, which manifest in architectural structures composed of interrelated elements obtained by refining previously identified elements. The elements selected for refinement must be those involved in the satisfaction of specific drivers.
9. **Design Concept Selection:** Select the most appropriate design concept by listing pros/cons and other criteria; constraints must restrict selections.
10. **Prototyping:** Create prototypes if the project incorporates emerging technologies, if the technology is new to the company, if QA satisfaction with the technology presents risks, if there's a lack of trusted information, or if configuration options/integration are unclear. Throwaway prototypes must not be used as a basis for further development.
11. **Evaluation Timing:** Conduct architectural evaluations early in the life cycle and repeat as appropriate to maintain design relevance.
12. **Evaluation Prerequisite:** An artifact describing the architecture must be readily available to perform an architectural evaluation.
13. **Evaluation Cost-Benefit:** The cost of an architectural evaluation must be less than the value it provides.
14. **Mandatory Evaluation Steps:** Every evaluation must include reviewers understanding the architecture, determining drivers, analyzing scenarios, and capturing problems.
15. **Evaluation Team:** The evaluation team must consist of 3-5 people, external to the project, recognized as competent, unbiased outsiders. The architect must willingly participate.
16. **Risk Management (Evaluation):** Group risks into risk themes based on common underlying concerns or systemic deficiencies. For each risk theme, identify which business goals are affected to elevate the risks to management attention.
17. **Agile Experimentation:** When requirements change, particularly quality attribute requirements, architects must adopt Agile experimentation (spikes), developed in a separate code branch and merged if successful.
18. **Distributed Teams:** Distributed development teams must coordinate. Dependencies among modules owned by globally distributed teams should be minimized. Remote teams must rely on more formal communication mechanisms (like documentation) and members must take initiative to communicate when doubts arise.
19. **Architect's Role:** Architects must create design and organize teams around that design, manage dependencies, orchestrate requests for changes, elicit/negotiate/review requirements, estimate cost/schedule/risk, define work breakdown, define tracking measures, recommend resource assignments, gather costs, make build/buy recommendations, design for quality, track the system, define quality metrics, identify/quantify/mitigate risks, determine technology requirements, and recommend technology/training/tools.
20. **Transparency:** The external view of the project needs to accurately reflect the internal situation, and internal activities need to accurately reflect the expectations of external stakeholders.
21. **Release Management:** Architects must work with project stakeholders to determine release tempo and increment contents. Early architectural increments should include module decomposition, uses, and preliminary C&C views. Architects must use their influence to ensure early releases address challenging quality attribute requirements and stage architecture releases to support project increments.
22. **Mobile Hardware:** The architect should actively drive early hardware discussions for mobile systems, emphasizing tradeoffs.
23. **ECU Allocation:** Assign tasks to electronic control units (ECUs) based on fit to function, criticality, location in the vehicle, connectivity, locality of communication, and cost, ensuring sufficient power for the function. Components that intensely communicate should be placed on the same ECU.

## IV. Documentation Standards

1. **Purpose-Driven Documentation:** Architecture documentation must be sufficiently transparent and accessible for new employees, concrete enough as a blueprint for construction or forensics, and contain enough information for analysis. It must expose only what actors on an interface need to know to interact with it.
2. **Required Content:** Architects must document both the structure and the behavior of the architecture. This includes documenting relevant views, adding information that applies to more than one view, and describing how architecture elements interact.
3. **View Selection:** Architects must choose the views to document and the notation to document these views, driven by the concerns of key stakeholders and the expected uses of the documentation. Ensure the expected benefits of creating and maintaining a particular view outweigh its costs.
4. **Minimum Views:** The documentation of any software architecture is unlikely to be complete without at least one module view.
5. **Decision & Rationale:** Record significant design decisions and their rationale as they are made, beyond chosen elements, relationships, and properties. Architects need to justify design decisions and record associated risks for review.
6. **Pattern Documentation:** If patterns are employed in the design, identify them within the documentation, record their use, and state why the solution approach was chosen and why the pattern is appropriate.
7. **Control Information:** Document control information must list the issuing organization, current version number, date of issue and status, change history, and procedure for submitting change requests.
8. **Version Control:** Document artifacts should be subject to version control. Project development plans should specify the process for keeping documentation current.
9. **Interface Documentation:** Documenting an interface represents a promise to actors that the element will fulfill its contract. A valid implementation is any implementation that does not violate this contract.
10. **Dynamic Architectures:** For architectures that change dynamically, document invariants (what is true about all versions) and the ways the architecture is allowed to change (e.g., in a variability guide).
11. **Traceability:** Capture and include trace links, connecting specific design decisions to requirements or business goals, as part of the architecture documentation.
12. **Behavior Documentation:** Architecture documentation requires behavior documentation that complements structural views.
13. **Notation Consistency:** If using informal notation for architectural views, maintain consistency in the use of symbols. Add a legend to diagrams to provide clarity and avoid ambiguity.
14. **Element Properties:** Record properties of modules (name, responsibilities, implementation information, revision history) as part of supporting documentation. Every element (component or connector) should have a name and type.
15. **C&C Protocol:** Connectors must embody a documented protocol of interaction, including conventions about order of interactions, locus of control, and handling of error conditions and timeouts.
16. **Implementation Constraints:** Modules must record implementation constraints that the implementation must follow. Module responsibilities should be described in sufficient detail to make clear what each module does.
17. **Automatically Generated Docs:** Generate interface documentation automatically where possible. If explicit interface mechanisms (e.g., protocol buffers) are used, the system will not work without up-to-date interface definitions. Incorporate interface definitions into a database for revision histories and searchability.
18. **Module Properties:** Module properties that guide implementation or are input into analysis should be recorded as supporting documentation.

## V. Interface Design & Management

1. **Interface Definition:** An interface is a boundary across which elements meet, interact, communicate, and coordinate. All elements must have interfaces.
2. **Access Control:** Elements must have interfaces that control access to their internals.
3. **Two-Way Contract:** An interface must define both what an element provides and what it requires from its environment. An interface serves as a contract between an element and its actors; changes must be made with care.
4. **Evolution:** All software, including interfaces, evolves.
5. **Deprecation:** When deprecating an interface, give extensive notice to actors. Introduce an error code to signify an interface's deprecation date or that it has been deprecated.
6. **Maintenance Commitment:** Adding resources to an interface implies a commitment to maintain those resources for as long as the element is in use.
7. **Least Surprise:** Interfaces must behave consistently with the actor’s expectations.
8. **Small Interfaces:** Exchange as little information as possible through interfaces.
9. **Uniform Access:** Avoid leaking implementation details through the interface; a resource must be accessible the same way regardless of implementation.
10. **Don't Repeat Yourself (DRY):** Interfaces must offer a set of composable primitives rather than many redundant ways to achieve the same goal.
11. **Consistency:** The architect must establish and follow conventions for naming resources, ordering API parameters, and handling errors. The design of interfaces should be consistent throughout all elements of the same architecture (insofar as possible) and follow the conventions of the underlying platform or programming language idioms.
12. **Successful Interaction:** Successful interaction with an interface requires agreement on interface scope, interaction style, representation/structure of exchanged data, and error handling.
13. **Data Formats:** Choose suitable data representation formats and data semantics to ensure compatibility and interoperability of architectural elements.
14. **Error Handling:** The interface must clearly define how actors can detect errors (e.g., as output or via an exception-handling channel). The specification of which exceptions, status codes, events, and information are used to describe erroneous outcomes must be part of the interface. Associating an error condition with a resource is prudent, and indicating the source of an error helps the system choose an appropriate correction and recovery strategy.
15. **Backward Compatibility:** Architectural decisions must include mechanisms for feature toggles and backward compatibility of interfaces to support rollback and feature disabling.
16. **Version Incompatibilities:** Mediate interactions between services to proactively avoid version incompatibilities when multiple service versions operate simultaneously.
17. **Dependencies Packaging:** Package elements with their dependencies to ensure consistent versions during deployment from development to production.

## VI. Quality Attribute Specification

1. **Scenario-Based Specification:** Specify all quality attribute (QA) requirements using scenarios in a common, testable, and unambiguous form.
2. **Scenario Structure:** All quality attribute scenarios must include six parts: Stimulus, Stimulus source, Response, Response measure, Environment, and Artifact.
3. **Measurable Responses:** Architects must define responses in scenarios to satisfy identified needs and ensure they are measurable to enable testing and verification of architectural achievement.
4. **Operational Modes:** For systems with multiple operational modes, the scenario environment must specify the active mode.
5. **Responsibility Clarity:** When precision is required, refer to "sets of specific responsibilities" instead of "functional requirements."
6. **Stakeholder-Driven QA:** For each important business goal scenario, describe a QA and response measure value that, if architected into the system, would help achieve the goal.
7. **QA Modeling:** Model the QA by understanding its sensitive parameters and the architectural characteristics that influence them. Model parameters can be derived from the stimuli, responses, artifacts, and environment characteristics.
8. **Design Approach Assembly:** Enumerate model parameters, and for each parameter, enumerate architectural characteristics and mechanisms that can affect it.
9. **Utility Tree:** A utility tree must begin with "Utility" as the root node, refining into specific QA scenarios under each major QA.
10. **Tactics-Based Questionnaires:** For each tactics question in a questionnaire, analysts must record tactic support (Y/N), risks (H/M/L), specific design decisions/location, and rationale/assumptions.

## VII. Security & Privacy

1. **Definition of Security:** Security measures a system's ability to protect data and information from unauthorized access while providing authorized access.
2. **Definition of Attack:** An attack is an action taken against a computer system with the intention of doing harm, including unauthorized access, modification, or denial of service.
3. **CIA Principles:**
    * **Confidentiality:** Data or services must be protected from unauthorized access.
    * **Integrity:** Data or services must not be subject to unauthorized manipulation.
    * **Availability:** The system must be available for legitimate use.
4. **Security Goal:** The system's response to an attack must be to preserve confidentiality, integrity, and availability (CIA) or deter attackers through monitoring.
5. **Attack Tree:** The root of an attack tree must be a successful attack, and nodes must represent possible direct causes, with children nodes decomposing those causes. Leaves of attack trees must represent the stimulus in a security scenario.
6. **Activity Tracking:** The system must track activities by recording access or modification, recording access attempts, and notifying appropriate entities of apparent attacks.
7. **Checksum/Hash:** A checksum is a validation mechanism using redundant information to verify files and messages. Even a slight change in original files or messages must result in a significant change in the hash value.
8. **Access Control:** Access control can be assigned per actor, per actor class, or per role. Access control is commonly performed using OAuth. Limit access by restricting the number of access points to resources or the type of traffic.
9. **Exposure Limitation:** Limiting exposure is typically realized by reducing the amount of data or services that can be accessed through a single access point.
10. **DMZ Architecture:** A demilitarized zone (DMZ) must sit between the Internet and an intranet, protected by a pair of firewalls, with the internal firewall acting as a single access point controlling traffic to the intranet.
11. **Encryption:** Communication links without authorization controls must use encryption for protection when passing data over publicly accessible communication links. Confidentiality is usually achieved by applying some form of encryption to data and communication.
12. **Input Validation:** Implement input validation using a security framework or validation class to perform filtering, canonicalization, and sanitization of external input. Data validation is the main form of defense against SQL injection and cross-site scripting (XSS).
13. **Credential Management:** Force users to change default security settings or choose new passwords after a maximum time period. Systems may require periodic reauthentication.
14. **Nonrepudiation:** Nonrepudiation must be achieved with a combination of digital signatures and authentication by trusted third parties.
15. **Attack Response:** If an attack is believed underway, limit access to sensitive resources. Many systems must limit access from a particular computer for repeated failed login attempts. Notify appropriate actors (operators, personnel, cooperating systems) when an attack is detected.
16. **Logging:** Logging operational data produced by the system is necessary so that failures can be analyzed to reproduce faults.
17. **Authorization:** Authorization means ensuring an authenticated actor has rights to access and modify data or services, usually enabled by access control mechanisms.
18. **Separation:** Separating different entities limits the scope of an attack.
19. **Personally Identifiable Information (PII):** PII is any information about an individual that can distinguish or trace identity (e.g., name, SSN, biometrics) or is linked/linkable to an individual (e.g., medical, financial). Privacy agreements must detail who, outside the collecting organization, is entitled to see PII. The collecting organization itself should have policies governing who within that organization can access PII data. PII is generally obscured for testing purposes. The architect is frequently asked to verify that PII is hidden from development team members who do not need access.
20. **Quantum Threat Awareness:** For secure systems, architects must follow advancements in quantum computing to understand potential impacts on conventional encryption algorithms.

## VIII. Availability & Resilience

1. **Fault Tolerance:** Design systems to mask or repair faults to prevent failures and ensure cumulative service outage does not exceed required values.
2. **Failure Determination:** A failure determination must involve an external observer.
3. **Availability Calculation:** Only unscheduled outages contribute to system downtime calculation for availability; do not include scheduled downtimes.
4. **Fault Categorization:** Categorize detected faults by severity and service impact to provide timely system status and enable appropriate repair strategies.
5. **SLA Specification:** A Service Level Agreement (SLA) must specify guaranteed availability levels and associated penalties for violations.
6. **Availability Response:** Availability scenarios must specify the desired system response to faults. Prevent faults from escalating into failures as a primary availability response.
7. **Fault Logging & Notification:** Log faults for later analysis. Notify appropriate entities (people or systems) when a fault occurs.
8. **Availability Timeframe:** Availability requirements must specify the time or time interval when the system must be available.
9. **Fault Prevention/Endurance:** Availability tactics must prevent or endure system faults to maintain service compliance with specifications.
10. **Monitoring:** System monitors must orchestrate software tactics to detect malfunctioning components.
11. **Watchdog:** Processes monitored by a watchdog must periodically reset the watchdog counter/timer during nominal operation.
12. **Ping/Echo:** Implement Ping/Echo with a defined time threshold for timeout detection.
13. **Heartbeat Overhead:** For scalable systems, reduce heartbeat overhead by piggybacking messages onto other control messages.
14. **Event Ordering:** Use sequence numbers for event ordering in distributed systems where timestamps may be inconsistent; for critical coordination, use mechanisms like vector clocks to determine the order of events rather than comparing times.
15. **Condition Monitors:** Condition monitors must be simple and ideally provably correct to avoid introducing new software errors.
16. **Voting Logic:** Realize voting logic as a simple, rigorously reviewed, and tested singleton to ensure low error probability. Implement voting only when multiple sources are available for evaluation. Implement sophisticated voter mechanisms for analytic redundancy, beyond simple majority or average.
17. **Parameter Protection:** Implement parameter fence by placing a known data pattern immediately after variable-length parameters of an object. Implement parameter typing to ensure sender and receiver agreement on message content type.
18. **Rollback Mechanisms:** Rollback mechanisms must have access to a copy of a previous good state (checkpoint) for components. Implement a limit on the number of retries before declaring a permanent failure.
19. **Exception Handling:** Avoid system crashes as an exception handling strategy due to negative impacts on availability, usability, and testability.
20. **Function Patching:** New software function versions in a function patch must use the entry and exit points of the deprecated function.
21. **Transactional Semantics:** Systems targeting high-availability services must leverage transactional semantics (ACID properties) for asynchronous messages between distributed components.
22. **Component Competence:** Design components to increase their competence set, handling more fault cases as part of normal operation.
23. **Redundancy Strategies:**
    * **Active Redundancy (Hot Spare):** All nodes in a protection group must receive and process identical inputs in parallel to maintain synchronous state. Periodically compare the states of active and standby components to ensure synchronization.
    * **Passive Redundancy (Warm Spare):** Active members of the protection group must provide periodic state updates to redundant spares.
    * **Cold Sparing:** A power-on-reset procedure must be initiated on redundant spares prior to being placed in service upon failover. Ensure power-on-reset procedures result in a device operating in a known state.
    * **Triple Modular Redundancy (TMR):** Each of the three components must receive identical inputs and forward its output to voting logic. TMR voting logic must detect inconsistencies among the three output states, report a fault, and decide which output to use in case of inconsistency.
24. **Circuit Breaker:** Subsequent invocations must return immediately without passing the service request until a circuit breaker is reset.
25. **Nonstop Forwarding:** Implement nonstop forwarding with functionality split into supervisory/control plane and data plane.
26. **Data Center Failures:** Assume that one or more computers will fail every day in a data center with tens of thousands of physical computers.

## IX. Deployability & DevOps

1. **Testability for CD:** Architects must ensure systems are testable to support continuous deployment.
2. **Deployment Awareness:** Architects must consider how executables are updated, invoked, measured, monitored, and controlled on host platforms.
3. **Granular & Efficient:** Architecture must support granular, controllable, and efficient deployments.
4. **Automation:** Continuous deployment must be fully automated, requiring no human intervention. Continuous deployment must incorporate continuous automated testing.
5. **Isolated Stages:** Each deployment pipeline stage must operate in an isolated environment suited for its specific actions.
6. **Version Control & Review:** Code must pass standalone unit tests and undergo appropriate review before commitment to version control.
7. **Integration Environment:** Commitment to version control must trigger build activities in the integration environment. Integration environment tests must include unit tests run against the built system and integration tests for the whole system.
8. **Staging Environment:** Promote built services to the staging environment only after all integration environment tests pass.
9. **Production Deployment:** Deploy applications to the production environment only after passing all staging environment tests.
10. **Production Monitoring:** Services in the production environment must be closely monitored until quality confidence is established by all parties.
11. **Rollback Capability:** Implement rollback capability to revert to a previous version if problems are found in production. Rollback mechanisms must track or reverse consequences of all coordinated updates in a deployment, ideally automatically.
12. **Testing Infrastructure:** Consider testing infrastructure early in the development process when adopting continuous deployment.
13. **Environment Parity:** Strive for environment parity in virtualized deployment environments, differing only in scale, not hardware type or fundamental structure.
14. **Artifact Traceability:** Ensure traceability allows recovery of all artifacts (code, dependencies, test cases, tools) related to a problem-causing element. Maintain traceability information (code, dependency, test, and tool version numbers) in an artifact database.
15. **Repeatable Processes:** Ensure deployment processes are repeatable, yielding consistent results with the same artifacts. Restore original database values after tests to ensure repeatability.
16. **DevOps Goal:** DevOps practices must reduce time from commit to production while ensuring high quality.
17. **Post-Deployment Monitoring:** Implement "phone home" or log delivery capability in systems for DevOps forms that require post-deployment monitoring and error detection.
18. **Deployment Responses:** Deployability responses must include incorporating, deploying, monitoring new components, or rolling back previous deployments.
19. **Scaled Rollouts:** Scaled rollouts must include an architectural mechanism to route user requests to new or old service versions based on user identity.
20. **Deployment Scripts as Code:** Treat deployment scripts as code: document, review, test, and version control them.
21. **Feature Toggle (Kill Switch):** Integrate a feature toggle for dynamically enabling or disabling features.

## X. Testability

1. **Definition of Testability:** A system is testable if it can easily and quickly reveal faults during testing. If a fault is present, the system must fail during testing as quickly as possible.
2. **Architecture for Testability:** Architecture must enhance testability by making bug replication and root cause analysis easier.
3. **Control & Observation:** For proper testability, it must be possible to control each component’s inputs (and manipulate internal state) and observe its outputs (and internal state). A component must maintain state information, allow testers to assign values to that state, and make that information accessible on demand.
4. **Specialized Test Interfaces:** Specialized testing interfaces must be clearly identified or kept separate from access methods for required functionality. If test code is removed from performance-critical and safety-critical systems, ensure the released code has the same behavior, especially timing.
5. **Test Harness:** Test harnesses may include record-and-playback for data across interfaces, simulators for external environments, or distinct production software, assisting in executing test procedures and recording output.
6. **State Management:** For easy testing, state should be stored in a single, localized place. A state machine (or state machine object) is a convenient way to externalize state storage.
7. **Data Abstraction:** Abstract interfaces to allow easy substitution of test data.
8. **Sandboxing & Virtualization:** Isolate system instances from the real world for experimentation without permanent consequences or with rollback. Build versions of resources (e.g., system clock, memory, network) whose behavior is under control for testing.
9. **Assertions:** Hand-code assertions at desired locations to indicate faulty states and check data values against constraints.
10. **Component Replacement:** Component implementation can be swapped for a different one that facilitates testing.
11. **Probes & Aspects:** Activated preprocessor macros can expand to state-reporting code or activate probe statements. Aspects (AOP) can handle the cross-cutting concern of how state is reported.
12. **Complexity Management:** Limit structural complexity by avoiding or resolving cyclic dependencies, isolating and encapsulating dependencies on the external environment, and reducing dependencies between components.
13. **Inheritance Simplification:** Limit the number of classes from which a class is derived, the number of classes derived from a class, the depth of the inheritance tree, and the number of children of a class.
14. **Class Response:** Keep the response of a class (count of its methods plus invoked methods of other classes) low to increase testability.
15. **Modifiability Tactics:** Ensuring high cohesion, loose coupling, and separation of concerns can help with testability.
16. **Layered Testing:** In a layered pattern, test lower layers first, then higher layers with confidence in the lower layers.
17. **Nondeterminism:** Find and weed out sources of nondeterminism (e.g., unconstrained parallelism) to the extent possible. For unavoidable nondeterminism, use other tactics (e.g., record/playback).
18. **Dependency Injection:** A client is written with no knowledge of a concrete implementation; implementation specifics are injected, typically at runtime.

## XI. User Experience & Usability

1. **Definition of Usability:** Usability is concerned with the ease of task accomplishment and the provision of user support.
2. **UI Design Process:** The user interface design process must consist of generating and testing designs, with a plan to iterate.
3. **Architecture for UI Iteration:** Design the architecture to make user interface iteration less painful.
4. **Cancel Command:** When a user issues a cancel command, the system must be listening for it (constant listener, not blocked). The activity being canceled must be terminated, any resources used by it must be freed, and collaborating components must be informed.
5. **Undo/Redo:** To support undo, the system must maintain sufficient information about system state for restoration (e.g., state snapshots or a set of reversible operations). For operations not easily reversed, the system must maintain a more elaborate record of the change.
6. **Pause/Resume:** Provide the ability to pause and resume long-running operations.
7. **Aggregation:** Provide the ability to aggregate lower-level objects into a single group for repetitive operations.
8. **System Initiative:** The system must rely on a model of the user, a model of the task, or a model of the system state when taking the initiative. Encapsulate model information to facilitate tailoring or modification.
9. **Observer Pattern:** Observers must register themselves with the subject. When the state of the subject changes, the observers must be notified.
10. **Memento Pattern:** The caretaker knows nothing about how state is managed; the memento is simply an abstraction.

## XII. Mobile & Embedded Systems

1. **Definition of Mobile System:** A mobile system has the ability to be in movement while continuing to deliver some or all of its functionality.
2. **Architect's Concerns (Mobile):** The architect must be concerned with monitoring the power source, throttling energy usage, and tolerating loss of power. Resource choices must balance the resource's contribution against its volume, weight, and cost.
3. **Hardware Robustness:** The system's computer must not suffer permanent damage if power is cut at any time.
4. **OS Robustness:** The system's computer must (re)start the OS robustly whenever sufficient power is provided.
5. **Software Launch:** The system's OS must have the software scheduled to launch as soon as the OS is ready.
6. **Runtime Integrity:** The runtime environment can be killed at any moment without affecting the integrity of binaries, configurations, and operational data in permanent storage.
7. **State Consistency:** The runtime environment must keep the state consistent after a restart (whether a reset or a resume).
8. **Startup Time:** The runtime must start after a failure so that the startup time from system power on to the software being in a ready state is less than a specified period.
9. **Communication Minimalism:** Only strictly required communication interfaces should be included in a mobile system to optimize power consumption, heat generation, and space allocation.
10. **Seamless Connectivity:** Transitions between different communication protocols must be seamless to the user. If multiple protocols are simultaneously available, the system should choose a protocol dynamically based on factors such as cost, bandwidth, and power consumption.
11. **Connectivity Loss:** The system should be designed so that data integrity is maintained in case of a loss of connectivity. Computation must be resumed without loss of consistency when connectivity returns.
12. **Graceful Handling:** The system should be designed to deal gracefully with limited or no connectivity, dynamically providing degraded and fallback modes.
13. **Sensor Integration:**
    * **Definition of Sensor:** A sensor detects physical environmental characteristics and translates them into an electronic (assumed digital) representation.
    * **Definition of Actuator:** An actuator takes a digital representation as input and causes an action in the environment.
    * **Architect's Sensor Concerns:** The architect must address how to create an accurate environmental representation from sensor inputs, how the system should respond to it, the security and privacy of sensor data/actuator commands, and degraded operation.
    * **Sensor Driver:** The lowest level of the sensor stack must be a software driver to read the raw data periodically from the sensor.
    * **Sensor Period:** The period frequency of sensor readings is a parameter that must influence both the processor load and the accuracy of the created representation.
    * **Smoothing:** Smoothing is a process that uses a series of measurements over time to produce an estimate that tends to be more accurate than single readings.
    * **Conversion:** The converter is responsible for converting readings from whatever form is reported by the sensor into a common form meaningful to the application.
    * **Sensor Fusion:** Sensor fusion combines data from multiple sensors to build a more accurate, complete, or dependable representation of the environment.
14. **Safety Criticality:** Physical resources that have safety consequences must not fail or must have backups.
15. **Environmental Understanding:** There should be an understanding of the environment in which the system will be operated prior to making hardware choices.
16. **Offloading to Cloud:** The architect must determine if the mobile system has sufficient power for specific functions, if there is adequate connectivity to offload some functions, and how to satisfy performance requirements when functions are split between mobile and cloud.
17. **Logging:** Logs should be offloaded to a location where they are accessible regardless of the mobile system's accessibility.

## XIII. Cloud & Distributed Systems

1. **Load Balancing Algorithms:** A load balancer algorithm balances load uniformly only if every request consumes roughly the same resources. The client must not know (or need to know) how many instances of the service exist or their IP addresses. A load balancer must be very efficient.
2. **Health Checks:** Health checks are a mechanism for a load balancer to determine if an instance is performing properly. If an instance fails a health check, it must be marked as unhealthy, and no further messages should be sent to it. The load balancer must check multiple times before moving an instance to an unhealthy list and periodically check the unhealthy list to determine if an instance is again responding.
3. **Client Robustness:** Clients must be designed to resend a request if they do not receive a timely response.
4. **Service Idempotence:** Services must be designed such that multiple identical requests can be accommodated.
5. **Stateless Services:** Design and implement services to be stateless. Direct sessions and sticky messages should only be used under special circumstances due to the risk of instance failure or overload.
6. **Distributed Coordination Tools:** Do not attempt to solve distributed coordination problems yourself; use existing solution packages like Apache Zookeeper, Consul, or etcd.
7. **Autoscaling Visibility:** Autoscaling activities must be invisible to service clients.
8. **Autoscaler Metrics:** The autoscaler must not create or remove instances based on instantaneous values of CPU utilization or network I/O bandwidth metrics; metrics must be averaged over a reasonable time interval. Autoscaler rules typically use longer time intervals for VM creation/removal due to the time required for VM allocation/boot.
9. **Instance Removal:** When the autoscaler removes an instance, it must notify the load balancer to stop sending requests and notify the instance itself to terminate activities and shut down (draining). The service developer is responsible for implementing the appropriate interface to receive instructions to terminate and drain an instance of their service.
10. **Container Autoscaling:** Scaling containers involves a two-level decision: whether an additional container/Pod is needed, and whether it can be allocated on an existing runtime engine or if a new instance (VM) must be allocated.
11. **Container OS Compatibility:** The operating system for a container must be compatible with the container runtime engine. Containers are currently limited to Linux, Windows, or iOS.
12. **Container Scope:** Containers generally run a single service. Avoid putting multiple services in a container, as this could bloat the image size and increase startup time/memory footprint.
13. **Container Image Size:** Container image size must be small, including only necessary programs and libraries.
14. **Pod Communication:** Containers in a Pod must share an IP address and port space to receive requests and can communicate using IPC mechanisms (semaphores/shared memory) and shared ephemeral storage volumes.
15. **Pod Lifetime:** Containers in Pods must have the same lifetime and be allocated and deallocated together.
16. **Serverless Statelessness:** Serverless architecture containers must be stateless. Any state needed for coordination must be stored in an infrastructure service delivered by the cloud provider or passed as parameters.
17. **FaaS Execution Time:** For Function-as-a-Service (FaaS), the service must process the request and exit within the provider's time limit or it will be terminated.
18. **Public Cloud Accessibility:** Services built using public cloud infrastructure must be accessible on the public Internet.
19. **VM Allocation:** When requesting a new virtual machine (VM) in the cloud, specify the cloud region, instance type, and ID of a VM image. The cloud provider must ensure enough physical hardware resources are available so that a request for a VM will not fail due to insufficient resources.
20. **Distributed System Time:** Most distributed systems are designed so that time synchronization among devices is not required for applications to function correctly.
21. **Container Scripting:** Create a script for container image creation steps and store it in a file specific to the tool used. Use version control on the container specification file to ensure identical images and controlled modifications.

## XIV. Architectural Debt Management

1. **Analysis Process:** The architecture debt analysis process requires:
    * A tool to extract issues from an issue tracker.
    * A tool to extract a log from a revision control system.
    * A tool to reverse-engineer the code base for syntactic dependencies.
    * A tool to build Design Structure Matrices (DSMs) and identify anti-patterns.
    * A tool to calculate debt associated with each hotspot.
2. **Data Sources:** Source code is used to determine structural dependencies. Revision history is used to determine the co-evolution of code units. Issue information is used to determine the reason for changes.
3. **Debt Identification:** If architecture debt is suspected, architects need to identify specific files and their flawed relationships.
4. **Hotspot Identification Rules:**
    * **Unstable interface:** Search for a file with many dependents that changes frequently with other files.
    * **Modularity violation:** Search for two or more structurally independent files that change together frequently.
    * **Unhealthy inheritance:** Search for either a parent class depending on its child class in an inheritance hierarchy, or a client of the class hierarchy depending on both the parent and one or more of its children.
    * **Cyclic dependency/clique:** Search for sets of files forming a strongly connected graph (structural dependency path between any two elements).
    * **Package cycle:** Determine by discovering packages that form a strongly connected graph.
    * **Crossing:** Search for a file with high fan-in and fan-out and substantial co-change relations with these files.
5. **Debt Quantification:** For each file, determine the total number of bug fixes, changes, and churn. Sum these metrics for files in each identified anti-pattern.
6. **Debt Remediation Rules:**
    * **Clique:** If a clique exists, a dependency needs to be removed or reversed to break the cycle.
    * **Unhealthy inheritance:** If unhealthy inheritance is present, some functionality needs to be moved (typically child to parent).
    * **Modularity violation:** If a modularity violation is identified, the shared "secret" needs to be encapsulated as its own abstraction.
7. **Refactoring:** If identified architecture debt is severe, it should be removed through refactoring.

## XV. Organizational & Professional Conduct

1. **Competence:** A competent architect must master the body of knowledge and remain up-to-date, continuously acquiring knowledge and honing skills.
2. **Mentorship:** Architects must be mentored and must mentor others.
3. **Metrics:** Architects must implement the capture of metrics and define quality metrics.
4. **Skill Development:** Architects must define the required technical skill sets, recommend training, and interview candidates.
5. **Team Coordination:** Architects must ensure communication and coordination among developers and solicit feedback on progress, problems, and risks.
6. **Documentation Oversight:** Architects must oversee documentation.
7. **Organizational Support:** Organizations should:
    * Hire talented architects and establish an architect career track.
    * Make the architect position highly regarded and encourage architects to join professional organizations.
    * Establish an architect certification and mentoring program, as well as an architecture training and education program.
    * Measure architects' performance and encourage external certifications.
    * Reward or penalize architects based on project success or failure.
    * Establish organization-wide architecture practices, clear architect responsibilities and authority, and an architect communication and knowledge-sharing forum.
    * Establish an architecture review board and include architecture milestones in project plans.
    * Involve architects in product definition and hold organization-wide architecture conferences.
    * Measure and track the quality of architectures produced and bring in outside expert architecture consultants.
    * Involve architects in advising on development team structure and give architects influence throughout the entire project life cycle.
    * Establish and maintain a repository of reusable architectures and artifacts.
    * Create and maintain a repository of design concepts.
    * Provide a centralized resource to analyze and help with architecture tools.

## XVI. Legal & Compliance

1. **Copyright:** Obtain permission from the publisher prior to any prohibited reproduction, storage, or transmission of this publication.
2. **Trademarks:** When trademarks appear in the book and the publisher is aware of the claim, print them with initial capital letters or in all capitals.
3. **Functional Safety:** Functional Safety Integrity Levels (SILs) define the safety criticality of functions, from SIL 4 (most dependable) to SIL 1 (least dependable). For road vehicle functional safety, conform to the ISO 26026 standard.
4. **GDPR Compliance:** Cloud regions help cloud providers comply with regulatory constraints such as the General Data Protection Regulation (GDPR).
5. **Organizational Processes:** Organizational processes must account for insider threats.

## XVII. Quantum Computing Principles

1. **QPU-CPU Communication:** Communications between a Quantum Processing Unit (QPU) and a classic CPU must be in terms of classic bits.
2. **Qubit Probabilities:** The sum of probabilities (|α|² + |β|²) for a qubit measurement delivering 0 or 1 must be 1.
3. **No-Cloning Theorem:** There is no direct copying of a qubit. If copying a qubit to another is desired, indirect means must be used.
4. **Measurement Destroys Qubit:** A measurement (read) of a qubit will destroy the qubit and deliver either 0 or 1. The value of a qubit input to a READ operation collapses to either 0 or 1.
5. **NOT Operation:** A NOT operation on a qubit flips its amplitudes.
6. **Z Operation:** A Z operation adds π to the phase of a qubit (modulo 2π).
7. **HAD Operation:** A HAD operation creates an equal superposition (amplitudes of 0 and 1 are equal). For a HAD operation, a 0 input generates a phase of 0 radians, and a 1 input generates a phase of π radians.
8. **CNOT Operation:** For a CNOT operation, if the control bit (first qubit) is 1, a NOT is performed on the second qubit. If the control bit is 0, the second qubit remains unchanged.
9. **Quantum Teleportation:** Quantum teleportation depends on entanglement and utilizes three qubits. The destruction of the original qubit's state must be accepted during teleportation. The recipient qubit will have the same state as the original, destroyed qubit after teleportation. During teleportation, two classical bits are transferred to the recipient location. Measuring qubits A and γ during teleportation destroys their state.
10. **HHL Algorithm:** For the HHL algorithm to solve Ax=b with quantum computers, the `b` values must be quickly accessible, and the matrix `A` must satisfy certain conditions, including being well-conditioned (determinant non-zero or close to zero). If the matrix `A` is sparse, it likely can be processed efficiently. The result of applying the HHL algorithm is that `x` values appear in superposition, thus a mechanism is needed for efficiently isolating actual values from superposition.

## Key Highlights

* Design solutions for quality attribute requirements (e.g., security, performance, availability) into the system's architecture from the very beginning; they cannot be "bolted on" later in development.
* Architectures must possess conceptual integrity and technical consistency, applying the same approach consistently across the system for similar concerns like error handling or logging.
* Design well-defined modules based on information hiding to encapsulate volatile elements, promoting high cohesion, loose coupling, and independence for modifiability and distributed team work.
* Architects must identify, record, and continuously evaluate Architecturally Significant Requirements (ASRs) based on business value and technical risk, dedicating most attention to high-risk ASRs.
* Utilize an iterative design approach to support incremental implementation, create prototypes for emerging or risky technologies, and conduct architectural evaluations early and repeatedly in the life cycle.
* Document all significant design decisions, their rationale, and associated risks, ensuring that architectural documentation is transparent, version-controlled, accessible, and purpose-driven.
* Architect systems for high testability to facilitate bug replication and root cause analysis, and enable fully automated continuous deployment with integrated testing and reliable rollback capabilities.
* Design services to be stateless for enhanced scalability and resilience in cloud and distributed systems, and leverage proven, existing solution packages for distributed coordination rather than custom implementations.
* Proactively identify, quantify, and actively remediate architectural debt through refactoring, focusing on structural flaws like cyclic dependencies, modularity violations, or unhealthy inheritance.
* Ensure robust security and privacy measures are integral, preserving confidentiality, integrity, and availability (CIA) through input validation, strong access control, encryption, and careful management of Personally Identifiable Information (PII).
