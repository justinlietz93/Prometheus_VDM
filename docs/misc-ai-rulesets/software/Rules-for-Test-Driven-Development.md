# Rules for Test Driven Development

Hard technical rules, syntax requirements, and constraints extracted from the document segment, formatted as a Markdown bulleted list and grouped by category:

**Generated on:** October 27, 2025 at 11:41 PM CDT

---

## TDD Process Core

* **Write New Code Conditionally**: Only write new code if an automated test has failed.
* **Eliminate Duplication**: Ruthlessly eliminate duplication. This is a primary driver for design within TDD.
* **Follow the Red/Green/Refactor Cycle**:
  * **Red**: Quickly add a test that doesn't work, and perhaps doesn't even compile at first.
  * **Green**: Make the test work quickly, committing whatever temporary "sins" are necessary.
  * **Refactor**: Eliminate all duplication created in merely getting the test to work.
* **Prioritize Functionality then Cleanliness**: First solve the "that works" part of the problem, then solve the "clean code" part.
* **Maintain Rhythm**: Always maintain the Red/Green/Refactor rhythm.
* **Aim for Minimal Changes**: Strive to be never more than one change away from a green bar in the "pure form" of TDD.

### Testing Practices & Quality

* **Start with Tests**: Begin with tests, not objects, when approaching a new operation.
* **Imagine Perfect Interfaces**: Invent the perfect interface for an operation when writing its test.
* **Start Simple**: Begin by testing a variant of an operation that doesn't do anything (Starter Test).
* **Incremental Test Selection**: Pick a test that will teach you something and that you are confident you can implement (One Step Test).
* **Readable Test Data**: Use data that makes the tests easy to read and follow.
* **Meaningful Data Differences**: If there is a difference in test data, it should be meaningful.
* **Reflect Inputs**: Ensure tests reflect multiple inputs if the system has to handle them.
* **Avoid Constant Reuse**: Do not use the same constant to mean more than one thing in test data.
* **Evident Data**: Include expected and actual results in the test itself, making their relationship apparent.
* **Assert First**: Start writing a test by writing its assertions.
* **Specific Assertions**: Be specific in assertions (e.g., `assertEquals(50, area)` instead of `assertTrue(area != 0)`).
* **Black Box Testing**: Avoid assertions that are too dependent on internal implementation details; focus on externally visible behavior.
* **Child Tests for Complexity**: If a test is too big to maintain the red/green rhythm, write a smaller "Child Test" representing the broken part, get it working, then reintroduce the larger test.
* **Dynamic Test List**: Add new implied tests and refactorings to the Test List as development progresses.
* **Prioritize Test List Items**: Address all items left on the Test List when a session is done.
* **Avoid Postponing Tests**: Do not move test cases to a "later" list if you can think of a test that might not work.
* **Learning Tests for External Software**: Write tests for externally produced software before the first time you use a new facility in the package.
* **Defer Tangential Ideas**: When a tangential idea arises, add a test for it to the list and return to the original topic (Another Test).
* **Regression Tests for Defects**: When a defect is reported, write the smallest possible test that fails and, once repaired, will pass (Regression Test).
* **Achieve 100% Statement Coverage**: TDD, followed religiously, should result in 100% statement coverage.
* **Defect Insertion Validation**: Ensure that changing the meaning of a line of code breaks a test.
* **Improve Coverage via Simplification**: Improve test coverage by simplifying program logic through refactoring.
* **TDD Test Scope**: Do not expect TDD tests to replace other types of testing (e.g., Performance, Stress, Usability).
* **External Code Testing**: Do not test external or third-party code unless there is a specific reason to distrust it.
* **Document External Behavior**: Document unusual behavior in external code with tests that will fail if the behavior changes.
* **Confidence-Driven Deletion**: Do not delete a test if it reduces your confidence in the system's behavior.
* **Communication-Driven Retention**: Do not delete tests that speak to different scenarios for a reader, even if they exercise the same code path.
* **Delete Redundant Tests**: If two tests are redundant with respect to both confidence and communication, delete the least useful.
* **Test Suite Performance**: Aim for test suite execution time under ten minutes.
* **Test for Rollover**: Include tests for integer rollover conditions.
* **Test Error Conditions**: Test error conditions if they are expected to work.
* **Mock Objects**: Create a fake version of an expensive or complicated resource that returns constants for testing.
* **Mitigate Mock Risk**: Reduce Mock Object risk by having a set of tests that can apply to both the mock and the real object.
* **Self Shunt**: Have the object under test communicate with the test case itself instead of with the object it expects.
* **Log String**: Keep a log in a string and append to it when messages are called to test the sequence of method invocations.
* **Crash Test Dummy**: Test error code that is unlikely to be invoked by using a special object that throws an exception.
* **Specific Exception Catching**: In an Exception Test, catch only the particular exception you expect, and explicitly `fail()` if the exception isn't thrown.
* **Test Method Naming**: Represent a single test case as a method whose name begins with "test".
* **Descriptive Test Names**: The remainder of a test method's name should suggest to a future reader why the test was written.
* **Simple Test Methods**: Ensure test methods are easy to read, typically using straightline code.
* **Separate Fixtures**: Use a new subclass of `TestCase` for each new kind of test fixture.
* **Fixture Initialization**: Initialize fixture objects as instance variables within `setUp()` methods.
* **Resource Release**: Release external resources in `tearDown()` methods.
* **Clean Test State**: Ensure each test leaves the world in exactly the same state as before it ran.
* **Suite Hierarchy**: Make a suite of all tests by creating one suite for each package and one aggregating the package tests for the whole application.
* **Executable Suites**: Provide a `main()` method for `AllTests` classes to allow direct execution.

### Object Design & Architecture

* **Organic Design**: Design organically, with running code providing feedback between decisions.
* **Cohesive, Loosely Coupled Components**: Design for many highly cohesive, loosely coupled components to make testing easy.
* **Private Instance Variables**: Ensure instance variables are private (default visibility).
* **Value Object Immutability**: Values of Value Object instance variables must never change once set in the constructor.
* **Value Object Operations**: Operations on Value Objects must always return a new object to avoid side effects.
* **Value Object Equality**: Value Objects must implement the `equals()` method.
* **Prefer Polymorphism**: Prefer polymorphism over explicit class checks (e.g., `getClass()`, `instanceof`) in business logic.
* **Centralized Exchange Rates**: Centralize knowledge about exchange rates (e.g., in a `Bank` object).
* **Ignorant Core Objects**: Keep objects at the heart of the system as ignorant of the rest of the world as possible to maintain flexibility.
* **Avoid Constructor-Only Subclasses**: Do not create subclasses solely for the purpose of defining constructors.
* **Avoid Global Resources**: Do not store expensive resources in global variables, even if they masquerade as Singletons.
* **Null Object Pattern**: Create an object representing a special case, giving it the same protocol as regular objects.
* **Template Method**: Implement invariant sequences of computation with a method written entirely in terms of other methods.
* **Pluggable Object**: Introduce Pluggable Objects when a conditional representing variation appears for the second time.
* **Pluggable Selector**: Use Pluggable Selector only when cleaning up a straightforward situation where numerous subclasses implement a single method, to avoid gratuitous subclasses.
* **Factory Method**: Create an object by calling a method instead of using a constructor, but only when flexibility in object creation is needed.
* **Imposter Pattern**: Introduce a new variation into a computation by introducing a new object with the same protocol but a different implementation.
* **Composite Pattern**: Implement an object whose behavior is the composition of the behavior of a list of other objects by making it an Imposter for the component objects.
* **Collecting Parameter**: Add a parameter to an operation to collect results spread over several objects.

### Refactoring Rules & Strategies

* **Refactor Untested Code First**: Write missing tests before refactoring untested code (retroactively test).
* **Visibility for Subclasses**: Change field visibility from private to protected if subclasses require access to them.
* **Rollback on Red**: If a refactoring causes a red bar, back out the change to return to green before attempting another fix.
* **Reconcile Differences**: Gradually bring similar code closer, unifying it only when it is absolutely identical.
* **Isolate Change**: First, isolate the part of a method or object that needs to change.
* **Migrate Data (Duplication)**: Temporarily duplicate data when moving between data representations.
  * **Internal-to-External Migration Steps**: Add new format instance variable, set it everywhere old format is set, use it everywhere old format is used, delete old format, change external interface.
  * **External-to-Internal Migration Steps**: Add new format parameter, translate to old format, delete old parameter, replace old format uses with new, delete old format.
* **Extract Method Steps**:
    1. Find a logical region of code.
    2. Ensure no assignments to temporary variables declared outside the region.
    3. Copy code to new method and compile.
    4. Add parameters for original method's temporary variables or parameters used in the new method.
    5. Call the new method from the original.
* **Inline Method Steps**:
    1. Copy the method.
    2. Paste the method over the method invocation.
    3. Replace all formal parameters with actual parameters, handling side effects carefully.
* **Extract Interface Steps**:
    1. Declare the interface (rename existing class if its name becomes the interface name).
    2. Have the existing class implement the interface.
    3. Add necessary methods to the interface, expanding visibility in the class if needed.
    4. Change type declarations from the class to the interface where possible.
* **Move Method Steps**:
    1. Copy the method to the target class, suitably named, and compile.
    2. Add parameters to pass original object references or variables if needed.
    3. Do not move the method if the target class sets variables of the original object.
    4. Replace the body of the original method with an invocation of the new method.
* **Method Object Steps**:
    1. Create an object with the same parameters as the method.
    2. Make the method's local variables also instance variables of the new object.
    3. Create one method (e.g., `run()`) in the new object whose body is the same as the original method's.
    4. In the original method, create a new object and invoke its `run()` method.
* **Add Parameter Steps**:
    1. If the method is in an interface, add the parameter to the interface first.
    2. Add the parameter to the method.
    3. Use compiler errors to identify and change calling code.
* **Method Parameter to Constructor Parameter Steps**:
    1. Add the parameter to the constructor.
    2. Add an instance variable with the same name.
    3. Set the instance variable in the constructor.
    4. Convert method parameter references to instance variable references.
    5. Delete the parameter from the method and its callers once no references remain.
    6. Remove superfluous `this.` from references.
    7. Rename the variable correctly.

### Environment & Personal Discipline

* **Rapid Environment Response**: Ensure the development environment provides rapid response to small changes.
* **Avoid Interrupting Interruptions**: Do not interrupt an interruption.
* **Debug-Only Code Exception**: Avoid writing debug-only `toString()` methods without tests unless the risk of failure is low and there's already a red bar.
* **Pace Adjustment**: When facing complex compilation errors, slow down and break down the problem, or trust the compiler to guide fixes.
* **Take Breaks**: Take a break when tired or stuck.
* **Stuck Strategy**: When unable to proceed, follow the sequence: Obvious Implementation -> Fake It -> Triangulate -> Take a shower (Break).
* **Do Over**: Throw away code and start over if feeling lost or if the code becomes a mess.
* **Ergonomics**: Prioritize a comfortable chair for programming.
* **Pairing Setup**: Ensure sufficient desk space for pair programming, allowing keyboard adjustments for each partner.
* **Hardware Allocation**: Allocate the hottest possible machines for shared development and use cheaper machines for individual tasks (e.g., email).
* **Broken Test (Solo)**: Leave the last test broken when programming alone to provide an obvious starting point for the next session.
* **Clean Check-in (Team)**: Leave all tests running when programming in a team.
* **Pre-Check-in Run**: Always ensure all tests are running before checking in code on a team project.
* **Integration Test Failure**: If integration tests fail, the simplest rule is to discard your work and start over.
* **Forbidden Practice**: Do not comment out tests to make the suite pass.
* **Midstream TDD Adoption**: Do not attempt full-scale retrofitting of tests or refactoring when switching to TDD midstream.
* **Master the Rhythm First**: Master the red/green/refactor rhythm in your own practice before attempting to spread TDD.

### Language-Specific Constraints / Syntax

* **JUnit Equality Convention**: The `expected` value generally goes first in `assertEquals` calls (e.g., `assertEquals(50, actual)`).
* **Java Interface Methods**: Methods in Java interfaces must be `public`.
* **Java Abstract Methods**: In Java, declare a submethod as `abstract` in a Template Method if it makes no sense for the computation without being filled in by subclasses.
* **Java Interface Narrowness**: In Java, interfaces for Self Shunt should be as narrow as possible, as all operations must be implemented.
* **Java Hashing Requirements**: If using objects as keys in a hash table (e.g., `java.util.Hashtable`), they must implement both `equals()` and `hashCode()`.

## Key Highlights

* Always follow the Red/Green/Refactor cycle: first, write a failing test; second, make it pass quickly; third, refactor to eliminate duplication and improve design.
* Only write new production code if an automated test has failed, ensuring that tests drive all development.
* Ruthlessly eliminate duplication, as this is a primary driver for design evolution within the Test-Driven Development process.
* Prioritize functionality first by making the test pass, then focus on cleaning up the code through refactoring.
* Focus tests on externally visible behavior, avoiding assertions dependent on internal implementation details, and begin writing tests by defining specific assertions.
* When a defect is reported, immediately write the smallest possible test that fails, then fix the defect to make that test pass.
* Before refactoring untested code, write missing tests, and if a refactoring causes a test to fail, immediately roll back to a green state before attempting another fix.
* Maintain the integrity of the test suite by never commenting out tests to make them pass, and ensure the entire suite executes in under ten minutes.

## Next Steps & Suggestions

* Conduct an assessment of current TDD adoption and adherence to the outlined principles across development teams to identify gaps and areas for improvement.
* Initiate a focused effort to optimize existing test suites for performance (aiming for under ten minutes execution time) and achieve 100% statement coverage as per TDD guidelines.
* Develop and roll out targeted training for developers on advanced TDD practices, including detailed refactoring techniques and object design principles described in the summary.
* Review and standardize test method naming conventions, effective use of fixtures, mock object strategies, and assertion specificity to enhance test readability and maintainability.
