# Rules for High Quality Code

These rules encapsulate best practices, coding standards, and architectural principles essential for high-quality software development, readability, maintainability, and collaboration.

**Generated on:** October 28, 2025 at 12:34 AM CDT

---

## I. Professionalism & Code Quality

* **1. Always Strive for Clean Code:** Consistently write clean, high-quality code. This is paramount for project success, maintainability, and efficiency.
* **2. Continuously Improve:** Embed continuous code improvement as an intrinsic part of professionalism; expect and engage in continual rework to enhance existing code.
* **3. Defend Quality:** Do not compromise code quality due to schedule pressure or management demands.
* **4. Rigor & Accuracy:** Code must be rigorous, accurate, formal, and detailed enough for a machine to understand and execute.
* **5. Embrace Simplicity:** Always use the simplest thing that can possibly work.
* **6. Don't Repeat Yourself (DRY):** Eliminate duplication in code as a primary enemy of good design. Actively remove duplication, even in small code segments.

## II. Naming Conventions

* **1. Reveal Intent:** Use intention-revealing names for variables, functions, classes, and other constructs. If a name requires a comment to explain its purpose, it fails to reveal its intent.
* **2. Avoid Disinformation:** Do not use names that mislead or provide disinformation. This includes inconsistent spellings and using similar names for subtly different concepts.
* **3. Make Meaningful Distinctions:** When names must differ, make meaningful distinctions. Avoid arbitrary number series (`a1`, `a2`) or noise words (`Info`, `Data`, `variable`, `table`, `the`).
* **4. Prefer Pronounceable Names:** Names should be pronounceable to facilitate discussion and comprehension.
* **5. Scope-Appropriate Length:** The length of a name should correspond to the size of its scope. Give search-friendly names to variables or constants used in multiple places.
* **6. Avoid Encodings:** Do not include type or scope information in names (e.g., Hungarian Notation, `m_` prefixes for member variables) if modern IDEs provide this context.
* **7. Interface vs. Implementation Encoding:** When encoding interfaces or implementations, prefer encoding the implementation (e.g., `ShapeFactoryImpl` over `IShapeFactory`).
* **8. Class & Object Naming:** Class and object names must be nouns or noun phrases (e.g., `Customer`, `WikiPage`, `Account`). Avoid weasel words like `Manager`, `Processor`, `Data`, `Info`, or `Super` in class names. A class name must not be a verb.
* **9. Method Naming:** Method names must be verbs or verb phrases (e.g., `postPayment`, `deletePage`).
* **10. Standard Accessors/Mutators:** Name accessors, mutators, and predicates according to the JavaBean standard (e.g., `get`, `set`, `is`).
* **11. Static Factory Methods for Constructors:** When constructors are overloaded, use static factory methods with names that describe their arguments.
* **12. Clarity Over Cuteness:** Do not use cute or colloquial names; choose clarity over entertainment.
* **13. Consistent Vocabulary:** Pick one word per abstract concept and use it consistently across different classes. Avoid using the same word for two different purposes (avoid puns).
* **14. Use Domain & CS Terms:** Use computer science terms, algorithm names, pattern names, and math terms where appropriate. Use problem domain names when no "programmer-ese" applies.
* **15. Provide Context:** Add meaningful context to names by enclosing them in well-named classes, functions, or namespaces. As a last resort, prefixing may be necessary. Do not add gratuitous context (e.g., system abbreviations). Add no more context than necessary.
* **16. Avoid Ambiguous Characters:** Avoid using `l` (lowercase L) or `O` (uppercase O) as variable names, especially in combination, due to their resemblance to `1` and `0`.

## III. Function Design

* **1. Keep Functions Small:** Keep functions small, ideally under 20 lines, and certainly under 100 lines.
* **2. Simple Blocks:** Keep `if`, `else`, `while` blocks to a single line, preferably a function call.
* **3. Limit Indentation:** Limit function indentation to one or two levels; avoid deep nesting.
* **4. Single Responsibility:** Functions must do one thing, do it well, and do it only.
* **5. Consistent Abstraction:** Maintain a consistent level of abstraction within a function; avoid mixing levels of abstraction.
* **6. The Stepdown Rule:** Code should read like a top-down narrative, descending one level of abstraction at a time.
* **7. Limited Switch Statements:** Tolerate switch statements only if they appear once, are used to create polymorphic objects, and are hidden behind an inheritance relationship.
* **8. Minimize Arguments:** The ideal number of arguments for a function is zero (niladic). Next best is one (monadic), followed closely by two (dyadic). Avoid three arguments (triadic) where possible, and polyadic functions (more than three) require very special justification.
* **9. Avoid Output Arguments:** Avoid output arguments; return transformations as the return value instead.
* **10. No Flag Arguments:** Avoid flag arguments (passing a boolean into a function); split functions into two if a flag would be used.
* **11. Argument Objects:** If a function needs more than two or three arguments, wrap those arguments into a class of their own (argument objects).
* **12. No Side Effects:** Functions must have no side effects.
* **13. Explicit Temporal Coupling:** If a temporal coupling is unavoidable, it must be clearly indicated in the function's name.
* **14. Command Query Separation (CQS):** Functions must either do something or answer something, but not both.
* **15. Enforce Static Factories:** Consider enforcing the use of static factory methods by making corresponding constructors private.
* **16. Multiple Exit Points (with care):** If functions are small, occasional multiple `return`, `break`, or `continue` statements are acceptable if they improve expressiveness.
* **17. No Goto:** Avoid `goto` statements.

## IV. Class & Object Design

* **1. Small Classes:** Software systems must be composed of many small classes, not a few large ones.
* **2. Encapsulate Data:** Variables must be private to prevent external dependencies and preserve freedom to change their type/implementation. Avoid automatically adding public getters and setters that expose private variables as if they were public.
* **3. Abstract Interfaces:** A class must expose abstract interfaces that allow users to manipulate the essence of data, not its implementation details. Objects must hide their data behind abstractions and expose functions that operate on that data.
* **4. Single Responsibility Principle (SRP):** Keep classes small, with a single responsibility, and encapsulate their data behind abstract interfaces. If a concise name cannot be derived, the class is likely too large.
* **5. Small Number of Instance Variables:** Classes should have a small number of instance variables.
* **6. High Cohesion:** Each method of a class should manipulate one or more of its instance variables. When classes lose cohesion, split them into new, more cohesive classes.
* **7. Law of Demeter:** Adhere to the Law of Demeter: a method should only call methods of its own class, objects it creates, arguments, or direct instance variables. Avoid "train wreck" chains of calls (e.g., `ctxt.getOptions().getScratchDir().getAbsolutePath()`).
* **8. Tell, Don't Ask:** If an object is an object, tell it to do something; do not ask it about its internals.
* **9. Reduce Change Risk:** Organize classes to reduce the risk of change. If you find yourself frequently modifying a class, consider fixing its design.
* **10. Open-Closed Principle (OCP):** Follow the Open-Closed Principle (OCP): classes should be open for extension but closed for modification. Incorporate new features by extending the system, not by modifying existing code.
* **11. Dependency Inversion Principle (DIP):** Introduce interfaces and abstract classes to help isolate the impact of changing concrete details. Client classes should depend upon abstractions, not on concrete details.
* **12. Protect Encapsulation:** Loosening encapsulation (making variables/functions protected or package scope for tests) is always a last resort.

## V. Data Structures

* **1. Expose Data, No Functions:** Data structures must expose their data and have no meaningful functions.
* **2. Avoid Hybrids:** Avoid creating hybrid structures that are half object and half data structure; they are the worst of both worlds.
* **3. Data Transfer Objects (DTOs):** DTOs are classes with public variables and no functions.
* **4. Active Record Separation:** Treat Active Records as data structures and create separate objects that contain business rules.

## VI. Comments & Documentation

* **1. Rewrite, Don't Comment Bad Code:** Do not comment bad code; rewrite it.
* **2. Minimize Comments:** Minimize comments; they are, at best, a necessary evil indicating a failure to express intent clearly in code.
* **3. Ensure Accuracy:** Ensure comments are accurate; inaccurate comments are far worse than no comments at all. Avoid misleading comments.
* **4. Code Over Comments:** Prefer expressing intent in code through clear names and small functions, rather than relying on comments.
* **5. Legal Comments:** Legal comments (copyright, authorship) are necessary and reasonable, and should refer to a standard license or external document rather than containing all terms and conditions.
* **6. TODOs as Temporary Notes:** TODO comments are acceptable for temporary notes about future work but are not an excuse to leave bad code. Scan and eliminate them regularly.
* **7. Javadocs for Public APIs Only:** Require well-written Javadocs for public APIs only; do not generate them for internal classes or functions.
* **8. Avoid Redundancy & Noise:** Avoid redundant, mumbling, or noise comments written merely to fulfill process requirements (e.g., restating the obvious, "The name.").
* **9. Local Relevance:** Comments must describe the code they appear near; do not offer system-wide information, historical discussions, or irrelevant details in a local comment.
* **10. Obvious Connection:** The connection between a comment and the code it describes must be obvious.
* **11. Don't Comment Out Code:** Do not comment-out code; delete it as source control systems will remember it.
* **12. No Journal Comments/Bylines:** Journal comments (log entries) and bylines (attributions) must be completely removed from source code, as source control systems handle this.
* **13. Avoid Closing Brace Comments:** Avoid closing brace comments; shorten functions instead.
* **14. No HTML in Source Comments:** HTML in source code comments is an abomination. If comments are extracted to appear in a Web page, the tool, not the programmer, should adorn them with HTML.

## VII. Formatting & Readability

* **1. Consistent Formatting:** Code must be nicely formatted. Teams must agree to a single formatting style and apply it consistently using an automated tool.
* **2. Short Lines:** Strive to keep lines short (e.g., limit to 120 characters).
* **3. Vertical Spacing:** Use vertical white space to separate distinct concepts and visually group tightly related lines. Code with strong conceptual affinity should have less vertical distance between its parts.
* **4. Variable Declaration Placement:** Declare variables as close to their usage as possible. Local variables should appear at the top of very short functions. Control variables for loops should usually be declared within the loop statement. Instance variables must be declared at the top of the class, in one well-known place.
* **5. Function Ordering (Stepdown Rule):** Order functions vertically so that callers appear above callees (The Stepdown Rule), ensuring function call dependencies point in the downward direction.
* **6. Horizontal Spacing:** Use horizontal white space to associate strongly related things and disassociate weakly related things.
  * Surround assignment operators with white space.
  * Do not put spaces between function names and opening parentheses.
  * Separate arguments within function call parentheses with spaces.
  * Use white space to accentuate the precedence of operators (e.g., no space for high precedence, space for low precedence).
* **7. Avoid Horizontal Alignment:** Avoid horizontal alignment for variable declarations or assignment statements.
* **8. Indentation:** Indent lines of source code in proportion to their position in the hierarchy (scope).
  * Statements at the file level (e.g., class declarations) must not be indented.
  * Methods within a class are indented one level to the right of the class.
  * Implementations of methods are indented one level to the right of the method declaration.
  * Block implementations are indented one level to the right of their containing block.
  * Avoid breaking the indentation rule for short `if` statements, `while` loops, or functions; expand and indent scopes instead.
* **9. No Dummy Bodies:** Avoid dummy bodies of `while` or `for` statements; if unavoidable, ensure they are properly indented and surrounded by braces.
* **10. Java Class Organization:** Follow the standard Java convention for class organization: Public static constants first, then private static variables, followed by private instance variables, and then public functions, with private utilities placed immediately after their calling public function.

## VIII. Error Handling & Null Management

* **1. Don't Obscure Logic:** Error handling must not obscure the main logic.
* **2. Prefer Exceptions:** Prefer exceptions over returning error codes for error handling. Throw an exception when an error is encountered.
* **3. Use `try-catch-finally` Proactively:** When writing code that could throw exceptions, start by writing the `try-catch-finally` statement first.
* **4. Consistent State:** The `catch` block must leave the program in a consistent state.
* **5. Prefer Unchecked Exceptions:** Prefer unchecked exceptions in general application development due to the dependency costs of checked exceptions.
* **6. Informative Exceptions:** Each thrown exception must provide informative messages and sufficient context to determine the source and location of an error.
* **7. Caller-Centric Exception Design:** Define exception classes in terms of a caller's needs (i.e., how they are caught).
* **8. Single Exception Class per Area:** Use a single exception class for a particular area of code unless there's a specific need to catch exceptions separately.
* **9. Exceptions for Errors, Not Control Flow:** Define the normal flow of execution; do not use exceptions for normal special cases (use the Special Case Pattern instead).
* **10. Extract Error Handling:** Extract the bodies of `try` and `catch` blocks into their own functions. If a function handles errors, it must do nothing else.
* **11. `try` Block Structure:** If the keyword `try` exists in a function, it should be the very first word, and there should be nothing after the `catch`/`finally` blocks.
* **12. OCP for Exceptions:** When using exceptions, new exception classes should be derivatives of the base exception class (adhering to OCP).
* **13. No `null` Returns:** Do not return `null` from methods. If tempted to return `null`, consider throwing an exception or returning a Special Case object. If calling a third-party method that returns `null`, wrap it to throw an exception or return a Special Case object.
* **14. No `null` Arguments:** Do not pass `null` into methods; forbid passing `null` by default.

## IX. System Boundaries & Integration

* **1. Clean Integration:** Cleanly integrate foreign code (third-party, open source, components from other teams).
* **2. Localize Boundary Interfaces:** Minimize exposure of third-party or boundary interfaces; keep them localized inside the class or close family of classes where they are used, and avoid passing them liberally throughout the system.
* **3. Restrict Public API Exposure:** Avoid returning boundary interfaces from, or accepting them as arguments to, public APIs.
* **4. Learning Tests:** Write learning tests to explore and understand third-party code.
* **5. Outbound Tests:** Ensure clean boundaries are supported by a set of outbound tests that exercise the interface the same way production code does.
* **6. Define Your Own Interface:** Define your own interface for code that does not yet exist to avoid being blocked by external dependencies.
* **7. Wrap Third-Party APIs:** Wrap third-party APIs using patterns like Adapter to minimize dependencies, simplify mocking for testing, and define a consistent API you are comfortable with.
* **8. Clear Separation & Tests:** Code at the boundaries needs clear separation and tests that define expectations.

## X. Unit Testing & TDD

* **1. The Three Laws of TDD:**
  * You may not write production code until you have written a failing unit test.
  * You may not write more of a unit test than is sufficient to fail, and not compiling is failing.
  * You may not write more production code than is sufficient to pass the currently failing test.
* **2. Test Code Quality:** Treat test code with the same importance, care, and cleanliness as production code. Prioritize readability, clarity, simplicity, and density of expression in tests.
* **3. DRY in Tests:** Eliminate duplicate code in tests (DRY principle).
* **4. Expressive Tests:** Do not load tests with details that interfere with expressiveness.
* **5. BUILD-OPERATE-CHECK:** Follow the BUILD-OPERATE-CHECK pattern for test structure.
* **6. Testing DSLs:** Invent testing APIs that act as a domain-specific language to make tests expressive and succinct.
* **7. Single Concept per Test:** Test a single concept in each test function; minimize the number of assert statements in a test and avoid long test functions that test miscellaneous things.
* **8. F.I.R.S.T. Principles:** Adhere to the F.I.R.S.T. principles for tests:
  * **F**ast: Tests should run quickly.
  * **I**ndependent: Tests should not depend on each other.
  * **R**epeatable: Tests should produce the same results in any environment.
  * **S**elf-Validating: Tests should have a clear boolean output (pass/fail).
  * **T**imely: Tests should be written just before the production code that makes them pass.
* **9. Executable Requirements:** Well-specified requirements must be as formal as code and act as executable tests.
* **10. Documentation by Example:** Well-written unit tests must act as documentation by example.
* **11. Testable Design:** Make systems fully testable to drive better designs.

## XI. Architectural Design

* **1. Separate Startup from Runtime:** Software systems must separate the startup process (object construction and dependency wiring) from the runtime logic.
* **2. Consolidate Construction:** Move all aspects of object construction to `main` or modules called by `main`; the application itself must have no knowledge of `main` or the construction process.
* **3. Abstract Factory for Object Creation:** When the application must create objects, use the ABSTRACT FACTORY pattern to keep construction details separate from application code.
* **4. Dependency Injection (DI):** Use Dependency Injection (DI) to separate object construction from use. Objects should not take responsibility for instantiating their dependencies but should provide setter methods or constructor arguments for dependencies to be injected.
* **5. Incremental Growth:** Software system architectures can grow incrementally if proper separation of concerns is maintained.
* **6. Avoid Big Design Up Front (BDUF):** Avoid Big Design Up Front (BDUF) as it inhibits adapting to change.
* **7. Modular POJO Architecture:** An optimal system architecture consists of modularized domains of concern, each implemented with Plain Old Java Objects (POJOs), integrating different domains using minimally invasive Aspects or Aspect-like tools.
* **8. Test-Driven Architecture:** System architecture can be test-driven.
* **9. Postpone Decisions:** Postpone architectural and design decisions until the last possible moment to make informed choices.
* **10. Wise Use of Standards:** Use standards wisely, only when they add demonstrable value.
* **11. Domain-Specific Languages (DSLs):** Systems need Domain-Specific Languages (DSLs) to minimize the "communication gap" between domain concepts and code. DSLs allow all levels of abstraction and domains to be expressed as POJOs.
* **12. Clear Intent:** System intent should be clear at all levels of abstraction.
* **13. Pragmatism Over Dogmatism:** Resist dogmatism (e.g., an interface for every class, separating fields and behavior always); adopt a pragmatic approach.
* **14. Overall System Smallness:** Keep the overall system small while keeping functions and classes small.

## XII. Concurrency

* **1. Isolate Concurrency Code:** Keep concurrency-related code separate from other code (SRP).
* **2. Limit Shared Data:** Severely limit access to shared data, using encapsulation or copies to avoid sharing where possible.
* **3. Independent Threads:** Threads should be as independent as possible. Attempt to partition data into independent subsets that can be operated on by independent threads.
* **4. Understand Concurrent Algorithms:** Learn basic concurrent algorithms (Producer-Consumer, Readers-Writers, Dining Philosophers) and understand their solutions.
* **5. Prefer Server-Based Locking:** Prefer server-based locking over client-based locking, as client-based locking is risky and requires consistent application.
* **6. Wrap Non-Thread-Safe Third-Party Code:** When integrating non-thread-safe third-party code, use an Adapter pattern to add locking for thread safety, or prefer thread-safe collections with extended interfaces.
* **7. Small Synchronized Sections:** Keep synchronized sections as small as possible. Avoid using more than one synchronized method on the same shared class.
* **8. Graceful Shutdown:** Think about graceful shutdown early in the design phase and get it working early.
* **9. POJOs for Non-Threaded Logic:** Place as much of your system as possible into Plain Old Java Objects (POJOs) that are not thread-aware.
* **10. Test Nonthreaded Code First:** Get nonthreaded code working first before addressing threading bugs; ensure code works reliably outside of threads.
* **11. Deadlock Prevention:**
  * To prevent deadlock, consistently break at least one of the four deadlock conditions (mutual exclusion, lock & wait, no preemption, circular wait).
  * Break mutual exclusion: Use resources that permit simultaneous use (e.g., `AtomicInteger`), or increase resource count to exceed competing threads.
  * Break lock & wait: If a required resource cannot be immediately acquired, release all currently held resources and restart the acquisition process.
  * Break no preemption: Implement a mechanism for a thread to discover a resource is busy and ask the owner to release it; if the owner is also waiting, it must release all its resources and start over.
  * Break circular wait: Enforce a global ordering for resource allocation, ensuring all threads acquire resources strictly in that predetermined order.
* **12. Concurrency Testing:**
  * Write tests that have the potential to expose concurrent problems.
  * Design multithreaded tests to be flexible, tunable, and specifically simulate multiple users under varying loads.
  * Run multithreaded tests frequently and continuously, with different programmatic and system configurations, and under load, on all target platforms.
  * If concurrent tests ever fail, always consider the code broken and track down the failure; do not ignore intermittent failures as "one-offs."
  * Carefully log the conditions under which a multithreaded test failed.
  * Instrument multithreaded test and production code (e.g., by adding calls to `Object.wait()`, `Object.sleep()`, `Object.yield()`, and `Object.priority()`) to increase the likelihood of exposing threading issues.
  * Run with more threads than processors or cores to encourage task swapping and expose bugs.
  * Make concurrency-supporting code pluggable (e.g., run with one thread, several threads, or test doubles).

## XIII. Domain-Specific API & Logic (JFreeDate Example)

*Note: These rules are highly specific to a particular domain/API and serve as concrete examples of how general principles manifest. They are included for completeness but are not universally applicable.*

* **1. Java Syntax & API Conventions:**
  * Adhere to specific Java syntax conventions for package declarations (`org.jfree.date`), static imports (`import static ...`), and standard imports (`import ...`).
  * Implement standard Java API methods (`equals`, `hashCode`, `compareTo`) with correct signatures.
  * Define constructors with appropriate parameter types and provide public static factory methods for instance creation.
  * Define private helper methods for internal calculations.
* **2. Date Range & Validation:**
  * Enforce specific date range constraints using constants: e.g., `EARLIEST_DATE_ORDINAL` (2 for 1-Jan-1900), `LATEST_DATE_ORDINAL` (2958465 for 31-Dec-3399), `MINIMUM_YEAR_SUPPORTED` (1900), `MAXIMUM_YEAR_SUPPORTED` (9993).
  * Implement robust validation for constructor arguments (year, day, serial) against defined ranges.
  * Throw `IllegalArgumentException` with informative messages for invalid inputs (e.g., "Invalid ‘day’ argument.", "SpreadsheetDate: Serial must be in range...").
* **3. Behavior & Logic:**
  * Adhere to specific date ordinal conventions (e.g., 1-Jan-1900 corresponds to ordinal value 2).
  * When retrieving the month from a `Calendar` object, add 1 for 1-indexed representations.
  * Ensure specific utility methods return expected domain values (e.g., `_getMinimmYear()` returns `MINIMUM_YEAR_SUPPORTED`, `getDayOfWeekForOrdinalZero()` returns `Day.SATURDAY`).
  * Implement `equals` method logic to compare `DayDate` objects based on their ordinal day values, returning `false` for non-`DayDate` objects.
  * Implement `hashCode` method logic to return the ordinal day value.
  * Delegate `compareTo` method logic to a `daysSince` comparison.
  * Accurately implement ordinal day and day/month/year calculations, accounting for leap years and adjusting for the `EARLIEST_DATE_ORDINAL` convention.

## Key Highlights

* Prioritize clean, high-quality code and continuous improvement, never compromising quality due to external pressures.
* Ensure names reveal intent, use a consistent vocabulary, and prefer clear code over extensive comments to enhance readability and maintainability.
* Design functions to be small, focused on a single responsibility, with minimal arguments, while avoiding side effects and flag parameters for clarity.
* Construct small, cohesive classes that adhere to the Single Responsibility Principle, encapsulate data, and follow the Open-Closed and Dependency Inversion Principles for flexible, maintainable designs.
* Handle errors using informative exceptions rather than returning or accepting null, and ensure the program always remains in a consistent state after an error.
* Treat test code with the same importance as production code, creating fast, independent, repeatable, self-validating, and timely tests that document behavior and drive design.
* Isolate and wrap third-party code at system boundaries to minimize dependencies, and separate object construction from runtime logic using dependency injection.
* Isolate concurrency code, severely limit shared data, and thoroughly test for multi-threading issues and deadlocks, always planning for graceful system shutdown.

## Next Steps & Suggestions

* Integrate static analysis tools (e.g., linters, code formatters, SonarQube) into the CI/CD pipeline to automatically enforce formatting, naming conventions, and identify common rule violations like DRY, excessive function arguments, and deep nesting.
* Develop a phased adoption roadmap for these comprehensive principles, starting with high-impact areas such as Single Responsibility Principle (SRP), clean function design, and robust unit testing, supported by dedicated team training sessions or workshops.
* Update the team's code review checklist and 'Definition of Done' to explicitly incorporate key rules from the summary, ensuring consistent application across the codebase and serving as a quality gate for new and modified code.
* Conduct a baseline code audit or gap analysis on a representative module or project to assess current adherence to these rules and prioritize specific areas for immediate refactoring and improvement efforts.
