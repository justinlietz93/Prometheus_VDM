import argparse
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .utils import setup_logging
from .dependency_map import build_dependency_map, scan_dependencies
from .header_manager import process_files

class CodebaseWatcher(FileSystemEventHandler):
    def __init__(self, project_root, map_output, log_file, tracking_handler):
        self.project_root = project_root
        self.map_output = map_output
        self.log_file = log_file
        self.tracking_handler = tracking_handler

    def on_any_event(self, event):
        if not event.is_directory:
            print(f"Change detected: {event.src_path}")
            map_path = build_dependency_map(self.project_root, self.map_output)
            scan_dependencies(map_path, self.project_root, self.log_file, self.tracking_handler)
            process_files(self.project_root, map_path)

def main():
    parser = argparse.ArgumentParser(description="Live dependency analyzer.")
    parser.add_argument("project_root", help="Project root directory")
    parser.add_argument("--map-output", help="Dependency map output path", default=None)
    parser.add_argument("--log-output", help="Full path to the dependency scan log file", default=None)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--background", action="store_true", help="Run in background")
    args = parser.parse_args()

    project_root = os.path.abspath(args.project_root)
    if not os.path.exists(project_root):
        print(f"Error: Project root {project_root} does not exist.")
        sys.exit(1)

    dependency_tracking_dir = os.path.join(project_root, 'dependency_tracking')
    log_file_path = args.log_output or os.path.join(dependency_tracking_dir, "dependency_scan.log")
    log_file, tracking_handler = setup_logging(log_file_path, args.verbose)

    print("Initializing Dependency Analyzer...")
    map_path = build_dependency_map(project_root, args.map_output)
    scan_dependencies(map_path, project_root, log_file, tracking_handler)
    process_files(project_root, map_path)

    if args.background:
        print(f"Running in background, logging to {log_file_path}...")
    else:
        print(f"Watching {project_root} for changes...")

    event_handler = CodebaseWatcher(project_root, args.map_output, log_file, tracking_handler)
    observer = Observer()
    observer.schedule(event_handler, project_root, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped watching.")
    observer.join()

if __name__ == "__main__":
    main()
