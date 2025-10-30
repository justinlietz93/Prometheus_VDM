# Rules for System Design and Implementation Guidelines

These rules serve as commandments for writing clean, maintainable, and robust code across the system, encompassing principles from high-level architecture to low-level implementation details and specific domain constraints.

**Generated on:** October 28, 2025 at 12:16 AM CDT

---

## 1. General Principles & Code Quality

* You will rewrite bad code, not comment it.
* You will continuously strive for clean and simple code, preventing code rot.
* You will not ignore any part of the code; for in the ignored parts, bugs hide.
* You will eliminate all duplication; for duplication is the primary enemy of well-designed systems.
* You will ensure code clearly expresses the author's intent.
* You will use the simplest thing that can possibly work.
* You will delete unused code or data, including functions and their tests if they become unnecessary.
* You will ensure consistent conventions across all similar code constructs.
* You will avoid arbitrary structural choices in code.

## 2. Naming Conventions

* You will use long, descriptive, multi-word names that clearly state their purpose; names are preferred over comments.
* You will be consistent in naming conventions across modules, using the same phrases, nouns, and verbs.
* For monadic functions, You will form clear verb/noun pairs.
* You will consider keyword forms for function names to encode argument intent and order (e.g., `assertExpectedEqualsActual`).
* You will make variable names unambiguous, especially to prevent shadowing.
* You will ensure function names accurately describe their actions, particularly regarding side effects (e.g., use `plusDays` for returning a new instance, not for modifying an existing one).
* You will use standard nomenclature where possible (e.g., include "Decorator" in class names).
* You will choose names at the appropriate level of abstraction.
* You will replace magic numbers with named constants.
* You will eliminate scope encoding prefixes (e.g., `f_` for fields).

## 3. Comments

* The only truly good comment is the one thou found a way not to write; explain thyself in code where possible.
* If a comment is necessary, You will ensure it is accurate, concise, uses careful words, correct grammar and punctuation, and avoids stating the obvious.
* You will only use comments for copyright/authorship statements and references to external documents.
* You will avoid mandated comments that add no value or clutter code.
* You will use comments to warn programmers about consequences (e.g., performance impact, non-thread-safe behavior).
* `TODO` comments are acceptable for temporary work notes, but are not an excuse for bad code and must be regularly reviewed and eliminated.
* You will not use comments for bylines, change logs, or information better suited for source control or issue tracking systems.
* You will avoid redundant, misleading, mumbling, noise comments, or comments for self-explanatory code.
* You will delete commented-out code; use source control instead.
* You will not use HTML formatting directly in comments; use `<pre>` tags for pre-formatted blocks if necessary.
* Comments must describe nearby code, not system-wide or historical details, and their connection to the code must be obvious.
* You will avoid function headers for short, well-named functions, and Javadocs for non-public code.
* You will not use closing brace comments.

## 4. Functions

* You will make functions very small, ideally rarely exceeding 20 lines.
* Nested blocks (`if`, `else`, `while`) should be one line, preferably a function call, limiting indentation to one or two levels.
* Functions must have a single responsibility, performing one thing well and only one thing.
* Statements within a function must all be at the same level of abstraction, enabling a top-down narrative (The Stepdown Rule).
* You will avoid large switch statements. If unavoidable, encapsulate them in a low-level, non-repeated class, preferably for creating polymorphic objects hidden behind inheritance.
* You will strive for zero, one, or two arguments (niladic, monadic, dyadic). You will avoid triadic functions and never use more than three arguments.
* You will not use flag arguments; split the function into separate functions instead.
* You will avoid output arguments; prefer state changes on owning objects or return values for transformations.
* If many arguments are needed, You will wrap them into an argument object class.
* Functions must not have side effects; they should only perform actions implied by their name.
* You will explicitly expose temporal couplings between functions, or make them explicit in function names.
* Functions must either do something (command) or answer something (query), but not both.
* You will encapsulate conditionals to clarify their intent.
* You will express conditionals as positives rather than negatives when possible.
* You will encapsulate boundary conditions within functions.
* You will eliminate extraneous or redundant `if` statements.

## 5. Classes & Objects

* ### Encapsulation

  * You will keep variables and utility functions private; avoid public variables.
  * You will understand that hiding implementation is about abstractions, not just getters/setters.
  * You will not expose data details; express data in abstract terms.
  * You will avoid adding getters and setters without careful consideration.
  * You will loosen encapsulation (e.g., for tests) only as a last resort.

* ### Class Design

  * Classes must be small, with a single responsibility (SRP), and few instance variables, demonstrating high cohesion.
  * You will split classes if they lose cohesion or cannot be concisely named.
  * You will avoid 'weasel' words (e.g., `Manager`, `Processor`, `Data`) in class names.
  * You will be able to describe a class briefly (around 25 words) without using "if," "and," "or," "but."
  * Classes must be open for extension but closed for modification (OCP).
  * Classes must depend on abstractions, not concrete details (DIP), using interfaces and abstract classes for isolation.
  * You will avoid hybrid structures that are half object and half data structure.
  * Methods operating on an object's instance variables should be non-static.

* ### Objects vs. Data Structures

  * Objects must hide their data behind abstractions and expose functions.
  * Data structures must expose their data and have no meaningful functions.
  * Simple data structures with procedures are appropriate when not everything needs to be an object.

* ### Law of Demeter

  * You will adhere to the Law of Demeter: a module should not know the innards of objects it manipulates.
  * Objects must not expose internal structure via accessors.
  * You will avoid "train wrecks" (chains of calls like `a.getB().getC().doSomething()`).
  * You will tell objects to do something, rather than asking for their internals for external manipulation.

* ### Data Transfer Objects (DTOs)

  * DTOs are classes with public variables and no functions.
  * You will treat Active Records as data structures, encapsulating business rules in separate objects.

## 6. Formatting

* You will apply a consistent, team-agreed formatting style using automated tools.

* ### Vertical Formatting

  * You will keep source files small (e.g., typically 200 lines, with an upper limit of 500 lines for significant systems).
  * You will structure files with high-level concepts at the top, increasing detail downwards (Newspaper Metaphor).
  * You will separate distinct concepts with blank lines and group related lines densely.
  * You will keep conceptually related code physically close; do not separate into different files without a strong reason.
  * You will declare variables near their first use: local variables at the function top, loop variables within the loop statement, instance variables at the class top.
  * You will arrange functions so callers are above callees, with dependencies pointing downwards.
  * You will place abstract methods at the top of a class definition.
  * You will avoid protected variables.

* ### Horizontal Formatting

  * You will keep lines short (generally not exceeding 100-120 characters); do not shrink font size to fit long lines.
  * You will use horizontal whitespace to associate strongly related things and disassociate weakly related things, and to accentuate operator precedence.
  * You will surround assignment operators with whitespace.
  * You will not put spaces between function names and opening parentheses.
  * You will separate arguments within function call parentheses to accentuate the comma.
  * You will avoid horizontal alignment of declarations or assignments.

* ### Indentation

  * You will indent code according to hierarchical scope to make scopes visible.
  * Classes are not indented. Methods, method implementations, and block implementations are indented one level.
  * You will avoid single-line `if`/`while` bodies; always expand and indent with braces, even for empty loop bodies.

## 7. Error Handling

* Error handling must not obscure the primary logic of the code.

* ### Exceptions

  * You will throw exceptions for errors instead of returning error codes, especially from command functions.
  * You will define `try-catch-finally` statements upfront to ensure consistent program state.
  * You will extract `try` and `catch` block bodies into dedicated functions that do nothing else.
  * The `try` keyword should be the very first word in an error-handling function, with nothing after `catch`/`finally`.
  * You will prefer unchecked exceptions for general application development; use checked exceptions for critical libraries.
  * You will provide sufficient context (source, location, message, operation, failure type) with each thrown exception.
  * You will define exception classes based on how they are caught; create new classes only when distinct catching is required.
  * You will wrap third-party APIs that throw exceptions to minimize dependencies and define a comfortable API.

* ### Normal Flow & Null Avoidance

  * You will use the Special Case Pattern (creating a class or object to handle special cases) to avoid client code dealing with exceptional behavior directly.
  * You will avoid returning `null` from methods; prefer exceptions or Special Case Objects.
  * You will wrap third-party APIs that return `null`.
  * You will avoid passing `null` into methods unless explicitly required by the API; otherwise, forbid it by default.

## 8. Unit & Integration Testing

* ### Three Laws of TDD

  * You will not write production code until a failing unit test has been written.
  * You will not write more of a unit test than is sufficient to fail.
  * You will not write more production code than is sufficient to pass the currently failing test.

* ### Test Quality

  * You will treat test code with the same importance, design, and cleanliness as production code.
  * You will prioritize readability, clarity, simplicity, and density in tests.
  * You will continuously refactor test code for expressiveness.

* ### Assertions & Isolation

  * You will test a single concept per test function, minimizing assertions per concept.
  * When testing thread-aware code, You will test only the thread-aware code in isolation.

* ### F.I.R.S.T. Principles

  * **Fast:** Tests must run quickly.
  * **Independent:** Tests must not depend on each other and be runnable in any order.
  * **Repeatable:** Tests must be repeatable in any environment.
  * **Self-Validating:** Tests must have a boolean pass/fail output without manual interpretation.
  * **Timely:** You will write unit tests just before the production code they validate.

* ### Continuous Verification

  * You will maintain an automated test suite to verify system behavior remains unchanged after every modification.
  * You will ensure the code is working correctly before making the next incremental change during refactoring.

## 9. Concurrency

* ### General Principles

  * You will exercise extreme caution with concurrent programs, assuming "one-off" failures are threading issues; never ignore them.

* ### Defense Principles

  * You will apply the Single Responsibility Principle to concurrency code, separating it from other logic.
  * You will severely limit shared data access and scope.
  * You will avoid sharing data by copying objects or partitioning data for independent threads.
  * You will be familiar with thread-safe collections and concurrent algorithms (Producer-Consumer, Readers-Writers).
  * You will avoid using multiple dependent methods on shared objects; if unavoidable, ensure correctness with client-based, server-based, or adapted server locking.
  * Critical sections must be guarded, and synchronized sections kept as small as possible to minimize contention.
  * You will find and lock regions of code that must be locked, but not lock regions that do not need it.
  * You will avoid calling one locked section from another.
  * You will implement graceful shutdown code early.
  * Producers must wait for free queue space before writing; consumers must wait for items before consuming.
  * You will separate thread-aware code from thread-ignorant code using Plain Old Java Objects (POJOs) or equivalent.

* ### Testing Concurrent Code

  * You will write and frequently run concurrent tests that expose problems across various configurations and loads.
  * You will never ignore concurrent test failures, even if subsequent runs pass.
  * You will isolate and fix non-threading bugs before addressing threading issues.
  * You will make thread-based code pluggable (for various thread counts/execution patterns) and tunable (for performance adjustments).
  * You will run tests with more threads than processors/cores to encourage task swapping.
  * You will run threaded code on all target deployment platforms early and often.
  * You will instrument code (e.g., using `wait()`, `sleep()`, `yield()`) to force failures and ferret out stubborn bugs.

## 10. System Architecture & Design

* You will separate system construction/wiring (e.g., in `main`) from runtime logic; the application should not know about its construction.
* You will modularize the startup process.
* You will ensure a global, consistent strategy for resolving major dependencies.
* An object must not instantiate its own dependencies; delegate this to an authoritative mechanism (Dependency Injection/Inversion of Control).
* You will use the Abstract Factory pattern when the application needs to control object creation, but construction details should remain separate.
* You will build systems incrementally, implementing today's stories and refactoring, maintaining flexibility for evolving circumstances.
* An optimal system architecture consists of modularized domains of concern, implemented with Plain Old Java Objects (POJOs) or equivalent.
* You will integrate different domains with minimally invasive Aspects or Aspect-like tools.
* You will postpone design decisions until the last possible moment to make informed choices.
* You will use standards wisely, only when they add demonstrable value.
* A good Domain-Specific Language (DSL) minimizes the communication gap between domain concepts and code, allowing POJO expression across abstraction levels.
* You will ensure clear intent at all levels of abstraction in a system.
* A design is "simple" if it runs all tests, contains no duplication, expresses programmer intent, and minimizes classes/methods (in order of priority).
* You will design for testability, promoting small, single-purpose, loosely coupled classes (using DIP, DI, interfaces, abstraction).
* After adding a few lines of code, You will pause, reflect, clean up if degraded, and run tests.
* During refactoring, You will apply good design principles: increase cohesion, decrease coupling, separate concerns, modularize, shrink functions/classes, and choose better names.
* You will prioritize having tests, eliminating duplication, and expressiveness over minimizing class/method count; resist dogmatism (e.g., an interface for every class) that leads to excessive small entities.
* You will make logical dependencies physical; ensure a physical dependency is established if something logically depends on an implementation detail.

## 11. Boundaries & Third-Party Integration

* You will cleanly integrate foreign (third-party, open-source, or internal team) code with thine own.
* You will keep the boundaries of thy software clean.
* You will not liberally pass boundary interfaces (e.g., `Map`) around the system; keep them encapsulated within the class or a close family of classes where they are used.
* You will avoid returning boundary interfaces from, or accepting them as arguments to, public APIs.
* You will write learning tests to explore and understand third-party code APIs.
* A clean boundary must be supported by a set of outbound tests that exercise the interface in the same way production code does.
* You will write thine own application-specific interface for external systems to maintain control and readability.
* Code at the boundaries needs clear separation and tests that define expectations.
* You will avoid letting too much of thy code know about third-party particulars.
* You will depend on code thou control, not code thou do not.
* You will manage third-party boundaries by having very few places in the code that refer to them (e.g., wrapping them or using an Adapter pattern).

## 12. Language & Platform Specifics (Example: Java)

* You will not inherit constants; use enums or static imports instead.
* You will use enums for constants (e.g., months, days of the week).
* You will shorten long import lists by using wildcard imports (`import package.*`).

## 13. Domain-Specific Implementation Details (Example: SpreadsheetDate)

* ### Architectural Directives

  * The `SpreadsheetDate` class must extend `DayDate`.
  * The `SpreadsheetDate` class must provide static factory methods for instance creation.
  * The `SpreadsheetDate`'s `equals` method must compare instances based on their ordinal day.
  * The `SpreadsheetDate`'s `hashCode` method must return the ordinal day.
  * The `SpreadsheetDate`'s `compareTo` method must delegate to the `daysSince` method of `DayDate`.

* ### Data Constraints & Validation

  * The earliest supported ordinal date is 2 (representing 1-Jan-1900).
  * The latest supported ordinal date is 2958465 (representing 31-Dec-3399).
  * The minimum supported year is 1900.
  * The maximum supported year is 9993.
  * For `day, month, year` construction, `year` must be within `MINIMUM_YEAR_SUPPORTED` and `MAXIMUM_YEAR_SUPPORTED`, and `day` must be valid for the specified `month` and `year` (>=1 and <= last day).
  * For `serial` construction, `serial` must be within `EARLIEST_DATE_ORDINAL` and `LATEST_DATE_ORDINAL`.
  * Constructors or methods encountering invalid arguments shall throw `IllegalArgumentException`.

* ### Behavioral Logic

  * `SpreadsheetDate` uses the convention where 1-Jan-1900 equals the ordinal value of 2.
  * `SpreadsheetDate` instances should derive from `java.util.Date` using `GregorianCalendar` for component extraction.
  * When initializing with `int month`, internally convert to a `Month` enum via `Month.fromInt()`.
  * The `getDayOfWeekForOrdinalZero` method must return `Day.SATURDAY`.
  * The `equals` method must return `false` if the comparing object is not an instance of `DayDate`.
  * The `calcOrdinal` method calculates the ordinal day by adding `EARLIEST_DATE_ORDINAL` to accumulated days.

* ### Structural & API Rules

  * Classes must reside in the `org.jfree.date` package.
  * `static import` may be used for specific enum values (e.g., `org.jfree.date.Month.FEBRUARY`).
  * `java.util.*` classes may be imported.
  * `SpreadsheetDate` must define public static final integer constants for date boundaries (`EARLIEST_DATE_ORDINAL`, `LATEST_DATE_ORDINAL`, `MINIMUM_YEAR_SUPPORTED`, `MAXIMUM_YEAR_SUPPORTED`).
  * `SpreadsheetDate` must define static final integer arrays (`AGGREGATE_DAYS_TO_END_OF_PRECEDING_MONTH`, `LEAP_YEAR_AGGREGATE_DAYS_TO_END_OF_PRECEDING_MONTH`).
  * `SpreadsheetDate` must declare private instance variables: `ordinalDay`, `day`, `month`, and `year`.
  * Constructors must accept `(int day, Month month, int year)`, `(int day, int month, int year)`, and `(int serial)`.
  * Public getter methods (`getOrdinalDay()`, `getYear()`, `getMonth()`, `getDayOfMonth()`) must be provided.
  * Public `equals(Object object)`, `hashCode()`, and `compareTo(Object other)` methods must be defined.
  * Private helper methods (`calcOrdinal`, `calcDayMonthYear`, `huntForMonthContaining`, `daysBeforeThisMonth`, `huntForYearContaining`, `firstOrdinalOfYear`) must be used for internal calculations.
  * A public static factory method `createInstance(Date date)` must be provided.

## Key Highlights

* Continuously strive for clean, simple code by eliminating all duplication, which is the primary enemy of well-designed systems.
* Use long, descriptive names that clearly state their purpose, preferring names over comments to express intent.
* Keep functions very small, ideally rarely exceeding 20 lines, and ensure each function has a single responsibility.
* Design classes to be small, with a single responsibility, few instance variables, and high cohesion.
* Adhere to the Law of Demeter by ensuring modules do not expose or know the internal structure of objects they manipulate, avoiding 'train wrecks'.
* Implement error handling using exceptions instead of error codes, and strictly avoid returning or passing `null` from or to methods.
* Treat test code with the same importance, design, and cleanliness as production code, and never write production code until a failing unit test has been written.
* Delegate object dependency instantiation to an authoritative mechanism like Dependency Injection to promote modularity and testability.
* Severely limit shared data access and scope in concurrent programs to mitigate threading issues and ensure correctness.
* Manage third-party code boundaries by wrapping foreign APIs and minimizing direct references, thereby maintaining control and reducing external coupling.

## Next Steps & Suggestions

* Implement and configure static analysis tools (e.g., linters, SonarQube, Checkstyle) to automate the detection and enforcement of as many of these rules as possible, integrating them into the CI/CD pipeline.
* Develop a comprehensive training program and a phased rollout plan to educate all development teams on these rules, focusing on practical application and addressing common pitfalls.
* Conduct an initial code audit across existing projects or critical modules against a prioritized subset of these rules to establish a baseline, identify major areas of non-compliance, and inform refactoring efforts.
* Establish a clear governance model for these rules, defining ownership, processes for updates, clarification, and handling exceptions, and integrate rule adherence into the formal code review process.
