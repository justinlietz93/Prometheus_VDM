import json
import matplotlib.pyplot as plt
import numpy as np

def analyze_results():
    """
    Loads benchmark results from results.json, analyzes the data,
    and generates plots to visualize the performance of the algorithms.
    """
    try:
        with open('results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("Error: results.json not found. Please run the benchmark first.")
        return

    sizes = list(results.keys())
    size_labels = [s.split('x')[0] for s in sizes] # Extract numeric size for x-axis

    fum_times, astar_times, qlearning_times = [], [], []
    fum_rates, astar_rates, qlearning_rates = [], [], []

    for size in sizes:
        fum_times.append(results[size]['FUM']['avg_time'])
        astar_times.append(results[size]['A*']['avg_time'])
        qlearning_times.append(results[size]['Q-Learning']['avg_time'])
        
        fum_rates.append(results[size]['FUM']['success_rate'])
        astar_rates.append(results[size]['A*']['success_rate'])
        qlearning_rates.append(results[size]['Q-Learning']['success_rate'])

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Algorithm Performance Benchmark', fontsize=16)

    # Plot 1: Average Solve Time
    ax1.plot(size_labels, fum_times, 'o-', label='FUM Solver')
    ax1.plot(size_labels, astar_times, 's-', label='A* Solver')
    ax1.plot(size_labels, qlearning_times, '^-', label='Q-Learning Solver')
    ax1.set_xlabel('Maze Size (N x N)')
    ax1.set_ylabel('Average Solve Time (seconds)')
    ax1.set_title('Scalability: Solve Time vs. Maze Size')
    ax1.legend()
    ax1.grid(True)
    # Use a logarithmic scale for time if the differences are very large
    if max(fum_times) / min(astar_times + [1e-9]) > 100:
        ax1.set_yscale('log')
        ax1.set_ylabel('Average Solve Time (log scale)')


    # Plot 2: Success Rate
    ax2.plot(size_labels, fum_rates, 'o-', label='FUM Solver')
    ax2.plot(size_labels, astar_rates, 's-', label='A* Solver')
    ax2.plot(size_labels, qlearning_rates, '^-', label='Q-Learning Solver')
    ax2.set_xlabel('Maze Size (N x N)')
    ax2.set_ylabel('Success Rate')
    ax2.set_title('Reliability: Success Rate vs. Maze Size')
    ax2.set_ylim(0, 1.1)
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the figure
    output_filename = 'benchmark_analysis.png'
    plt.savefig(output_filename)
    print(f"Analysis complete. Plot saved to {output_filename}")

if __name__ == "__main__":
    analyze_results()