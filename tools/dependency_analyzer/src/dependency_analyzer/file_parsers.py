import ast
import os
import subprocess
import json
import logging

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

def parse_python_file(file_path):
    if not file_path.lower().endswith('.py'):
        return {"provides": [], "imports": [], "uses": [], "external": [], "description": "Non-Python file"}
    if not os.path.exists(file_path):
        logging.warning(f"File does not exist for parsing: {file_path}")
        return {"provides": [], "imports": [], "uses": [], "external": [], "description": "File not found"}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except SyntaxError as e:
        logging.warning(f"Syntax error in {file_path}: {e}")
        return {"provides": [], "imports": [], "uses": [], "external": [], "description": f"Syntax error: {e}"}
    
    from .config import STANDARD_LIB
    imports = []
    uses = set()
    external = set()
    provides = set()
    imported_names = {}
    is_test_file = False
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            provides.add(node.name)
            if any(isinstance(base, ast.Name) and base.id == 'TestCase' for base in node.bases):
                is_test_file = True
        elif isinstance(node, ast.FunctionDef):
            provides.add(node.name)
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in ('get', 'post', 'put', 'delete'):
                        if isinstance(decorator.func.value, ast.Name) and decorator.func.value.id == 'app':
                            uses.add(node.name)
        if isinstance(node, ast.Import):
            for name in node.names:
                alias = name.asname or name.name
                imported_names[alias] = name.name
                imports.append({"import": name.name, "as": name.asname})
                if name.name.split('.')[0] not in STANDARD_LIB:
                    external.add(name.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for name in node.names:
                alias = name.asname or name.name
                full_name = f"{module}.{name.name}" if module else name.name
                imported_names[alias] = full_name
                imports.append({"from": module, "import": name.name, "as": name.asname})
                if module.split('.')[0] not in STANDARD_LIB:
                    external.add(module.split('.')[0])
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if node.func.value.id in imported_names:
                    uses.add(f"{imported_names[node.func.value.id]}.{node.func.attr}")
            elif isinstance(node.func, ast.Name) and node.func.id in imported_names:
                uses.add(imported_names[node.func.id])
    
    if is_test_file:
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test'):
                uses.add(node.name)
    
    description = next((n.value.s.strip() for n in tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Str)), 
                       f"Handles {os.path.basename(file_path).split('.')[0]} in {os.path.basename(os.path.dirname(file_path))} module.")
    return {"provides": list(provides), "imports": imports, "uses": list(uses), "external": list(external), "description": description}

def parse_js_file(file_path):
    if not os.path.exists(file_path):
        logging.warning(f"File does not exist for parsing: {file_path}")
        return {"provides": [], "imports": [], "requires": [], "uses": [], "external": [], "description": "File not found"}
    try:
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'parse_js.js')
        node_path = os.path.join(os.path.dirname(__file__), '..', 'nodejs', 'node.exe' if os.name == 'nt' else 'node')
        if not os.path.exists(script_path) or not os.path.exists(node_path):
            logging.error(f"Missing script {script_path} or Node.js {node_path}")
            return {"provides": [], "imports": [], "requires": [], "uses": [], "external": [], "description": "Node.js setup incomplete"}
        cmd = [node_path, script_path, file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        error_output = result.stderr.strip()
        if error_output:
            logging.error(f"Error parsing {file_path} with Node.js: {error_output}")
            try:
                return json.loads(error_output)
            except json.JSONDecodeError:
                return {"provides": [], "imports": [], "requires": [], "uses": [], "external": [], "description": f"Parse error: {error_output}"}
        return json.loads(output)
    except Exception as e:
        logging.error(f"Unexpected error parsing {file_path}: {e}")
        return {"provides": [], "imports": [], "requires": [], "uses": [], "external": [], "description": f"Parse error: {str(e)}"}

def parse_html_file(file_path):
    if not os.path.exists(file_path):
        logging.warning(f"File does not exist for parsing: {file_path}")
        return {"provides": [], "imports": [], "requires": [], "external": [], "description": "File not found"}
    try:
        if not BeautifulSoup:
            logging.warning(f"Skipping {file_path}: BeautifulSoup not installed.")
            return {"provides": [], "imports": [], "requires": [], "external": [], "description": "HTML parsing skipped"}
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        scripts = [tag['src'] for tag in soup.find_all('script') if tag.get('src')]
        return {"provides": [], "imports": scripts, "requires": [], "external": scripts, 
                "description": f"HTML entry for {os.path.basename(file_path).split('.')[0]}"}
    except Exception as e:
        logging.warning(f"Error parsing {file_path}: {e}")
        return {"provides": [], "imports": [], "requires": [], "external": [], "description": "Parse error"}
