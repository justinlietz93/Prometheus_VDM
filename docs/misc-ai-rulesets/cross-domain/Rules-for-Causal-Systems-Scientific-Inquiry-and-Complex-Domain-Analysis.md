# Rules for Causal Systems, Scientific Inquiry, and Complex Domain Analysis

These rules synthesize foundational principles, modeling requirements, methodological practices, and domain-specific constraints from various segments of scientific inquiry and system design. They provide a comprehensive, de-duplicated framework for understanding, representing, and analyzing causal relationships and complex systems.

**Generated on:** October 2, 2025 at 4:52 PM CDT

---

## I. Fundamental Principles & Philosophical Stance

1. **Causal Thinking Purpose:** Causal thinking must provide a substantive account to avoid triviality and enable the distinction between mere correlations and exploitable correlations for manipulation and control.
2. **Causal Knowledge Function:** Causal knowledge must enable robust inferences across different times and contexts, even based on incomplete system state knowledge.
3. **Epistemic Nature of Causation:** Notions such as cause and explanation must be construed as fundamentally epistemic, with ontological commitments and relations understood as presupposing a broader philosophical framework.
4. **Intervention Modifiability:** The ability to modify or intervene in a system is critical for identifying and understanding causal relationships.

## II. Causal Theory & Concepts

1. **Causal Relation Asymmetry:** The causal relation must be asymmetric; effects generally do not precede their causes. For spatiotemporal variables, this asymmetry typically aligns with temporal asymmetry.
2. **Locality of Causal Influence:** Any causal influence between two localized events must be mediated by a spatiotemporally continuous causal process and propagate at a finite speed. The world must be at least approximately local for interventionist accounts of causation to be valid.
3. **Common Cause Principle:** Spatially distant correlated events not directly related as cause and effect must possess a common cause in their past that explains and screens off their correlation, allowing inference of causal dependence from statistical dependence.
4. **Causal Relata Nature:** Causes are events that bring about other events. Enablers are conditions making causation possible. Intermediaries transport force/meaning without transformation. Mediators transform, translate, distort, and modify elements, making their input an unreliable predictor of output.
5. **Mechanism Definition:** A mechanism for a phenomenon must consist of entities whose activities and interactions are organized so as to be responsible for the phenomenon, being decomposable and intrinsically causal.
6. **Constraint Definition:** For a process P, a configuration C acts as a constraint if, within P's characteristic timescale, C is not locally affected by P in properties relevant to its causal power (Conservation) and C exerts a causal power over P, causing an observable difference in P's behavior (Causal Power). Constraints must be local, contingent, reduce degrees of freedom, and remain conserved at the relevant timescale.
7. **Constraint Dependence:** A dependence relation between two constraints occurs when the replacement or repair of one constraint depends on the action of another. Minimal causal dependence between constraints must involve one dependent and one enabling constraint.
8. **Organizational Closure:** A set of constraints C realizes organizational closure if each constraint Cᵢ in C is both directly dependent on at least one other constraint in C (Cᵢ is dependent) and at least one other constraint Cⱼ in C depends on Cᵢ (Cᵢ is enabling), establishing mutual dependence. Not all causal circularity constitutes closure.
9. **Causal Complexity:** Causes often operate in configurations ("teams" or "causal recipes"), and distinct configurations can produce distinct contributions (equifinality, multifinality). Causal principles are not universally applicable due to mechanistic heterogeneity.
10. **Causal Indeterminacy:** In cases of causal indeterminacy, an event's causal role can only be specified and attributed retrospectively, after the sequence's termination, and cannot be paraphrased to fit a non-narrative causal presentation. Both forward-looking and backward-looking indeterminacy must be considered when specifying counterfactual dependencies.
11. **Transference Theories:** Transference theories require a spacetime background and conservation principles, focusing on fundamental physical causal processes across distinct events. They succeed by providing local, approximate, and idealized descriptions of matter, with interaction energies confined to the interaction event.

## III. Causal Modeling & Representation

1. **Causal Structure Representation:** Causal relationships must be represented using causal structures consisting of directed graphs (with causal "arrows") and structural equations. Interventionist accounts must capture causal asymmetry by representing causal structures as directed acyclic graphs. When systems involve cycles between variables, techniques like converting data into time-indexed series or considering smaller time units must be used to ensure acyclicity.
2. **Structural Equations:** A causal model's structural equations must specify how the value of an effect variable functionally depends on its causes.
3. **Exogenous and Intervention Variables:** Exogenous variables in a causal model must be posited to be probabilistically independent. Intervention variables must be independent of all other exogenous variables.
4. **Background Conditions for Causal Techniques:** To use causal Bayes net techniques for causal structure discovery, important background conditions such as Causal Markov, Causal Faithfulness, or independence must hold. Minimally, causal relata must be representable as random variables and possess a structure that makes Causal Markov, Modularity, and Faithfulness conditions applicable.
5. **Model Simplification:** To reduce model complexity, modelers may remove elements or keep them constant based on computational analysis (e.g., sensitivity analysis), in lieu of biological information.
6. **Variable Inclusion:** If a variable does not cause anything within a model's scope, it should not normally be included in that model.
7. **Strongest Causes for Outcome:** When the primary concern is finding the cause most likely to bring about an outcome, the model must include the strongest causes.
8. **Policy-Relevant Models:** A model developed for policymakers must include factors that can be influenced by policy to be effective, highlighting potential points of control.
9. **Causal Model Utility:** Causal models lead to worse decisions unless they are closely tailored to a given decision context.
10. **Experimental Interaction Representation:** Experimental interactions must be represented in models that include at least some local classical variables.

## IV. System Definition & Individuation

1. **System Definition:** Systems are best defined as units of research that are, or can be, investigated as such. They are "worldly" entities consisting of objects of scientific research, primarily specified by the objects they contain, and can be classified as tokens or types. Systems are not phenomena, events, or processes, but they may bring about phenomena.
2. **System Treatment & Success:** A collection of things is a system if scientists successfully treat it as a system, enabling insights beyond mere description. The mere intention to treat it as such is insufficient.
3. **Conceptualization for Investigation:** Conceptualizing something as a system is crucial for its identification and must form the basis for a successful investigation, enabling scientists to run certain inferences about it.
4. **System Boundaries & External Influences:** Systems can only be investigated if relevant external influences on their behavior are known. A system must be defined such that external influences can be accounted for (e.g., using boundary conditions, external fields, or random variables if statistically known) or neglected if negligible for the inquiry. The ability to control (know) external forces is a causal condition on systemhood.
5. **System Isolation:** Experimental science requires the ability to dynamically isolate subsystems. While real-world systems are rarely fully isolated, imagined model systems are isolated by scientific definition. The causal condition is fulfilled for systems known to be isolated or if external forces are fully known and exogenously fixed.
6. **Internal Cohesion:** A strategy for handling external forces is to define the system such that the most important forces on all constituents originate within the system. Systemhood is threatened more by significant mutual interactions with the environment than by mere external influences.
7. **Theoretical System Description:** From a theoretical perspective, a system is described using differential equations that refer to its parts, allow for external fields, and assume specific boundary conditions.
8. **Causal System Individuation Criteria:** Individuating causal systems is crucial for scientific endeavors like measuring, predicting, and explaining. This requires knowing what the system is responsible for, its boundaries, its parts, and how it differs from other systems. The criteria for individuating causal systems must be causal, based on knowing what makes it the system it is.
9. **Cross-Cutting Systems:** Individuating cross-cutting causal systems without natural boundaries requires defining the phenomenon the system is responsible for and how its parts are relevant to that phenomenon. Spatiotemporal parthood is insufficient; instead, parts of a system must causally interact more intensively with each other than with non-parts. For systems with a focal individual, this intensity demand restricts to interactions with that individual.
10. **Biological Individuality (General):** Practitioners of biological sciences must address problems of individuation, conceiving biological individuals as coexisting processes that remain temporarily and spatially interconnected and cohesive.
11. **Biological Individuality (Closure of Constraints):** Living systems must be individuated based on their organizational closure of constraints. This functional mode is grounded in ascertaining organizational closure, not physical boundaries. The boundaries of a living system (as a causal system) are defined by the set of enabling and dependent constraints that functionally constitute its organization.
12. **Internal/External Constraints for Biological Systems:** For an item to be internal to a living system, it must be internal to its closed organization, acting as both a dependent and an enabling constraint. If exclusively enabling or dependent, it is considered external, even if within physical boundaries.
13. **Living System Organization:** Living systems exhibit two distinct yet interdependent causal regimes: an open regime of thermodynamic processes/reactions, and an organizationally closed regime of dependence between system components acting as constraints. They are thermodynamically open while being organizationally closed. Organizational closure, distinct from thermodynamic closure, is requisite for self-maintenance and autonomy.
14. **Degrees of Individuality:** Different degrees of individuality can be attributed to living systems based on the closure of constraints, inversely related to their degrees of openness. Functional integration and internal cohesion are characterized by how components are wired to collectively achieve self-maintenance.
15. **Biological Identity & Persistence:** Relational identity requires stable relations among relevant properties for synchronic and diachronic identity. To reidentify the same biological individual across time, either a sufficiently similar topology of relations between enabling and dependent constraints, and/or an equivalent set of functional roles, must be preserved. A genealogical conception of identity, accounting for changes across evolutionary time, must complement relational identity. Theoretical descriptions should not rely solely on invariants, as constraints arise from historical processes.

## V. Research & Methodological Practices

### A. General Methodology

1. **Research Framework (Pragmatist):** When employing a pragmatist framework, researchers must embrace pluralism when framing problematic situations, defining specific problems, and constructing aims.
2. **Causal Discovery Methodology:** All types of causes share a common methodology of causal discovery. Causes, if they exist, must be discovered through interventionist methods.
3. **Modular Systems:** Investigating systems with internal causal structure requires the system to be modular, including at least some independently specifiable subsystems on which individual interventions are possible.
4. **Phenomenon Operationalization:** To conduct experiments and measure a relevant phenomenon, it must first be operationalized, often by identifying measurable variables (proxies) that adequately represent it due to close linkage.
5. **Exclusion of Irrelevant Factors:** Causal system individuation must exclude irrelevant causal factors (e.g., background conditions, sterile effects).
6. **Causal Claims Across Levels:** Causal claims should primarily be within-level, accompanied by supervenience or identity relations, unless scientific contexts necessitate irreducibly across-level claims (e.g., community-level factors affecting individual risk). Across-level claims are problematic when higher-level factors are multiply realizable. Scientists must recognize when such claims are ambiguous.
7. **Data Translation:** The results of studies using novel, self-contained scenarios will not necessarily translate to real-world settings where prior knowledge is unavoidable.

### B. Intervention Design & Reliability

1. **Intervention Conditions:** One can intervene into a system and evaluate an intervention's impact only if one knows where to intervene (parts) and the system's typical behaviors or outputs. Manipulations must be specific, not merely "on/off" changes, to exclude background factors.
2. **Intervention Reliability & Limitations:** For interventions to be a reliable guide to causal structure, they must satisfy various independence assumptions. Interventions into a causal structure must be "surgical," leaving the rest of the causal structure intact, and must not violate physical law. Interventionism would not apply if all states were entangled; non-locally entangled quantum systems can only be manipulated if embedded in non-entangled local causal structures. If interactions are truly instantaneous, surgical interventions and initial independence assumptions are problematic.
3. **Intervention Focus (Feasibility):** Interventions should focus on those that are scientifically relevant or plausible for scientific inferences about control and explanation. Infeasible interventions can be pragmatically dismissed.
4. **Intervention Integration in Practice:** Any intervention, particularly in practical fields like farming or education, must be integrated fruitfully and sustainably by accounting for the specific ontology of the practices involved.

### C. Specific Research Paradigms

1. **Randomized Controlled Trials (RCTs) for Generalizability:** When conducting RCTs with the aim of generalizability, contextual and historical factors should be treated as background noise to isolate the desired effect.
2. **RCT Results Format:** Results from RCTs must be presented in the format "X has an effect on Y," where X describes the intervention (independent variable) and Y represents the measured construct (dependent variable).
3. **Qualitative Social Science (Single-Case vs. Generic Claims):**
    * Causation is identified at the single-case level, where complex interactions occur among actors, with context intrinsic to causal explanation.
    * Generic causal claims serve as research instruments, with their productivity as a focus being more important than their truth or representational accuracy.
    * Qualitative researchers should analyze how something came about in a single case and derive generic causal claims that can be fruitfully used as "things to be explained" in future single cases.
    * Generic claims do not add to single-case analysis, cannot predict or explain single cases, and are less informative than single-case descriptions, primarily serving as instruments to provide a productive focus for single-case analysis.
    * Researchers should search for mediators, particularly social factors, rather than direct causes.

### D. Policy & Healthcare Application

1. **Policy Process (Causal Understanding):** The policy process requires understanding in causal terms, specifying the causal notion involved. It involves iterative activities (agenda setting, formation, implementation) understood within material, institutional, ideational, and actor contexts. Both problems and solutions must be deliberately constructed, and policy formation needs to anticipate incentive structures.
2. **Policy Implementation:** Effective policy implementation requires involving implementers and target groups in policy formation.
3. **Democratic Policy Process:** Democratic policy processes can be based on top-down approaches (decisions earnestly carried out) or bottom-up approaches (participatory democracy involving target groups).
4. **Evidence-Based Medicine (EBM):** The core mission of EBM is to establish causal relations between medical interventions and their effects using specific methods (RCTs, meta-analysis). Recommendations must be based on interpreting and synthesizing production mechanisms from RCTs, meta-analysis, and experiential knowledge.
5. **Health Technology Assessments (HTAs):** HTAs must use causal methods complemented by assessing policy-relevant criteria (cost, cost-effectiveness) with standardized measures. Phronetic HTA should synthesize understandings from researchers, practitioners, and patients regarding causes and mechanisms.

## VI. Explanation & Model Evaluation

1. **Explanatory vs. Predictive Models:** Predictive power of a model cannot stand for its explanatory power. Predictive and explanatory models are evaluated divergently and cannot be automatically replaced. To make a predictive model explanatory, additional theoretical work is required. Arbitrary machine learning frameworks must not replace causal-explanatory theories, though a specific, non-flexible, machine-generated model instance can be used for explanatory purposes.
2. **Good Model Utility:** A good model should best enable prediction, explanation, and intervention. Accuracy is a necessary but insufficient condition for a good model's utility.
3. **Explanatory Power Criteria:** Explanatory power includes non-sensitivity to background conditions, precision (level of detail/contrast classes), factual accuracy, degree of integration into existing knowledge, and cognitive saliency. Explanations must aim to render phenomena intelligible, involving logical consistency and empirical adequacy.
4. **Explanation Quality (General):** An explanation must be identified within the upper bounds of simplicity, accuracy, and relevance. Explanations should use more abstract variables for simplicity and not contain irrelevant variables.
5. **Specificity & Generalization:** Specificity is defined as the removal of variables from an explanation not relevant to the current case. More general explanations should address a wider range of "what-if-things-had-been-different" questions. A generalization's breadth must be carefully distinguished from having multiple explanatory structures. Explanations based on generalizations that are more accurate and cover more counterfactual cases are prioritized.
6. **Theoretical Commitments:** Explanatory models should make substantial theoretical commitments. Explanatory theories must not be too flexible by explaining physically or biologically impossible phenomena, as this makes them empirically vacuous and unfalsifiable.
7. **Causal-Explanatory Model Validity:** Causal-explanatory models should be structurally valid, elucidating the causal process. Contrast classes for causal-explanatory models must be constrained by an overarching theoretical framework, not by mere data fitting.
8. **Model Evaluation Benchmarks:** Predictive performance can be evaluated using Akaike information criterion, minimum description length, or out-of-sample error rates. Bayesian information criterion should not be used solely for predictive accuracy. Predictive models are evaluated on generalization to out-of-sample data; causal-explanatory models by fit to in-sample evidence.
9. **Overfitting & Underfitting:** A model with an R² of 1 is almost surely overfitted. Bias error leads to underfitting; variance error leads to overfitting.
10. **XAI (Explainable AI) Principles:**
    * Causal-based XAI approaches must display causal connections.
    * Explanations for what is false, or using false explanans, are forbidden.
    * For "how-seeking" questions, only the algorithm's inner workings leading to the output need to be revealed; tethering to the real world is not necessary.
    * For "why-seeking" questions, the explanans and explanandum must be tethered to the world or scientific knowledge, transcending ML model assumptions. Algorithms must be tethered to identify and disregard unsuitable explanations.
11. **Narrative Explanation:** In certain cases, a narrative form of explanation is necessary. Historical events reconstructed in a narrative must be related to subsequent events to ensure plot unity and continuity. Temporal ordering is essential. Specifying an event's causal antecedents in a narrative requires the sequence's termination. Before an event is categorized for explanation, questions about its causes cannot be asked.
12. **Empirical Adequacy for Explanation:** Intelligibility requires empirical adequacy, which cannot be determined by formal analogs but by the accepted epistemic framework of the scientific community. For historical events, it is relative to their framing.
13. **Theory Principles:** An explicit theory must provide principles to determine and measure relevant facts and assess competing accounts.

## VII. Specialized Systems & Contexts

### A. Relativistic & Physical Systems

1. **Matter Theory Prescriptions:** Every matter theory must come with dynamical equations for how fields change across events and an assignment of energy and momentum to atomic events as a function of the field configuration.
2. **General Relativity (GR) Prescriptions:** GR must prescribe how the spacetime metric determines spacetime curvature. The Einstein Field Equation (EFE) must fix how energy and momentum are correlated with spacetime curvature.
3. **Spacetime Metric Determination:** Given EFE, the spacetime metric at an atomic event must determine the energy and momentum at that event. However, it must not determine the matter configuration, as different configurations can yield the same energy/momentum.
4. **Matter Configuration & Curvature:** Changes in matter distribution must depend on curvature, and matter configuration must determine only the Ricci curvature (a structural part of spacetime curvature).
5. **Relativistic Causality:** Relativistic causality demands that field values on a domain of dependence (D(A)) are determined by field values on a closed subset of the initial hypersurface (A). In probabilistic theories, the probability distribution on A must determine the distribution on D(A).
6. **Ordinary Matter & Light (GR):** The history of ordinary matter must be represented by a four-dimensional cylinder-like region with a timelike linear dimension. No ordinary object may travel faster than light. Only light rays may have their linear dimension in a null direction.
7. **Intervention in GR Spacetimes:** In GR spacetimes with timelike curves that loop back, the interventionist assumption that causal relations are non-cyclic is violated.
8. **Worldly Infrastructure for Causal Reasoning:** The physical infrastructure supporting causal notions must crucially involve features characterizing prevailing initial and boundary conditions, and the world must be thermodynamically normal. In anti-entropic worlds, initial particle positions and momenta must be strongly correlated to ensure entropy decreases.

### B. Adverse Outcome Pathways (AOP) Framework

1. **AOP Framework Robustness:** The AOP framework must demonstrate proven robustness through rigorous scientific and transparency tests.
2. **AOP Definition:** An AOP must be defined as a sequence of causally connected biological events, initiating at the molecular level.
3. **AOP Component Distinction:** The AOP framework must clearly distinguish four main component parts: molecular initiating events (MIE), key events (KE), adverse outcomes (AO), and the causal relationships between them (KER).
4. **AOP Progression:** AOP pathways must progress through different biological levels, from cellular to the whole organism.
5. **Adverse Outcome Nature:** The adverse outcome in an AOP pathway must be observable at the whole organism level and represent the final event observed in in vivo testing, recognized for its regulatory significance.
6. **AOP Purpose:** AOPs must serve to synthesize and organize existing scientific knowledge about toxicity pathways available in the literature, not to generate new primary research findings.
7. **Causal Claims in KER:** Causal claims must be explicitly established within each Key Event Relationship (KER), demonstrating that an upstream event causes a downstream event when its effect is of adequate strength and duration.
8. **AOP Terminology & Syntax:** AOP diagrams must consistently use "MIE" to denote Molecular Initiating Event, "KE" for Key Event, "AO" for Adverse Outcome, and "—>" for Key Event Relationship.
9. **Molecular Initiating Event (MIE) Definition:** An MIE must be defined as a specialized key event representing the initial interaction of a chemical or stressor at the molecular level within an organism, initiating the AOP.
10. **Key Event (KE) Definition:** A KE must be a measurable change in a biological or physiological state that is essential to the progression of a defined biological perturbation, meaning the pathway would not proceed without it.
11. **Key Event Relationship (KER) Definition:** A KER must be a scientifically based relationship connecting two key events, establishing a causal and predictive link that facilitates inference or extrapolation.
12. **AOP Methodology:** AOPs must integrate and synthesize knowledge derived from both in vitro and in vivo animal testing methods.
13. **Comprehensive Event Description:** All events within an AOP must be described comprehensively, specifying what is measured, how the measurement is made, and the relevance across species, sexes, and life stages.
14. **Essentiality Assessment (WoE):** The essentiality of key events must be assessed using a Weight-of-Evidence (WoE) approach adapted from the Bradford-Hill criteria, specifically emphasizing direct counterfactual evidence, such as the reversibility of events upon cessation of dosing or prevention of a key event. Stronger support is garnered when counterfactual evidence supports multiple key events.
15. **Overall Weight of Evidence:** Each AOP must provide a clear methodology for judging the overall weight of evidence for the entire sequence of Key Events leading to the Adverse Outcome.

### C. Social, Bio-Social, & Ethical Considerations

1. **Structural Racism:** The term "racism" must include structural factors that do not necessarily involve explicit or conscious racist beliefs, not just overt individual acts. Interventions on structural racism must be systemic, requiring changes in resource availability.
2. **Social Causes in Disease Causation:** It is central to recognize the bearing of social conditions (inequalities, limited access, social exclusion) in causing concrete pathologies.
3. **Bio-Social Medical Practices:** Medical practices must uncover causal mechanisms that are bio-social in nature. Accounts of disease causation must not reduce disease to mere biological causes and must include various information sources (biological/social markers, patient testimony).
4. **Socio-markers Purpose:** The aim when using socio-markers is to pick up signals to reconstruct the continuum from social factors to disease, analogous to biomarkers.
5. **Epistemic Justice in Healthcare:** Accounts of disease causation considering biological and social markers are better positioned to allow patients' testimonial contributions, serving as a step toward epistemic justice. Overfocusing on biological causes while neglecting social factors can lead to epistemic injustices.
6. **Patient Role & Testimony:** Patients are a necessary source of information for the diagnostic process in bio-social accounts of disease causation. Bio-social accounts must admit patients' direct contributions to medical discourse as the most direct way to access socio-markers.
7. **ML Systems & Social Markers:** ML systems that fail to operationalize social markers effectively displace, by default, social markers collected through patient testimony. ML designers often dismiss patient testimony markers as irrelevant. Operationalizing socially charged concepts while deflating their meaning in ML risks promoting a biologization of health.
8. **Health/Disease Concepts in ML:** Concepts of health and disease are not causally neutral; their conceptualization impacts what causes are sought and actions should follow. ML systems using empty or homogenized socially constructed concepts will leave social inequalities unconsidered, even if these are real causes of health disparities.
9. **Social Mechanisms:** Social mechanisms must involve the categorization of agents, with behavior partly determined by social roles. Their presence must be established by empirical research.

### D. Education Systems & Philosophy

1. **Educational Causal Context:** Causal factors within educational contexts must not be analyzed in isolation from interrelated realms, such as family dynamics or broader societal activities.
2. **Education Causality Scope:** Education must not be understood solely through purely natural causal terms, nor systematically modeled based on narrow biological constructs (e.g., cognitive load) without considering its wider, complex, and dynamic entanglement in real-life educational situations.
3. **Aristotelian Causes in Education:** A scientific account of education, if based purely on Aristotelian "efficient causes," must not neglect the formal, material, and final causes.
4. **Teleological Explanations in Education:** When education is conceived as a dynamic ecology and teleological ecosystem aimed at actualizing values (e.g., autonomous thinking, freedom, care), intentional-teleological explanations of causation must be privileged over purely natural explanations in decision-making processes.

## VIII. Compliance, Quality Assurance & Governance

1. **AOP Framework Compliance (EU/OECD):** Toxicity testing within the EU must prioritize and actively seek alternative testing approaches. The OECD must develop, publish, and ensure strict adherence to relevant standards for the assembly and adoption of Adverse Outcome Pathways (AOPs).
2. **AOP Review Process:** AOPs must undergo a rigorous review process by specialist experts across relevant biological levels before being applied to inform risk assessments. This process must guarantee the quality of information, ensure transparency, require clear disclosure of conflicts of interest for authors and reviewers, name all reviewers, and make reviews public and open for comments.
3. **AOP Wiki Authorship & Citability:** The AOP Wiki must acknowledge authorship and support the citability of discrete AOP elements, providing functionality equivalent to a peer-reviewed scholarly journal. An endorsed AOP or elements within the AOP Wiki must be treated as equivalent to a peer-reviewed scholarly publication.
4. **AOP Wiki Licensing:** Authorial control on the AOP Wiki must be maintained through the application of appropriate Creative Commons (CC) licenses, ensuring that authors’ work is open and properly attributed upon re-use. If a more restrictive license is applied to work on the AOP Wiki prior to publication, it must be renewed annually and cannot be imposed permanently.
5. **AOP Wiki Design for Regulators:** The AOP Wiki's design must facilitate the consideration, comparison, and integration of different forms of evidence for effective uptake and use by regulators and policy makers.
6. **Education System Governance:** Educational systems must not be governed primarily by narrow causal thinking but rather require a complex weighing of reasons and profound insight into how to help learners and teachers realize their potential in alignment with their purposes.

## Key Highlights

* Causal thinking must provide a substantive account to distinguish between mere correlations and exploitable correlations for manipulation and control.
* The ability to modify or intervene in a system is critical for identifying and understanding causal relationships, and causes must be discovered through interventionist methods.
* A model developed for policymakers must include factors that can be influenced by policy to be effective, highlighting potential points of control, as causal models lead to worse decisions unless tailored to a given decision context.
* Systems can only be investigated if relevant external influences on their behavior are known and accounted for, or neglected if negligible for the inquiry.
* Predictive power of a model cannot stand for its explanatory power; these models are evaluated divergently and require additional theoretical work to make a predictive model explanatory.
* For interventions to be a reliable guide to causal structure, they must satisfy various independence assumptions, be 'surgical' in leaving other causal structures intact, and not violate physical law.
* Medical practices must uncover causal mechanisms that are bio-social in nature, incorporating diverse information sources, including patient testimony, rather than reducing disease to solely biological causes.
* Causal-based Explainable AI (XAI) approaches must display causal connections, with 'why-seeking' explanations tethered to the real world or scientific knowledge beyond mere ML model assumptions.
* Adverse Outcome Pathways (AOPs) must undergo a rigorous, transparent review by specialist experts across relevant biological levels before informing risk assessments, ensuring quality and disclosing conflicts of interest.
* Living systems must be individuated based on their organizational closure of constraints, which is requisite for self-maintenance and autonomy, defining their functional boundaries.

## Example ideas

* Develop a standardized methodology for individuating complex causal systems, focusing on identifying internal cohesion, external influences, and 'organizational closure' principles, to improve the precision and reliability of interventions and causal models.
* Implement a robust framework for distinguishing between predictive and causal-explanatory models, especially in AI/ML applications, mandating that 'why-seeking' explanations demonstrate clear causal connections tethered to real-world phenomena, rather than solely relying on predictive accuracy or internal algorithm workings.
* Integrate socio-cultural, structural, and contextual factors into all causal analyses for policy-relevant and healthcare systems, developing methodologies to identify and operationalize these 'socio-markers' and explicitly addressing their impact to avoid 'biologization of health' and epistemic injustices.
* Adopt a 'Weight-of-Evidence' methodology, inspired by the Adverse Outcome Pathway (AOP) framework, for rigorously validating causal claims in scientific and regulatory contexts, requiring explicit demonstration of essentiality, counterfactual evidence, and transparent expert review of proposed causal links.
