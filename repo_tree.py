"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import os
from pathlib import Path


def should_ignore(name: str) -> bool:
    """Check if a file or directory should be ignored (hidden files starting with dot)."""
    return name.startswith('.')


def get_tree_structure(directory: Path, prefix: str = "", is_last: bool = True) -> list[str]:
    """
    Recursively generate ASCII tree structure for a directory.
    
    Args:
        directory: Path object representing the directory to traverse
        prefix: String prefix for proper indentation
        is_last: Boolean indicating if this is the last item in current level
        
    Returns:
        List of strings representing the tree structure
    """
    lines = []
    
    try:
        # Get all entries in the directory (both files and subdirectories)
        entries = sorted([e for e in directory.iterdir() if not should_ignore(e.name)])
    except PermissionError:
        # Skip directories we don't have permission to read
        return lines
    
    # Separate directories and files for better organization
    dirs = [e for e in entries if e.is_dir()]
    files = [e for e in entries if e.is_file()]
    
    # Combine them: directories first, then files
    all_entries = dirs + files
    
    for idx, entry in enumerate(all_entries):
        is_last_entry = (idx == len(all_entries) - 1)
        
        # Choose the appropriate connector
        connector = "└── " if is_last_entry else "├── "
        
        # Add directory indicator
        entry_name = f"{entry.name}/" if entry.is_dir() else entry.name
        
        # Add the current entry
        lines.append(f"{prefix}{connector}{entry_name}")
        
        # If it's a directory, recurse into it
        if entry.is_dir():
            # Update prefix for children
            extension = "    " if is_last_entry else "│   "
            lines.extend(get_tree_structure(entry, prefix + extension, is_last_entry))
    
    return lines


def print_tree(root_path: str = ".") -> None:
    """
    Print the complete directory tree starting from root_path.
    
    Args:
        root_path: Path to the root directory (default is current directory)
    """
    root = Path(root_path).resolve()
    
    if not root.exists():
        print(f"Error: Path '{root_path}' does not exist")
        return
    
    if not root.is_dir():
        print(f"Error: Path '{root_path}' is not a directory")
        return
    
    # Print the root directory name
    print(f"{root.name}/")
    
    # Generate and print the tree
    tree_lines = get_tree_structure(root)
    for line in tree_lines:
        print(line)


def main() -> None:
    """Main entry point for the script."""
    print_tree(".")


if __name__ == "__main__":
    main()
