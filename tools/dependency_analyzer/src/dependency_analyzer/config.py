"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import os
from .file_parsers import parse_python_file, parse_js_file, parse_html_file

# Standard library modules to exclude from external dependencies
STANDARD_LIB = {
    'os', 'sys', 'json', 'ast', 'pathlib', 're', 'time', 'datetime', 'logging', 
    'sqlite3', 'fastapi', 'uvicorn', 'unittest'
}

# File parsers by extension
FILE_PARSERS = {
    '.py': parse_python_file,
    '.js': parse_js_file,
    '.html': parse_html_file
}

# Default output directory
DEPENDENCY_TRACKING_DIR = 'dependency_tracking'
