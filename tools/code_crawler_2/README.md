# Code Crawler Utility

## 1. Overview

Code Crawler is a powerful, project-agnostic command-line utility designed to help developers and AI agents understand and visualize complex codebases. It scans a directory, analyzes its contents, and generates detailed reports in various formats. Its key features include:

- **Comprehensive Analysis:** Gathers metadata on every file, including size, lines of code (LOC), and language.
- **Intelligent Chunking:** Automatically divides large codebases into smaller, more manageable XML reports for easier processing by large language models.
- **Visual Diagrams:** Generates interactive Mermaid diagrams that provide a clear, hierarchical view of the project's structure.
- **Customizable ignore patterns:** Easily exclude unnecessary files and directories (like `.git`, `__pycache__`, or `node_modules`) to keep reports clean and focused.
- **Flexible Output:** Supports various output formats and naming conventions to suit different workflows.

This tool is designed to be run as a Python module from the root of your project, ensuring that all paths and ignore patterns are handled consistently and reliably.

## 2. How to Run

Because this tool is a proper Python module, you should run it from the **root directory** of the project you want to analyze.

### Basic Command

```bash
python -m code_crawler --input . --output MyProjectReport.xml
```

- `python -m code_crawler`: This tells Python to run the `code_crawler` module.
- `--input .`: Specifies that the analysis should start from the current directory (the project root).
- `--output MyProjectReport.xml`: Sets the base name for the generated report file(s).

### Command-Line Flags & Examples

You can customize the crawler's behavior with the following flags.

-   `--input <path>` **(Required)**
    Specifies the root directory to scan.
    *Example:* `--input .` to scan the current directory.

-   `--output <filename.ext>` (Optional)
    Sets the base name for the output report file(s).
    *Example:* `--output MyProject.xml`

-   `--chunks <number>` (Optional)
    Splits the report into a specified number of smaller files. This is useful for very large projects that might exceed the context window of an LLM. When used, this creates a subdirectory named after your output file to store the chunked parts.
    *Example:* `--chunks 4` will create four report files (`MyProject_part_1.xml`, `MyProject_part_2.xml`, etc.) inside a `MyProject` folder.

-   `--mermaid` (Optional)
    In addition to the XML report, this generates a `.md` file containing a Mermaid diagram that visualizes the entire file and directory structure.
    *Example:* Using this flag will create `MyProject_diagram.md`.

-   `--notebooklm` (Optional)
    Adds a special markdown header (e.g., `# MyProject_part_1 of 4`) to the top of each report file. This is a compatibility feature for easy import into Google's NotebookLM.

-   `--dt` (Optional)
    Adds a timestamp to the generated report(s), either in the XML metadata or in the NotebookLM header, to indicate when the crawl was performed.

## 3. Output Structure

All reports and diagrams are saved in a new directory named `code_crawler_results/`, which is created in your project root.

- **Single Report (chunks=1):** If you don't specify chunking, a single XML report will be created.
  - `code_crawler_results/MyProjectReport.xml`

- **Multiple Chunks (chunks > 1):** If you request multiple chunks, a subdirectory is created to keep them organized.
  - `code_crawler_results/MyProjectReport/MyProjectReport_part_1.xml`
  - `code_crawler_results/MyProjectReport/MyProjectReport_part_2.xml`
  - `...`

- **Mermaid Diagram:** If you use the `--mermaid` flag, a markdown file containing the diagram is always created in the main results directory.
  - `code_crawler_results/MyProjectReport_diagram.md`

## 4. How to Configure Ignore Patterns

To prevent the crawler from analyzing certain files or directories, edit the `ignore_patterns` list in `code_crawler/config.py`.

The patterns are simple glob-style strings and are matched from the project root.

**Examples:**
```python
# code_crawler/config.py

ignore_patterns = [
    # Ignores all files with the .log extension
    '*.log',

    # Ignores the entire 'node_modules' directory
    'node_modules/*',

    # Ignores a specific nested directory
    'src/assets/legacy/*',
]
```
