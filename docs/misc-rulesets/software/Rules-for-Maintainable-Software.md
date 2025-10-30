# Rules for Maintainable Software: A Refactoring and Design Compendium

**Generated on:** October 27, 2025 at 10:05 PM CDT

---

## I. General Refactoring Principles & Process

1. **Thou Shalt Preserve Observable Behavior:** Refactoring operations must restructure a program without altering its external, observable behavior.
2. **Thou Shalt Separate Activities:** Divide development time distinctly between adding new functionality and refactoring existing code; do not mix these activities within the same change set.
3. **Thou Shalt Integrate Continuously and Incrementally:** Perform refactoring systematically in minimal, discrete steps, integrating continuously in small bursts rather than scheduling large, dedicated refactoring periods.
4. **Thou Shalt Refactor Proactively:** Refactor code to facilitate the addition of new features *before* implementing them.
5. **Thou Shalt Refactor Reactively:** Engage in refactoring to improve code clarity when fixing bugs or during the code review process.
6. **Thou Shalt Avoid Refactoring Near Deadlines:** Do not initiate significant refactoring when a project is very close to its release deadline.
7. **Thou Shalt Not Postpone Refactoring Indefinitely:** Except for imminent deadlines, do not postpone refactoring due to a perceived lack of time, as this often signals a *need* for refactoring.
8. **Thou Shalt Aim for Reasonable Design:** Trust refactoring to evolve initial reasonable designs into optimal ones, rather than striving for perfect upfront designs.
9. **Thou Shalt Build the Simplest Solution:** Always implement the simplest thing that can possibly work to achieve the desired outcome.
10. **Thou Shalt Defer Performance Optimization:** Focus on performance optimization in a dedicated phase, not during refactoring, which primarily aims for clarity and maintainability.
11. **Thou Shalt Address Code Smells:** Actively identify and change code that exhibits "bad smells."
12. **Thou Shalt Modify Code Ownership for Collaboration:** Adjust code ownership policies and foster team coordination to facilitate large-scale refactoring efforts.
13. **Thou Shalt Document Refactoring Intentions:** Maintain a list of pending changes (e.g., tests to add, unrelated refactorings, documentation updates) to stay focused on the current refactoring's goal of behavior preservation.

## II. Code Design & Structure

14. **Thou Shalt Prioritize Human Readability:** Design code for human understanding above strict machine efficiency or conciseness.
15. **Thou Shalt Emphasize Semantic Clarity in Naming:** Name all entities, especially extracted methods, by their intention and purpose, not their implementation details. Rename badly named methods immediately. Reorder parameters if it clarifies intent.
16. **Thou Shalt Replace Descriptive Comments with Methods:** Convert blocks of code with explanatory comments into well-named methods that clearly articulate the code's purpose.
17. **Thou Shalt Adhere to Query-Modifier Separation:** Strictly separate methods that query an object's state from those that modify it. A method returning a value must not have observable side effects.
18. **Thou Shalt Place Methods with Their Data:** Co-locate methods on the object whose data they primarily utilize.
19. **Thou Shalt Co-locate Related Changes:** Put code and data that frequently change together in the same location.
20. **Thou Shalt Localize Variations:** Ensure that changes for a specific variation are localized to a single class, with the class's typing expressing that variation.
21. **Thou Shalt Decompose Methods Aggressively:** Strive for smaller, more focused methods by aggressive decomposition.
22. **Thou Shalt Avoid Long Parameter Lists:** Leverage objects to encapsulate related parameters and maintain short parameter lists.
23. **Thou Shalt Unify Duplicated Code:** Eliminate duplicate code structures and behavior to improve design, prevent bugs, and enhance maintainability. Refactor when a similar code pattern or duplication appears for the third time.
24. **Thou Shalt Separate UI and Business Logic:** Ensure presentation classes contain only UI-related logic, and domain objects contain only business logic, devoid of visual code.
25. **Thou Shalt Manage Bidirectional Associations Prudently:** Use bidirectional associations only when strictly necessary, assigning control of them to a single class to centralize logic.
26. **Thou Shalt Limit Array Usage:** Use arrays exclusively for ordered collections of similar objects, not for collections of different types.

## III. Encapsulation & Immutability

27. **Thou Shalt Hide Data Fields:** All data fields must be hidden (private). Immediately encapsulate any public fields. Never expose class fields directly as public.
28. **Thou Shalt Encapsulate Collections:** Getters for collections must return a read-only view or a copy, not the collection object itself. Do not provide setters for collections; instead, provide `add` and `remove` methods.
29. **Thou Shalt Hide Methods When Possible:** Make methods as private as possible to improve interface clarity and control visibility.
30. **Thou Shalt Publish Interfaces Only When Needed:** Avoid premature publication of interfaces. If a refactoring changes a published interface, retain both the old and new interfaces (marking the old as `deprecated`) until users adapt.
31. **Thou Shalt Encapsulate Downcasts:** Prevent client code from performing downcasts directly by encapsulating them within the object providing the type.
32. **Thou Shalt Favor Immutability for Value Objects:** Make value objects immutable to prevent aliasing bugs and ensure predictable state. For fields that should not change after object creation, do not provide a setting method and declare the field `final`.
33. **Thou Shalt Provide Most Specific Return Types:** Return the most specific type possible from methods to avoid forcing clients to downcast.
34. **Thou Shalt Define Null Interfaces Without Methods:** When implementing the Null Object pattern, the null interface should not define any methods.

## IV. Object-Oriented Design & Hierarchy

35. **Thou Shalt Replace Type Codes with Polymorphism:**
    * If a type code is pure data, replace it with a dedicated class.
    * If a type code influences conditional behavior, use `Replace Type Code with Subclasses` (if immutable at runtime) or `Replace Type Code with State/Strategy` (if mutable or already subclassed).
    * If a type code is passed to a constructor, replace the constructor with a factory method.
    * When extracting a subclass and a field designates information now indicated by the hierarchy, eliminate the field by `Self Encapsulating Field` and replacing the getter with polymorphic constant methods. Refactor all users of this field with `Replace Conditional with Polymorphism`.
36. **Thou Shalt Structure Data Classes Simply:** Data classes must have private fields with getting and setting methods for each data item.
37. **Thou Shalt Respect Superclass Contracts:** When altering a method to return a subclass, ensure the subclass does not break the contract of the superclass.
38. **Thou Shalt Limit Inheritance:** Use inheritance for a single set of variations; for multiple ways a class needs to vary, prefer delegation. Understand that constructors are not inherited and class-based behavior cannot be changed after object creation via subclasses.
39. **Thou Shalt Declare Abstract Superclasses Appropriately:** If a superclass can no longer be directly instantiated after extracting a subclass, declare it `abstract`.
40. **Thou Shalt Protect Superclass Fields for Subclass Access:** If fields in a superclass are private, make them `protected` if subclasses need to refer to them when pulling up.
41. **Thou Shalt Call Superclass Constructors First:** In a subclass constructor, always call the superclass constructor as the *first step*.
42. **Thou Shalt Manage Pulled-Up Methods with Fields:** When pulling up a method that uses a subclass field, either pull up the field (`Pull Up Field`) or `Self Encapsulate Field` and declare/use an abstract getting method in the superclass.
43. **Thou Shalt Declare Abstract Methods for Common Signatures:** If methods have the same signature but different bodies across a hierarchy, declare the common signature as an `abstract` method on the superclass.
44. **Thou Shalt Prefer Inheritance to Delegation Judiciously:** Avoid `Replace Delegation with Inheritance` if not all methods of the delegated class are used, as a subclass must always follow the superclass's interface.

## V. Testing & Validation

45. **Thou Shalt Ensure Code Functionality Before Refactoring:** Code must be mostly correct and functional before any refactoring begins.
46. **Thou Shalt Build a Robust Test Suite First:** Always begin refactoring by building a solid, self-checking test suite for the targeted code.
47. **Thou Shalt Test Continuously and Frequently:** Follow a rhythm of continuous testing and small changes during refactoring. Run tests frequently, at least daily, localizing tests to compile cycles.
48. **Thou Shalt Automate All Tests:** All tests must be fully automatic and self-checking, requiring no manual intervention.
49. **Thou Shalt Ensure Fast and Focused Tests:** Tests run during refactoring must be fast and focused specifically on the changed code.
50. **Thou Shalt Never Skip Tests:** Resist the temptation to skip running tests due to perceived slowness.
51. **Thou Shalt Test New Features First:** When adding a new feature, begin by writing its corresponding test.
52. **Thou Shalt Write Bug-Exposing Tests:** Upon receiving a bug report, first write a unit test that specifically exposes and reproduces the bug.
53. **Thou Shalt Prioritize Risk-Driven Testing:** Focus testing efforts on high-risk areas of the codebase.
54. **Thou Shalt Avoid Excessive Testing:** Do not write tests for simple accessors that merely read or write fields.
55. **Thou Shalt Test Boundary Conditions:** Concentrate testing efforts on boundary conditions.
56. **Thou Shalt Test Expected Error Conditions:** Include tests for expected error conditions, such as thrown exceptions.
57. **Thou Shalt Be Pragmatic with Testing:** Do not let the inability to catch all bugs deter writing tests that catch most. Prefer running incomplete tests over not running comprehensive tests at all.
58. **Thou Shalt Separate Test Types:** Differentiate between unit tests (highly localized to a single package) and functional tests (ensuring overall software functionality, typically black-box).

## VI. Error Handling & Assertions

59. **Thou Shalt Use Exceptions for Exceptional Behavior:** Employ exceptions to separate normal processing from error processing, reserving them for unexpected errors rather than as a substitute for conditional tests.
60. **Thou Shalt Provide Tests for Expected Conditions:** If a caller can reasonably be expected to check a condition before calling a method, provide a test for that condition, and the caller should use it.
61. **Thou Shalt Use Unchecked Exceptions for Caller Responsibility:** If the caller is responsible for testing a condition, make the resulting exception unchecked.
62. **Thou Shalt Use Guard Clauses for Exceptional Conditions:** Implement guard clauses for conditional checks when the behavior is truly exceptional, ensuring they either return or throw an exception.
63. **Thou Shalt Make Assumptions Explicit with Assertions:** Use assertions to explicitly state conditions that *must* be true within the code's logic.
64. **Thou Shalt Use Assertions Sparingly and Internally:** Do not overuse assertions. Use them only for essential internal conditions that *must* hold, not for external system interaction, and not for checking everything that might be true.
65. **Thou Shalt Handle Assertion Failures Gracefully:** Assertion failures must always result in unchecked exceptions.
66. **Thou Shalt Remove Assertions from Production Code:** Design assertions to be easily removable (e.g., via a compile-time flag) so they do not affect performance or behavior in production.
67. **Thou Shalt Guard Assertion Expressions:** Ensure any expressions within assertion parameters are guarded if they should not execute in production.
68. **Thou Shalt Remove Unnecessary Assertions:** If code functions correctly even when an assertion fails, or if an assertion becomes confusing, remove it.
69. **Thou Shalt Avoid Duplicate Code in Assertions:** Use `Extract Method` to remove duplicate code found within assertions.

## VII. Concurrency & Parallelism

70. **Thou Shalt Maintain Test-and-Set Operations:** In multithreaded systems, if a query and modifier are separated, but a single atomic test-and-set operation is required, retain a third, synchronized method that performs both actions by calling the separate query and modify methods.
71. **Thou Shalt Restrict Visibility for Unsynchronized Methods:** If separate query and modify operations are not synchronized, restrict their visibility to package or private levels.
72. **Thou Shalt Prefer Immutability in Concurrent Contexts:** Be cautious when shortening parameter lists in concurrent programming; prefer passing immutable objects whenever possible.

## VIII. Language & Platform Specifics

73. **Thou Shalt Use Exact Types for Monetary Values (Java):** Never use `double` for monetary values in commercial Java software.
74. **Thou Shalt Understand Java's Pass-by-Value:** Be aware that Java strictly uses pass-by-value for all parameters.
75. **Thou Shalt Treat Java Parameters as Final:** Do not assign new values to method parameters in Java; treat them as `final` (enforced with the `final` keyword).
76. **Thou Shalt Leverage the Compiler for Reference Hunting (Java):** Use the compiler in strongly typed languages like Java to find dangling references, especially when removing features.
77. **Thou Shalt Respect Java Checked Exception Inheritance:** The Java compiler prevents adding new checked exceptions to a method's `throws` clause in overriding methods if not present in the superclass.
78. **Thou Shalt Adhere to `equals()` and `hashCode()` Contract (Java):** If `equals()` is overridden, `hashCode()` must also be overridden. Define `hashCode()` by XORing hash codes of fields used in `equals()`.
79. **Thou Shalt Enable Conditional Assertion Execution (Java):** Use a `final` static boolean flag (e.g., `Assert.ON`) for conditional assertion execution, allowing compiler optimization to remove assertions from production code.
80. **Thou Shalt Avoid Refactoring-Impeding C++ Features:** To ease refactoring, avoid C++ language features such as raw pointers, cast operations, `sizeof(object)`, pointer arithmetic, and conditional tests based on object size, as they expose internal representation and can break behavior.

## IX. Refactoring Execution Directives

81. **Thou Shalt Compile and Test After Each Significant Step:** During refactoring, always compile and test after each major change or discrete step to immediately identify and localize issues.
82. **Thou Shalt Restrict Method Extraction (Extract Method):** Do not extract a method if a more meaningful name cannot be found, or if more than one local-scope variable is modified (instead, use `Split Temporary Variable` first).
83. **Thou Shalt Avoid Inlining Polymorphic Methods (Inline Method):** Do not inline polymorphic methods that are overridden by subclasses.
84. **Thou Shalt Ensure Query Side-Effect Freedom (Replace Temp with Query):** Ensure that any query methods extracted are free of side effects.
85. **Thou Shalt Declare Explaining Variables as Final (Introduce Explaining Variable):** Declare temporary variables introduced for explanation as `final`.
86. **Thou Shalt Not Split Collecting Temporaries (Split Temporary Variable):** Do not split temporary variables that accumulate values (e.g., `i = i + expression`).
87. **Thou Shalt Make Source Object Field Final (Replace Method with Method Object):** In a new method object, the field for the source object must be `final`.
88. **Thou Shalt Restrict Moving Polymorphic Methods (Move Method):** Moving polymorphic methods is restricted unless their polymorphism can be replicated in the target class.
89. **Thou Shalt Encapsulate Before Moving Fields (Move Field):** Encapsulate public fields before moving them.
90. **Thou Shalt Avoid Unnecessary Back Links (Extract Class):** Do not create a back link in a newly extracted class unless it is explicitly needed.
91. **Thou Shalt Hide Delegates (Hide Delegate):** Create delegating methods on the server class to hide delegate objects from clients.
92. **Thou Shalt Isolate Foreign Methods (Introduce Foreign Method):** Foreign methods must not access client class features; pass all needed values as parameters. The first parameter must be an instance of the server class. Mark foreign methods with a comment like "foreign method; should be in server".
93. **Thou Shalt Use Wrappers for Mutable Local Extensions (Introduce Local Extension):** For local extensions, use a wrapper if the original object is mutable; otherwise, a subclass is simpler.
94. **Thou Shalt Prefer Direct Access in Constructors/Observers (Self Encapsulate Field, Duplicate Observed Data):** When self-encapsulating a field, prefer direct field access or a separate initialization method over using the setter in the constructor. Similarly, when updating GUI components from event handlers or within an observer's update method, use direct access to avoid infinite recursion.
95. **Thou Shalt Avoid Consolidating Conditional Expressions with Side Effects (Consolidate Conditional Expression):** Do not consolidate conditional expressions if any of them have side effects.
96. **Thou Shalt Replace Control Flag Assignments with Control Flow (Remove Control Flag):** Replace assignments to a control flag's break-out value with `break`, `continue`, or `return` statements.
97. **Thou Shalt Make Superclass Members Protected for Polymorphism (Replace Conditional with Polymorphism):** Private superclass members may need to be made `protected` when moving conditional logic to subclasses.
98. **Thou Shalt Systematically Apply Null Objects (Introduce Null Object):** Replace all `null` returns for a source object with a null object. Replace all null checks (`== null`) with calls to `isNull()` on the object. Place assertions to check for `null` in locations where null objects are expected to eliminate actual `null` values.

## X. Tooling & Environment

99. **Thou Shalt Recognize Tooling Limitations:** Refactoring tools must reasonably preserve program behavior, though total preservation (e.g., minor performance changes) is impossible.
100. **Thou Shalt Be Wary of Reflection Limitations:** If a program uses reflection to execute methods by name, automated renaming will cause runtime exceptions that tools may not detect at compile time; rely on text searches and increased testing for such cases.
101. **Thou Shalt Demand Fast Tools:** Refactoring tools must operate quickly; slow analysis discourages their use.
102. **Thou Shalt Utilize Program Databases:** A refactoring tool requires a program database (searchable repository) to find references to program entities across the entire program.
103. **Thou Shalt Use Parse Trees for Fine-Grained Refactorings:** Refactoring tools need parse trees to manipulate system portions below the method level (e.g., extracting method fragments).

## Key Highlights

* Refactoring operations must restructure a program without altering its external, observable behavior.
* Divide development time distinctly between adding new functionality and refactoring existing code; do not mix these activities within the same change set.
* Do not postpone refactoring due to a perceived lack of time, as this often signals a *need* for refactoring.
* Design code for human understanding above strict machine efficiency or conciseness.
* Eliminate duplicate code structures and behavior to improve design, prevent bugs, and enhance maintainability.
* All data fields must be hidden (private); never expose class fields directly as public.
* Always begin refactoring by building a solid, self-checking test suite for the targeted code.
* During refactoring, always compile and test after each major change or discrete step to immediately identify and localize issues.

## Next Steps & Suggestions

* Operationalize continuous refactoring: Establish clear processes and guidelines for integrating continuous, small-scale refactoring into daily development workflows, ensuring distinct separation from new feature development and proactive refactoring before new implementations.
* Strengthen automated testing foundation: Conduct an audit and strategic improvement plan for existing automated test suites to guarantee they are comprehensive, fast, and self-checking, thereby providing the necessary safety net for all refactoring activities.
* Enforce design and code quality standards: Integrate key design principles (e.g., semantic naming, aggressive method decomposition, strong encapsulation, polymorphism over type codes) into mandatory code review processes and consider adopting static analysis tools to proactively identify and rectify 'code smells'.
* Invest in developer education and practical application: Develop and roll out practical workshops or training modules focusing on the explicit refactoring execution directives and object-oriented design principles to enhance the team's ability to apply these commandments effectively and consistently.
