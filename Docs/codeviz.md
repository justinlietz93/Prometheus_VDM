graph TD

    10["User<br>External Actor"]
    11["External LLM APIs<br>API"]
    subgraph 1["Tooling System<br>Python/TypeScript"]
        34["Code Crawlers<br>Python"]
        35["Dependency Analyzer<br>Python"]
        36["Python Utilities Generator<br>TypeScript/React"]
    end
    subgraph 2["Derivation &amp; Proofs System<br>Python/Markdown/PDF"]
        31["Computational Proofs<br>Python"]
        32["Claims &amp; Papers<br>PDF"]
        33["Theoretical Derivations<br>Markdown"]
    end
    subgraph 3["FUM Demo System<br>Python"]
        28["Main Demo Script<br>Python"]
        29["FUM Core Logic (Demo)<br>Python"]
        30["Advanced Math (Demo)<br>Python"]
        %% Edges at this level (grouped by source)
        28["Main Demo Script<br>Python"] -->|orchestrates| 29["FUM Core Logic (Demo)<br>Python"]
        28["Main Demo Script<br>Python"] -->|uses| 30["Advanced Math (Demo)<br>Python"]
    end
    subgraph 4["FUM Runtime System<br>Python"]
        12["Core Engine<br>Python"]
        13["Substrate<br>Python"]
        14["Runtime Loop<br>Python"]
        15["CLI<br>Python"]
        16["Data Management<br>Python"]
        subgraph 5["Physics &amp; Advanced Math<br>Python"]
            25["Memory Steering<br>Python"]
            26["Dynamical Systems<br>Python"]
            27["Void Dynamics<br>Python"]
        end
        subgraph 6["Frontend<br>Flask/Dash"]
            23["Callbacks<br>Python"]
            24["Components<br>Python"]
            %% Edges at this level (grouped by source)
            6["Frontend<br>Flask/Dash"] -->|uses| 23["Callbacks<br>Python"]
            6["Frontend<br>Flask/Dash"] -->|uses| 24["Components<br>Python"]
        end
        subgraph 7["API/LLM Integration<br>Python"]
            22["LLM Providers<br>Python"]
            %% Edges at this level (grouped by source)
            7["API/LLM Integration<br>Python"] -->|routes to| 22["LLM Providers<br>Python"]
        end
        subgraph 8["I/O System<br>Python"]
            19["Sensors<br>Python"]
            20["Actuators<br>Python"]
            21["Visualization<br>Python/Websockets"]
        end
        subgraph 9["Cortex<br>Python"]
            17["Maps<br>Python"]
            18["Void Walkers (Scouts)<br>Python"]
            %% Edges at this level (grouped by source)
            9["Cortex<br>Python"] -->|uses| 17["Maps<br>Python"]
            9["Cortex<br>Python"] -->|dispatches| 18["Void Walkers (Scouts)<br>Python"]
        end
        %% Edges at this level (grouped by source)
        15["CLI<br>Python"] -->|configures| 4["FUM Runtime System<br>Python"]
        8["I/O System<br>Python"] -->|visualizes| 6["Frontend<br>Flask/Dash"]
        8["I/O System<br>Python"] -->|provides data to| 12["Core Engine<br>Python"]
        6["Frontend<br>Flask/Dash"] -->|communicates via| 8["I/O System<br>Python"]
        12["Core Engine<br>Python"] -->|manages| 9["Cortex<br>Python"]
        12["Core Engine<br>Python"] -->|manages| 13["Substrate<br>Python"]
        12["Core Engine<br>Python"] -->|orchestrates| 14["Runtime Loop<br>Python"]
        16["Data Management<br>Python"] -->|provides data to| 9["Cortex<br>Python"]
        16["Data Management<br>Python"] -->|provides data to| 12["Core Engine<br>Python"]
        16["Data Management<br>Python"] -->|provides data to| 13["Substrate<br>Python"]
        5["Physics &amp; Advanced Math<br>Python"] -->|provides models to| 12["Core Engine<br>Python"]
        5["Physics &amp; Advanced Math<br>Python"] -->|provides models to| 13["Substrate<br>Python"]
        14["Runtime Loop<br>Python"] -->|drives| 12["Core Engine<br>Python"]
    end
    %% Edges at this level (grouped by source)
    10["User<br>External Actor"] -->|uses| 1["Tooling System<br>Python/TypeScript"]
    10["User<br>External Actor"] -->|interacts with| 3["FUM Demo System<br>Python"]
    10["User<br>External Actor"] -->|interacts with| 4["FUM Runtime System<br>Python"]
    3["FUM Demo System<br>Python"] -->|based on| 2["Derivation &amp; Proofs System<br>Python/Markdown/PDF"]
    4["FUM Runtime System<br>Python"] -->|leverages| 2["Derivation &amp; Proofs System<br>Python/Markdown/PDF"]
    7["API/LLM Integration<br>Python"] -->|connects to| 11["External LLM APIs<br>API"]
    36["Python Utilities Generator<br>TypeScript/React"] -->|uses| 11["External LLM APIs<br>API"]
