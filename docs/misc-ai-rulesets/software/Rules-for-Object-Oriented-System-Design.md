# Rules for Object-Oriented System Design & Implementation

These rules represent the distilled, synthesized, and de-duplicated technical rules for designing and implementing object-oriented systems, with specific considerations for C++ and Smalltalk.

**Generated on:** October 27, 2025 at 10:29 PM CDT

---

## I. General Design Principles

1. **You will design for reusability**, ensuring systems address future problems and evolve accordingly.
2. **You will minimize redesign**, striving to avoid or reduce it in software development.
3. **You will program to an interface**, defined by an abstract class, not a concrete implementation.
4. **You will avoid concrete class dependencies**, never declaring variables as instances of particular concrete classes, committing only to an interface.
5. **You will favor object composition** over class inheritance for code reuse.
6. **You will promote loose coupling** between classes to increase reusability, maintainability, and extensibility, and avoid tightly coupled systems.
7. **You will encapsulate varying concepts**, isolating them into separate objects or hierarchies to enhance flexibility and reusability.
8. **You will hide implementation details**, shielding clients to prevent cascading changes.
9. **You will isolate algorithms** that are likely to change.
10. **You will avoid hard-coding specifics**, using mechanisms for changes at compile-time or run-time rather than specific operations or product classes.
11. **You will limit platform dependencies**, designing systems to minimize reliance on specific hardware and software platforms.
12. **You will decompose systems** into objects thoughtfully, considering encapsulation, granularity, dependency, flexibility, performance, evolution, and reusability.
13. **You will apply design patterns judiciously**, only when the flexibility they afford is genuinely needed.
14. **You will not over-generalize designs**, as this can make it harder to restrict components.

## II. Object-Oriented Programming Fundamentals

1. **You will encapsulate an object's internal state and implementation details;** they must not be accessed directly, and their representation must be invisible from outside the object.
2. **Operations are the sole mechanism** for changing an object’s internal data.
3. **You will ensure object identifiers are address space-independent.**
4. **You will avoid ad hoc dispatching schemes**, as they often decrease type safety.
5. **You will ensure interfaces are well-defined** for effective object composition.

## III. Language-Specific Implementation

### A. C++ Implementation Conventions

1. **You will define polymorphic base classes with a virtual destructor.**
2. **You will declare abstract interfaces by inheriting publicly from classes with pure virtual member functions.**
3. **You will use private inheritance to approximate pure implementation (class) inheritance.**
4. **You will define factory methods as virtual functions**, often pure virtual.
5. **You will not call virtual factory methods in a Creator’s constructor**, as the concrete implementation may not be available yet.
6. **You will declare constructors for classes intended to be Singletons as protected** to prevent direct instantiation.
7. **You will declare primitive operations called by a template method as protected members.**
8. **You will declare primitive operations that *must* be overridden as pure virtual functions.**
9. **You will make template methods nonvirtual** and not intended for overriding.
10. **You will use a reference count** when sharing implementations among multiple objects (e.g., in the Bridge pattern), incremented and decremented by a Handle class.
11. **You will declare classes that should only be instantiated by specific patterns (e.g., Memento) as `friend` classes** to the originator, and define their wide interface members as private and narrow interface members as public.

### B. Smalltalk Implementation Conventions

1. **You will not rely on variable type declarations for compile-time checks**, as Smalltalk compilers do not check if assigned objects are subtypes.
2. **You will understand inheritance in Smalltalk as primarily implementation inheritance.**
3. **You will be able to assign instances of any class to a variable** as long as they support the operations performed on the variable's value.
4. **You will override the `new` operation to ensure a Singleton class has only one instance.**
5. **You will define generic proxy classes whose superclass is `nil`**.
6. **You will implement the `doesNotUnderstand:` method in proxies** to forward messages to the real subject using `self realSubject perform: aMessage selector withArguments: aMessage arguments`.
7. **You will ensure the real subject exists** before forwarding messages via `doesNotUnderstand:`.
8. **You will define `doesNotUnderstand:` with an argument that is an instance of `Message`**.
9. **You will define an `error:` method in protection proxies** that send `error:` for illegal messages, copying its definition and any used methods from `class Object` to avoid infinite loops.
10. **You will not expect identity (`==`) on Smalltalk proxies to mean identity on their real subjects**, as `doesNotUnderstand:` typically does not trap `==`.
11. **You will parameterize adapters with one or more blocks** to support adaptation without subclassing.

## IV. Design Pattern rules

### Abstract Factory (87)

1. **You will use this pattern when:**
    * A system must be independent of how its products are created, composed, and represented.
    * A system should be configured with one of multiple families of related product objects.
    * A family of related product objects must be designed to be used together.
    * You will want to provide a class library of products, and only their interfaces, not implementations, are revealed.
2. **You will isolate product class names** within the concrete factory's implementation, preventing their appearance in client code.
3. **You will ensure clients use only interfaces declared by AbstractFactory and AbstractProduct classes.**
4. **You will normally create a single instance of a ConcreteFactory class at run-time.**
5. **You will use a different concrete factory to create different product objects.**
6. **You will acknowledge that supporting new kinds of products requires extending the factory interface**, which involves changes to the `AbstractFactory` class and all its subclasses.
7. **You will consider the implications of parameterized `Make` operations:** clients may not be able to differentiate products or safely perform subclass-specific operations through the abstract interface without downcasting.

### Builder (97)

1. **You will use this pattern when:**
    * The algorithm for creating a complex object should be independent of the parts that make up the object and how they are assembled.
    * The construction process must allow different representations for the object that is constructed.
2. **You will design the Builder interface to be general enough** to allow the construction of products for all kinds of concrete builders.
3. **You will ensure the Director retrieves the product from the builder only when the product is finished.**
4. **You will not allow product's internal structure classes to appear in the Builder's interface.**
5. **You will ensure the Builder (e.g., `MazeBuilder`) defines an interface for creating parts, but does not create the product itself.**

### Chain of Responsibility (223)

1. **You will use this pattern when:**
    * More than one object may handle a request, and the handler isn't known a priori.
    * The handler should be ascertained automatically.
    * You will want to issue a request to one of several objects without specifying the receiver explicitly.
    * The set of objects that can handle a request should be specified dynamically.
2. **You will ensure objects in the chain have a common type.**
3. **You will avoid explicit coupling between the sender of a request and its receiver.**
4. **You will chain receiving objects, passing the request along until an object handles it.**
5. **You will ensure the `Handler` defines an interface for handling requests**, and it may implement the successor link.
6. **You will ensure a `ConcreteHandler` handles requests it is responsible for; otherwise, it must forward the request to its successor.**
7. **You will ensure a `ConcreteHandler` can access its successor.**
8. **You will ensure the `Client` initiates the request to a `ConcreteHandler` object on the chain.**
9. **You will ensure requests propagate along the chain** until a `ConcreteHandler` object takes responsibility.
10. **You will introduce new references if no preexisting references exist for a chain.**
11. **You will provide a default implementation of `HandleRequest` in the `Handler`** that forwards the request to the successor if one exists.
12. **You will ensure a `ConcreteHandler` subclass not interested in a request relies on the default forwarding implementation** if not overriding.
13. **You will agree on request encoding if using a request code parameter** and manually pack/unpack parameters.
14. **You will ensure handlers know the `Request` subclass to access specific parameters** if using request objects.
15. **You will dispatch requests in `Handler::HandleRequest()` using `theRequest->GetKind()`** (C++ specific).
16. **You will cast arguments to their appropriate `Request` subclass type** for specific handlers (e.g., `HandleHelp`, `HandlePrint`) (C++ specific).
17. **You will ensure an `ExtendedHandler::HandleRequest()` calls `Handler::HandleRequest()` for unhandled requests** and handles only those it is interested in.
18. **You will acknowledge that a fixed sender-receiver interface may require a custom dispatching scheme.**

### Command (223)

1. **You will use this pattern when:**
    * You will want to parameterize objects by an action to perform.
    * You will want to specify, queue, and execute requests at different times.
    * You will want to support undo.
    * You will want to support logging changes for reapplication in case of a system crash.
    * You will want to structure a system around high-level operations built on primitive operations.
2. **You will ensure the `Command` declares an interface for executing an operation.**
3. **You will ensure `ConcreteCommand` defines a binding between a `Receiver` object and an action**, and implements `Execute` by invoking corresponding operations on `Receiver`.
4. **You will ensure the `Client` creates a `ConcreteCommand` object and sets its `Receiver`.**
5. **You will ensure the `Invoker` asks the command to carry out the request.**
6. **You will ensure the `Receiver` knows how to perform operations** associated with carrying out a request.
7. **You will ensure the client creates a `ConcreteCommand` object and specifies its receiver.**
8. **You will store the `ConcreteCommand` object in an `Invoker` object.**
9. **You will ensure the invoker issues a request by calling `Execute` on the command.**
10. **You will ensure `ConcreteCommand` stores state for undoing the command prior to invoking `Execute`** when commands are undoable.
11. **You will ensure `ConcreteCommand` invokes operations on its receiver to carry out the request.**
12. **You will provide an operation to reverse execution (e.g., `Unexecute` or `Undo`)** for commands supporting undo/redo.
13. **You will ensure `ConcreteCommand` classes supporting undo/redo may need to store additional state**, including the `Receiver` object, arguments, and original values.
14. **You will ensure the `Receiver` provides operations to return itself to its prior state.**
15. **You will store only the last executed command for single-level undo.**
16. **You will store a history list of executed commands for multiple-level undo/redo.**
17. **You will copy an undoable command before placing it on the history list** if its state can vary across invocations (or after execution if its state changes during execution).
18. **You will store sufficient information in the command to restore objects to their original state** for undo/redo.
19. **You will ensure `MacroCommand` is responsible for deleting its subcommands.**
20. **You will ensure `MacroCommand::Execute()` traverses all subcommands and calls `Execute()` on each.** If `Unexecute` is implemented, subcommands must be unexecuted in reverse order.
21. **You will ensure C++ `Command` objects support polymorphic execution** via their `virtual void Execute() = 0;` interface.

### Decorator (175)

1. **You will use this pattern when:**
    * You will want to add responsibilities to individual objects dynamically and transparently, without affecting other objects.
    * You will want responsibilities that can be withdrawn.
    * Extension by subclassing is impractical due to a proliferation of subclasses for combinations of responsibilities.
2. **You will ensure a decorator object’s interface conforms to the interface of the component it decorates.**
3. **You will ensure the decorator forwards requests to its Component object**, and may perform additional actions before or after forwarding.
4. **You will not rely on object identity when using decorators**, as a decorated component is not identical to the component itself.
5. **You will keep the common `Component` class lightweight**, focusing on defining an interface rather than storing data.
6. **You will ensure the component does not know about its decorators** (decorators are transparent to the component).
7. **You will ensure decorators support the Component interface operations** (e.g., `Add`, `Remove`, `GetChild`) when used with Composite.
8. **You will prefer existing composition classes for embellishing multiple objects**, adding new classes to embellish the result, rather than mixing many kinds of composition with embellishment.

### Facade (185)

1. **You will use this pattern when:**
    * You will want to provide a simple, unified interface to a complex subsystem.
    * You will want to decouple clients from the implementation details of a subsystem.
    * You will want to layer a subsystem.
2. **You will ensure the Facade defines a higher-level, unified interface to a subsystem.**
3. **You will ensure the Facade knows which subsystem classes are responsible for a request** and delegates client requests to them.
4. **You will ensure subsystem classes have no knowledge of the facade** and keep no references to it.
5. **You will ensure clients that use the facade do not access its subsystem objects directly.**
6. **You will ensure dependent subsystems communicate with each other solely through their facades** to simplify dependencies.

### Factory Method (107)

1. **You will use this pattern when:**
    * A class cannot anticipate the class of objects it must create.
    * A class wants its subclasses to specify the objects it creates.
    * A class delegates responsibility to one of several helper subclasses, and You will want to localize the knowledge of which helper subclass is the delegate.
2. **You will ensure the Creator class cannot anticipate the class of objects it must create.**
3. **You will ensure the Creator class wants its subclasses to specify the objects it creates.**
4. **You will ensure subclasses of the Creator override the factory method to return an instance of a ConcreteProduct.**
5. **You will not create the concrete product in the constructor if using lazy initialization;** instead, initialize a pointer to `0`, and an accessor method creates it on demand.

### Flyweight (195)

1. **You will use this pattern when:**
    * An application uses a large number of objects.
    * Storage costs are high for objects.
    * Most object state can be made extrinsic.
    * Many groups of objects can be replaced by a few shared flyweight objects.
    * The application does not depend on object identity.
2. **You will ensure objects can be shared only if they do not define context-dependent (extrinsic) state.**
3. **You will ensure Flyweight objects have no intrinsic state;** any state they store must be independent of their context.

### Interpreter (249)

1. **You will use this pattern when:**
    * There is a language to interpret.
    * Statements in the language can be represented as abstract syntax trees.
    * The grammar is simple.
    * Efficiency is not a critical concern.
2. **You will ensure `AbstractExpression` declares an abstract `Interpret` operation** common to all nodes.
3. **You will ensure `TerminalExpression` implements an `Interpret` operation** associated with terminal symbols, with an instance required for every terminal symbol in a sentence.
4. **You will require one `NonterminalExpression` class for every grammar rule** (`R ::= R1R2...Rn`), maintaining instance variables of type `AbstractExpression` for each symbol (`R1` through `Rn`) and implementing `Interpret` recursively.
5. **You will ensure `Context` contains information global to the interpreter.**
6. **You will ensure the `Client` builds (or is given) an abstract syntax tree, initializes the `Context`, and invokes the `Interpret` operation.**
7. **You will define `Interpret` in each `NonterminalExpression` node** in terms of `Interpret` on each subexpression.
8. **You will ensure the `Interpret` operation of each `TerminalExpression` defines the base case in the recursion.**
9. **You will ensure `Interpret` operations at each node use the context to store and access the state.**
10. **You will ensure the C++ `Context` class provides `bool Lookup(const char*) const` and `void Assign(VariableExp*, bool)`** for Boolean Expressions.
11. **You will ensure C++ `VariableExp` constructor duplicates the name string for its internal name member.**
12. **You will ensure Smalltalk grammar definitions follow these rules:**
    * An `expression` must be a `literal`, `alternation`, `sequence`, `repetition`, or an `expression` enclosed in `{ }*`.
    * An `alternation` must be two `expression`s separated by `|`.
    * A `sequence` must be two `expression`s separated by `&`.
    * A `repetition` must be an `expression` followed by `**` (or `repeat`).
    * A `literal` must be one or more characters.
13. **You will ensure `SequenceExpression::match:` matches `expression1` first, then `expression2` using the result.**
14. **You will ensure `AlternationExpression::match:` returns the union of states from `alternative1` and `alternative2`.**
15. **You will ensure `RepetitionExpression::match:` tries to find as many matching states as possible**, and its output state must contain all possible matched states (including zero or more repetitions).
16. **You will ensure `LiteralExpression::match:` is the only `match:` operation that advances the stream**, and returns a new `Set` containing copies of `tStream` where `tStream nextAvailable: components size` equals `components`.
17. **You will ensure the state returned by `LiteralExpression::match:` contains a copy of the input stream.**
18. **You will ensure each alternative of an `AlternationExpression` sees identical copies of the input stream.**

### Iterator (257)

1. **You will use this pattern when:**
    * You will want to access an aggregate object’s contents without exposing its internal representation.
    * You will want to support multiple traversals of aggregate objects.
    * You will want to provide a uniform interface for traversing different aggregate structures.
2. **You will ensure `Iterator` defines an interface for accessing and traversing elements.**
3. **You will ensure `ConcreteIterator` implements the `Iterator` interface** and keeps track of the current position in the traversal.
4. **You will ensure `Aggregate` defines an interface for creating an `Iterator` object.**
5. **You will ensure `ConcreteAggregate` implements the `Iterator` creation interface** to return an instance of the proper `ConcreteIterator`.
6. **You will ensure a `ConcreteIterator` keeps track of the current object in the aggregate** and can compute the succeeding object.
7. **You will ensure clients using an external iterator explicitly advance the traversal and request the next element.**
8. **You will not place an iterator's traversal algorithm directly in the iterator** if it needs to access an aggregate's private variables, as this violates encapsulation.
9. **You will ensure a robust iterator ensures insertions and removals do not interfere with traversal** without copying the aggregate, typically relying on registration with the aggregate.
10. **You will ensure the minimal `Iterator` interface consists of `First`, `Next`, `IsDone`, and `CurrentItem` operations.**
11. **You will allocate polymorphic iterators dynamically by a factory method**, and clients are responsible for their deletion.
12. **You will use a stack-allocated proxy (e.g., `IteratorPtr` in C++)** that deletes the real iterator in its destructor and disallows copy construction/assignment to ensure proper cleanup of polymorphic iterators.
13. **You will allow `Iterator` subclasses privileged access to aggregate members** via protected operations defined in the `Iterator` class, without changing the aggregate's public interface for new friends.
14. **You will ensure an external iterator for a `Composite` stores a path through the `Composite`** to track the current object.
15. **You will ensure a `Nulllterator`'s `IsDone()` operation always evaluates to `true`.**
16. **You will ensure C++ `ListIterator::CurrentItem()` throws `IteratorOutOfBounds` if `IsDone()` is true.**
17. **You will ensure `List<Item>::CreateIterator()` returns a new `ListIterator<Item>(this)`** (C++ specific).

### Mediator (273)

1. **You will use this pattern when:**
    * A set of objects communicate in well-defined but complex ways, resulting in unstructured and difficult-to-understand interdependencies.
    * Reusing an object is difficult because it refers to and communicates with many other objects.
    * A behavior distributed between several classes should be customizable without a lot of subclassing.
2. **You will ensure `Mediator` defines an interface for communicating with `Colleague` objects.**
3. **You will ensure `ConcreteMediator` implements cooperative behavior by coordinating `Colleague` objects**, and must know and maintain its colleagues.
4. **You will ensure each `Colleague` class knows its `Mediator` object** and communicates with its `Mediator` whenever it would have otherwise communicated with another colleague.
5. **You will ensure `Colleagues` send and receive requests from a `Mediator` object.**
6. **You will ensure the `Mediator` implements cooperative behavior by routing requests between appropriate colleagues.**
7. **You will consider using the `Observer` pattern for Mediator implementation:** `Colleague` classes act as `Subjects` and send notifications, and the `Mediator` responds by propagating change effects.
8. **You will ensure observers are notified only after all subjects have been modified** if an operation involves changes to several interdependent subjects (to avoid redundant updates).
9. **You will use a `ChangeManager` to map subjects to observers, provide an interface to maintain this mapping, define a particular update strategy, and update all dependent observers at the request of a subject.**
10. **You will ensure that if `Mediator`'s interface is fixed, it may need to implement its own dispatching scheme.**
11. **You will encode requests and pack arguments** to support open-ended operations.
12. **You will ensure C++ `DialogDirector` defines a virtual destructor, `ShowDialog()`, and `virtual void WidgetChanged(Widget*) = 0;`, along with `virtual void CreateWidgets() = 0;`.**
13. **You will ensure C++ `Widget` constructor takes a `DialogDirector*`.**
14. **You will ensure C++ `Widget` defines `virtual void Changed()` and `virtual void HandleMouse(MouseEvent& event)`, where `Changed()` calls `_director->WidgetChanged(this)`.**

### Memento (283)

1. **You will use this pattern when:**
    * A snapshot of (some portion of) an object’s state must be saved for restoration.
    * A direct interface to obtaining the state would expose implementation details and break encapsulation.
2. **You will ensure `Memento` objects store the internal state of the `Originator` object.**
3. **You will ensure `Memento` objects protect against access by objects other than the `Originator`.**
4. **You will ensure `Caretaker` sees a narrow interface to the `Memento`, while `Originator` sees a wide interface.**
5. **You will ideally permit only the `Originator` that produced the `Memento` to access its internal state.**
6. **You will ensure `Originator` creates a `Memento` containing a snapshot of its current internal state and uses the `Memento` to restore its internal state.**
7. **You will ensure `Caretaker` is responsible for the `Memento`’s safekeeping**, but never operates on or examines its contents.
8. **You will ensure `Caretaker` requests a `Memento` from an `Originator`, holds it for a time, and passes it back to the `Originator` for restoration.**
9. **You will ensure `Mementos` are passive;** only the `Originator` that created a `Memento` will assign or retrieve its state.
10. **You will ensure a `Caretaker` is responsible for deleting the `Mementos` it cares for.**
11. **You will ensure `Memento` objects are pass-by-value only** (or have an extremely narrow interface without polymorphic operations for clients).
12. **You will allow `Memento` to save only incremental changes** if `Mementos` are created/passed back in a predictable sequence.
13. **You will ensure C++ `Originator` provides `Memento* CreateMemento()` and `void SetMemento(const Memento*)`.**
14. **You will ensure C++ `Originator` has a private `State* _state` member.**
15. **You will ensure C++ `Memento` constructor is private**, and its `SetState(State*)` and `State* GetState()` methods are private.

### Observer (293)

1. **You will use this pattern when:**
    * An abstraction has two aspects, one dependent on the other, to vary and reuse them independently.
    * A change to one object requires changing others, and the number of objects needing change is unknown.
    * An object should notify others without making assumptions about their identity (i.e., avoiding tight coupling).
2. **You will ensure `Subject` knows its observers** and provides an interface for attaching and detaching `Observer` objects.
3. **You will ensure `Observer` defines an updating interface** for objects to be notified.
4. **You will ensure `ConcreteSubject` stores state of interest to `ConcreteObserver` objects** and sends a notification to its observers when its state changes.
5. **You will ensure `ConcreteObserver` maintains a reference to a `ConcreteSubject` object**, stores state that should stay consistent with the subject’s, and implements the `Observer` updating interface.
6. **You will ensure `ConcreteSubject` notifies its observers** whenever a change occurs that could make observers' state inconsistent.
7. **You will allow a `ConcreteObserver` object to query the subject for information to reconcile its state** after being informed of a change.
8. **You will extend the `Update` interface to identify the notifying subject** (e.g., by passing the subject as a parameter) if an observer depends on more than one subject.
9. **You will ensure deleting a subject does not produce dangling references in its observers;** the subject should notify its observers upon deletion.
10. **You will ensure `Subject` state is self-consistent before calling `Notify`.**
11. **You will ensure `Notify()` is the last operation in a template method** when using template methods in abstract `Subject` classes.
12. **You will document which `Subject` operations trigger notifications.**
13. **You will ensure `Observer` classes ascertain what changed without help from the `Subject`** if using the pull model.
14. **You will ensure observers are notified only after all subjects have been modified** if an operation involves changes to several interdependent subjects (to avoid redundant updates).
15. **You will use a `ChangeManager` to map subjects to observers, provide an interface to maintain this mapping, define a particular update strategy, and update all dependent observers at the request of a subject.**
16. **You will ensure C++ `Subject` defines `virtual void Attach(Observer*)`, `virtual void Detach(Observer*)`, and `virtual void Notify()`.**
17. **You will ensure C++ `Observer` defines `virtual void Update(Subject* theChangedSubject) = 0;`.**
18. **You will ensure C++ `ClockTimer::Tick()` updates its internal time-keeping state and calls `Notify()`.**
19. **You will ensure C++ `DigitalClock::Update()` checks if `theChangedSubject` is its `_subject` and calls `Draw()` if so.**

### Prototype (117)

1. **You will use this pattern when:**
    * A system should be independent of how its products are created, composed, and represented.
    * The classes to instantiate are specified at run-time.
    * You will want to avoid building a class hierarchy of factories that parallels the class hierarchy of products.
    * Instances of a class can have one of only a few different combinations of states.
2. **You will ensure each subclass of Prototype implements the `Clone` operation.**
3. **You will usually require a deep copy when cloning prototypes with complex structures** to ensure independence of clone and original, meaning the clone's components must be clones of the prototype's components.
4. **You will ensure composite circuit objects used as prototypes implement `Clone` as a deep copy** for structural prototyping.
5. **You will not manage prototypes directly;** clients should store and retrieve them from a prototype manager (registry) before cloning.
6. **You will never require clients to downcast the return value of `Clone`** to the desired type.
7. **You will ensure objects used as prototypes in C++ have a copy constructor for cloning.**

### Proxy (207)

1. **You will use this pattern when:**
    * You will need a more versatile or sophisticated reference to an object than a simple pointer.
    * A remote proxy is required for objects in different address spaces.
    * A virtual proxy is required for creating expensive objects on demand.
    * A protection proxy is required for controlling access to a sensitive object.
    * A smart reference is required to perform additional actions when an object is accessed.
2. **You will ensure a proxy provides an interface identical to its subject's interface** to allow substitution.
3. **You will ensure Proxy objects control access to their real subjects.**
4. **You will ensure a remote proxy encodes requests/arguments** and sends them to the real subject in a different address space.
5. **You will ensure a protection proxy checks that the caller has necessary access permissions** before performing a request.
6. **You will ensure the subject is reference counted** when using copy-on-write; copying the proxy increments the count, and the proxy copies the subject only when modified.
7. **You will ensure the proxy knows the concrete class** if it instantiates its real subject (e.g., virtual proxy).
8. **You will ensure the proxy keeps a reference to the real subject** after creating it.
9. **You will ensure that if precise timing of subject loading is needed** (e.g., only on `Draw` call for a virtual proxy in C++), each forwarding operation is manually implemented rather than relying solely on `operator->` overloading.
10. **You will ensure C++ `Graphic` base class defines a virtual destructor and pure virtual methods** for common operations (e.g., `Draw`, `HandleMouse`, `GetExtent`, `Load`, `Save`), and its constructor is protected.
11. **You will ensure a C++ `ImageProxy` (as a virtual proxy example) follows these rules:**
    * It inherits publicly from the `Graphic` interface.
    * It defines a constructor that takes a filename and saves a local copy, initializing `_extent` to `Point::Zero` and `_image` to `0`.
    * It provides a `GetImage()` method that creates a new `Image` instance using the filename if `_image` is `0`.
    * Its `GetExtent()` method returns the cached `_extent` if not `Point::Zero`, otherwise loads the image and retrieves its extent.
    * Its `Draw()` and `HandleMouse()` methods load the image and forward calls to the real image.
    * Its `Save()` method saves `_extent` and `_fileName` to the provided `ostream`.
    * Its `Load()` method retrieves `_extent` and `_fileName` from the provided `istream`.

### Singleton (127)

1. **You will use this pattern when:**
    * There must be exactly one instance of a class, and it must be accessible to clients from a well-known access point.
    * The sole instance should be extensible by subclassing, and clients should be able to use an extended instance without modifying their code.
2. **You will ensure a class has exactly one instance.**
3. **You will ensure the class provides a global point of access to its sole instance.**
4. **You will ensure clients access a Singleton instance solely through its `Instance` operation.**
5. **You will initialize the instance variable referring to the singleton with an instance of the subclass** when subclassing Singleton and selecting at run-time.
6. **You will modify the `Instance` operation whenever a new Singleton subclass is defined** if it directly determines the subclass to instantiate.
7. **You will ensure no dependencies exist between singletons across translation units** when relying on automatic global or static object initialization in C++ to avoid errors.

### State (305)

1. **You will use this pattern when:**
    * An object’s behavior depends on its state and must change at run-time.
    * Operations have large, multipart conditional statements that depend on the object’s state, making them hard to understand and maintain.
2. **You will ensure `Context` defines the interface of interest to clients** and maintains an instance of a `ConcreteState` subclass that defines the current state.
3. **You will ensure `State` defines an interface for encapsulating behavior** associated with a particular state of the `Context`.
4. **You will ensure each `ConcreteState` subclass implements behavior** associated with a state of the `Context`.
5. **You will ensure `Context` delegates state-specific requests to the current `ConcreteState` object.**
6. **You will allow a `Context` to pass itself as an argument to the `State` object** handling the request.
7. **You will ensure `Context` is the primary interface for clients.**
8. **You will allow clients to configure a `Context` with `State` objects**, but clients shall not deal with `State` objects directly once configured.
9. **You will allow either `Context` or `ConcreteState` subclasses to decide which state succeeds another** and under what circumstances.
10. **You will add an interface to `Context` allowing `State` objects to set the `Context`'s current state** if `State` subclasses specify transitions.
11. **You will ensure C++ `TCPConnection` declares `TCPState` as a friend class.**
12. **You will ensure C++ `TCPConnection` has a private `void ChangeState(TCPState*)` method and a private `TCPState* _state` member.**
13. **You will ensure C++ `TCPState` defines virtual methods for state-specific operations** (e.g., `Transmit`, `ActiveOpen`, `Close`) and a protected `void ChangeState(TCPConnection*, TCPState*)` method.
14. **You will ensure `TCPState` subclasses maintain no local state and require only one instance** (Singleton-like behavior).
15. **You will obtain the unique instance of each `TCPState` subclass via its static `Instance()` operation.**

### Strategy (315)

1. **You will use this pattern when:**
    * Many related classes differ only in their behavior.
    * You will want to configure a class with one of many behaviors.
    * You will need different variants of an algorithm.
    * An algorithm uses data that clients should not know about, to avoid exposing complex, algorithm-specific data structures.
    * A class defines many behaviors appearing as multiple conditional statements.
2. **You will ensure `Strategy` declares an interface common to all supported algorithms.**
3. **You will ensure `Context` uses the `Strategy` interface** to call the algorithm defined by a `ConcreteStrategy`.
4. **You will ensure `ConcreteStrategy` implements the algorithm** using the `Strategy` interface.
5. **You will ensure `Context` is configured with a `ConcreteStrategy` object** and maintains a reference to a `Strategy` object.
6. **You will allow `Context` to define an interface that lets `Strategy` access its data.**
7. **You will ensure `Strategy` and `Context` interact to implement the chosen algorithm.**
8. **You will allow a `Context` to pass all data required by the algorithm to the `Strategy`, or pass itself as an argument to `Strategy` operations.**
9. **You will ensure a `Context` forwards requests from its clients to its `Strategy`.**
10. **You will ensure clients usually create and pass a `ConcreteStrategy` object to the `Context`**, and thereafter interact with the `Context` exclusively.
11. **You will ensure the `Strategy` and `Context` interfaces enable efficient mutual data access.**
12. **You will ensure `Context` defines a more elaborate interface to its data** if a `Strategy` requests data from its `Context` explicitly.
13. **You will configure the strategy at compile-time and not change it at run-time** if using C++ templates for strategy configuration.
14. **You will design C++ `Compositor`'s interface carefully** to support all layout algorithms that subclasses might implement.

### Template Method (325)

1. **You will use this pattern when:**
    * You will want to implement invariant parts of an algorithm once and defer varying steps to subclasses.
    * Common behavior among subclasses should be factored and localized to avoid code duplication.
    * You will want to control subclass extensions by defining hook operations.
2. **You will ensure `AbstractClass` defines abstract primitive operations** for concrete subclasses to implement.
3. **You will ensure `AbstractClass` implements a template method defining the skeleton of an algorithm**, calling primitive operations as well as operations defined in `AbstractClass` or other objects.
4. **You will ensure `ConcreteClass` implements the primitive operations** to carry out subclass-specific steps.
5. **You will ensure `ConcreteClass` relies on `AbstractClass` to implement the invariant steps of the algorithm.**
6. **You will specify which operations are hooks** (may be overridden) and which are abstract operations (must be overridden) in template methods.
7. **You will call a hook operation from a template method in the parent class** to give the parent class control over subclass extensions, allowing subclasses to override the hook.

### Visitor (331)

1. **You will use this pattern when:**
    * An object structure contains many classes with differing interfaces, and operations depend on concrete classes.
    * Many distinct and unrelated operations need to be performed on an object structure, to avoid "polluting" classes with these operations.
    * Classes defining the object structure rarely change, but new operations are often defined.
2. **You will ensure `Visitor` declares a `Visit` operation for each `ConcreteElement` class** in the object structure. The `Visit` operation's name and signature must identify the class sending the `Visit` request.
3. **You will ensure `ConcreteVisitor` implements each operation declared by `Visitor`**, with each operation implementing a fragment of the algorithm for its corresponding `Element` class.
4. **You will ensure `Element` defines an `Accept` operation that takes a visitor as an argument.**
5. **You will ensure `ConcreteElement` implements an `Accept` operation** that calls the matching `Visit...` operation on the visitor, supplying itself as an argument.
6. **You will allow `ObjectStructure` to enumerate its elements** and optionally provide a high-level interface for the visitor to visit its elements.
7. **You will ensure a client creates a `ConcreteVisitor` object and traverses the object structure, visiting each element with the visitor.**
8. **You will declare C++ `Visitor` classes with a virtual destructor and a `virtual void Visit...` operation for each `ConcreteElement` class**, with the argument being a particular `ConcreteElement`, and a protected constructor.
9. **You will declare C++ `Element` classes with a virtual destructor, `virtual void Accept(Visitor&) = 0;`, and a protected constructor.**
10. **You will ensure a C++ `CompositeElement::Accept(Visitor& v)` iterates through its children**, calling `i.CurrentItem()->Accept(v)` for each, and then calls `v.VisitCompositeElement(this)`.
11. **You will ensure that if the object structure is responsible for iteration, a collection iterates over its elements and calls `Accept` on each, and a composite traverses its children recursively by having `Accept` call `Accept` on each child.**

## V. Foundation Library (C++) Definitions

### List Class

1. **You will provide a `List` template class with the following members:**
    * Constructor: `List(long size = DEFAULT_LIST_CAPACITY)`.
    * Copy Constructor: `List(List&)`.
    * Destructor: `~List()`.
    * Assignment Operator: `List& operator=(const List&)`.
    * Accessors: `long Count() const`, `Item& Get(long index) const`, `Item& First() const`, `Item& Last() const`.
    * Inclusion Check: `bool Includes(const Item&) const`.
    * Modification: `void Append(const Item&)`, `void Prepend(const Item&)`, `void Remove(const Item&)`, `void RemoveLast()`, `void RemoveFirst()`, `void RemoveAll()`.
    * Stack Operations: `Item& Top() const`, `void Push(const Item&)`, `Item& Pop()`.
2. **You will ensure the `List` destructor frees internal data structures but not the elements themselves.**
3. **You will not design the `List` class for subclassing; its destructor must not be virtual.**
4. **You will ensure the `Remove(const Item&)` operation requires the `Item` type to support the `==` operator.**

### Iterator Class (Base for Lists)

1. **You will provide an `Iterator` template base class with a protected constructor and the following pure virtual methods:**
    * `virtual void First() = 0;`
    * `virtual void Next() = 0;`
    * `virtual bool IsDone() const = 0;`
    * `virtual Item CurrentItem() const = 0;`

### ListIterator Class

1. **You will provide a `ListIterator` template class inheriting from `Iterator<Item>` with the following members:**
    * Constructor: `ListIterator(const List<Item>* aList)`.
    * Implementation of `Iterator` interface: `First()`, `Next()`, `IsDone()`, `CurrentItem()`.
    * Private members: `const List<Item>* _list`, `long _current`.
2. **You will initialize `_list` with `aList` and `_current` with `0` in the constructor.**
3. **You will set `_current` to `0` in `First()`.**
4. **You will increment `_current` in `Next()`.**
5. **You will return `true` if `_current` is greater than or equal to `_list->Count()` in `IsDone()`.**
6. **You will return the item at `_current` from `_list` in `CurrentItem()`, after throwing `IteratorOutOfBounds` if `IsDone()` is true.**

### Point Class

1. **You will define `Coord` as `float`.**
2. **You will provide a `Point` class with a static `const Point Zero` member representing `Point(0, 0)`.**
3. **You will provide a `Point` constructor that takes optional `Coord x` (default `0.0`) and `Coord y` (default `0.0`).**
4. **You will provide `Coord X() const`, `void X(Coord x)`, `Coord Y() const`, and `void Y(Coord y)` methods.**
5. **You will overload binary and unary arithmetic operators** (`+`, `-`, `*`, `/`, `+=`, `-=`, `*=`, `/=`, unary `-`).
6. **You will overload comparison operators** (`==`, `!=`).
7. **You will overload stream operators** (`<<`, `>>`).

### Rect Class

1. **You will provide a `Rect` class with a static `const Rect Zero` member, equivalent to `Rect(Point(0, 0), Point(0, 0))`.**
2. **You will provide `Rect` constructors that take `Coord x, Coord y, Coord w, Coord h` or `const Point& origin, const Point& extent`.**
3. **You will provide `Coord Width() const`, `void Width(Coord)`, `Coord Height() const`, `void Height(Coord)`, `Coord Left() const`, `void Left(Coord)`, `Coord Bottom() const`, `void Bottom(Coord)` methods.**
4. **You will provide `Point& Origin() const`, `void Origin(const Point&)`,`Point& Extent() const`, `void Extent(const Point&)` methods.**
5. **You will provide `void MoveTo(const Point&)`, `void MoveBy(const Point&)` methods.**
6. **You will provide `bool IsEmpty() const`, `bool Contains(const Point&) const` methods.**

## Key Highlights

* You will design for reusability, ensuring systems address future problems and evolve accordingly.
* You will program to an interface, defined by an abstract class, not a concrete implementation, and avoid concrete class dependencies.
* You will favor object composition over class inheritance for code reuse.
* You will promote loose coupling between classes to increase reusability, maintainability, and extensibility, avoiding tightly coupled systems.
* You will encapsulate an object's internal state and implementation details, ensuring they are invisible from outside to prevent direct access and cascading changes.
* You will isolate algorithms and concepts that are likely to change, avoiding hard-coding specifics to enhance system flexibility and reusability.
* You will apply design patterns judiciously, only when the flexibility they afford is genuinely needed, and avoid over-generalizing designs.

## Next Steps & Suggestions

* Develop or integrate static analysis rules and linter configurations to automatically check for adherence to core design principles and language-specific implementation conventions (e.g., virtual destructors, avoiding concrete class dependencies).
* Conduct a focused code audit of a critical existing codebase, using these rules as a checklist to identify areas for refactoring, improved maintainability, and greater design pattern conformance.
* Prioritize the rules based on their impact, frequency of violation, and ease of adoption, then create practical code examples and dedicated training modules to facilitate their understanding and application across development teams.
* Investigate the applicability and potential updates required for these rules in the context of modern programming languages (e.g., Java, C#, Python, Go) and evolving architectural patterns (e.g., microservices, cloud-native development).
