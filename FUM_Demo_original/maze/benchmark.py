# benchmark.py
import json
import time
import numpy as np
from fum_interface import FUM_Solver
# --- Baseline Algorithms (included for completeness) ---
from queue import PriorityQueue

class AStarSolver:
    def solve(self, maze):
        size = maze.shape[0]
        start = (0, 0)
        end = (size - 1, size - 1)
        
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = { (r, c): float('inf') for r in range(size) for c in range(size) }
        g_score[start] = 0
        f_score = { (r, c): float('inf') for r in range(size) for c in range(size) }
        f_score[start] = self._heuristic(start, end)

        while not open_set.empty():
            current = open_set.get()[1]

            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dr, current[1] + dc)
                if 0 <= neighbor[0] < size and 0 <= neighbor[1] < size and maze[neighbor[0], neighbor[1]] == 0:
                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, end)
                        open_set.put((f_score[neighbor], neighbor))
        return None

    def _heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

class QLearningSolver:
    def __init__(self, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.episodes = episodes
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def solve(self, maze):
        size = maze.shape[0]
        self._train(maze)
        
        start_pos = (0, 0)
        end_pos = (size - 1, size -1)
        path = [start_pos]
        current_pos = start_pos
        
        while current_pos != end_pos:
            state = current_pos
            if state not in self.q_table:
                return None # No path learned
                
            action = np.argmax(self.q_table[state])
            
            if action == 0: # Up
                next_pos = (current_pos[0] - 1, current_pos[1])
            elif action == 1: # Down
                next_pos = (current_pos[0] + 1, current_pos[1])
            elif action == 2: # Left
                next_pos = (current_pos[0], current_pos[1] - 1)
            else: # Right
                next_pos = (current_pos[0], current_pos[1] + 1)
            
            path.append(next_pos)
            current_pos = next_pos
            if len(path) > size * size: # Failsafe
                return None
        
        return path

    def _train(self, maze):
        size = maze.shape[0]
        for _ in range(self.episodes):
            pos = (0, 0)
            done = False
            while not done:
                state = pos
                if state not in self.q_table:
                    self.q_table[state] = np.zeros(4)

                if np.random.uniform(0, 1) < self.epsilon:
                    action = np.random.choice(4)
                else:
                    action = np.argmax(self.q_table[state])

                if action == 0: # Up
                    next_pos = (pos[0] - 1, pos[1])
                elif action == 1: # Down
                    next_pos = (pos[0] + 1, pos[1])
                elif action == 2: # Left
                    next_pos = (pos[0], pos[1] - 1)
                else: # Right
                    next_pos = (pos[0], pos[1] + 1)

                if not (0 <= next_pos[0] < size and 0 <= next_pos[1] < size and maze[next_pos[0], next_pos[1]] == 0):
                    reward = -10
                    done = True
                elif next_pos == (size - 1, size - 1):
                    reward = 10
                    done = True
                else:
                    reward = -1
                    done = False

                next_state = next_pos
                if next_state not in self.q_table:
                    self.q_table[next_state] = np.zeros(4)

                old_value = self.q_table[state][action]
                next_max = np.max(self.q_table[next_state])
                
                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state][action] = new_value
                
                pos = next_pos

def generate_maze(size=20):
    """
    Generates a maze using the Recursive Backtracking algorithm.
    The maze will have a single guaranteed path from start to end.
    Walls are 1, paths are 0.
    """
    # Ensure size is odd for the algorithm to work perfectly
    if size % 2 == 0:
        size += 1
        
    maze = np.ones((size, size), dtype=int)
    start_pos = (0, 0)
    
    # Use a stack for the backtracking process
    stack = [start_pos]
    maze[start_pos] = 0
    
    while stack:
        current_cell = stack[-1]
        r, c = current_cell
        
        neighbors = []
        # Check potential neighbors (2 cells away)
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and maze[nr, nc] == 1:
                neighbors.append((nr, nc))
        
        if neighbors:
            next_cell = neighbors[np.random.randint(len(neighbors))]
            nr, nc = next_cell
            
            # Carve path to the neighbor
            maze[nr, nc] = 0
            maze[r + (nr - r) // 2, c + (nc - c) // 2] = 0
            
            stack.append(next_cell)
        else:
            # Backtrack
            stack.pop()
            
    # Ensure start and end points are open
    maze[0, 0] = 0
    maze[size - 1, size - 1] = 0
    
    return maze

def run_benchmark():
    """
    Runs a scaled benchmark for all models across various maze sizes.
    """
    maze_sizes = [10, 20, 30, 40, 50]
    trials_per_size = 3
    results = {}

    for size in maze_sizes:
        size_key = f"{size}x{size}"
        print(f"--- Running Benchmark for Maze Size: {size_key} ---")
        
        # Initialize results structure for this size
        size_results = {
            "FUM": {"success_count": 0, "total_time": 0},
            "A*": {"success_count": 0, "total_time": 0},
            "Q-Learning": {"success_count": 0, "total_time": 0},
        }

        # --- Model Initialization ---
        # FUM is initialized *once per size* to test for cumulative learning.
        # A* and Q-Learning are re-initialized each time as they don't have this property.
        fum_model = FUM_Solver(iterations=500, eta=0.05, gamma=0.9)

        for i in range(trials_per_size):
            print(f"  Trial {i+1}/{trials_per_size}...")
            maze = generate_maze(size)

            # A* and Q-Learning are stateless for this benchmark's purpose
            astar_model = AStarSolver()
            qlearning_model = QLearningSolver(episodes=max(2000, size * 100))

            models = {
                "FUM": fum_model, "A*": astar_model, "Q-Learning": qlearning_model
            }
            
            for name, model in models.items():
                start_time = time.time()
                # FUM learns across trials, others are fresh.
                path = model.solve(maze.copy())
                end_time = time.time()
                
                size_results[name]["total_time"] += (end_time - start_time)
                if path:
                    size_results[name]["success_count"] += 1

        # Calculate averages for this size
        for name in models:
            total_time = size_results[name]["total_time"]
            success_count = size_results[name]["success_count"]
            size_results[name]["avg_time"] = total_time / trials_per_size if trials_per_size > 0 else 0
            size_results[name]["success_rate"] = success_count / trials_per_size if trials_per_size > 0 else 0
            # Remove raw counters for cleaner JSON output
            del size_results[name]["total_time"]
            del size_results[name]["success_count"]

        results[size_key] = size_results

    # Save the final results to a file
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("\nBenchmark complete. Results saved to results.json")

if __name__ == "__main__":
    run_benchmark()