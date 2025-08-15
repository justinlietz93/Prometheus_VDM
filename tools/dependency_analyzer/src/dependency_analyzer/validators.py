import ast
import os
import json
import logging
from .file_parsers import parse_js_file

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.file_path = ""
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({"import": alias.name, "as": alias.asname})
        self.generic_visit(node)
    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.name == '*':
                logging.warning(f"{self.file_path}: Avoid wildcard imports from {node.module}.")
            self.imports.append({"from": node.module, "import": alias.name, "as": alias.asname})
        self.generic_visit(node)

class UsageVisitor(ast.NodeVisitor):
    def __init__(self):
        self.names = set()
        self.attributes = set()
        self.variables = {}
    def visit_Name(self, node):
        self.names.add(node.id)
        self.generic_visit(node)
    def visit_Attribute(self, node):
        full_name = self.get_full_name(node)
        self.attributes.add(full_name)
        self.generic_visit(node)
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            self.attributes.add(self.get_full_name(node.func))
        elif isinstance(node.func, ast.Name):
            self.names.add(node.func.id)
        self.generic_visit(node)
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name) and isinstance(node.value, (ast.Name, ast.Attribute)):
            self.variables[node.targets[0].id] = self.get_full_name(node.value)
        self.generic_visit(node)
    def get_full_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.get_full_name(node.value)}.{node.attr}"
        return ""

def check_file_alignment(file_path, file_details):
    if not os.path.exists(file_path):
        logging.error(f"{file_path}: File does not exist on disk.")
        return

    ext = file_path.lower().split('.')[-1]
    if ext == 'py':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
        except SyntaxError as e:
            logging.error(f"{file_path}: Syntax error: {e}")
            return

        import_visitor = ImportVisitor()
        import_visitor.file_path = file_path
        import_visitor.visit(tree)
        actual_imports = import_visitor.imports

        defined = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                defined.add(node.name)

        usage_visitor = UsageVisitor()
        usage_visitor.visit(tree)
        actual_uses = usage_visitor.names.union(usage_visitor.attributes)
        variable_mappings = usage_visitor.variables

        for exp_imp in file_details.get("imports", []):
            if isinstance(exp_imp, dict):
                imp_key = exp_imp.get("import")
                imp_from = exp_imp.get("from", "")
                imp_as = exp_imp.get("as") or imp_key
                found = any(
                    imp.get("import") == imp_key or
                    (imp.get("from") or "").startswith(imp_from) or
                    imp.get("as") == imp_as
                    for imp in actual_imports
                )
                if not found:
                    logging.warning(f"{file_path}: Potentially missing import {exp_imp} (check aliases or usage).")
        
        for ext in file_details.get("external", []):
            if not any(imp.get("import").startswith(ext) or (imp.get("from") or "").startswith(ext) for imp in actual_imports):
                logging.warning(f"{file_path}: Missing external library {ext} in imports.")

        for prov in file_details.get("provides", []):
            if prov not in defined:
                logging.warning(f"{file_path}: Missing definition for {prov} (may be dynamic or nested).")

        for use in file_details.get("uses", []):
            if '.' in use:
                if use not in actual_uses and not any(use.startswith(var) for var in variable_mappings.values()):
                    logging.warning(f"{file_path}: Missing attribute use {use} (check indirect usage).")
            else:
                if use not in actual_uses and use not in variable_mappings:
                    logging.warning(f"{file_path}: Missing use of {use} (check variable assignments).")

    elif ext == 'js':
        parsed_data = parse_js_file(file_path)
        actual_imports = parsed_data.get("imports", [])
        actual_provides = parsed_data.get("provides", [])

        for exp_imp in file_details.get("imports", []):
            if isinstance(exp_imp, dict):
                imp_key = exp_imp.get("import")
                imp_from = exp_imp.get("from", "")
                imp_as = exp_imp.get("as") or imp_key
                found = any(
                    imp.get("import") == imp_key or
                    (imp.get("from") or "").startswith(imp_from) or
                    imp.get("as") == imp_as
                    for imp in actual_imports
                )
                if not found:
                    logging.warning(f"{file_path}: Potentially missing import {exp_imp} (check aliases or usage).")

        for ext in file_details.get("external", []):
            if not any(imp.get("import", "").startswith(ext) or (imp.get("from") or "").startswith(ext) for imp in actual_imports):
                logging.warning(f"{file_path}: Missing external library {ext} in imports.")

        for prov in file_details.get("provides", []):
            if prov not in actual_provides:
                logging.warning(f"{file_path}: Missing definition for {prov} (may be dynamic or nested).")
