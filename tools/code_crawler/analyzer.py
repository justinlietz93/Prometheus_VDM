# ==============================================================================
# Code Crawler: File Analyzer (`analyzer.py`)
# ==============================================================================
#
# This module contains the core logic for analyzing a directory. It is
# responsible for:
#   1.  Walking the directory tree from a given root path.
#   2.  Applying the ignore patterns defined in `config.py` to filter out
#       unwanted files and directories.
#   3.  Gathering metadata for each valid file (size, lines of code, language).
#   4.  Calculating global statistics for the entire project.
#   5.  Generating a simple ASCII representation of the directory structure.
#
# The primary function, `analyze_directory`, returns a "master report"
# dictionary that contains all this information. This report is then used by
# `__main__.py` to plan chunks and generate the final XML output.
#
# ==============================================================================

import os
import fnmatch
import json # Using JSON for the temporary file for simplicity and readability

def find_project_root(start_path):
    """Walks up from start_path to find the project root (contains .git)."""
    path = os.path.abspath(start_path)
    while True:
        if os.path.isdir(os.path.join(path, '.git')):
            return path
        parent = os.path.dirname(path)
        if parent == path:  # Reached the filesystem root (e.g., 'C:\')
            return os.path.abspath(start_path)
        path = parent

def get_loc(file_path):
    """Calculates the lines of code (LOC) for a given file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string."""
    if size_bytes is None: return ""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    kb = size_bytes / 1024
    if kb < 1024:
        return f"{kb:.1f} KB"
    mb = kb / 1024
    if mb < 1024:
        return f"{mb:.1f} MB"
    gb = mb / 1024
    return f"{gb:.1f} GB"

def is_ignored(path, project_root, ignore_patterns):
    """
    Checks if a given path should be ignored, using .gitignore-style logic
    relative to a fixed project root.
    """
    relative_path_from_project_root = os.path.relpath(path, project_root)
    if relative_path_from_project_root == '.':
        return False

    is_dir = os.path.isdir(path)
    normalized_path = relative_path_from_project_root.replace(os.sep, '/')
    if is_dir and not normalized_path.endswith('/'):
        normalized_path += '/'

    for pattern in ignore_patterns:
        pattern = pattern.strip()
        if not pattern or pattern.startswith('#'):
            continue

        if pattern.endswith('/'):
            if fnmatch.fnmatch(normalized_path, pattern + '*'):
                return True
        elif '/' in pattern:
            if fnmatch.fnmatch(normalized_path, pattern):
                return True
        else:
            if fnmatch.fnmatch(os.path.basename(normalized_path.strip('/')), pattern):
                return True
            if is_dir and any(fnmatch.fnmatch(part, pattern) for part in normalized_path.strip('/').split('/')):
                return True

    return False

def analyze_directory(root_dir, ignore_patterns, see_ignored=False):
    """
    Analyzes a directory, gathers file metadata, and generates a correct
    ASCII tree representation.
    """
    abs_root_dir = os.path.abspath(root_dir)
    project_name = os.path.basename(abs_root_dir)
    report = {
        'project_name': project_name,
        'files_metadata': {},
        'ascii_map_data': [], # KEY CHANGE: This will now hold tuples of (line, path)
        'global_stats': {'total_files': 0, 'total_size': 0, 'total_loc': 0}
    }

    project_root = find_project_root(abs_root_dir)
    print(f"Project root identified for ignore patterns: {project_root}")

    tree = {}
    original_dir_struct = {} 
    
    for dirpath, dirnames, filenames in os.walk(abs_root_dir, topdown=True):
        rel_path = os.path.relpath(dirpath, abs_root_dir)
        parts = rel_path.split(os.sep) if rel_path != '.' else []

        if see_ignored:
            current_level_orig = original_dir_struct
            for part in parts:
                current_level_orig = current_level_orig.setdefault(part, {})
            for d in sorted(dirnames):
                current_level_orig.setdefault(d, {})
            for f in sorted(filenames):
                current_level_orig[f] = None

        dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(dirpath, d), project_root, ignore_patterns)]

        current_level = tree
        for part in parts:
            current_level = current_level.setdefault(part, {})

        for filename in sorted(filenames):
            full_path = os.path.join(dirpath, filename)
            if not is_ignored(full_path, project_root, ignore_patterns):
                try:
                    size = os.path.getsize(full_path)
                    loc = get_loc(full_path)
                    report['global_stats']['total_files'] += 1
                    report['global_stats']['total_size'] += size
                    report['global_stats']['total_loc'] += loc
                    report['files_metadata'][full_path] = {'size': size, 'loc': loc}
                    current_level[filename] = {'size': size, 'loc': loc}
                except OSError:
                    current_level[filename] = {'size': 0, 'loc': 0, 'error': 'access denied'}
        
        for dirname in sorted(dirnames):
            current_level.setdefault(dirname, {})

    final_tree = original_dir_struct if see_ignored else tree
    
    # This helper function now returns a list of (line, path) tuples
    def _format_tree(node, current_path, prefix="", is_root=True):
        line_path_tuples = []
        if is_root:
            line_path_tuples.append((f"{project_name}/", abs_root_dir))
            
        entries = sorted(node.keys())
        for i, name in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            
            full_path = os.path.join(current_path, name)
            content = node[name]
            is_dir = isinstance(content, dict) and 'size' not in content

            line_str = f"{prefix}{connector}{name}"

            if is_dir:
                line_path_tuples.append((f"{line_str}/", full_path))
                new_prefix = prefix + ("    " if is_last else "│   ")
                line_path_tuples.extend(_format_tree(content, full_path, new_prefix, is_root=False))
            
            else: 
                line_path_tuples.append((line_str, full_path))
                
                file_meta = report['files_metadata'].get(full_path, {})
                loc = file_meta.get('loc', 0)
                size = file_meta.get('size', 0)
                info_str = f"(LOC: {loc}, Size: {format_size(size)})"

                new_prefix = prefix + ("    " if is_last else "│   ")
                line_path_tuples.append((f"{new_prefix}{info_str}", None)) # Metadata line has no associated path

        return line_path_tuples

    report['ascii_map_data'] = _format_tree(final_tree, abs_root_dir)
    
    return report