import os
import json
import uuid
import re
import logging
from .utils import list_files_in_directory

def generate_file_key():
    return f"header_key_{uuid.uuid4().hex}"

def load_or_create_header_keys(project_root):
    dependency_tracking_dir = os.path.join(project_root, 'dependency_tracking')
    if not os.path.exists(dependency_tracking_dir):
        os.makedirs(dependency_tracking_dir)
    keys_file = os.path.join(dependency_tracking_dir, 'header_keys.json')
    return json.load(open(keys_file, 'r', encoding='utf-8')) if os.path.exists(keys_file) else {}

def save_header_keys(project_root, header_keys):
    dependency_tracking_dir = os.path.join(project_root, 'dependency_tracking')
    with open(os.path.join(dependency_tracking_dir, 'header_keys.json'), 'w', encoding='utf-8') as f:
        json.dump(header_keys, f, indent=4)

def format_dependencies(file_details):
    lines = []
    if file_details.get("imports"):
        lines.append("Imports:")
        imports = file_details["imports"]
        if imports and isinstance(imports[0], dict):
            for imp in imports:
                if "from" in imp:
                    lines.append(f"  - from {imp['from']} import {imp['import']} as {imp['as'] or imp['import']}")
                else:
                    lines.append(f"  - import {imp['import']} as {imp['as'] or imp['import']}")
        else:
            lines.extend(f"  - {imp}" for imp in imports)
    if file_details.get("uses"):
        lines.append("Uses:")
        lines.extend(f"  - {use}" for use in file_details["uses"])
    if file_details.get("external"):
        lines.append("External Dependencies:")
        lines.extend(f"  - {ext}" for ext in file_details["external"])
    return "\n".join(lines) or "No dependencies found."

def get_comment_syntax(file_path):
    ext = file_path.lower().split('.')[-1]
    return {
        'py': (', '),
        'js': ('/**', '*/'),
        'html': ('<!--', '-->')
    }.get(ext, (None, None))

def remove_existing_headers(full_content, file_key, start_comment, end_comment):
    pattern = (
        f"{re.escape(start_comment)}\s*\n"
        f"#\s{re.escape(file_key)}_start\s*\n"
        f"(?:#.*\n)*?"
        f"#\s{re.escape(file_key)}_end\s*\n"
        f"{re.escape(end_comment)}\s*\n?"
    )
    matches = list(re.finditer(pattern, full_content, re.MULTILINE))
    if not matches:
        return full_content
    new_content = full_content
    for match in reversed(matches):
        new_content = new_content[:match.start()] + new_content[match.end():]
    return new_content

def add_or_update_header(file_path, rel_path, file_details, header_keys):
    start_comment, end_comment = get_comment_syntax(file_path)
    if not start_comment:
        logging.warning(f"Skipping {rel_path}: Unsupported file type.")
        return
    file_key = header_keys.setdefault(rel_path, generate_file_key())
    deps = format_dependencies(file_details)
    header = [
        f"{start_comment}\n",
        f"# {file_key}_start\n",
        "#\n",
        f"# File: {rel_path}\n",
        "# Dependencies:\n",
    ] + [f"# {line}\n" for line in deps.split('\n')] + [
        "#\n",
        f"# {file_key}_end\n",
        f"{end_comment}\n"
    ]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = remove_existing_headers(content, file_key, start_comment, end_comment)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(''.join(header) + content)
        logging.debug(f"Updated header in {rel_path}")
    except Exception as e:
        logging.error(f"Error updating {file_path}: {e}")

def find_dependency_map(project_root):
    dependency_tracking_dir = os.path.join(project_root, 'dependency_tracking')
    map_path = os.path.join(dependency_tracking_dir, 'dependency_map.json')
    return map_path if os.path.exists(map_path) else None

def process_files(project_root, dependency_map_path=None):
    dependency_map_path = dependency_map_path or find_dependency_map(project_root)
    if not dependency_map_path:
        logging.error(f"No dependency_map.json found in {project_root}.")
        return
    try:
        with open(dependency_map_path, 'r', encoding='utf-8') as f:
            dependency_map = json.load(f)
    except Exception as e:
        logging.error(f"Error loading {dependency_map_path}: {e}")
        return
    
    header_keys = load_or_create_header_keys(project_root)
    processed_files = set()
    all_files = set(list_files_in_directory(project_root))
    
    for rel_path, file_details in dependency_map.get("files", {}).items():
        file_path = os.path.normpath(os.path.join(project_root, rel_path.replace('/', os.sep)))
        norm_rel_path = os.path.relpath(file_path, project_root).replace(os.sep, '/')
        if norm_rel_path in processed_files:
            logging.warning(f"Skipping duplicate entry for {norm_rel_path} in dependency map.")
            continue
        processed_files.add(norm_rel_path)
        if os.path.exists(file_path):
            add_or_update_header(file_path, norm_rel_path, file_details, header_keys)
    
    save_header_keys(project_root, header_keys)
