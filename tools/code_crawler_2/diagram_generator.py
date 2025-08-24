# ==============================================================================
# Code Crawler: Mermaid Diagram Generator (`diagram_generator.py`)
# ==============================================================================
#
# This module is responsible for generating a Mermaid syntax diagram that
# represents the file and directory structure of the analyzed project.
#
# HOW IT WORKS:
#   1.  It receives the "master report" dictionary from `__main__.py`, which
#       contains all the file metadata gathered by the analyzer.
#   2.  It builds a nested dictionary (`tree`) that mirrors the actual
#       directory structure of the project.
#   3.  It recursively traverses this tree to calculate aggregate statistics
#       (like total size and item count) for each directory.
#   4.  It performs a second traversal to build the Mermaid script, creating
#       nodes for each file and directory with their respective metadata.
#   5.  The final script is returned to `__main__.py` to be saved to a file.
#
# ==============================================================================

import os

def generate_mermaid_diagram(master_report, root_dir):
    """
    Generates a Mermaid diagram representing the directory structure.

    Args:
        master_report (dict): The master analysis report from the crawler.
        root_dir (str): The root directory of the scan.

    Returns:
        str: The Mermaid diagram script.
    """
    files_metadata = master_report.get('files_metadata', {})
    if not files_metadata:
        return "graph TD\n    A[No files found to diagram.];"

    # 1. Build a nested dictionary representing the file tree
    tree = {}
    for path, meta in files_metadata.items():
        relative_path = os.path.relpath(path, root_dir)
        parts = relative_path.split(os.sep)
        current_level = tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        # Attach metadata to the file node (leaf)
        current_level['_meta'] = meta

    # 2. Recursively calculate stats for each directory
    def calculate_dir_stats(node):
        if '_meta' in node: # It's a file
            return node['_meta'].get('size', 0), 1
        
        total_size = 0
        total_files = 0
        direct_child_count = len(node)

        for child_name, child_node in node.items():
            child_size, child_files = calculate_dir_stats(child_node)
            total_size += child_size
            total_files += child_files
        
        node['_meta'] = {
            'size': total_size,
            'files_in_subtree': total_files,
            'direct_children': direct_child_count
        }
        return total_size, total_files

    calculate_dir_stats(tree)

    # 3. Recursively build the Mermaid script
    mermaid_lines = ["graph TD"]
    
    def build_mermaid_lines(node, parent_id, indent="    "):
        for name, child_node in sorted(node.items()):
            if name == '_meta':
                continue

            node_id = f"{parent_id}_{name.replace('.', '_').replace('-', '_')}"
            meta = child_node.get('_meta', {})
            
            if 'direct_children' in meta: # It's a directory
                label = (
                    f"\"{name}/<br>"
                    f"<i>({meta['direct_children']} items, "
                    f"{meta['size'] / 1024:.2f} KB)</i>\""
                )
                mermaid_lines.append(f"{indent}{parent_id} --> {node_id}[{label}]")
                build_mermaid_lines(child_node, node_id, indent + "    ")
            else: # It's a file
                lang = os.path.splitext(name)[1].lstrip('.') or 'unknown'
                label = (
                    f"\"{name}<br>"
                    f"<i>({meta.get('loc', 0)} LOC, "
                    f"{meta.get('size', 0)} B, {lang})</i>\""
                )
                # Corrected: Removed the invalid empty string from the link
                mermaid_lines.append(f"{indent}{parent_id} --> {node_id}([{label}])")


    project_name = master_report.get('project_name', 'Project Root')
    root_label = f"\"{project_name}/<br><i>({tree['_meta']['direct_children']} items, {tree['_meta']['size'] / 1024:.2f} KB)</i>\""
    mermaid_lines.append(f"    root[{root_label}]")
    build_mermaid_lines(tree, "root")
    
    return "\n".join(mermaid_lines)
