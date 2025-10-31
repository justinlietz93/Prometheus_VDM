"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a proprietary license. Use requires written
permission from Justin K. Lietz. See LICENSE file for full terms.

Knowledge Graph Analysis - TDA Validation Runner
"""

import os
import sys
import analyze_kg_topology

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create results directory if it doesn't exist
results_dir = os.path.join(current_dir, "../results")
os.makedirs(results_dir, exist_ok=True)

# Run analysis
print("Running TDA Knowledge Graph analysis...")
results_data, summary_data = analyze_kg_topology.run_analysis(
    snapshot_dir=analyze_kg_topology.SNAPSHOT_DIR,
    pattern=analyze_kg_topology.SNAPSHOT_PATTERN,
    weight_threshold=analyze_kg_topology.WEIGHT_THRESHOLD,
    maxdim=analyze_kg_topology.MAX_DIM_HOMOLOGY
)

# Save results to file
if results_data and summary_data:
    output_file = os.path.join(results_dir, "tda_analysis_results.txt")
    with open(output_file, 'w') as f:
        f.write("# TDA KNOWLEDGE GRAPH ANALYSIS RESULTS\n\n")
        
        # Write correlation results
        f.write("## Correlation Results\n\n")
        if 'corr_m1_eff' in summary_data:
            r = summary_data['corr_m1_eff']['r']
            p = summary_data['corr_m1_eff']['p']
            f.write(f"- M1 (Total B1 Persistence) vs Efficiency Score: r={r:.4f}, p={p:.4g}\n")
        
        if 'corr_m2_path' in summary_data:
            r = summary_data['corr_m2_path']['r']
            p = summary_data['corr_m2_path']['p']
            f.write(f"- M2 (Persistent B0 Count) vs Pathology Score: r={r:.4f}, p={p:.4g}\n")
            
        if 'corr_comp_path' in summary_data:
            r = summary_data['corr_comp_path']['r']
            p = summary_data['corr_comp_path']['p']
            f.write(f"- Component Count vs Pathology Score: r={r:.4f}, p={p:.4g}\n")
        
        f.write("\n## Detailed Results\n\n")
        f.write("| Snapshot | M1 (B1 Persistence) | M2 (B0 Count) | Component Count | Efficiency | Pathology |\n")
        f.write("|----------|---------------------|---------------|-----------------|------------|----------|\n")
        
        for i, result in enumerate(results_data):
            m1 = result['m1_total_b1_persistence']
            m2 = result['m2_persistent_b0_count']
            cc = result['component_count']
            eff = result['efficiency_score']
            path = result['pathology_score']
            f.write(f"| {i:02d} | {m1:.2f} | {m2} | {cc} | {eff:.4f} | {path:.4f} |\n")
        
        f.write("\n## Computation Time (seconds)\n\n")
        if 'avg_times' in summary_data:
            times = summary_data['avg_times']
            for key, val in times.items():
                f.write(f"- {key}: {val:.6f}\n")
        
else:
    print("Analysis failed. No results to save.")
