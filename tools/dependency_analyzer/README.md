# Dependency Analyzer

A standalone tool that analyzes dependencies in your codebase, updates live as files change, and runs as a background process.

## Setup
1. Download the executable from the releases page (e.g., dependency-analyzer.exe).
2. Run: `dependency-analyzer <project_root> [--verbose] [--background]`

## Features
- Parses Python, JavaScript/TypeScript/JSX, and HTML files.
- Generates `dependency_map.json`, `dependency_metadata.csv`, and logs in `dependency_tracking/`.
- Updates dependency headers in source files in real-time.
- Runs as a background process with live monitoring.

## Building from Source
1. Install Python dependencies: `pip install -r requirements.txt`
2. Add Node.js: Download Node.js (e.g., v20.17.0) and extract to `dependency_analyzer/nodejs`, then run `nodejs/npm install @babel/parser`.
3. Bundle: `pyinstaller --add-data "src/dependency_analyzer/scripts;dependency_analyzer/scripts" --add-data "nodejs;nodejs" --onefile src/dependency_analyzer/cli.py -n dependency-analyzer`
4. Run: `dist/dependency-analyzer <project_root> --verbose`

## Usage
- Foreground: `dependency-analyzer /path/to/codebase --verbose`
- Background: `dependency-analyzer /path/to/codebase --background`
