import os
import sys
import logging
import pathspec

class TrackingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.warning_or_higher_count = 0

    def emit(self, record):
        if record.levelno >= logging.WARNING:
            self.warning_or_higher_count += 1

    def has_issues(self):
        return self.warning_or_higher_count > 0

def setup_logging(log_file_path, verbose=False):
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = logging.FileHandler(log_file_path, encoding='utf-8', mode='w')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_level = logging.DEBUG if verbose else logging.INFO
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    tracking_handler = TrackingHandler()
    tracking_handler.setLevel(logging.WARNING)
    root_logger.addHandler(tracking_handler)

    root_logger.setLevel(logging.DEBUG)
    logging.debug(f"Logging configured. Log file: {log_file_path}")
    return log_file_path, tracking_handler

def load_gitignore(root_dir):
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = ['node_modules/']
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            patterns.extend([p.strip() for p in f.readlines() if p.strip() and not p.startswith('#')])
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)

def should_ignore(path, root_dir, spec):
    if not spec:
        return False
    rel_path = os.path.relpath(path, root_dir).replace(os.sep, '/')
    return spec.match_file(rel_path) or 'node_modules' in rel_path.split('/')

def list_files_in_directory(directory):
    supported_extensions = ('.py', '.js', '.html')
    found_files = []
    spec = load_gitignore(directory)
    for dirpath, dirnames, filenames in os.walk(directory):
        dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d), directory, spec)]
        for filename in filenames:
            if filename.lower().endswith(supported_extensions):
                file_path = os.path.join(dirpath, filename)
                if should_ignore(file_path, directory, spec):
                    continue
                rel_path = os.path.relpath(file_path, directory).replace(os.sep, '/')
                found_files.append(rel_path)
    return found_files
