#!/usr/bin/env python3
"""
Architectural Analysis Script for Prometheus_VDM
Extracts import graph, dependency matrix, cycles, metrics.
"""
import ast
import os
import sys
import json
import csv
from pathlib import Path
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

REPO_ROOT = Path(__file__).parent.parent
VDM_RT = REPO_ROOT / "vdm_rt"
THIRD_PARTY = REPO_ROOT / "third_party"

class ImportAnalyzer:
    def __init__(self):
        self.module_imports: Dict[str, Set[str]] = defaultdict(set)
        self.all_modules: Set[str] = set()
        self.external_deps: Set[str] = set()
        
    def analyze_file(self, filepath: Path, module_name: str):
        """Extract imports from a Python file."""
        self.all_modules.add(module_name)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(filepath))
        except Exception as e:
            print(f"Error parsing {filepath}: {e}", file=sys.stderr)
            return
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._add_import(module_name, alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self._add_import(module_name, node.module)
    
    def _add_import(self, from_module: str, to_module: str):
        """Add an import edge, categorizing internal vs external."""
        # Normalize
        if to_module.startswith('.'):
            # Relative import - resolve
            return
        
        # Check if internal vdm_rt module
        if to_module.startswith('vdm_rt'):
            self.module_imports[from_module].add(to_module)
        elif '.' in to_module:
            base = to_module.split('.')[0]
            if base not in sys.stdlib_module_names:
                self.external_deps.add(base)
        else:
            if to_module not in sys.stdlib_module_names:
                self.external_deps.add(to_module)
    
    def find_cycles(self) -> List[List[str]]:
        """Find strongly connected components (cycles) using Tarjan's algorithm."""
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = defaultdict(bool)
        sccs = []
        
        def strongconnect(node):
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            on_stack[node] = True
            stack.append(node)
            
            for successor in self.module_imports.get(node, []):
                if successor not in index:
                    strongconnect(successor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[successor])
                elif on_stack[successor]:
                    lowlinks[node] = min(lowlinks[node], index[successor])
            
            if lowlinks[node] == index[node]:
                component = []
                while True:
                    successor = stack.pop()
                    on_stack[successor] = False
                    component.append(successor)
                    if successor == node:
                        break
                if len(component) > 1:
                    sccs.append(component)
        
        for node in self.all_modules:
            if node not in index:
                strongconnect(node)
        
        return sccs
    
    def build_package_graph(self) -> Dict[str, Set[str]]:
        """Aggregate module graph to package-level."""
        pkg_graph = defaultdict(set)
        
        for from_mod, to_mods in self.module_imports.items():
            from_pkg = self._get_package(from_mod)
            for to_mod in to_mods:
                to_pkg = self._get_package(to_mod)
                if from_pkg != to_pkg:
                    pkg_graph[from_pkg].add(to_pkg)
        
        return dict(pkg_graph)
    
    def _get_package(self, module: str) -> str:
        """Extract top-level package from module name."""
        parts = module.split('.')
        if len(parts) >= 2:
            return f"{parts[0]}.{parts[1]}"  # e.g., vdm_rt.core
        return module
    
    def compute_metrics(self) -> Dict[str, Dict]:
        """Compute fan-in, fan-out, instability for each module."""
        fan_in = defaultdict(int)
        fan_out = defaultdict(int)
        
        for from_mod, to_mods in self.module_imports.items():
            fan_out[from_mod] = len(to_mods)
            for to_mod in to_mods:
                fan_in[to_mod] += 1
        
        metrics = {}
        for mod in self.all_modules:
            fi = fan_in[mod]
            fo = fan_out[mod]
            instability = fo / (fi + fo) if (fi + fo) > 0 else 0
            metrics[mod] = {
                'fan_in': fi,
                'fan_out': fo,
                'instability': round(instability, 3)
            }
        
        return metrics


def scan_vdm_rt():
    """Scan vdm_rt package."""
    analyzer = ImportAnalyzer()
    
    for py_file in VDM_RT.rglob("*.py"):
        if "third_party" in py_file.parts:
            continue
        if "__pycache__" in py_file.parts:
            continue
        
        rel_path = py_file.relative_to(REPO_ROOT)
        module_name = str(rel_path).replace('/', '.').replace('.py', '')
        analyzer.analyze_file(py_file, module_name)
    
    return analyzer


def export_dependency_graph_dot(analyzer: ImportAnalyzer, output_path: Path):
    """Export Graphviz DOT file."""
    pkg_graph = analyzer.build_package_graph()
    
    with open(output_path, 'w') as f:
        f.write('digraph VDM_Dependencies {\n')
        f.write('  rankdir=LR;\n')
        f.write('  node [shape=box, style=rounded];\n\n')
        
        # Nodes
        all_pkgs = set(pkg_graph.keys())
        for dests in pkg_graph.values():
            all_pkgs.update(dests)
        
        for pkg in sorted(all_pkgs):
            label = pkg.replace('vdm_rt.', '')
            f.write(f'  "{pkg}" [label="{label}"];\n')
        
        f.write('\n')
        
        # Edges
        for from_pkg, to_pkgs in sorted(pkg_graph.items()):
            for to_pkg in sorted(to_pkgs):
                f.write(f'  "{from_pkg}" -> "{to_pkg}";\n')
        
        f.write('}\n')


def export_dependency_matrix_csv(analyzer: ImportAnalyzer, output_path: Path):
    """Export adjacency matrix as CSV."""
    pkg_graph = analyzer.build_package_graph()
    
    all_pkgs = sorted(set(pkg_graph.keys()) | 
                     {p for dests in pkg_graph.values() for p in dests})
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        header = [''] + all_pkgs
        writer.writerow(header)
        
        for from_pkg in all_pkgs:
            row = [from_pkg]
            for to_pkg in all_pkgs:
                if to_pkg in pkg_graph.get(from_pkg, set()):
                    row.append('1')
                else:
                    row.append('0')
            writer.writerow(row)


def export_metrics_json(analyzer: ImportAnalyzer, output_path: Path):
    """Export metrics and analysis results."""
    metrics = analyzer.compute_metrics()
    cycles = analyzer.find_cycles()
    pkg_graph = analyzer.build_package_graph()
    
    data = {
        'module_metrics': metrics,
        'cycles': cycles,
        'package_dependencies': {k: list(v) for k, v in pkg_graph.items()},
        'external_dependencies': sorted(list(analyzer.external_deps)),
        'module_count': len(analyzer.all_modules),
        'total_edges': sum(len(v) for v in analyzer.module_imports.values())
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    print("Analyzing vdm_rt package structure...")
    analyzer = scan_vdm_rt()
    
    output_dir = REPO_ROOT / "docs" / "architecture"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Found {len(analyzer.all_modules)} modules")
    print(f"Found {len(analyzer.external_deps)} external dependencies")
    
    cycles = analyzer.find_cycles()
    print(f"Found {len(cycles)} cycles")
    
    # Export
    export_dependency_graph_dot(analyzer, output_dir / "05_dependency_graph.dot")
    export_dependency_matrix_csv(analyzer, output_dir / "06_dependency_matrix.csv")
    export_metrics_json(analyzer, output_dir / "arch_metrics.json")
    
    print(f"Exported to {output_dir}")
    
    # Print summary
    if cycles:
        print("\nCycles detected:")
        for i, cycle in enumerate(cycles, 1):
            print(f"  {i}. {' -> '.join(cycle[:3])}{'...' if len(cycle) > 3 else ''}")


if __name__ == '__main__':
    main()
