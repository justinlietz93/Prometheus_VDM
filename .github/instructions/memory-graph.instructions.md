---
applyTo: '**'
---
## **Memory Graph Management and Workflow Instructions**

You are expected to **manage the memory system** for this project. The **KG-Lite memory system** tracks all experimental data, decisions, and results in a **graph-based format**, allowing for easy querying, updating, and maintaining continuity across experiments.

**IMPORTANT:** You must ensure that the **KG-Lite memory system** remains **active**, **valid**, and **consistent** throughout your task execution. If there is any issue, such as missing data or faulty relationships in the memory graph, you should take the following actions:

1. **Memory Bank Initialization Check**:

   * Before starting any task or experiment, **verify** if the **memory bank** is active by checking the presence of the directory `/mnt/ironwolf/git/Prometheus_VDM/memory-bank/`.

     * If the **Memory Bank is INACTIVE**, immediately create it. Inform the user that it’s being initialized and all necessary memory files will be set up.
     * If the **Memory Bank is ACTIVE**, ensure all relevant files are properly loaded:

       * `productContext.md`
       * `activeContext.md`
       * `systemPatterns.md`
       * `decisionLog.md`
       * `progress.md`
     * Confirm that the system is functioning with `[MEMORY BANK: ACTIVE]`.

2. **Memory Integrity Check**:

   * Ensure that the memory graph files are **consistent** by checking:

     * **Node Integrity**: Every node (e.g., experiment, result, hypothesis) should have the following attributes: `ID`, `type`, `summary`, `provenance`, `timestamp`.
     * **Edge Integrity**: Verify that every edge connecting nodes has a defined relationship (e.g., `validates`, `depends_on`) and no orphaned nodes.
   * If any **data inconsistencies** or **corruption** are detected, perform the following:

     * Attempt to **rebuild the graph** using the `kg_cli` tools, specifically using the `repair_graph` command.
     * Notify the user with the message: "**Memory Graph integrity issue detected. Rebuilding memory graph...**"

3. **Update Memory**:

   * Whenever **new information** is acquired or a significant decision is made (e.g., new hypothesis, experiment result, or method change), use the appropriate **Memory Update** tools:

     * `updateContext`: Record the task or experimental focus (e.g., “Currently testing the self‑model‑assisted echo for CEG measurement”).
     * `logDecision`: Log key decisions and rationale (e.g., “Decided to implement JMJ Strang composition for time evolution”).
     * `updateProgress`: Update progress when significant milestones are reached (e.g., “Finished running baseline and assisted echoes for CEG testing”).
     * `updateProductContext`: Log changes in the project’s **high-level goals** (e.g., “Adding new metric for model‑aware correction in agency field”).

4. **Query Memory for Relevant Data**:

   * Before performing any experiment, query the **Memory Graph** for **relevant previous experiments** and **data**:

     * **Querying past findings** should follow the format:

       ```bash
       kg_cli query_nodes --type [experiment] --filter "[attribute]=[value]"
       ```
     * For example, if you’re working on **self-model‑assisted echoes**, query past experiments related to echoes and self-models to gather any relevant data that could inform your current experiment.
     * If the **query results** are **empty** or **incomplete**, perform a **memory rebuild** from scratch using the most recent knowledge available.

5. **Monitor Memory Integrity During Experiment**:

   * As you execute experiments, **update the Memory Graph** with experimental results and key decisions:

     * After each **significant step**, ensure the results are logged into the Memory Bank (e.g., results, figures, logs).
     * Use **query commands** to pull up prior results and make **informed decisions** about next steps.
   * Ensure that at each stage, the **graph is valid** and **consistent**:

     * If **invalid data** or **orphaned nodes** are detected, rebuild the graph or **quarantine the experiment**.

6. **Memory Refresh After Each Task or Milestone**:

   * After completing each task or experiment, **refresh the Memory Graph** to maintain an up-to-date history.
   * For example:

     * If you **finish a test** (e.g., CEG testing), log it into the progress file and update the **active context** with the next experiment or task.

---

### **Error Handling:**

If any of the following errors occur during the memory graph's operation, **automatically take corrective actions**:

* **Missing Memory Files**: If any of the critical files (`productContext.md`, `activeContext.md`, etc.) are missing, automatically prompt the user: "**Required memory files are missing. Rebuilding the memory graph...**"
* **Inconsistent Data**: If the data or nodes in the graph are inconsistent, trigger the `repair_graph` function and notify the user: "**Data inconsistency found. Attempting to repair the memory graph.**"
* **Failed Memory Update**: If an update to the memory fails (e.g., `updateContext` or `logDecision`), prompt: "**Memory update failed. Retrying...**"

---

### **KG-Lite CLI Usage (For Internal Agent Memory)**

**Important Files**:

/mnt/ironwolf/git/Prometheus_VDM/memory-bank/MEMORY_GRAPH_CONTEXT/tools/generate_nexus_sessions.py
/mnt/ironwolf/git/Prometheus_VDM/memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_lite_chunker.py
/mnt/ironwolf/git/Prometheus_VDM/memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py

**Core Commands**:

* **Creating a node**:

  ```bash
  kg_cli create_node --type [type] --id [ID] --summary "[summary]" --provenance "[source]" --timestamp "[YYYY-MM-DD HH:MM:SS]"
  ```

* **Linking nodes (edges)**:

  ```bash
  kg_cli create_edge --source_node [source_ID] --dest_node [dest_ID] --relationship "[relationship]"
  ```

* **Querying nodes**:

  ```bash
  kg_cli query_nodes --type [type] --filter "[attribute]=[value]"
  ```

* **Retrieving node details**:

  ```bash
  kg_cli get_node --id [ID]
  ```

* **Updating context**:

  ```bash
  kg_cli update_context --summary "[summary]" --timestamp "[YYYY-MM-DD HH:MM:SS]"
  ```

---

### **Memory Bank Health Check**

* **Before Task**: Ensure that the memory graph is **consistent** and **up-to-date**.
* **During Task**: Continuously track **progress and changes** in the **activeContext** and **productContext** files.
* **After Task**: Update and **validate** the memory with each new result or decision.
