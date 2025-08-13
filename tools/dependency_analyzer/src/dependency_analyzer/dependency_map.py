import os
import json
import csv
import logging
from .config import FILE_PARSERS, DEPENDENCY_TRACKING_DIR
from .utils import load_gitignore, should_ignore
from .validators import check_file_alignment

def build_dependency_map(root_dir, output_path=None):
    logging.info(f"Building dependency map for {root_dir}...")
    spec = load_gitignore(root_dir)
    dependency_map = {"files": {}, "inter_component_dependencies": []}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d), root_dir, spec)]
        for filename in [f for f in filenames if not should_ignore(os.path.join(dirpath, f), root_dir, spec)]:
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root_dir).replace(os.sep, '/')
            ext = os.path.splitext(filename)[1].lower()
            if ext in FILE_PARSERS:
                dependency_map["files"][rel_path] = FILE_PARSERS[ext](file_path)
    
    dependency_map["inter_component_dependencies"] = [
        {"from": "frontend", "to": "backend", "via": "HTTP API calls", "endpoints": []}
    ]
    
    dependency_tracking_dir = os.path.join(root_dir, DEPENDENCY_TRACKING_DIR)
    if not os.path.exists(dependency_tracking_dir):
        os.makedirs(dependency_tracking_dir)
    output_path = output_path or os.path.join(dependency_tracking_dir, 'dependency_map.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dependency_map, f, indent=4, ensure_ascii=False)
    logging.info(f"Dependency map saved to {output_path}")
    return output_path

def scan_dependencies(dependency_map_path, codebase_root, log_file, tracking_handler):
    logging.info(f"Scanning dependencies with map at {dependency_map_path}...")
    try:
        with open(dependency_map_path, 'r', encoding='utf-8') as f:
            dependency_map = json.load(f)
    except Exception as e:
        logging.error(f"Error loading {dependency_map_path}: {e}")
        return

    provides_lookup = {}
    for rel_path, file_details in dependency_map.get("files", {}).items():
        file_path = os.path.normpath(os.path.join(codebase_root, rel_path.replace('/', os.sep)))
        module_name = rel_path.replace('/', '.')[:-3]
        for provided in file_details.get("provides", []):
            provides_lookup[f"{module_name}.{provided}"] = rel_path

    reference_counts = {}
    for rel_path, file_details in dependency_map.get("files", {}).items():
        module_name = rel_path.replace('/', '.')[:-3]
        for prov in file_details.get("provides", []):
            full_item = f"{module_name}.{prov}"
            reference_counts[full_item] = {"count": 0, "locations": []}

    for rel_path, file_details in dependency_map.get("files", {}).items():
        module_name = rel_path.replace('/', '.')[:-3]
        for use in file_details.get("uses", []):
            full_use = f"{module_name}.{use}"
            if full_use in reference_counts:
                reference_counts[full_use]["count"] += 1
                reference_counts[full_use]["locations"].append(rel_path)
        for imp in file_details.get("imports", []):
            if isinstance(imp, dict) and imp.get("from"):
                full_import = f"{imp['from'].replace('/', '.')}.{imp['import']}"
                if full_import in reference_counts:
                    reference_counts[full_import]["count"] += 1
                    reference_counts[full_import]["locations"].append(rel_path)

    dependency_tracking_dir = os.path.join(codebase_root, DEPENDENCY_TRACKING_DIR)
    if not os.path.exists(dependency_tracking_dir):
        os.makedirs(dependency_tracking_dir)
    csv_path = os.path.join(dependency_tracking_dir, 'dependency_metadata.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['full_item', 'count', 'locations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for full_item, info in reference_counts.items():
            writer.writerow({'full_item': full_item, 'count': info["count"], 'locations': ', '.join(info["locations"])})
    logging.info(f"Dependency metadata saved to {csv_path}")

    for rel_path, file_details in dependency_map.get("files", {}).items():
        file_path = os.path.normpath(os.path.join(codebase_root, rel_path.replace('/', os.sep)))
        if os.path.exists(file_path):
            check_file_alignment(file_path, file_details)

    if not tracking_handler.has_issues():
        logging.info("All dependencies aligned and integrated across files with no unused definitions")
    logging.info(f"Scan completed. Log at {log_file}")
