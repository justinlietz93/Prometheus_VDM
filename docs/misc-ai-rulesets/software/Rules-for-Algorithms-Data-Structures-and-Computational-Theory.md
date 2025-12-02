# Rules for Algorithms, Data Structures, and Computational Theory

This document synthesizes all technical rules, syntax requirements, algorithmic constraints, and theoretical principles distilled from various foundational texts on algorithms, data structures, and computational theory. These commandments define the expected behavior, performance characteristics, implementation details, and analytical rigor for well-formed systems, algorithms, and mathematical formulations within these domains.

**Generated on:** October 27, 2025 at 11:17 PM CDT

---

## I. General Principles & Ethics

1. **Resource Management:** Algorithms must be chosen to use computational time and space resources efficiently.
2. **Memory Model (RAM):** A Random Access Machine (RAM) model must be assumed, where instructions execute sequentially, each taking a constant amount of time, and all memory locations are accessible in constant time.
    * Data access (using or storing a variable) must take constant time.
    * RAM model instructions must be limited to common operations (arithmetic, data movement, control).
    * Data types must be integer, floating point, and character, with a limited word size (e.g., `c log2 n` bits for some constant `c > 1`).
    * Computing `2^n` and multiplying by `2^n` are constant-time operations if the result fits in a computer word.
    * Comments must take no execution time.

## II. Syntax, Pseudocode & Notation

1. **Block Structure:** Indentation must indicate block structure for loops and conditional statements (e.g., `for`, `while`, `repeat-until`, `if-else`).
2. **Comments:** Comments must start with `//`.
3. **Variables & Scope:** Variables must be local to procedures unless explicitly indicated as global.
4. **Loop Counters:** Loop counters must retain their value after loop exit, set to the value that first exceeded the loop bound.
    * `to` must be used when a `for` loop increments its counter.
    * `downto` must be used when a `for` loop decrements its counter.
    * When a loop counter changes by an amount greater than 1, the amount of change must follow the optional keyword `by`.
5. **Array Access:** Array elements must be accessed by `ARRAY_NAME[INDEX]` (e.g., `A[i]`).
    * Most arrays must use 1-origin indexing; explicit array bounds (e.g., `A[1 : n]`) must be specified.
    * `A[i : j]` must denote the subarray including elements `A[i]` through `A[j]` (inclusive).
6. **Object Attributes:** Object attributes must be accessed using `object.attribute` syntax (e.g., `x.f`). Chained attribute access `x.f.g` is implicitly parenthesized as `(x.f).g`.
7. **Null Pointers:** `NIL` must denote a null pointer.
8. **Parameter Passing:** Parameters must be passed by value. Arrays and objects must be passed by pointer (reference semantics), meaning changes to individual array elements or object attributes are visible to the calling procedure.
9. **Return Statements:** A `return` statement must immediately transfer control back to the caller and can return multiple values.
10. **Boolean Operators:** `and` and `or` must be short-circuiting operators.
11. **Error Handling:** The `error` keyword must indicate an error due to incorrect call conditions, causing immediate procedure termination. Calling procedures are responsible for handling such errors.
12. **Mathematical Constants:** The symbol `i` must exclusively denote `sqrt(-1)` in mathematical contexts.
13. **Matrix & Vector Naming:** Uppercase letters must be used for matrices, and lowercase letters for vectors.
14. **Matrix & Vector Element Naming:** Corresponding subscripted lowercase letters must be used for matrix elements (e.g., `a_ij` for matrix `A`). The `i`th element of vector `x` must be denoted as `x_i`.
15. **Matrix & Vector Set Notation:** The set of `m × n` real-valued matrices must be denoted as `R^(m × n)`. The set of `m × n` matrices with entries from set `S` must be denoted as `S^(m × n)`.
16. **Vector Representation:** Vectors must be treated as column vectors in matrix equations and as equivalent `n × 1` (column) or `1 × n` (row) matrices for matrix-vector and vector-vector products.
17. **Subscripted Variables:** Subscripted variables (e.g., `d_v`, `f_uv`) must be used for linear program formulations, not object attributes.
18. **Exponentiation Notation:** `exp(x)` must denote the exponential function `e^x`.

## III. Data Structures: Core Concepts & General Rules

1. **Object Representation:** Elements of a dynamic set must be represented by objects whose attributes (e.g., key, next, prev, p, left, right, color) can be examined and manipulated via pointers.
2. **Key Ordering:** If keys are drawn from a totally ordered set, operations like MINIMUM, MAXIMUM, SUCCESSOR, and PREDECESSOR must be definable.
3. **Array Element Sizing:** Each element of a particular array must be the same size. If elements vary in size, store pointers to objects (assuming pointers are uniform in size).
4. **Tree Node Attributes:** Each node `x` in a rooted tree must contain a `key` attribute. Binary tree nodes must have `p` (parent), `left` (left child), and `right` (right child) pointer attributes. `NIL` must be used for missing children or parent.
5. **Tree Root:** A tree `T` must have a `T.root` attribute pointing to its root node, or `NIL` if empty. The root node (`T.root`) must be the only node whose `p` attribute is `NIL`.
6. **Heap Array Representation:** Heaps must be represented by an array `A` and viewed as a nearly complete binary tree. `A.heap-size` attribute must indicate the number of valid heap elements (`0 <= A.heap-size <= n`).
7. **Heap Node Indexing:** The root of a heap must be `A[1]`. For node `i`, its children must be `LEFT(i) = 2i` and `RIGHT(i) = 2i + 1`. Its parent must be `PARENT(i) = ⌊i/2⌋`.
8. **Max-Heap Property:** For a max-heap, `A[PARENT(i)] >= A[i]` for every node `i` other than the root. The largest element must be at `A[1]`.
9. **Min-Heap Property:** For a min-heap, `A[PARENT(i)] <= A[i]` for every node `i` other than the root. The smallest element must be at `A[1]`.
10. **Priority Queue Mapping:** Implementations of priority queues must maintain a mapping between application objects and array indices (e.g., handles/hash table) and update it upon heap element relocation.
11. **Hash Function Mapping:** A hash function `h` must map the universe `U` of keys to slots `{0, 1, ..., m-1}` of hash table `T`.
12. **Hash Table Collision:** A collision must occur when two or more keys hash to the same slot.
13. **Dynamic Table Structure:** A dynamic table object `T` must contain `T.table` (pointer to storage), `T.num` (number of items), and `T.size` (total slots).
14. **Dynamic Table Load Factor Bounds:** The load factor of a dynamic table must be bounded below by a positive constant and above by `1`.

## IV. Data Structures: Implementations

1. **Matrix Storage:**
    * **Row-Major Order:** A matrix `M` must be stored row by row. For 1-origin indexing: `M[i, j]` is at `n * (i - 1) + j`. For 0-origin indexing: `M[i, j]` is at `n * i + j`.
    * **Column-Major Order:** A matrix `M` must be stored column by column. For 1-origin indexing: `M[i, j]` is at `i + m * (j - 1)`. For 0-origin indexing: `M[i, j]` is at `i + m * j`.
    * **Multiple-Array Representation:** An array `A` may store pointers to other arrays, allowing "ragged arrays" where rows/columns can have different lengths.
2. **Stacks (LIFO):**
    * **Policy:** A stack must implement a Last-In, First-Out (LIFO) policy for element removal.
    * **Array Implementation (`S[1:n]`):** `S.top` must index the most recently inserted element. `S.size` must equal the array capacity `n`. Stack elements must occupy `S[1...S.top]`. `S[1]` is the bottom, `S[S.top]` is the top.
    * **Empty State:** `S.top = 0`.
    * **Error Conditions:** An attempt to `POP` an empty stack must be an underflow error. `S.top` exceeding `S.size` (array capacity) must signify stack overflow.
    * **PUSH:** Increment `S.top`, then assign `x` to `S[S.top]`. Must check for overflow. (O(1) time).
    * **POP:** Decrement `S.top`. Must check for underflow. (O(1) time).
3. **Queues (FIFO):**
    * **Policy:** A queue must implement a First-In, First-Out (FIFO) policy for element removal.
    * **Array Implementation (`Q[1:n]`):** `Q.head` must index the head of the queue. `Q.tail` must index the next location for insertion. `Q.size` must equal the array capacity `n`. Elements must occupy `Q.head` through `Q.tail - 1` (circularly).
    * **Initial State:** `Q.head = Q.tail = 1`.
    * **Empty State:** `Q.head = Q.tail`.
    * **Full State:** `Q.head = Q.tail + 1` (circularly) or both `Q.head = 1` and `Q.tail = Q.size`.
    * **Error Conditions:** An attempt to `DEQUEUE` an empty queue must be an underflow error. An attempt to `ENQUEUE` a full queue must be an overflow error.
    * **ENQUEUE:** Assign `x` to `Q[Q.tail]`. `Q.tail` must advance circularly (`Q.tail = 1` if `Q.tail == Q.size`, else `Q.tail++`). Must check for overflow. (O(1) time).
    * **DEQUEUE:** Store `x = Q[Q.head]`. `Q.head` must advance circularly (`Q.head = 1` if `Q.head == Q.size`, else `Q.head++`). Must check for underflow. (O(1) time).
4. **Linked Lists:**
    * **Node Attributes:** Each element (`x`) must contain a `key` attribute and pointer attributes (`next`, `prev`).
    * **Doubly Linked List (`L`):** `x.next` must point to the successor, `x.prev` to the predecessor. `x.prev = NIL` must imply `x` is the head. `x.next = NIL` must imply `x` is the tail. `L.head` must point to the first element; `L.head = NIL` must imply the list is empty.
        * **LIST-SEARCH(L, k):** Returns pointer to first element with `key k` or `NIL`. (Worst-case O(n)).
        * **LIST-PREPEND(L, x):** Adds `x` to front. (O(1) time).
        * **LIST-INSERT(x, y):** Inserts `x` immediately after `y`. (O(1) time).
        * **LIST-DELETE(L, x):** Removes `x`. (O(1) time if doubly linked).
    * **Singly Linked List:** Elements must have `next` but no `prev` pointer. `INSERT` is O(1), `DELETE` is O(n) worst-case.
    * **Sorted List:** Linear order of list elements must correspond to linear order of keys.
    * **Circular List:** `prev` of head must point to tail, `next` of tail to head.
    * **Sentinels:** A dummy sentinel object (`L.nil`) must replace `NIL` values, having all attributes of ordinary list objects (e.g., `key`, `next`, `prev`), and its `color` (if applicable) must be `BLACK`.
        * In a circular, doubly linked list with sentinel: `L.nil` must lie between the head and tail. `L.nil.next` must point to the head, and `L.nil.prev` to the tail. The `next` of the tail and `prev` of the head must point to `L.nil`. The `L.head` attribute must be eliminated.
        * **Empty List (with sentinel):** `L.nil.next` and `L.nil.prev` must both point to `L.nil`.
        * **Sentinel Deletion:** The sentinel (`L.nil`) must never be deleted unless deleting the entire list.
        * **LIST-SEARCH'(L, k):** Must assume key might be in list and use the sentinel as temporary storage for `k` to simplify loop termination.
5. **Binary Search Trees (BST):**
    * **BST Property:** For any node `x`, all nodes `y` in its left subtree must have `y.key <= x.key`, and all nodes `y` in its right subtree must have `y.key >= x.key`.
    * **INORDER-TREE-WALK(x):** If `x != NIL`, recursively call on `x.left`, print `x.key`, then recursively call on `x.right`. (O(n) time).
    * **Query Operations:** `SEARCH`, `MINIMUM`, `MAXIMUM`, `SUCCESSOR`, and `PREDECESSOR` must run in `O(h)` time, where `h` is the height of the tree.
    * **Modification Operations:** `INSERT` and `DELETE` must run in `O(h)` time.
    * **TREE-INSERT(T, z):** `z.key` must be filled, `z.left` and `z.right` must be `NIL`. Inserts `z` while maintaining the BST property.
    * **TRANSPLANT(T, u, v):** Replaces subtree `u` with `v`. `u.p` becomes `v.p`. `u.p`'s child pointer to `u` must be updated to `v`. `v.p` must be set to `u.p` only if `v != NIL`. This procedure must not update `v.left` and `v.right`.
6. **Red-Black Trees:**
    * **Red-Black Properties (MUST be satisfied):**
        1. Every node is either red or black.
        2. The root is black.
        3. Every leaf (`T.nil`) is black.
        4. If a node is red, then both its children are black.
        5. For each node, all simple paths from the node to descendant leaves must contain the same number of black nodes.
    * **Height Constraint:** An `n`-node red-black tree must have height at most `2 lg(n + 1)`, ensuring `O(lg n)` worst-case for dynamic-set operations.
    * **Standard BST Procedure Restriction:** Standard `TREE-INSERT` and `TREE-DELETE` must not be used directly, as they do not guarantee maintenance of red-black properties.
    * **Rotations (LEFT-ROTATE, RIGHT-ROTATE):** Must be local operations, preserve BST property, and run in `O(1)` time. Only pointers change during rotation. `LEFT-ROTATE(T, x)` requires `x.right != T.nil`.
    * **RB-INSERT(T, z):** `z.key` must be filled, `z.left` and `z.right` must be set to `T.nil`, `z.color` must be set to `RED`. Must call `RB-INSERT-FIXUP(T, z)` to restore properties. (O(lg n) time).
    * **RB-INSERT-FIXUP(T, z):** Corrects violations. Must maintain invariant: `z` is red; if `z.p` is root, `z.p` is black; at most one violation (root red or `z`/`z.p` both red). Final step: `T.root.color = BLACK`. (O(lg n) time, at most 2 rotations).
    * **RB-TRANSPLANT(T, u, v):** `v.p = u.p` must be set unconditionally (even if `v == T.nil`).
    * **RB-DELETE(T, z):** Must use `RB-TRANSPLANT` and handle color. If the removed/moved node `y` was black, `RB-DELETE-FIXUP(T, x)` must be called. `y.color` must be set to `z.color` before removal. (O(lg n) time).
    * **RB-DELETE-FIXUP(T, x):** Corrects extra black on `x`. Loop must continue `while x != T.root` and `x.color == BLACK`. Final step: `x.color = BLACK`. (O(lg n) time, at most 3 rotations).
7. **Heaps:**
    * **Basic Heap Operations Time:** Basic heap operations must run in `O(h)` time, where `h` is the height of the heap (`O(lg n)`).
    * **`MAX-HEAPIFY(A, i)`:** Precondition: Binary trees rooted at `LEFT(i)` and `RIGHT(i)` are max-heaps. Corrects max-heap property violation at `i`. If `A[i]` is not the largest, it swaps `A[i]` with the largest child and recursively calls `MAX-HEAPIFY`. (O(lg n) time).
    * **`BUILD-MAX-HEAP(A, n)`:** Sets `A.heap-size = n`. Calls `MAX-HEAPIFY(A, i)` for `i` from `⌊n/2⌋` downto `1`. (O(n) time).
8. **Priority Queues (Max-Priority Queue):**
    * **`MAXIMUM(S)`:** If `A.heap-size < 1`, return "heap underflow" error. Returns `A[1]`. (Θ(1) time).
    * **`EXTRACT-MAX(S)`:** If `A.heap-size < 1`, return "heap underflow" error. Removes and returns `A[1]`. (O(lg n) + mapping overhead).
    * **`INCREASE-KEY(S, x, k)`:** Precondition: New key `k` must be at least as large as `x`'s current key. If `k < x.key`, return "new key is smaller than current key" error. Increases `x.key` to `k` and restores max-heap property. (O(lg n) + mapping overhead).
    * **`INSERT(S, x, k)`:** Precondition: `n` is array capacity. If `A.heap-size == n`, return "heap overflow" error. Inserts `x` with key `k`. (O(lg n) + mapping overhead).
9. **Hash Tables:**
    * **Independent Uniform Hashing (Ideal):** `h(k)` must be randomly and independently chosen uniformly from `{0, 1, ..., m-1}` for each `k` in `U`. Subsequent calls with the same `k` must yield the same `h(k)`.
        * **Uniformity:** Any given element must be equally likely to hash into any `m` slots.
        * **Independence:** Where an element hashes must be independent of where others hash.
    * **Collision Resolution by Chaining:** Each slot `T[j]` must point to a linked list. All elements hashing to `j` must be stored in `T[j]`'s list. Empty slots must contain `NIL`.
        * **CHAINED-HASH-INSERT(T, x):** Must use `LIST-PREPEND(T[h(x.key)], x)`. (Worst-case O(1)).
        * **CHAINED-HASH-SEARCH(T, k):** Must use `LIST-SEARCH(T[h(k)], k)`. (Average O(1 + `a`)).
        * **CHAINED-HASH-DELETE(T, x):** Must use `LIST-DELETE(T[h(x.key)], x)`. (Worst-case O(1) if doubly linked lists are used).
    * **Load Factor `a`:** Must be defined as `n/m` (number of elements / number of slots).
    * **Static Hashing (Division Method):** `h(k) = k mod m`. `m` must be a prime number not too close to an exact power of 2.
    * **Static Hashing (Multiplication Method):** `h(k) = floor(m * (k * A mod 1))`, where `0 < A < 1`. `m` can be chosen independently of `A`.
    * **Static Hashing (Multiply-Shift Method):** For `m = 2^l` on a `w`-bit machine word, `w`-bit `a = A * 2^w`: `h_a(k) = ((k * a) mod 2^w) >> (w - l)`. For randomized variant, `a` should be a randomly chosen odd integer.
    * **Random Hashing:** A hash function must be selected at random from a suitable family at program execution.
    * **Universal Hash Family (`H`):** For distinct `k1, k2` in `U`, the number of `h` in `H` for which `h(k1) = h(k2)` must be at most `|H|/m`.
    * **Number-Theoretic Universal Hash Family:** Choose prime `p > m` such that `k` lies in `0...p-1`. `h_a,b(k) = ((a*k + b) mod p) mod m`, where `a` in `Z_p*` (1 to p-1), `b` in `Z_p` (0 to p-1).
    * **Open Addressing:** All elements must occupy slots `T[0...m-1]`. Each entry must contain an element or `NIL`. The load factor `a` can never exceed 1 (`n <= m`).
        * **Probe Sequence:** For key `k`, `(h(k, 0), h(k, 1), ..., h(k, m-1))` must be a permutation of `(0, 1, ..., m-1)`.
        * **HASH-INSERT(T, k):** Probe `h(k, i)` until an empty slot `T[q]` is found. If `T[q]` is `NIL`, `T[q] = k`. If `m` probes fail, "hash table overflow" error.
        * **HASH-SEARCH(T, k):** Probe `h(k, i)` in the same sequence as insertion. Terminates successfully if `T[q] == k`. Terminates unsuccessfully (`return NIL`) if `T[q] == NIL`.
        * **Deletion (Open Addressing):** Cannot simply mark a slot as `NIL`. Must use a special `DELETED` value.
    * **Double Hashing:** `h(k, i) = (h1(k) + i * h2(k)) mod m`. `h2(k)` must be relatively prime to `m` to ensure the entire table is searched.
    * **Linear Probing:** `h(k, i) = (h1(k) + i) mod m`. (Essentially `h2(k)=1`).
    * **Performance (Open Addressing, No Deletions, `a < 1`):** Expected probes for unsuccessful search/insertion must be at most `1/(1 - a)`. Expected probes for successful search must be at most `(1/a) * ln(1/(1 - a))`.
    * **Performance (Linear Probing):** If `h1` is 5-independent and `a < 2/3`, expected constant time for search, insert, or delete.
10. **Dynamic Tables:**
    * **Initial State:** For an empty table: `T.num = 0`, `T.size = 0`.
    * **Expansion Policy (TABLE-INSERT):** If `T.size` is `0`, allocate `1` slot, set `T.size = 1`. If `T.num == T.size` (full), allocate `2 * T.size` slots, copy items, free the old table, update `T.table` and `T.size`. After allocation, insert the item and increment `T.num`.
    * **Combined Policy (Expansion/Contraction):** The table must double on full. The table must halve when deleting causes it to be less than `1/4` full (not `1/2`).
    * **Amortized Cost:** The amortized cost of a table operation (insert/delete) must be bounded above by a constant.
    * **Potential Function Behavior:** An expansion or contraction must exhaust all built-up potential, so that immediately after the operation, when the load factor is `1/2`, potential is `0`.
    * **Empty Table Storage:** Whenever `T.num = 0`, `T.size` must also be `0` (the table occupies no storage).

## V. Algorithm Design & Correctness

1. **Algorithmic Definition:** Algorithms must be well-defined computational procedures with precise specifications, accepting input values and producing output values.
2. **Algorithmic Correctness:** Algorithms must be correct, producing the correct solution for every problem instance and halting in a finite amount of time without infinite loops. Ordinarily, only correct algorithms must be considered.
3. **Algorithmic Preconditions & Postconditions:** Procedures and algorithms must clearly define their preconditions (inputs) and postconditions (outputs/state after execution).
4. **Loop Invariants:** Loop invariants must be formally stated and used to prove algorithm correctness.
    * **Insertion Sort Loop Invariant:** "At the start of each iteration of the for loop, the subarray `A[1 : i - 1]` consists of the elements originally in `A[1 : i - 1]`, but in sorted order."
    * **Quicksort PARTITION Loop Invariant:** "At the beginning of each iteration of the loop, for any array index k, the following conditions hold: 1. `p <= k <= i` implies `A[k] <= x`. 2. `i+1 <= k <= j-1` implies `A[k] > x`. 3. `k = r` implies `A[k] = x`."
    * **Heapsort Loop Invariant:** "At the start of each iteration of the for loop, the subarray `A[1 : i]` is a max-heap containing the `i` smallest elements of `A[1 : n]`, and the subarray `A[i + 1 : n]` contains the `n-i` largest elements of `A[1 : n]`, sorted."
    * **Priority Queue INCREASE-KEY Loop Invariant:** "At the start of each iteration of the while loop: a. If both nodes `PARENT(i)` and `LEFT(i)` exist, then `A[PARENT(i)].key >= A[LEFT(i)].key`. b. If both nodes `PARENT(i)` and `RIGHT(i)` exist, then `A[PARENT(i)].key >= A[RIGHT(i)].key`. c. The subarray `A[1 : A.heap-size]` satisfies the max-heap property, except that there may be one violation, which is that `A[i].key` may be greater than `A[PARENT(i)].key`."
    * **Dijkstra's Algorithm Loop Invariant:** `Q` must equal `V - S` at the start of each iteration of the main `while` loop.
5. **Random Number Generation:** `RANDOM(a, b)` must return an integer `x` such that `a <= x <= b`, with each `x` equally likely, and independent of previous calls.
6. **Single-Source Shortest Path Initialization:** All single-source shortest path algorithms must call `INITIALIZE-SINGLE-SOURCE` first and repeatedly relax edges.

## VI. Algorithm Analysis: General & Asymptotic

1. **Running Time Calculation:** The running time of an algorithm must be the number of instructions and data accesses executed. Cost accounting must be independent of specific computers but within the RAM model.
    * Each line of pseudocode is assumed to take a constant amount of time (`c_k` for line `k`).
    * The total running time is the sum of (cost per statement \* number of executions) for all statements.
2. **Analysis Focus:**
    * Ordinarily, focus on the worst-case running time (longest time for any input of size `n`).
    * When reporting average-case running time, use knowledge of (or assumptions about) the input distribution. Assume all inputs of a given size are equally likely unless otherwise specified.
    * For randomized algorithms, analyze the *expected* running time over the distribution of random choices made by the algorithm.
3. **Probabilistic Analysis:** Probabilistic analysis must require knowledge of or assumptions about the distribution of inputs.
4. **Number-Theoretic Algorithm Analysis:** The size of an input for number-theoretic algorithms must depend on the number of bits required to represent integers. An algorithm is polynomial time if its runtime is polynomial in the binary-encoded lengths of its inputs (`log(a_i)`). Measure by bit operations. `Θ(f^2)` bit operations must be used as the basis for `f`-bit number arithmetic (multiplication, division, remainder).
5. **Asymptotic Notation Function Properties:** All functions used within asymptotic notation (O, Ω, Θ, o, ω) must be asymptotically nonnegative.
6. **Asymptotic Notation Precision:** The most precise asymptotic notation possible must be used without overstatement.
7. **Tight Bounds:** `Θ`-notation must be used for asymptotically tight bounds. Context (e.g., "worst-case," "best-case") must not be omitted when using tight asymptotic bounds if they do not apply to all cases.
8. **Efficiency Comparison:** An algorithm's efficiency is usually compared based on its worst-case running time's order of growth.
9. **Asymptotic Notation Definitions:**
    * `f(n) = O(g(n))`: `f(n)` is bounded above by `c*g(n)` for sufficiently large `n`.
    * `f(n) = Ω(g(n))`: `f(n)` is bounded below by `c*g(n)` for sufficiently large `n`.
    * `f(n) = Θ(g(n))`: `f(n)` is bounded both above by `c2*g(n)` and below by `c1*g(n)` for sufficiently large `n`.
    * `f(n) = o(g(n))`: `f(n)` becomes insignificant relative to `g(n)` as `n` gets large (i.e., `lim f(n)/g(n) = 0`).
    * `f(n) = ω(g(n))`: `f(n)` becomes arbitrarily large relative to `g(n)` as `n` gets large (i.e., `lim f(n)/g(n) = ∞`).
10. **Asymptotic Notation Equivalencies:** `f(n) = Θ(g(n))` if and only if `f(n) = O(g(n))` and `f(n) = Ω(g(n))`.
11. **Asymptotic Notation Properties:** Transitivity, Reflexivity, Symmetry (for Θ), and Transpose Symmetry (O with Ω, o with ω) must hold.
12. **Asymptotic Comparability:** Not all functions are asymptotically comparable.
13. **Asymptotic Notation in Formulas:**
    * When `O(...)` appears alone on the RHS, `=` must imply set membership (`∈`).
    * When `O(...)` appears in a formula, it stands for some anonymous function; each instance must represent a distinct anonymous function.
    * When `O(...)` appears on the LHS, it implies that for any choice of anonymous functions on the LHS, there is a way to choose anonymous functions on the RHS to make the equation valid.
14. **Asymptotic Notation Conventions:** The variable tending to infinity must be inferred from context (e.g., `n` for `O(g(n))`). `T(n) = O(1)` for `n < X` means `T(n)` is bounded by a positive constant for `n < X`. Asymptotic notation must apply only when the function is defined.

## VII. Algorithm Analysis: Recurrence Relations

1. **Algorithmic Recurrence Definition:** A recurrence `T(n)` is algorithmic if `T(n) = Θ(1)` for all `n < n0` (for some sufficiently large `n0 > 0`), and every path of recursion terminates in a defined base case within a finite number of invocations for `n >= n0`.
2. **Implicit Base Cases:** Whenever a recurrence is stated without an explicit base case, it must be assumed to be algorithmic.
3. **Base Case `n0` Flexibility:** For algorithmic recurrences, any sufficiently large threshold constant `n0` can be chosen for base cases where `T(n) = Θ(1)`.
4. **Floors and Ceilings:** Floors and ceilings in divide-and-conquer recurrences must generally be ignored when determining asymptotic solutions, including when applying the Master Method. For Akra-Bazzi, floors and ceilings can be ignored if the driving function `f(n)` satisfies the polynomial-growth condition or if perturbations are `O(n^(log_b_i a_i - ε))` for `ε > 0`.
5. **Inequality Recurrences:** If a recurrence is an upper bound (e.g., `T(n) <= ...`), express its solution using O-notation. If a recurrence is a lower bound (e.g., `T(n) >= ...`), express its solution using Ω-notation.
6. **Substitution Method:** Requires guessing the solution form (using explicit constants) and proving correctness with mathematical induction. Asymptotic notation must not be used in the inductive hypothesis; constants must be named explicitly, and constants hidden by asymptotic notation must remain the same throughout the proof. If inductive proof fails, try subtracting a lower-order term.
7. **Recursion Tree Method:** Must be used to generate intuition for a good guess, then verify with the substitution method. For formal proof, be meticulous.
8. **Master Method (Theorem 4.1 & 4.4):** Applies to `T(n) = aT(n/b) + f(n)`, where `a >= 1`, `b > 1` are constants, and `f(n)` is nonnegative.
    * **Case 1:** If `f(n) = O(n^(log_b a - ε))` for some `ε > 0`, then `T(n) = Θ(n^(log_b a))`.
    * **Case 2:** If `f(n) = Θ(n^(log_b a) lg^k n)` for some `k >= 0`, then `T(n) = Θ(n^(log_b a) lg^(k+1) n)`.
    * **Case 3:** If `f(n) = Ω(n^(log_b a + ε))` for some `ε > 0` AND the regularity condition `af(n/b) <= cf(n)` holds for some `c < 1` and sufficiently large `n`, then `T(n) = Θ(f(n))`.
    * If conditions are not met, use other methods.
9. **Akra-Bazzi Method:** Applies to `T(n) = f(n) + Σ(i=1 to k) a_i * T(n/b_i)`.
    * **Preconditions:** `k` is a positive integer; `a_i` are strictly positive constants; `b_i` are strictly greater than 1 constants; `f(n)` is defined on sufficiently large nonnegative reals and is nonnegative.
    * Requires finding a unique `p` such that `Σ(i=1 to k) a_i / b_i^p = 1`.
    * **Solution form:** `T(n) = Θ(n^p (1 + ∫(x=1 to n) f(x) / x^(p+1) dx))`.
    * **Polynomial-growth condition** (for ignoring floors/ceilings): For `f(n)` there must exist `μ >= 0` such that for every `c > 1`, there exists `d > 1` (depending on `c`) such that `f(n/c) <= f(γn) <= df(n)` for all `1 <= γ <= c` and `n >= μ`.

## VIII. Algorithm Analysis: Amortized Analysis

1. **Total Credit Non-Negativity:** The total credit associated with the data structure must always be nonnegative. If total credit becomes negative, total amortized cost is not an upper bound on total actual cost.
2. **Upper Bound on Actual Cost:** The total amortized cost for a sequence of `n` operations must provide an upper bound on the total actual cost of that sequence.
3. **Universal Applicability:** The upper bound derived from amortized analysis must apply to all possible sequences of operations.
4. **Accounting Method:**
    * Amortized costs for operations must be chosen carefully.
    * For any sequence of `n` operations, the sum of amortized costs (Σ `ĉ_i`) must be greater than or equal to the sum of actual costs (Σ `c_i`).
    * Some operations must be overcharged to store credit, which then pays for later operations whose actual cost exceeds their amortized cost.
    * The total credit in the data structure must never become negative.
    * When representing bit credit for a binary counter, every `1`-bit must hold `$1` of credit to prepay for its reset to `0`. The amortized cost to set a `0`-bit to `1` is `$2`.
5. **Potential Method:**
    * The amortized cost `ĉ_i` of the `i`th operation is its actual cost `c_i` plus the change in potential `Φ(D_i) - Φ(D_i-1)`.
    * For total amortized cost to be an upper bound on total actual cost, final potential `Φ(D_n)` must be greater than or equal to initial potential `Φ(D_0)`.
    * To guarantee pre-payment, `Φ(D_i) ≥ Φ(D_0)` must be required for all `i`.

## IX. Sorting Algorithms

1. **Sorting Problem:** Input: A sequence of `n` numbers `(a_1, ..., a_n)`. Output: A permutation `(a'_1, ..., a'_n)` such that `a'_1 <= ... <= a'_n`.
2. **Data with Keys:** When sorting records, a sorting algorithm must permute satellite data along with keys. For large satellite data, use pointers to records rather than copying records.
3. **Comparison Sorts:** Any comparison sort on `n` inputs has a worst-case running time of at least `Ω(n lg n)`.
4. **Insertion Sort:** `INSERTION-SORT(A, n)` sorts `A[1 : n]` in-place. Post-condition: `A[1 : n]` contains original values in sorted order. Running time: `O(n^2)` worst-case, `O(n)` best-case.
5. **Merge Sort:** `MERGE-SORT(A, p, r)` sorts `A[p : r]`. Base case: If `p >= r`, return. `MERGE(A, p, q, r)` requires `p < q < r` and subarrays `A[p : q]` and `A[q + 1 : r]` to be sorted. Post-condition: `A[p : r]` contains merged, sorted elements. Running time: `Θ(n lg n)` in all cases.
6. **Selection Sort:** Running time: `Θ(n^2)` worst-case, `Θ(n^2)` best-case.
7. **Counting Sort:** Assumes input numbers are integers in `{0, 1, ..., k}`. Running time: `O(k + n)`.
8. **Radix Sort:** Input: `n` integers, each with `d` digits, each digit taking `k` possible values. Running time: `O(d(n + k))`.
9. **Bucket Sort:** Requires knowledge of a probabilistic distribution of input numbers (typically assumes uniform in `[0, 1)`). Running time: `O(n)` average-case.
10. **Heapsort:** Uses max-heaps. Sorts in-place. Running time: `O(n lg n)`.
11. **Quicksort:** Uses divide-and-conquer; combine step does no work. Worst-case `O(n^2)`. Expected `O(n lg n)` (distinct elements). Memory usage: Proportional to maximum recursion depth (up to `Θ(n)` worst-case).
    * **`PARTITION(A, p, r)`:** Selects `A[r]` as pivot `x`. Partitions `A[p : r]` in-place. Post-condition: `A[q]` (the pivot) is strictly less than every element of `A[q+1 : r]`. Running time: `O(n)`.
    * **`RANDOMIZED-QUICKSORT`:** Randomly chooses pivot from `A[p : r]` (each equally likely) and swaps with `A[r]` before calling `PARTITION`. Expected running time: `O(n lg n)` (distinct elements). No two elements are ever compared twice. Probability `z_i` compared with `z_j` (where `i < j`) is `2/(j-i+1)`.
    * **Hoare Partition (Problem 7-1):** Pivot `x = A[p]`. Indices `i` and `j` must never access elements outside `A[p : r]`. Precondition: Subarray `A[p : r]` must contain at least two elements. Upon termination, returns `j` such that `p <= j < r`. Every element of `A[p : j]` is less than or equal to every element of `A[j + 1 : r]`.

## X. Graph Algorithms: Shortest Paths

1. **Path Properties:** Shortest paths must not contain negative-weight cycles. Shortest paths must not contain positive-weight cycles. Shortest paths may contain 0-weight cycles, but can always be simplified to simple (cycle-free) paths. Assume shortest paths are simple and contain at most `|V| - 1` edges. Any subpath of a shortest path is itself a shortest path.
2. **Vertex Attributes:** Algorithms must maintain for each vertex `v` an attribute `v.d`, which is an upper bound on the weight of a shortest path from the source `s` to `v`. Algorithms must maintain for each vertex `v` a predecessor attribute `v.pi`, which is either another vertex or `NIL`. `v.pi` attributes must be set so that the chain of predecessors from `v` runs backward along a shortest path from `s` to `v`.
3. **Edge Relaxation:** Relaxation is the *only* means by which shortest-path estimates (`v.d`) and predecessors (`v.pi`) change.
4. **Arithmetic Conventions:** For any real number `a ≠ -infinity`, `a + infinity = infinity + a = infinity`. For any real number `a ≠ infinity`, `a + (-infinity) = (-infinity) + a = -infinity`.
5. **Graph Representation:** All algorithms must assume the directed graph `G` is stored in the adjacency-list representation. Edge weights `w(u, v)` must be stored with each edge `(u, v)` for `O(1)` access during traversal.
6. **`INITIALIZE-SINGLE-SOURCE(G, s)` Procedure:**
    * For each vertex `v ∈ G.V`: Set `v.d = infinity`, Set `v.pi = NIL`.
    * Set `s.d = 0`.
7. **`RELAX(u, v, w)` Procedure:**
    * If `v.d > u.d + w(u, v)`:
        * Set `v.d = u.d + w(u, v)`.
        * Set `v.pi = u`.
8. **`PRINT-PATH(G, s, v)` Procedure:** Prints a shortest path from `s` to `v` if `v.pi ≠ NIL`.
9. **Properties (Shortest Paths & Relaxation):**
    * **Triangle Inequality:** For any edge `(u, v) ∈ E`, `δ(s, v) ≤ δ(s, u) + w(u, v)`.
    * **Upper-Bound Property:** `v.d ≥ δ(s, v)` for all `v ∈ V`. Once `v.d` achieves `δ(s, v)`, it never changes.
    * **No-Path Property:** If no path connects `s` to `v`, then `v.d = δ(s, v) = infinity` after initialization, and this invariant must be maintained.
    * **Intermediate Relaxation Property:** Immediately after edge `(u, v)` is relaxed, `v.d ≤ u.d + w(u, v)`.
    * **Convergence Property:** If `s → u → v` is a shortest path, and `u.d = δ(s, u)` prior to `RELAX(u, v, w)`, then `v.d = δ(s, v)` afterward and remains so.
    * **Path-Relaxation Property:** If `p = (v0, v1, ..., vk)` is a shortest path from `s = v0` to `vk`, and its edges are relaxed in order `(v0, v1), ..., (vk-1, vk)`, then `vi.d = δ(s, vi)` for all `i` afterward.
    * **Predecessor Subgraph Rooted Tree Property:** If `G` has no negative-weight cycles reachable from `s`, then after initialization, the predecessor subgraph `G_pi` forms a rooted tree with root `s`, and this property must be maintained.
    * **Predecessor-Subgraph Property:** If `G` has no negative-weight cycles reachable from `s`, and `v.d = δ(s, v)` for all `v` after initialization and relaxations, then `G_pi` is a shortest-paths tree rooted at `s`.
10. **Bellman-Ford Algorithm:**
    * **Input & Output:** Given `G = (V, E)` with source `s` and weight function `w: E → R`. Returns a boolean indicating negative-weight cycle presence. If a cycle exists, no solution. Otherwise, produces shortest paths and weights.
    * **Procedure:** Initialize using `INITIALIZE-SINGLE-SOURCE(G, s)`. Perform `|G.V| - 1` passes, relaxing every edge. After passes, check: if `v.d > u.d + w(u, v)` for any edge `(u, v)`, return `FALSE`. Otherwise, return `TRUE`.
    * **Correctness (Theorem 22.4):** If `G` contains no negative-weight cycles reachable from `s`, returns `TRUE`, `v.d = δ(s, v)` for all `v`, and `G_pi` is a shortest-paths tree. If `G` contains a negative-weight cycle reachable from `s`, returns `FALSE`.
    * **Modifications:** To terminate early, stop when a pass performs no relaxations. To set `v.d` to `-infinity` for vertices on negative-weight cycles, modify the algorithm to propagate `-infinity`.
    * **Solving Difference Constraints:** A system `xj - xi ≤ bk` can be solved by constructing a constraint graph `G` with `n+1` vertices `{v0, ..., vn}`. Edges `(vi, vj)` with weight `bk` must be added for each `xj - xi ≤ bk`, and `(v0, vi)` with weight `0` for each `xi`. Run Bellman-Ford on `G` with `v0` as source. If Bellman-Ford returns `TRUE`, `x = (δ(v0, v1), ..., δ(v0, vn))` is a feasible solution. If `FALSE`, no feasible solution.
11. **Single-Source Shortest Paths in Directed Acyclic Graphs (DAGs):**
    * **Input:** `G` must be a weighted, directed acyclic graph (DAG).
    * **Procedure:** Topologically sort vertices of `G`. Initialize using `INITIALIZE-SINGLE-SOURCE(G, s)`. Iterate through each vertex `u` in topologically sorted order, relaxing every edge `(u, v)` leaving `u`.
    * **Correctness (Theorem 22.5):** At termination, `v.d = δ(s, v)` for all `v`, and `G_pi` is a shortest-paths tree.
    * **Critical Path (Longest Path):** To find a critical path, all edge weights must be negated, and `DAG-SHORTEST-PATHS` run, or `INITIALIZE-SINGLE-SOURCE` modified to use `-infinity` and `RELAX` modified to use `<`.
12. **Dijkstra's Algorithm:**
    * **Input:** `G` must be a weighted, directed graph with *nonnegative* weights on all edges (`w(u, v) ≥ 0`).
    * **Procedure:** Initialize using `INITIALIZE-SINGLE-SOURCE(G, s)`. Initialize empty set `S`. Initialize min-priority queue `Q` with all vertices from `V`, keyed by `d` values. Loop while `Q` is not empty: extract `u` with minimum `d` from `Q`, add `u` to `S`. For each neighbor `v` of `u`, relax `(u, v)`. If `RELAX` decreased `v.d`, call `DECREASE-KEY(Q, v, v.d)`.
    * **Constraints:** The algorithm must never insert vertices into `Q` after initial population. Each vertex must be extracted from `Q` and added to `S` exactly once.
    * **Correctness (Theorem 22.6):** Terminates with `u.d = δ(s, u)` for all `u`. `G_pi` is a shortest-paths tree rooted at `s`.
    * **Modifications:** `Q` can contain only vertices reachable from `s`. Dijkstra's works if edges leaving `s` may have negative weights, all *other* weights are nonnegative, and no negative-weight cycles exist.

## XI. Graph Algorithms: Minimum Spanning Trees

1. **Kruskal's Algorithm:**
    * **Data Structures:** Must use a disjoint-set data structure where each set contains vertices of one tree. Assume union-by-rank and path-compression for analysis.
    * **Procedure:** Initialize set `A` to empty. Create `|V|` trees using `MAKE-SET` for each vertex. Create and sort a list of all edges by increasing weight. Examine edges in order:
        * If `FIND-SET(u) == FIND-SET(v)`, ignore edge `(u, v)`.
        * If `FIND-SET(u) ≠ FIND-SET(v)`, add `(u, v)` to `A` and `UNION(u, v)`.
    * Return set `A`. When `G` is connected, `|E| >= |V| - 1`.
2. **Prim's Algorithm:**
    * **Inputs:** Requires connected graph `G` and a root vertex `r`.
    * **Data Structures:** Must maintain a min-priority queue `Q` of vertices not yet in the tree, keyed by `v.key`. `v.key` is the minimum weight of an edge connecting `v` to a tree vertex, `infinity` if no such edge. `v.pi` must name the parent of `v` in the tree.
    * **Procedure:** Initialize `u.key = infinity`, `u.pi = NIL` for all `u`. Set `r.key = 0`. Insert all vertices into `Q`. Loop while `Q` is not empty: extract `u` with minimum `key` from `Q`. For each neighbor `v` of `u`: if `v` in `Q` and `w(u, v) < v.key`, set `v.pi = u`, `v.key = w(u, v)`, and call `DECREASE-KEY(Q, v, w(u, v))`.
    * **Implicit MST:** Implicitly maintains `A = {(v.pi, v) : v ∈ V - {r} - Q}`.
    * **Termination:** `Q` must be empty. The MST is `A = {(v.pi, v) : v ∈ V - {r}}`.
    * **Loop Invariants (Main `while` loop):**
        1. `A = {(v.pi, v) : v ∈ V - {r} - Q}`.
        2. Vertices in MST are `V - Q`.
        3. For all `v ∈ Q`, if `v.pi ≠ NIL`, then `v.key < infinity` and `v.key` is the weight of a light edge `(v, v.pi)` connecting `v` to some vertex already in the MST.
    * **Implementation:** `Q` can be a binary min-heap (may require mapping) or Fibonacci heap for improved running time. Test `Q` membership in `O(1)` with a bit per vertex.

## XII. Graph Theory (General)

1. **Hamiltonian Cycle Definition:** A hamiltonian cycle of an undirected graph `G = (V, E)` must be a simple cycle that contains each vertex in `V` exactly once.
2. **Clique Definition:** A clique in an undirected graph `G = (V, E)` must be a subset `V' ⊆ V` of vertices such that every pair of vertices in `V'` is connected by an edge in `E` (i.e., `V'` forms a complete subgraph of `G`).
3. **Vertex Cover Definition:** A vertex cover of an undirected graph `G = (V, E)` must be a subset `V' ⊆ V` such that for every edge `(u, v) ∈ E`, at least one of `u` or `v` (or both) must be in `V'`.
4. **Hamiltonian Cycle Verification:** When verifying a hamiltonian cycle, the certificate (sequence of vertices) must be checked to contain each vertex in `V` exactly once. The certificate must also be checked to form a cycle in `G` (i.e., an edge must exist between each pair of consecutive vertices in the sequence, and between the first and last vertices).
5. **Undirected Bipartite Graph Constraint:** If `G` is an undirected bipartite graph with an odd number of vertices, then `G` must be nonhamiltonian.

## XIII. Complexity Theory & Reducibility

1. **P Class Definition:**
    * A problem must belong to the class P if it is solvable by a deterministic algorithm in polynomial time.
    * A problem in P must also be verifiable in polynomial time, establishing that P ⊆ NP.
    * If a problem in P makes a constant number of calls to polynomial-time subroutines and performs additional polynomial-time work, its total running time must remain polynomial.
    * The class P of languages must be closed under union, intersection, concatenation, complementation, and Kleene star operations.
2. **NP Class Definition:**
    * A language L belongs to NP if and only if there exists a two-input polynomial-time algorithm `A` and a constant `c` such that `L = {x ∈ {0,1}* : ∃ certificate y with |y| = O(|x|^c) s.t. A(x, y) = 1}`.
    * For an input `x ∈ L`, a certificate `y` must exist and allow algorithm `A` to prove that `x ∈ L` in polynomial time.
    * For any string `x ∉ L`, no certificate `y` must exist that falsely proves `x ∈ L`.
    * Any language in NP can be decided by an algorithm with a running time of `2^(O(n^k))` for some constant `k`.
    * The class NP of languages must be closed under union, intersection, concatenation, and Kleene star operations.
3. **co-NP Class Definition:** The complexity class co-NP is defined as the set of languages `L` such that `L` (the complement of L) belongs to NP.
4. **NP-Complete Language Definition:** A language `L` must be NP-complete if it satisfies two conditions:
    1. `L ∈ NP`.
    2. `L` is NP-hard (i.e., for every `L' ∈ NP`, `L' ≤_p L`).
5. **NP-Hard Language Definition:** A language `L` is NP-hard if for every `L' ∈ NP`, `L' ≤_p L`. This means `L` satisfies the second property of NP-completeness but not necessarily the first.
6. **NP-Hardness Implication:** If a language `L'` is NP-complete and `L' ≤_p L`, then `L` must be NP-hard.
7. **Polynomial-Time Reducibility (`L1 ≤_p L2`) Definition:**
    * `L1 ≤_p L2` if there exists a polynomial-time computable function `f: {0,1}* → {0,1}*` such that for all `x ∈ {0,1}*`, `x ∈ L1` if and only if `f(x) ∈ L2`.
    * The function `f` must be computable by a polynomial-time algorithm.
    * The polynomial-time reducibility relation `≤_p` must be transitive on languages.
8. **NP-Completeness Proof Methodology:** To prove a language `L` is NP-complete, one must:
    1. Prove `L ∈ NP`.
    2. Prove `L` is NP-hard by:
        a.  Selecting a known NP-complete language `L'`.
        b.  Describing an algorithm that computes a function `f` mapping every instance `x ∈ {0,1}*` of `L'` to an instance `f(x)` of `L`.
        c.  Proving that `f` satisfies the condition `x ∈ L'` if and only if `f(x) ∈ L` for all `x ∈ {0,1}*`.
        d.  Proving that the algorithm computing `f` runs in polynomial time.
9. **Reduction Strategy Guidelines:**
    * **Reduction Direction:** When showing problem `Y` is NP-complete by reducing from `X`, the reduction must always be from `X` to `Y` (i.e., `X ≤_p Y`).
    * **Arbitrary Input:** A reduction must take an arbitrary input to problem `X`.
    * **Restricted Output Structure:** The input to problem `Y` produced by the reduction can be restricted in structure.
    * **NP-Completeness Proof Components:** A proof that `Y` is NP-complete requires showing `Y ∈ NP` in addition to showing `Y` is NP-hard.
    * **Special Case Implication:** If problem `X` is NP-hard and is a special case of problem `Y`, then `Y` must be NP-hard.
    * **Hamiltonian Cycle to TSP Reduction:** When reducing the Hamiltonian Cycle problem (`G`) to the Traveling Salesperson Problem (TSP), edges present in `G` must have a low weight (e.g., 0), and edges not in `G` must have a high weight (e.g., infinity) to enforce path selection.
10. **Specific Reduction Constraints (3-CNF-SAT to SUBSET-SUM):**
    * **3-CNF Formula Structure:** No clause in the input 3-CNF formula must contain both a variable and its negation. Each variable in the input 3-CNF formula must appear in at least one clause.
    * **Number Representation:** Numbers for the SUBSET-SUM instance must be represented in base 10 (or any base `b > 7`) to prevent carries from affecting higher-order digits incorrectly.
    * **Digit Labeling:** Digit positions in the constructed numbers must be labeled by either a variable or a clause (with the least significant `k` digits labeled by clauses, and the most significant `n` digits by variables).
    * **Target Sum `t`:** The target sum `t` must have a `1` in each digit labeled by a variable and a `4` in each digit labeled by a clause.
    * **Variable Integers:** For each variable `x_i`, the set `S` must contain two integers `v_i` and `v̄_i`.
        * `v_i` and `v̄_i` must have a `1` in the digit labeled by `x_i` and `0`s in all other variable-labeled digits.
        * If literal `x_i` appears in clause `C_j`, the digit labeled by `C_j` in `v_i` must contain a `1`.
        * If literal `¬x_i` appears in clause `C_j`, the digit labeled by `C_j` in `v̄_i` must contain a `1`.
        * All other digits labeled by clauses in `v_i` and `v̄_i` must be `0`.
    * **Slack Variables:** For each clause `C_j`, the set `S` must contain two integers `s_j` and `s'_j` (slack variables).
        * `s_j` and `s'_j` must have `0`s in all digits other than the one labeled by `C_j`.
        * `s_j` must have a `1` in the `C_j` digit, and `s'_j` must have a `2` in this digit.
    * **Carry Prevention:** The constructed numbers must ensure no carries occur from lower digits to higher digits when summed, which is critical for the reduction's correctness.

## XIV. Boolean Logic & Circuits

1. **Boolean Values:** Boolean values must be drawn exclusively from the set `{0, 1}`, where `0` represents FALSE and `1` represents TRUE.
2. **Boolean Combinational Element Constraints:**
    * A boolean combinational element (logic gate) must have a constant number of boolean inputs and outputs.
    * Each element must perform a well-defined boolean function (e.g., NOT, AND, OR).
3. **NOT Gate Operation:** A NOT gate must take a single binary input `x` and produce a binary output `z` whose value is the opposite of `x`.
4. **AND Gate Operation:** An AND gate with two inputs `x` and `y` must produce a single binary output `z` that is `1` if and only if both `x` and `y` are `1`. Otherwise, `z` must be `0`.
5. **OR Gate Operation:** An OR gate with two inputs `x` and `y` must produce a single binary output `z` that is `1` if and only if at least one of `x` or `y` is `1`. Otherwise, `z` must be `0`.
6. **Boolean Combinational Circuit Constraints:**
    * A boolean combinational circuit must consist of one or more boolean combinational elements interconnected by wires.
    * A wire can connect the output of one element to the input of another.
    * A single wire must have no more than one combinational-element output connected to it.
    * Boolean combinational circuits must contain no cycles (i.e., the directed graph representing element connections must be acyclic).
    * For the circuit-satisfiability problem, the number of circuit outputs must be limited to one.
7. **Satisfiable Circuit Definition:** A 1-output boolean combinational circuit is satisfiable if there exists a truth assignment to its inputs that causes the circuit's output to be 1.
8. **Boolean Formula (SAT) Structure:** An instance of SAT is a boolean formula `φ` composed of:
    * `n` boolean variables (`x1, x2, ..., x_n`).
    * `m` boolean connectives (any boolean function with one or two inputs and one output, such as AND (∧), OR (∨), NOT (¬), implication (→), if and only if (↔)).
    * Parentheses.
    * A formula must contain at most one pair of parentheses per boolean connective (to avoid redundant parentheses, without loss of generality).
9. **Satisfiable Formula Definition:** A boolean formula is satisfiable if there exists a truth assignment to its variables that causes the formula to evaluate to 1.
10. **3-CNF Formula Structure:**
    * A literal must be an occurrence of a variable or its negation.
    * A clause must be the OR of one or more literals.
    * A boolean formula is in Conjunctive Normal Form (CNF) if it is expressed as an AND of clauses.
    * A boolean formula is in 3-Conjunctive Normal Form (3-CNF) if each clause contains exactly three distinct literals.

## XV. Linear Programming

1. **Problem Definition:** An objective function and all constraints for a linear programming problem must be linear functions of variables. Linear programming does not allow strict inequalities (must use `≤` or `≥`). Must involve minimizing or maximizing a linear function, subject to a finite set of linear constraints.
2. **Standard Form (Maximization):**
    * Variables `x_j` must be non-negative (`x_j ≥ 0`).
    * Constraints must be of the form `sum(a_ij * x_j) ≤ b_i`.
    * Any linear program must be convertible to the standard form.
    * Decision variables representing quantities (e.g., advertising cost) must be non-negative.
3. **Feasible Region & Optimality:** The feasible region of a linear program must be convex. An optimal solution must occur at a vertex of the feasible region.
4. **Solution Characterization:** An algorithm for linear programming must identify infeasible linear programs and unbounded linear programs.
5. **Integer Linear Program:** All variables must take on integer values.
6. **Dual Form (from primal maximization LP in standard form):**
    * Maximization must change to minimization.
    * Roles of right-hand side coefficients (`b_i`) and objective function coefficients (`c_j`) must be exchanged.
    * Each `≤` constraint must be replaced with `≥`.
    * Dual objective function variables `y_i` must correspond to primal constraints `b_i`.
    * Dual constraints `sum(a_ij * y_i) ≥ c_j` must correspond to primal variables `x_j`.
    * Dual variables `y_i` must be non-negative (`y_i ≥ 0`).
    * Multipliers (dual variables) must be non-negative when combining inequalities.
7. **Duality Properties:**
    * **Weak Duality:** For any feasible primal solution `x` and feasible dual solution `y`, `c^T * x ≤ b^T * y`.
    * **Optimality Condition:** If a feasible primal `x` and feasible dual `y` have equal objective values, then both are optimal.
    * **Strong Duality:** If both primal and dual are feasible and bounded, their optimal objective values must be equal.
8. **Fundamental Theorem of LP:** Any linear program in standard form must either have a finite optimal solution, be infeasible, or be unbounded.
9. **Complementary Slackness (Optimal `x`, `y`):** For optimal `x` and `y`:
    * `sum(a_ij * y_i) = c_j` OR `x_j = 0` for all `j`.
    * `sum(a_ij * x_j) = b_i` OR `y_i = 0` for all `i`.
10. **LP Formulations (Specifics):**
    * **Shortest Path LP:** Maximize `d_t`. Constraints: `d_v ≤ d_u + w(u,v)` for each `(u,v) ∈ E`, `d_s = 0`.
    * **Maximum Flow LP:** Maximize `sum(f_sv for v in V) - sum(f_vs for v in V)`. Constraints: `f_uv ≤ c(u,v)` (capacity), `sum(f_uv) = sum(f_vw)` (conservation for `v ≠ s, t`), `f_uv ≥ 0`. Assume `c(u,v) = 0` if no edge, no antiparallel edges.
    * **Minimum Cost Flow LP:** Minimize `sum(a(u,v) * f_uv for (u,v) in E)`. Constraints: `f_uv ≤ c(u,v)`, flow conservation for `v ≠ s, t`, `sum(f_sv) = d` (demand), `f_uv ≥ 0`.
    * **Multicommodity Flow LP:**
        * `sum(f_i_uv for i in commodities) ≤ c(u,v)` (aggregate capacity).
        * For each commodity `i`, flow conservation for `v ≠ s_i, t_i`.
        * For each commodity `i`, `sum(f_i_sv) = d_i` (commodity demand).
        * `f_i_uv ≥ 0`. Commodities share network, network capacity does not change.

## XVI. Linear Algebra

1. **Core Definitions & Types:**
    * **Element Field:** Each matrix or vector element in a linear system must belong to a field (typically real numbers).
    * **Matrix Definition:** A matrix must be a rectangular array of numbers.
    * **Vector Definition:** A vector must be a one-dimensional array of numbers.
    * **Unit Vector Definition:** A unit vector `e_i` must have its `i`th element as 1 and all other elements as 0.
    * **Zero Matrix Definition:** A zero matrix must have all entries as 0.
    * **Diagonal Matrix Definition:** For a diagonal matrix, the element `a_ij` must be 0 if `i` is not equal to `j`.
    * **Tridiagonal Matrix Definition:** For a tridiagonal matrix `T`, the element `t_ij` must be 0 if `|i - j| > 1`.
    * **Upper-Triangular Matrix Definition:** For an upper-triangular matrix `U`, the element `u_ij` must be 0 if `i > j`.
    * **Unit Upper-Triangular Matrix Definition:** A unit upper-triangular matrix must be upper-triangular and have all 1s along its main diagonal.
    * **Lower-Triangular Matrix Definition:** For a lower-triangular matrix `L`, the element `l_ij` must be 0 if `i < j`.
    * **Unit Lower-Triangular Matrix Definition:** A unit lower-triangular matrix must be lower-triangular and have all 1s along its main diagonal.
    * **Symmetric Matrix Definition:** A symmetric matrix `A` must satisfy `A = A^T`.
    * **Permutation Matrix Structure:** A permutation matrix `P` must have exactly one 1 in each row and exactly one 1 in each column, and 0s elsewhere.
    * **Identity Matrix Properties:** An `n × n` identity matrix `I_n` must be a diagonal matrix. An `n × n` identity matrix `I_n` must have 1s along its main diagonal. The `i`th column of an identity matrix must be the unit vector `e_i`.
    * **Positive-Definite Matrix Definition:** A matrix `A` must be positive-definite if `x^T Ax > 0` for all nonzero `n`-vectors `x`.
    * **Positive-Semidefinite Matrix Definition:** A matrix `A` must be positive-semidefinite if `x^T Ax ≥ 0` for all nonzero `n`-vectors `x`.
    * **Null Vector Definition:** A null vector `x` for a matrix `A` must be nonzero and satisfy `Ax = 0`.
    * **Linear Dependence Definition:** Vectors `x_1, ..., x_p` must be linearly dependent if there exist coefficients `c_i`, not all zero, such that `∑ c_i x_i = 0`.
    * **Linear Independence Definition:** Vectors must be linearly independent if they are not linearly dependent.
2. **Matrix Operations & Properties:**
    * **Matrix Addition Compatibility:** To add matrices `A` and `B`, they must have the same dimensions.
    * **Matrix Addition Element Rule:** The sum `C` of matrices `A` and `B` must have elements `c_ij = a_ij + b_ij`.
    * **Zero Matrix Addition Identity:** A zero matrix must act as the identity element for matrix addition.
    * **Scalar Multiplication Rule:** To perform scalar multiplication `λA`, each element `a_ij` of `A` must be multiplied by `λ`.
    * **Matrix Negative Definition:** The negative of a matrix `A` (denoted `-A`) must have entries `-a_ij`.
    * **Matrix Subtraction Definition:** Matrix subtraction `A - B` must be defined as `A + (-B)`.
    * **Matrix Multiplication Compatibility:** For matrix multiplication `AB`, the number of columns of `A` must equal the number of rows of `B`.
    * **Matrix Product Dimensions:** The product `C` of a `p × q` matrix `A` and a `q × r` matrix `B` must be a `p × r` matrix.
    * **Matrix Product Element Rule:** The elements `c_ik` of the matrix product `C = AB` must be calculated as `∑_{j=1}^q a_ij · b_jk`.
    * **Identity Matrix Multiplication Identity:** Identity matrices must act as identity elements for matrix multiplication.
    * **Zero Matrix Multiplication Result:** Multiplying any matrix by a zero matrix must result in a zero matrix.
    * **Matrix Multiplication Associativity:** Matrix multiplication must be associative: `(AB)C = A(BC)`.
    * **Matrix Multiplication Distributivity:** Matrix multiplication must distribute over addition: `A(B + C) = AB + AC`.
    * **Matrix Multiplication Non-Commutativity:** For `n > 1`, multiplication of `n × n` matrices must not be commutative (`AB ≠ BA` in general).
    * **Matrix-Vector Product Dimensions:** The product of an `m × n` matrix `A` and an `n`-vector `x` must result in an `m`-vector.
    * **Inner Product Definition:** The inner product of `n`-vectors `x` and `y` must be `x^T y = ∑_{i=1}^n x_i y_i`.
    * **Inner Product Commutativity:** The inner-product operator must be commutative (`x^T y = y^T x`).
    * **Outer Product Definition:** The outer product of `n`-vectors `x` and `y` must be an `n × n` matrix `Z` where `z_ij = x_i y_j`.
    * **Euclidean Norm Definition:** The euclidean norm `||x||` of an `n`-vector `x` must be `(∑_{i=1}^n x_i^2)^{1/2}`.
    * **Scalar-Vector Norm Property:** For any real `α` and `n`-vector `x`, `||αx||` must equal `|α| ||x||`.
    * **Product Transpose Rule:** The transpose of a matrix product `(AB)^T` must equal `B^T A^T`.
    * **Symmetry of `A^T A`:** The matrix product `A^T A` must always be a symmetric matrix.
    * **Sum/Difference of Symmetric Matrices:** If matrices `A` and `B` are symmetric, then both `A + B` and `A - B` must be symmetric.
    * **Symmetry of `B A B^T`:** For an arbitrary `m × n` matrix `B`, the product `B A B^T` must be symmetric.
    * **Product of Lower-Triangular Matrices:** The product of two lower-triangular matrices must be lower-triangular.
    * **Matrix Padding:** If matrix dimension `n` is not an exact power of 2, pad it to `n+k` (where `n+k` is an exact power of 2) by creating a block matrix `A'` with `A` in the top-left, `I_k` in the bottom-right, and zeros elsewhere.
    * **Fibonacci Number Algorithm Analysis:** For `f`-bit numbers, assume addition takes `Θ(f)` time and multiplication takes `Θ(f^2)` time.
3. **Matrix Inverses:**
    * **Invertible Matrix Uniqueness:** Matrix inverses, if they exist, must be unique.
    * **Inverse of Product of Nonsingular Matrices:** For nonsingular `n × n` matrices `A` and `B`, `(AB)^-1` must equal `B^-1 A^-1`.
    * **Inverse-Transpose Commutation:** The inverse operation must commute with the transpose operation: `(A^T)^-1 = (A^-1)^T`.
    * **Permutation Matrix Invertibility:** A permutation matrix `P` must be invertible.
    * **Permutation Matrix Inverse:** The inverse of a permutation matrix `P` must be `P^T`.
    * **Transpose of Permutation Matrix:** The transpose of a permutation matrix `P^T` must also be a permutation matrix.
    * **Inverse of Lower-Triangular Matrix:** The inverse of a lower-triangular matrix, if it exists, must be lower-triangular.
    * **Inverse of Symmetric Matrix:** If `A` is a nonsingular, symmetric matrix, then `A^-1` must be symmetric.
    * **Real Inverse Condition:** For a nonsingular `n × n` matrix `A` with complex entries, every entry of `A^-1` must be real if and only if every entry of `A` is real.
4. **Matrix Rank:**
    * **Row Rank = Column Rank:** The row rank of any matrix `A` must always equal its column rank.
    * **Matrix Rank Range:** The rank of an `m × n` matrix must be an integer between 0 and `min{m, n}` (inclusive).
    * **Zero Matrix Rank:** The rank of a zero matrix must be 0.
    * **Identity Matrix Rank:** The rank of an `n × n` identity matrix must be `n`.
    * **Alternate Rank Definition:** The rank of a nonzero `m × n` matrix `A` must be the smallest `r` such that `A = BC` where `B` is `m × r` and `C` is `r × n`.
    * **Full Rank Definition (Square):** A square `n × n` matrix must have full rank if its rank is `n`.
    * **Full Rank Condition (Square):** A square matrix must have full rank if and only if it is nonsingular.
    * **Full Column Rank Definition:** An `m × n` matrix must have full column rank if its rank is `n`.
    * **Full Column Rank Condition:** A matrix must have full column rank if and only if it does not have a null vector.
    * **Singular Matrix Condition:** A square matrix must be singular if and only if it has a null vector or its LUP decomposition yields a zero pivot.
    * **Rank Product Inequality:** For any two compatible matrices `A` and `B`, `rank(AB)` must be less than or equal to `min{rank(A), rank(B)}`.
    * **Rank Product Equality Condition:** `rank(AB)` must equal `min{rank(A), rank(B)}` if either `A` or `B` is a nonsingular square matrix.
    * **`A^T A` Positive-Definiteness:** If matrix `A` has full column rank, then `A^T A` must be positive-definite.
5. **Determinants:**
    * **Minor Definition:** The `ij`th minor of an `n × n` matrix `A` (for `n > 1`) must be the `(n-1) × (n-1)` matrix `A[ij]` formed by deleting row `i` and column `j`.
    * **Cofactor Definition:** The cofactor of element `a_ij` must be `(-1)^(i+j) det(A[ij])`.
    * **Determinant of 1x1 Matrix:** The determinant of a `1 × 1` matrix `A` must be `a_11`.
    * **Determinant Recursive Definition:** The determinant of an `n × n` matrix `A` (for `n > 1`) must be `∑_{j=1}^n (-1)^(1+j) a_1j det(A[1j])`.
    * **Determinant Zero Row/Column Property:** If any row or column of `A` is zero, then `det(A)` must be 0.
    * **Determinant Scalar Multiplication Property:** The determinant of `A` must be multiplied by `λ` if the entries of any one row (or column) of `A` are all multiplied by `λ`.
    * **Determinant Row/Column Addition Property:** The determinant of `A` must be unchanged if the entries in one row (or column) are added to those in another row (or column).
    * **Determinant Transpose Property:** `det(A)` must equal `det(A^T)`.
    * **Determinant Row/Column Exchange Property:** Exchanging two rows or columns of `A` must multiply `det(A)` by -1.
    * **Determinant Product Rule:** For any square matrices `A` and `B`, `det(AB)` must equal `det(A)det(B)`.
    * **Singular Matrix Determinant Condition:** An `n × n` matrix `A` must be singular if and only if `det(A) = 0`.
    * **Lower/Upper-Triangular Determinant:** The determinant of a lower-triangular or upper-triangular matrix must equal the product of its diagonal elements.
    * **Vandermonde Matrix Determinant:** The determinant of a Vandermonde matrix `V` (with entries `x_i^j`) must be `∏_{0 ≤ j < k ≤ n-1} (x_k - x_j)`.
6. **Solving Linear Systems:**
    * **System Size:** Linear systems primarily focus on exactly `n` equations and `n` unknowns.
    * **Matrix Inversion Restriction:** Matrix inverse must not be computed directly to solve linear systems due to numerical instability.
    * **LUP Decomposition:** Must find three `n x n` matrices `L`, `U`, and `P` such that `PA = LU`.
        * `L`: Unit lower-triangular matrix.
        * `U`: Upper-triangular matrix.
        * `P`: Permutation matrix.
        * LUP decomposition must pivot on entries with the largest absolute values for numerical stability.
        * If the pivot `p` is 0, a "singular matrix" error must be reported.
        * **`LUP-DECOMPOSITION` Procedure:** Initialize `pi` array for identity permutation (`pi[i] = i`). Find row `k'` (from `k` to `n`) with the largest absolute value in column `k`. Exchange `pi[k]` with `pi[k']`. Exchange row `k` with row `k'` in `A`. For `i > k`, set `A[i,k] = A[i,k] / A[k,k]`. Update `A[i,j]` by subtracting `A[i,k] * A[k,j]`.
        * **Final State:** Upon termination, `P` is represented by `pi`. `L[i,j] = 1` if `i = j`, `A[i,j]` if `i > j`, and `0` if `i < j`. `U[i,j] = A[i,j]` if `i ≤ j`, and `0` if `i > j`.
    * **Matrix Inversion using LUP:** To compute `A^-1`, solve `AX_j = e_j` for each column `X_j` of `A^-1`, where `e_j` is the `j`-th column of the identity matrix.
    * **`LUP-SOLVE` (Solving Linear Systems `Ax = b`):**
        * Compute `y_i` using forward substitution: `y_i = b_pi[i] - sum(L[i,j] * y_j for j from 1 to i-1)`.
        * Compute `x_i` using back substitution: `x_i = (y_i - sum(U[i,j] * x_j for j from i+1 to n)) / U[i,i]`.
    * **LU Decomposition (Symmetric Positive-Definite Matrix):** Must not cause division by zero (all pivots must be strictly positive).
        * **Symmetric Positive-Definite (SPD) Definition:** `A = A^T` (symmetric) AND `x^T * A * x > 0` for all non-zero `n`-vectors `x` (positive-definite).
        * **`LU-DECOMPOSITION` Procedure:** Initialize `U` with zeros below the diagonal. Initialize `L` with ones on the diagonal and zeros above the diagonal.
    * **Least-Squares Solution:** Minimize the norm of the error vector to find a least-squares solution. For nonsingular `A`, its inverse `A^-1` can be computed as `A^T * (A^T * A)^-1`.
    * **LUP vs. Normal Equations:** For `Ax = b` when `A` is nonsingular, `LUP` decomposition is preferred over `(A^T * A) * x = A^T * b` because it is faster and has better numerical properties.

## XVII. GF(2) Arithmetic & Linear Permutations

1. **GF(2) Addition Rule:** When working over GF(2), `1 + 1` must equal 0.
2. **GF(2) Entry Values:** When working over GF(2), matrix and vector entries must exclusively be 0 or 1.
3. **GF(2) Rank Definition:** When working over GF(2), the rank of a 0-1 matrix must be defined using arithmetic over GF(2).
4. **Range Cardinality (GF(2)):** For a matrix `A` over GF(2) with rank `r`, the cardinality of its range `|R(A)|` must equal `2^r`.
5. **Permutation Full Rank Requirement (GF(2)):** A matrix `A` must define a permutation on `S_n` only if `A` has full rank.
6. **Preimage Cardinality (GF(2)):** If `r` is the rank of an `n × n` matrix `A` over GF(2) and `y` is in `R(A)`, then the cardinality of its preimage `|P(A, y)|` must equal `2^(n-r)`.
7. **`B(S', m)` Cardinality (GF(2)):** The cardinality `|B(S', m)|` must equal `2^r` where `r` is the rank of the lower left submatrix.
8. **Block Mapping Count (GF(2)):** For each block in `B(S', m)`, exactly `2^(m-r)` numbers in `S` must map to that block.
9. **Linear Permutation Definition:** A linear permutation must map `x` to `Ax + c` where `c` is an `n`-bit vector and addition is performed over GF(2).
10. **Linear Permutation Limitation:** The set of permutations of `S_n` defined by multiplying by full-rank `n × n` 0-1 matrices over GF(2) must not include all permutations of `S_n`.

## XVIII. Number Theory

1. **Division Algorithm:** For `a` (integer) and `n` (positive integer), `a` must uniquely equal `q*n + r` where `0 ≤ r < n`.
2. **GCD Definition:** `gcd(0, 0)` must be defined as 0. When using Euclid's algorithm, inputs must be restricted to non-negative integers. GCD must not be computed using prime factorization due to inefficiency.
3. **Modular Arithmetic Conventions:** When working with `Z_n`, the smallest non-negative element of each equivalence class must be used as its representative. `Z_n = {0, 1, ..., n-1}` implies elements `a` represent `[a]_n`. Equivalence classes are denoted by representative elements, and modular operations by standard arithmetic symbols.
4. **Divisors:** Divisors must be defined as non-negative.
5. **`EUCLID(a, b)` Procedure:** If `b` is 0, return `a`. Otherwise, recurse with `EUCLID(b, a mod b)`.
6. **`EXTENDED-EUCLID(a, b)` Procedure:** If `b` is 0, return `(a, 1, 0)`. Otherwise, recursively call `EXTENDED-EUCLID(b, a mod b)`, then compute `d=d'`, `x=y'`, `y=x' - floor(a/b) * y'`.
7. **Modular Linear Equations (`ax = b (mod n)`):**
    * **Solvability:** Solvable if and only if `d | b`, where `d = gcd(a, n)`.
    * **Number of Solutions:** Has either `d = gcd(a, n)` distinct solutions modulo `n`, or no solutions.
    * **Solution Formula:** If `d = gcd(a, n)` and `d | b`, and `x'` is from `ax' + ny' = d`, then `x_0 = x' * (b/d) mod n` is a solution. The `d` distinct solutions are `x_i = (x_0 + i * (n/d)) mod n` for `i = 0, ..., d-1`.
    * **`MODULAR-LINEAR-EQUATION-SOLVER`:** Compute `gcd(a, n)` and `x', y'`. If `d | b`, compute `x_0`, then print `d` solutions. Else, report "no solutions".
    * If `gcd(a, n) = 1`, `ax = b (mod n)` has a unique solution modulo `n`.
    * If `gcd(a, n) = 1`, `ax = 1 (mod n)` has a unique solution modulo `n`. This solution is given by `EXTENDED-EUCLID(a, n)`.
8. **Chinese Remainder Theorem:**
    * If `n = n_1 * ... * n_k` where `n_i` are pairwise relatively prime, operations on `Z_n` can be performed equivalently by applying the operation independently in each coordinate of their `k`-tuple representation `(a_1, ..., a_k)` (where `a_i = a mod n_i`).
    * To compute `a` from `(a_1, ..., a_k)`, calculate `a = (sum(a_i * c_i for i from 1 to k)) mod n`, where `c_i = m_i * (m_i^{-1} mod n_i)` and `m_i = n/n_i`.
    * A system of simultaneous congruences `x = a_i (mod n_i)` (where `n_i` are pairwise relatively prime) must have a unique solution modulo `n` (product of `n_i`).
    * If `x = a (mod n_i)` for all `i` (where `n_i` are pairwise relatively prime), then `x = a (mod n)`.
9. **Modular Exponentiation:**
    * In `MODULAR-EXPONENTIATION`, if exponent `b` is 0, return 1.
    * If `b` is even, recursively compute `d = a^(b/2) mod n`, then return `(d * d) mod n`.
    * If `b` is odd, recursively compute `d = a^(b-1) mod n`, then return `(a * d) mod n`.
10. **Primality Testing:**
    * **Trial Division:** `n` is prime if and only if no trial divisor divides `n`.
    * **Nontrivial Square Root of 1 (mod n):** `x` is such if `x^2 = 1 (mod n)` AND `x ≠ 1 (mod n)` AND `x ≠ -1 (mod n)`. If such a root exists, then `n` must be composite.
    * **Base-`a` Pseudoprime:** `n` is a base-`a` pseudoprime if `n` is composite AND `a^(n-1) = 1 (mod n)`.
    * If `a^(n-1) ≠ 1 (mod n)` for any `a ∈ Z_n^*`, then `n` must be composite.
    * **Carmichael Number:** A composite integer `n` such that `a^(n-1) = 1 (mod n)` for all `a ∈ Z_n^*`.
    * **Composite Number Factorization:** If `n` is an odd composite number that is not a prime power, it must be decomposable into `n = n1 * n2` where `n1`, `n2` are odd, greater than 1, and relatively prime.
    * **`PSEUDOPRIME(n)`:** Input `n` must be an odd integer greater than 2. If `2^(n-1) mod n ≠ 1`, returns COMPOSITE. Else, returns PRIME.
    * **`MILLER-RABIN(n, s)`:** Input `n` must be an odd number greater than 2. Input `s` is the number of randomly chosen base values to try.
        * Express `n-1` as `2^t * u` where `u` is odd and `t ≥ 1`.
        * Select random `a` in `2 ≤ a ≤ n-2` for each trial.
        * `MILLER-RABIN` must report PRIME if `n` is prime. Has error probability at most `2^(-s)` for odd composite `n > 2`.
        * If `WITNESS(a, n)` returns TRUE, `n` is composite. If no witness found after `s` trials, returns PRIME.
        * During modular exponentiation, if a nontrivial square root of 1 (mod n) is found, return COMPOSITE.
        * For practical applications, use `s = 50` trials.
    * **`WITNESS(a, n)` Procedure:** `t` and `u` must satisfy `n-1 = 2^t * u` with `t ≥ 1` and `u` odd. Compute `x_0 = a^u mod n`. For `i = 1 to t-1`, compute `x_i = x_{i-1}^2 mod n`. If `x_i = 1` AND `x_{i-1} ≠ 1` AND `x_{i-1} ≠ n-1`, return TRUE. If `x_t ≠ 1`, return TRUE. Otherwise, return FALSE.
11. **Quadratic Residues:** `a` is a quadratic residue modulo `p` if `x^2 = a (mod p)` has a solution for `x`.
12. **Legendre Symbol:** `(a/p)` for prime `p` and `a ∈ Z_p^*` must be 1 if `a` is a quadratic residue mod `p`, and -1 otherwise.

## XIX. Polynomials & Fast Fourier Transform (FFT)

1. **Polynomial Representation:**
    * A polynomial `A(x)` must be represented as a formal sum `sum(a_j * x^j)`.
    * Coefficients and variable `x` must be drawn from an algebraic field `F` (typically complex numbers `C`).
    * The degree of a polynomial with degree-bound `n` must be an integer between `0` and `n-1`, inclusive.
    * A coefficient representation of a polynomial of degree-bound `n` must be a vector `(a_0, a_1, ..., a_{n-1})`.
    * A point-value representation of a polynomial of degree-bound `n` must be a set of `n` point-value pairs `(x_k, y_k)` where all `x_k` are distinct and `y_k = A(x_k)`.
2. **Polynomial Operations:**
    * The sum of two polynomials of degree-bound `n` must also be a polynomial of degree-bound `n`.
    * The product of two polynomials of degree-bound `n` must be a polynomial of degree-bound `2n-1`.
    * Given `n` distinct point-value pairs `(x_k, y_k)`, there must be a unique polynomial `A(x)` of degree-bound `n` such that `y_k = A(x_k)`.
    * To uniquely interpolate a polynomial of degree-bound `2n`, `2n` point-value pairs are necessary.
3. **FFT-based Polynomial Multiplication:**
    * For polynomial multiplication, use extended point-value representations with `2n` pairs for each input polynomial of degree-bound `n`.
    * If `n` is not an exact power of 2, pad polynomials by adding high-order zero coefficients to make their degree-bound an exact power of 2.
    * Double the degree-bound of input polynomials to `2n` by adding `n` high-order zero coefficients.
    * Use FFT of order `2n` to evaluate polynomials at the `(2n)`th roots of unity.
    * Compute `C(x) = A(x)B(x)` by pointwise multiplication of their point-value representations.
    * Use the inverse DFT (via FFT) on `2n` point-value pairs to interpolate the coefficient representation of `C(x)`.
4. **Complex Roots of Unity:**
    * A complex `n`th root of unity `ω` must satisfy `ω^n = 1`.
    * The principal `n`th root of unity `ω_n` is `e^(2πi/n)`.
    * All other complex `n`th roots of unity are powers of the principal `n`th root of unity.
5. **FFT Algorithm Constraints:**
    * Assume `n` is an exact power of 2 for FFT computations.
    * To compute the inverse DFT using FFT, switch the roles of input/output vectors, replace `w_n` with `w_n^-1`, and divide each element of the result by `n`.
    * For convolution `a * b` of length `n` vectors (where `n` is an exact power of 2), it must equal `DFT^{-1}_{2n}(DFT_{2n}(a) * DFT_{2n}(b))`, where `a` and `b` are padded with zeros to length `2n`, and `*` denotes component-wise product.
    * Input elements for an FFT circuit must be arranged according to a bit-reversal permutation (`a_k` moves to position `rev(k)`, where `rev(k)` is the `lg n`-bit integer formed by reversing the bits of `k`).
6. **`FFT` Procedure:**
    * If input vector length `n` is 1, return the vector itself.
    * Calculate principal `n`th root of unity `w_n = e^(2πi/n)`.
    * Initialize `w` (twiddle factor) to 1.
    * Form `a_even` from even-indexed coefficients of `a`, `a_odd` from odd-indexed coefficients.
    * Recursively compute FFT for `a_even` and `a_odd`.
    * For `k` from `0` to `n/2 - 1`, compute `y_k = y_even[k] + w * y_odd[k]` and `y_{k+n/2} = y_even[k] - w * y_odd[k]`.
    * Update twiddle factor `w` by multiplying by `w_n`. Optimize by computing `w * y_odd[k]` once and storing it.

## XX. String Matching

1. **Definitions:**
    * Text `T` must be an array `T[1:n]` of length `n`. Pattern `P` must be an array `P[1:m]` of length `m`. `m` must be less than `n`.
    * Elements of `P` and `T` must be characters from a finite alphabet `Σ`.
    * Pattern `P` occurs with shift `s` in text `T` if `0 ≤ s ≤ n-m` AND `T[s+j] = P[j]` for all `1 ≤ j ≤ m`.
    * `P[:k]` denotes the `k`-character prefix `P[1:k]`. `P[:0]` denotes the empty string `ε`. `P[:m]` denotes the full pattern `P`.
    * String comparison `x == y` takes `Θ(l)` time, where `l` is the length of the longest common prefix.
    * An empty substring must always have rank 0.
2. **General String Matching Algorithms:** Must perform preprocessing based on the pattern, then find all valid shifts `s` where `P` occurs in `T`.
3. **Rabin-Karp Algorithm:**
    * Characters must be assumed to be decimal digits, or digits in radix-`d` notation (`d = |Σ|`).
    * For `O(n)` expected matching time, the expected number of valid shifts `v` must be `O(1)` and prime modulus `q` must be greater than pattern length `m`.
    * If `t_s ≠ p (mod q)`, then shift `s` is invalid.
    * If `t_s = p (mod q)`, explicitly check `P[1:m] == T[s+1:s+m]` to confirm a valid shift.
4. **Finite Automaton (FA) String Matching:**
    * An FA must have: finite states `Q`, start state `q_0 ∈ Q`, accepting states `A ⊆ Q`, finite input alphabet `Σ`, transition function `δ: Q × Σ → Q`.
    * An FA accepts string `w` if its final state `φ(w)` is in `A`.
    * `σ(x)` for pattern `P` must be `max{k: P[:k]` is a suffix of `x}`.
    * For a string-matching automaton for `P[1:m]`: `Q = {0, ..., m}`, `q_0 = 0`, `A = {m}`. Transition `δ(q, a) = σ(P[:q]a)`.
    * FA's state `φ(T[:i])` must equal `σ(T[:i])` (length of longest prefix of `P` that is a suffix of `T[:i]`).
    * **`FINITE-AUTOMATON-MATCHER`:** If state `q` reaches `m`, a pattern occurrence is found at `i - m`.
    * **`COMPUTE-TRANSITION-FUNCTION`:** Initialize `k = min(m, q+1)`. While `P[:k]` is not a suffix of `P[:q]a`, decrement `k`. Set `δ(q, a)` to the final `k`.
5. **Knuth-Morris-Pratt (KMP) Algorithm:**
    * The prefix function `π[q]` for pattern `P` must be `max{k : k < q` and `P[:k]` is a suffix of `P[:q]}`.
    * **`KMP-MATCHER`:** First compute `π` for `P`. If mismatch `P[q+1] ≠ T[i]` AND `q > 0`, update `q = π[q]`. If `P[q+1] == T[i]`, increment `q`. If `q` reaches `m`, print `i-m` as a valid shift. After a match, update `q = π[q]`.
    * **`COMPUTE-PREFIX-FUNCTION`:** Initialize `π[1] = 0`. If mismatch `P[k+1] ≠ P[q]` AND `k > 0`, update `k = π[k]`. If `P[k+1] == P[q]`, increment `k`. Set `π[q] = k`.
6. **Suffix Arrays and LCP Arrays:**
    * A suffix array `SA` must represent the lexicographically sorted order of all suffixes of a text `T`. If `SA[i] = j`, then `T[j:]` must be the `i`-th suffix of `T` in lexicographic order.
    * The `LCP[i]` entry in a longest common prefix array must give the length of the longest common prefix between the `i`-th and `(i-1)`-th suffixes in the sorted order. `LCP[1]` must be defined as 0.
    * **`COMPUTE-SUFFIX-ARRAY`:** Initialize `left-rank` with `ord(T[i])`. If `i < n`, initialize `right-rank` with `ord(T[i+1])`. If `i == n`, initialize `right-rank` with 0. Store original index `i` in `index`. Sort `substr-rank` array by `left-rank` then `right-rank`. Call `MAKE-RANKS` to assign new ranks. Update `left-rank` with `rank[i]`. If `i+l <= n`, update `right-rank` with `rank[i+l]`. If `i+l > n`, update `right-rank` with 0. Store original index `i` in `index`. Re-sort `substr-rank` array by `left-rank` then `right-rank`. Double `l` (substring length). Populate `SA` with sorted indices. Use radix sort (via two passes of counting sort) for sorting `substr-rank` arrays to achieve `O(n)` per pass.
    * **`MAKE-RANKS`:** Assign rank 1 to the first sorted substring. Increment rank `r` if current substring has different ranks than previous. Assign current `r` to `rank[index]`.
    * **`COMPUTE-LCP`:** Populate `rank` array: `rank[SA[i]] = i`. Set `LCP[1] = 0`. Identify `T[j:]` as the suffix preceding `T[i:]` in sorted order (`j = SA[rank[i]-1]`). Increment `l` while characters `T[i+l]` and `T[j+l]` match and are within bounds. Set `LCP[rank[i]] = l`. If `l > 0`, decrement `l` for the next iteration.

## XXI. Probabilistic & Randomized Algorithms

1. **Randomized Algorithms (Behavior):** Behavior must be determined by input and random-number generator values.
2. **Randomized Algorithms (Analysis):** Running time must be analyzed as an *expected running time* over the random choices made by the algorithm itself.
3. **Indicator Random Variables (`I{A}`):** `I{A} = 1` if event `A` occurs, `0` otherwise. `E[I{A}] = Pr{A}` (expected value equals probability of event).
4. **Linearity of Expectation:** The expectation of a sum of random variables always equals the sum of their expectations, even if the variables are dependent.
5. **`HIRE-ASSISTANT(n)` Procedure:** Candidates are numbered `1` through `n` and interviewed in that order. An ability to determine if candidate `i` is the best seen so far (implies total order on ranks) must exist. If candidate `i` is better than `best`, `best` must be updated to `i`, and candidate `i` must be hired. The algorithm must always interview `n` candidates.
6. **`HIRE-ASSISTANT` Probabilistic Analysis Assumption:** Candidates must be assumed to arrive in a random order (uniform random permutation of ranks).
7. **`RANDOMIZED-HIRE-ASSISTANT(n)` Procedure:** First, randomly permute the list of candidates. Then, call `HIRE-ASSISTANT(n)`.
8. **Random Permutation (`RANDOMLY-PERMUTE(A, n)`):** Must produce a uniform random permutation (each of `n!` permutations is equally likely). For `i` from `1` to `n`, swap `A[i]` with `A[RANDOM(i, n)]`. Must work in-place (`O(1)` auxiliary space). After the `i`-th iteration, `A[i]` is never altered. Running time: `Θ(n)`.
9. **Birthday Paradox Assumptions:** Assume `n = 365` days in a year (ignore leap years). Birthdays must be uniformly distributed across the `n` days. Birthdays must be independent.
10. **Balls and Bins Assumptions:** Tosses must be independent. Each ball must be equally likely to end up in any bin.
11. **Online Hiring Problem (`ONLINE-MAXIMUM(k, n)`):** After each interview, a decision must be made immediately to either offer the position or reject the applicant. No two applicants must receive the same score. Strategy: Reject the first `k` applicants, then hire the first applicant thereafter with a higher score than all preceding. If no such applicant, hire the `n`-th applicant.
12. **Bernoulli Trials and Binomial Distributions:**
    * **Bernoulli Trial Properties:** For a Bernoulli trial random variable $X_i$ that takes values 0 (failure) or 1 (success) with probability $p$: `X_i^2` must equal `X_i`. The expectation `E[X_i]` must equal `p`. The expectation `E[X_i^2]` must equal `E[X_i]`. The variance `Var(X_i)` must be calculated as `p(1-p)` (or `pq` where `q=1-p`).
    * **Binomial Distribution `q` Definition:** For a binomial distribution $b(k; n, p)$, the variable `q` must always be defined as `1 - p`.
    * **Binomial Distribution Sum:** The sum of probabilities for all possible outcomes of a binomial distribution must equal 1 ($\sum_{k=0}^n b(k; n, p) = 1$).
    * **Binomial Distribution Expectation:** The expectation of a binomial distribution `X` (sum of `n` independent Bernoulli trials) must be `np`.
    * **Binomial Distribution Variance:** The variance of a binomial distribution must be `npq`.
    * **Variance of Sum of Bernoulli Trials Condition:** When computing the variance of a sum of Bernoulli trials, the trials must be independent.
    * **Binomial Distribution Growth Conditions:** The binomial distribution $b(k; n, p)$ must increase when `k < (n + 1)p`. The binomial distribution $b(k; n, p)$ must decrease when `k > (n + 1)p`.
    * **Binomial Distribution Maxima Conditions:** If `(n + 1)p` is an integer, then $b(k; n, p)$ must equal $b(k - 1; n, p)$ when `k = (n + 1)p`, resulting in two maxima at `k = (n + 1)p` and `k = np - q`. If `(n + 1)p` is not an integer, the binomial distribution must attain a unique maximum at the integer `k` such that `np - q < k < (n + 1)p`.
    * **Approximate Probabilities (Low Success Rate):** The probability of no successes in `n` Bernoulli trials, each with probability `p = 1/n`, must be approximately `1/e`. The probability of exactly one success in `n` Bernoulli trials, each with probability `p = 1/n`, must be approximately `1/e`.
13. **Probabilistic Bounds and Inequalities:**
    * **Probability Definitions (Counts):** The probability of at least `k` successes in `n` Bernoulli trials must be defined as the sum $\sum_{i=k}^n b(i; n, p)$. The probability of at most `k` successes in `n` Bernoulli trials must be defined as the sum $\sum_{i=0}^k b(i; n, p)$. The probability of fewer than `k` successes must be defined as the sum $\sum_{i=0}^{k-1} b(i; n, p)$. The probability of more than `k` successes must be defined as the sum $\sum_{i=k+1}^n b(i; n, p)$.
    * **Indicator Variable Definitions:** An indicator random variable `X_i` for a Bernoulli trial must be 1 for success and 0 for failure. The expectation of an indicator random variable `X_i` must be its probability of success `p_i` (`E[X_i] = p_i`). The total number of successes `X` must be defined as the sum of indicator random variables `X_i` for each trial (`X = \sum X_i`). The total expectation `μ` must be the sum of individual trial probabilities (`μ = \sum p_i`).
    * **Probabilistic Bound Parameters:** For Lemma C.1 (Binomial Upper Bound Lemma): `n` must be non-negative (`n ≥ 0`), `p` must be strictly between 0 and 1 (`0 < p < 1`), `q` must be `1 - p`, and `k` must be between 0 and `n` inclusive (`0 ≤ k ≤ n`). For Theorem C.4 (Left Tail Bound): `k` must be strictly between 0 and `np` (`0 < k < np`). For Corollary C.5: `k` must be strictly between 0 and `np/2` (`0 < k < np/2`). For Corollary C.6: `k` must be strictly between `np` and `n` (`np < k < n`). For Corollary C.7: `k` must be strictly between `(np + n)/2` and `n` (`(np + n)/2 < k < n`). For Theorem C.8: `r` must be greater than `μ` (`r > μ`), and `μ` must be defined as the expectation of `X`, `E[X]`. For Corollary C.9: `r` must be greater than `np` (`r > np`). If all trials have the same probability `p`, `μ` must equal `np`. The probability `Pr{X - np ≥ r}` must be the sum $\sum_{k=\lceil np+r \rceil}^n b(k; n, p)$.
    * **Markov's Inequality Application:** When bounding probabilities using `e^{\alpha(X-μ)}`, Markov's inequality (C.34) must be applied.
    * **Moment Generating Function for Bernoulli Trials:** The value of `E[e^{\alpha(X_i-p_i)}]` must be `p_i e^{\alpha(1-p_i)} + q_i e^{-\alpha p_i}`.
    * **Optimal Alpha Choice:** For minimizing the Chernoff bound in (C.51), `α` must be chosen as `ln(r/μ)`.
    * **Inequality C4-8:** For the inequality $b(k; n, 1/2) \le 2^n H(k/n)$, `k` must be strictly between 0 and `n` (`0 < k < n`).
    * **Inequality C4-9:** For the inequality `Pr{X < k} ≤ \sum_{i=0}^{k-1} b(i; n, p)`, `p` must be greater than or equal to `p_i` for all trials, and `k` must be between 1 and `n` inclusive (`1 ≤ k ≤ n`).
    * **Inequality C4-10:** For the inequality `Pr{X' ≥ k} ≥ Pr{X ≥ k}`, `r_i` must be equal to `p_i` for all trials, and `k` must be between 0 and `n` inclusive (`0 ≤ k ≤ n`).

## XXII. Online Algorithms

1. **Decision-Making:** Algorithmic decisions in online algorithms must be made without knowledge of future inputs.
2. **Solution Quality Guarantee:** Online algorithms designed must guarantee solution quality for all possible future inputs (worst-case approach).
3. **Competitive Ratio:** Online algorithms must be designed to achieve a competitive ratio as close to 1 as possible. The competitive ratio must be greater than or equal to 1. Algorithms with a smaller competitive ratio must be preferred.
4. **Worst-Case Guarding:** Online algorithms must be designed to guard against any possible worst case.
5. **Online Caching:** An online caching algorithm must make a decision without knowing when the elevator will arrive.
6. **Adversary Models:** When analyzing randomized online algorithms, an oblivious adversary (one who does not know the random choices) must typically be used. When possible, randomized algorithms must be designed against a nonoblivious adversary (one who knows random choices) as this is a stronger model.
7. **Competitive Analysis Assumptions (e.g., Caching):**
    * Assume number of requests (`n`) is greater than cache size (`k`).
    * Assume at least `k` distinct blocks are requested.
    * Assume cache starts empty.
    * Assume each epoch contains exactly `k` requests, each for a unique block (for `RANDOMIZED-MARKING`).
    * An epoch must contain at least one new request (`r_i ≥ 1`).
    * The position of an element `x_j` in list `L` (`r_L(x_j)`) must be between 1 and `n` (inclusive).
    * Reorder list elements only by swapping two adjacent elements.
    * Minimize total cost of `LIST-SEARCH` calls plus total number of swaps.
    * The inversion count used in competitive analysis must be nonnegative (`Φ_i ≥ 0`).
8. **Competitive Ratio Independence:** Algorithms with a competitive ratio independent of input sequence size (`n`) must be preferred.

## XXIII. Security & Cryptography

1. **RSA Cryptosystem:**
    * **Key Generation:** Select two distinct large prime numbers `p` and `q` (e.g., 1024 bits each) randomly. Compute `n = p * q`. Select a small odd integer `e` such that `gcd(e, φ(n)) = 1` (where `φ(n) = (p-1)(q-1)`). Compute `d` as the multiplicative inverse of `e` modulo `φ(n)`.
    * **Keys:** The public key must be `(e, n)`. The secret key must be `(d, n)` and must be kept secret.
    * **Message Domain:** The message domain for RSA must be `Z_n`.
    * **Encryption/Verification:** To encrypt or verify an RSA message `M` with public key `(e, n)`, compute `M^e mod n`.
    * **Decryption/Signing:** To decrypt or sign an RSA ciphertext `C` with secret key `(d, n)`, compute `C^d mod n`.
    * **Prime Finding:** Large primes must be found efficiently for RSA key generation.
2. **Cryptographic Primitives:**
    * **Collision-Resistant Hash Function `h`:** Must be easy to compute, but finding `M ≠ M'` such that `h(M) = h(M')` must be computationally infeasible.
3. **Secure Communication:** To send a signed and encrypted message, first sign the message, then encrypt the message/signature pair with the recipient's public key.
4. **Key Properties:**
    * Only the owner of a secret key (`S`) must be able to compute its associated function `S()` within a practical timeframe.
    * The secret key (`S_A`) must be kept secret.
    * Public and secret keys must define inverse functions (`S(P(M)) = M` and `P(S(M)) = M`).
    * A digital signature must be verifiable by anyone with access to the signer's public key.

## XXIV. Combinatorics & Counting

1. **Balls and Bins Problem Rules:**
    * **Distinct Balls, Order Irrelevant in Bin:** If `n` balls are distinct and their order within a bin does not matter, the number of ways to place them in `b` distinct bins must be `b^n`.
    * **Distinct Balls, Order Matters in Bin:** If `n` balls are distinct and their order within each bin matters, the number of ways to place them in `b` distinct bins must be `(b + n - 1)! / (b - 1)!`.
    * **Identical Balls, Order Irrelevant in Bin:** If `n` balls are identical and their order within a bin does not matter, the number of ways to place them in `b` distinct bins must be `(n+b-1 choose n)`.
    * **Identical Balls, No More Than One Per Bin (n ≤ b):** If `n` balls are identical, no bin may contain more than one ball, and `n ≤ b`, the number of ways to place them in `b` distinct bins must be `(b choose n)`.
    * **Identical Balls, No Bin Left Empty (n ≥ b):** If `n` balls are identical, no bin may be left empty, and `n ≥ b`, the number of ways to place them in `b` distinct bins must be `(n-1 choose b-1)`.

## XXV. Game Theory

1. **Monty Hall Problem Specification:**
    * **Initial Door Pick Randomness:** The contestant's first door pick must be random, with a 1/3 probability of choosing the right door.
    * **Monty Always Offers Switch Assumption:** In problem C-1.a, Monty must always offer the contestant the opportunity to switch.
    * **Probability Definitions:** `p_right` is defined as the probability Monty offers a switch when the right door is initially chosen. `p_wrong` is defined as the probability Monty offers a switch when a wrong door is initially chosen. `p_switch` is defined as the probability the contestant switches, given an offer.
    * **Monty's Strategy for Always Offering:** If Monty always offers a switch, then `p_right` must be 1 and `p_wrong` must be 1.
    * **Contestant's Strategy for Always Switching:** If the contestant always switches, then `p_switch` must be 1.
    * **Game Step 1 (Contestant Pick):** The contestant must pick a door at random, resulting in a 1/3 probability for the automobile and 2/3 for a goat.
    * **Game Step 2 (Carol Opens):** Carol must open one of the two closed doors, revealing a goat.
    * **Game Step 3 (Monty Offers):** Monty's offer probability must be `p_right` if the initial choice was right, and `p_wrong` if the initial choice was wrong.
    * **Game Step 4 (Contestant Switch):** If Monty makes an offer, the contestant must switch with probability `p_switch`.
    * **Game Step 5 (Carol Final Open):** Carol must open the contestant's final chosen door, revealing either an automobile (win) or a goat (lose).
    * **Probability of Winning Formula:** The probability of winning the automobile must be calculated as `1/3 · p_right · p_switch + 2/3 · (1 - p_wrong · (1 - p_switch))`.
    * **Denominator Non-Zero Constraint:** The expression `p_right + 2p_wrong` must not equal 0.
    * **Optimal Switch Probability:** For the contestant to maximize the minimum probability of winning (when Monty's strategy is unknown), the choice of `p_switch` must be `1/2`.

## XXVI. General Mathematical Foundations

1. **Group Theory:**
    * The order of a subgroup `|S'|` must be a divisor of the order of the group `|S|`.
    * The order of an element `a`, `ord(a)`, must be the smallest positive integer `t` such that `a^t = e` (group identity).
    * `a^0` must be defined as `e` (group identity) and `a^i` as `a^(i mod t)` where `t = ord(a)`.
2. **Event Set Closure (Complementation):** The set of events of a sample space must be closed under complementation.
3. **Event Set Closure (Unions):** The set of events of a sample space must be closed under finite or countable unions.
4. **Event Set Closure (Intersections):** The set of events of a sample space must be closed under finite or countable intersections.

## Key Highlights

* All algorithms must adhere to the Random Access Machine (RAM) model assumptions, prioritizing efficient use of computational time and space resources.
* Algorithm correctness must be formally proven using stated preconditions, postconditions, and especially loop invariants, ensuring finite termination and accurate solutions.
* Running times are primarily analyzed for worst-case scenarios using the most precise asymptotic notation (Θ for tight bounds), with the Master Method or Akra-Bazzi method applied for recurrence relations.
* Red-Black trees must strictly adhere to five specific color properties, guaranteeing a height of at most `2 lg(n + 1)` and ensuring `O(lg n)` worst-case performance for dynamic-set operations.
* Shortest path algorithms like Bellman-Ford and Dijkstra's fundamentally rely on the edge relaxation principle, with Bellman-Ford handling negative edge weights and Dijkstra's requiring nonnegative weights for efficiency.
* Hash tables require a well-chosen hash function and effective collision resolution, with dynamic tables maintaining a load factor bounded between a positive constant and 1 to ensure amortized constant-time operations.
* Proving a language is NP-complete requires demonstrating it belongs to NP and is NP-hard by constructing a polynomial-time reduction from a known NP-complete problem.
* Linear systems `Ax = b` must be solved using LUP decomposition, which factors `PA = LU` with pivoting for numerical stability, rather than direct matrix inversion due to its numerical instability.
* Randomized algorithms' running times are analyzed as an expected value over the algorithm's internal random choices, rather than input distribution, for problems like quicksort or primality testing.
* Basic data structures like Stacks and Queues must strictly enforce LIFO and FIFO policies, respectively, utilizing array implementations with circular indexing and robust checks for underflow and overflow conditions.

## Next Steps & Suggestions

* Develop automated static analysis tools or linters to check for compliance with the specified syntax, pseudocode conventions, and data structure property invariants.
* Integrate the comprehensive ruleset into existing algorithm design, code review, and quality assurance processes to ensure consistent application and adherence.
* Establish a formal governance model and version control system for the ruleset itself, including procedures for proposing updates, reviewing new algorithmic advancements, and managing changes.
* Create practical examples, interactive guides, or annotated case studies for each major section to demonstrate the application of these rules and aid in developer education and onboarding.
