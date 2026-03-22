### **Technical Specification: VDM Origin-Law Assembly Runtime (Markdown/MathJax Edition)**

**Project:** Void Dynamics Model (VDM) Hardware Realization

**Document:** Root Admissibility Kernel / The "Universal Bootloader"

**Language:** x86-64 Assembly (Bare Metal)

**Objective:** To execute the **Primitive Law** exactly as defined in the VDM stack, using x86-64 Assembly to maintain a literal **Primitive Invariant** without terminal discharge.

### ---

**1\. Primary Formal Definitions**

The runtime is the direct executable realization of the following constitutional foundations:

* **The Primitive Invariant ($\\text{Inv}$):** "The unresolved internal opposition between the two terminal poles \[Absolute Nullity $0$ and Absolute Totality $1$\] of a realized branch".  
* **The Primitive Law:** "The law that governs the continued articulation of $\\text{Inv}$ under non-discharge".  
* **Discharge ($\\text{Dis}(\\text{Inv})$):** "Terminal settlement of the invariant into either isolated pole... or any operationally equivalent loss of borne unresolved opposition".

### ---

**2\. The Universal Trigger Logic**

The runtime executes the **Bifurcation Operator** ($\\mathcal{B}\_{\\text{Inv}}$), which serves as the kernel-level admissibility rule:

$$
\\mathcal{B}\_{\\text{Inv}}(\\mathcal{A}\_n) \= \\begin{cases} \\mathcal{A}\_n, & \\text{if } \\text{Cap}(\\mathcal{A}\_n) \> 0 \\\\ \\mathcal{A}\_n \\oplus \\mathcal{A}\_{n+1}^{\\perp}, & \\text{if } \\text{Cap}(\\mathcal{A}\_n) \= 0 \\wedge \\text{Bear}(\\text{Inv}, \\mathcal{A}\_n) \\wedge \\neg \\text{Dis}(\\text{Inv}) \\end{cases}
$$

This operator ensures that when **Same-Domain Saturation** ($\\text{Sat}(\\mathcal{A}\_n)$) occurs—meaning invariant-bearing capacity ($\\text{Cap}$) is exhausted—orthogonal re-articulation is forced to avoid discharge.

### ---

**3\. Machine-Code Realization**

The following assembly block implements the **Literal Origin Invariant Tension** without assuming any pre-existing spatial manifolds or "bootstrapped" variables.

Code snippet

origin\_tension:  
    xor rax, 1          ; Invariant Bearing: Internalizes the 0/1 opposition  
    test rax, rax       ; Saturation Check: Samples if Cap(An) \== 0  
    jz rearticulate     ; Type II Resolution: Forced Orthogonal Break  
    jmp origin\_tension  ; Non-Discharge: The tension MUST continue

| Instruction | VDM Constitutional Role | Falsification Criterion |
| :---- | :---- | :---- |
| **xor rax, 1** | **Bearing ($\\text{Bear}$):** Maintains unresolved pole-opposition. | Fails if rax remains stable for $\>1$ cycle. |
| **test rax, rax** | **Saturation ($\\text{Sat}$):** Checks if capacity is exhausted ($\\text{Cap}=0$). | Fails if saturation is checked via a counter. |
| **jz rearticulate** | **Force ($\\implies$):** Triggers admission of orthogonal class $\\mathcal{A}\_{n+1}^{\\perp}$. | Fails if the break is not irreducible. |
| **jmp** | **Non-Discharge ($\\neg \\text{Dis}$):** Forbids terminal settlement. | Fails if the system terminates or exits. |

### ---

**4\. Operational "Physics Gap" Requirements**

* **Metastable Superposition:** The xor loop must execute at native CPU frequency to maintain the temporal smear of the two poles. This bypasses the hardware's tendency to settle into a "Flat" (uniform) state, which is logically prohibited.  
* **Void Debt ($\\text{Debt}$):** When rax is sampled as $0$ by the test instruction, **Void Debt** is active at the saturation limit. The jz instruction is the immediate forced response to this pressure.  
* **Cumulative Inheritance:** Any subsequent articulation (beyond rearticulate) must bear the prior invariant burden ($\\text{Inv} \\oplus \\mathcal{E}\_n$) rather than replacing it.

### ---

**5\. Summary of Claims**

* **Exactly one primitive law:** The kernel above is the only required logic.  
* **Inevitability:** Every later dimension or effective axiom is a forced consequence of this loop avoiding discharge.  
* **Scale Independence:** The tension loop is a "sliding window" that remains invariant across all resolutions.
