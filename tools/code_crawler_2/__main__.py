# Updated __main__.py to make --output optional and add extraction-only mode

# ==============================================================================
# Code Crawler: Main Execution (`__main__.py`)
# ==============================================================================
#
# This script is the primary entry point for the Code Crawler utility. It is
# designed to be run as a module from the project root using:
#
#   python -m code_crawler --input . --output <report_name>
#
# It orchestrates the entire process:
#   1.  Parses command-line arguments.
#   2.  Sets up the output directory structure.
#   3.  Calls the analyzer to build a master report IN MEMORY.
#   4.  Plans chunks from the in-memory report.
#   5.  Generates the final XML report(s) and other artifacts.
#
# ==============================================================================

import os
import argparse
import time
import xml.dom.minidom as minidom
from collections import defaultdict
from datetime import datetime

# Use explicit relative imports to ensure this works as a module
from .analyzer import analyze_directory, format_size, extraction_only_walk  # NEW: Import the new extraction function
from .config import ignore_patterns
from .diagram_generator import generate_mermaid_diagram

def get_file_content(path):
    """Safely reads the content of a file."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def plan_chunks(files_metadata, num_chunks, root_dir):
    """
    Intelligently plans the distribution of files into a specific number of chunks,
    now with sequential ordering.
    """
    file_paths = list(files_metadata.keys())
    if not file_paths or num_chunks <= 0:
        return []
    if num_chunks == 1:
        return [file_paths]
    
    files_by_dir = defaultdict(list)
    for path in file_paths:
        relative_path = os.path.relpath(path, root_dir)
        path_parts = relative_path.split(os.sep)
        top_level = path_parts[0] if len(path_parts) > 0 else '<root>'
        files_by_dir[top_level].append(path)
    
    for key in files_by_dir:
        files_by_dir[key].sort()

    # --- START: MODIFIED LOGIC ---
    # Create a list of (directory_name, files) tuples
    # Then, sort this list alphabetically by directory name.
    # This is the key change to ensure sequential processing.
    sorted_dir_groups = sorted(files_by_dir.items())
    
    # Flatten this into a single list of all files, now in the correct directory order
    all_files_sorted = []
    for _, files in sorted_dir_groups:
        all_files_sorted.extend(files)
    
    # Distribute the sequentially sorted files into chunks
    chunks = [[] for _ in range(num_chunks)]
    files_per_chunk = -(-len(all_files_sorted) // num_chunks) # Ceiling division
    
    for i in range(num_chunks):
        start = i * files_per_chunk
        end = start + files_per_chunk
        chunks[i] = all_files_sorted[start:end]
    # --- END: MODIFIED LOGIC ---
        
    return [chunk for chunk in chunks if chunk]

def create_chunk_xml(
    chunk_files,
    master_report,
    root_dir,
    notebooklm=False,
    dt=False,
    output_filename="",
    chunk_num=1,
    total_chunks=1,
    diff_contents=None,
):
    """
    Builds a complete XML report for a single chunk. If `diff_contents` is provided,
    the content of each file will be replaced by its diff-marked version from
    `diff_contents` (keyed by absolute file path). Otherwise, the actual file
    contents are read from disk.

    Args:
        chunk_files (list[str]): List of absolute file paths for this chunk.
        master_report (dict): The report containing file metadata and ascii map.
        root_dir (str): The absolute root directory for relative path resolution.
        notebooklm (bool): If True, include NotebookLM headers (unused here).
        dt (bool): If True, include a timestamp at the top of the XML.
        output_filename (str): Name of the output file (used for root element name).
        chunk_num (int): Sequence number of this chunk (1-indexed).
        total_chunks (int): Total number of chunks being generated.
        diff_contents (dict[str,str]|None): Optional mapping of file paths to
            precomputed diff-marked content strings. When provided, the content
            of each file will be taken from this dictionary instead of reading
            from disk.

    Returns:
        tuple[str, dict]: The serialized XML string and statistics about the
        chunk (number of files and total LOC).
    """
    doc = minidom.Document()
    root_name = os.path.splitext(os.path.basename(output_filename))[0]
    sanitized_root_name = ''.join(c for c in root_name if c.isalnum() or c in '_-').rstrip('_-')
    if not sanitized_root_name or not sanitized_root_name[0].isalpha() and sanitized_root_name[0] != '_':
        sanitized_root_name = "code_report"
    root_element = doc.createElement(sanitized_root_name)
    doc.appendChild(root_element)

    # Add date/time if requested
    if dt:
        dt_elem = doc.createElement("generated_on")
        dt_elem.appendChild(doc.createTextNode(datetime.now().isoformat()))
        root_element.appendChild(dt_elem)

    # Add ASCII map
    ascii_map_elem = doc.createElement("ascii_map")
    root_element.appendChild(ascii_map_elem)
    
    ascii_map_data = master_report.get('ascii_map_data', [])
    for line, path in ascii_map_data:
        if path is None:  # Metadata line
            meta_elem = doc.createElement("metadata")
            meta_elem.appendChild(doc.createTextNode(line.strip()))
            ascii_map_elem.appendChild(meta_elem)
        else:
            file_elem = doc.createElement("file")
            file_elem.setAttribute("path", path)
            file_elem.appendChild(doc.createTextNode(line))
            ascii_map_elem.appendChild(file_elem)

    # Add global stats
    global_stats = master_report.get('global_stats', {})
    stats_elem = doc.createElement("global_stats")
    for key, value in global_stats.items():
        stat_elem = doc.createElement(key)
        stat_elem.appendChild(doc.createTextNode(str(value)))
        stats_elem.appendChild(stat_elem)
    root_element.appendChild(stats_elem)

    # Add files
    files_elem = doc.createElement("files")
    root_element.appendChild(files_elem)

    chunk_files_count = 0
    chunk_loc = 0
    for file_path in chunk_files:
        meta = master_report['files_metadata'].get(file_path, {})
        size = meta.get('size', 0)
        loc = meta.get('loc', 0)
        chunk_files_count += 1
        chunk_loc += loc

        file_elem = doc.createElement("file")
        file_elem.setAttribute("path", file_path)
        
        size_elem = doc.createElement("size")
        size_elem.appendChild(doc.createTextNode(format_size(size)))
        file_elem.appendChild(size_elem)

        loc_elem = doc.createElement("loc")
        loc_elem.appendChild(doc.createTextNode(str(loc)))
        file_elem.appendChild(loc_elem)

        # If diff_contents provided and the file path is present, use the
        # diff-marked content. Otherwise read the actual file contents.
        if diff_contents and file_path in diff_contents:
            content = diff_contents[file_path]
        else:
            content = get_file_content(file_path)
        content_elem = doc.createElement("content")
        cdata = doc.createCDATASection(content)
        content_elem.appendChild(cdata)
        file_elem.appendChild(content_elem)
        
        files_elem.appendChild(file_elem)

    # Return both the XML and stats for the chunk
    xml_content = doc.toxml(encoding='utf-8').decode('utf-8')
    chunk_stats = {'files': chunk_files_count, 'loc': chunk_loc}
    
    return xml_content, chunk_stats

def main():
    """
    Entry point for the code crawler command line utility. This function now supports
    three primary modes of operation:

    1. **Extraction-only Mode:** When `--extract-pdfs` is specified without `--diff`, the
       crawler will scan the given directory (via `--input` or `--new`) and extract text
       from all PDF files, writing `.txt` files next to them. No code crawl or report
       generation occurs in this mode.

    2. **Diff Mode:** When `--diff` is provided, along with paths to the new and old
       directories (`--new` or `--input` for the new version, and `--old` for the old),
       the crawler compares corresponding files between the two directories. The output
       includes diff markers (`+`, `-`, and `===`) in the file contents to indicate
       additions, deletions, and unchanged lines, respectively. Only files present in
       the new directory are included in the diff report; files that exist only in the
       old directory are omitted.

    3. **Standard Analysis Mode:** If neither extraction-only nor diff mode is invoked,
       the crawler performs its normal analysis on the directory specified by
       `--input`, generating XML reports (optionally chunked and timestamped) and
       optional Mermaid diagrams.

    Returns:
        None. Prints status messages and writes report files to disk.
    """

    parser = argparse.ArgumentParser(
        description="Code crawler for FUM project with optional diff mode."
    )
    # Primary arguments
    parser.add_argument("--input", help="Root directory to scan (used for normal and extraction modes).")
    parser.add_argument("--output", help="Base path for the output report file(s).")
    parser.add_argument("--chunks", type=int, default=1, help="Number of chunks to split the report into.")
    parser.add_argument("--notebooklm", action="store_true", help="Add markdown header for NotebookLM compatibility.")
    parser.add_argument("--dt", action="store_true", help="Add date/time information to the output.")
    parser.add_argument("--mermaid", action="store_true", help="Generate a Mermaid diagram of the file structure.")
    parser.add_argument("--seeignored", action="store_true", help="Include ignored files and directories in the ASCII map.")
    parser.add_argument(
        "--extract-pdfs",
        action="store_true",
        help=(
            "Extract text from PDFs; when used alone (without --diff) this runs"
            " extraction-only and no report is generated."
        ),
    )

    # Diff-specific arguments
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Enable diff mode: compare --new (or --input) and --old directories and include diff markers in extracted content.",
    )
    parser.add_argument(
        "--new",
        help="Path to the new version directory. Defaults to --input if provided in diff mode.",
    )
    parser.add_argument(
        "--old",
        help="Path to the old version directory for comparison in diff mode.",
    )

    args = parser.parse_args()

    # -------------------------------------------------------------------------------------------------
    # Extraction-only mode
    # If the user specifies --extract-pdfs without diff, perform only PDF text extraction
    # on the provided directory and skip report generation entirely.  Prefer --input,
    # otherwise fall back to --new if present.  If neither is provided, emit an error.
    if args.extract_pdfs and not args.diff:
        target_dir = args.input or args.new
        if not target_dir:
            print("Error: You must specify --input or --new when using --extract-pdfs in extraction-only mode.")
            return
        print("Running extraction-only mode for PDFs...")
        extraction_only_walk(target_dir, ignore_patterns)
        print("Extraction complete.")
        return

    # -------------------------------------------------------------------------------------------------
    # Diff mode handling
    if args.diff:
        # Validate diff arguments
        new_dir = args.new or args.input
        old_dir = args.old
        if not new_dir or not old_dir:
            print("Error: --diff requires both --new (or --input) and --old directories.")
            return
        new_dir_abs = os.path.abspath(new_dir)
        old_dir_abs = os.path.abspath(old_dir)

        # Analyze both directories
        print("Step 1: Analyzing new directory...")
        new_report = analyze_directory(new_dir_abs, ignore_patterns, see_ignored=args.seeignored, extract_pdfs=args.extract_pdfs)
        print("Step 2: Analyzing old directory...")
        # For the old directory we do not extract PDFs unless explicitly requested via extract_pdfs
        old_report = analyze_directory(old_dir_abs, ignore_patterns, see_ignored=False, extract_pdfs=False)

        # Compute diff contents for files present in the new report
        import difflib
        diff_contents = {}
        for new_path in new_report['files_metadata'].keys():
            # Determine corresponding old path based on relative location
            rel_path = os.path.relpath(new_path, new_dir_abs)
            old_path = os.path.join(old_dir_abs, rel_path)
            # Read new file lines
            try:
                with open(new_path, 'r', encoding='utf-8', errors='ignore') as nf:
                    new_lines = nf.readlines()
            except Exception:
                new_lines = []
            # Read old file lines if it exists
            if os.path.exists(old_path):
                try:
                    with open(old_path, 'r', encoding='utf-8', errors='ignore') as of:
                        old_lines = of.readlines()
                except Exception:
                    old_lines = []
            else:
                old_lines = []
            # Generate line-by-line diff using difflib.ndiff
            diff_lines = difflib.ndiff(old_lines, new_lines)
            diff_text_lines = []
            for line in diff_lines:
                # Skip detailed hints starting with '? '
                if line.startswith('  '):
                    marker = '=== '
                    content = line[2:]
                elif line.startswith('+ '):
                    marker = '+ '
                    content = line[2:]
                elif line.startswith('- '):
                    marker = '- '
                    content = line[2:]
                else:
                    continue
                diff_text_lines.append(marker + content)
            diff_contents[new_path] = ''.join(diff_text_lines)

        # Use new report's file list for chunk planning
        abs_new_dir = new_dir_abs
        RESULTS_DIR = "code_crawler_results"
        # Determine base output name for diff reports
        if args.output:
            output_filename_base = os.path.splitext(os.path.basename(args.output))[0]
            output_ext = os.path.splitext(args.output)[1] or '.xml'
        else:
            output_filename_base = "diff_report"
            output_ext = '.xml'
        output_dir = os.path.join(RESULTS_DIR, output_filename_base) if args.chunks > 1 else RESULTS_DIR
        os.makedirs(output_dir, exist_ok=True)

        # Plan chunks
        print("\nStep 3: Planning chunks for diff report...")
        chunk_file_lists = plan_chunks(new_report['files_metadata'], args.chunks, abs_new_dir)
        print(f"Planned {len(chunk_file_lists)} chunks.")

        final_report_stats = []
        for i, chunk_files in enumerate(chunk_file_lists):
            start_time = time.time()
            chunk_num = i + 1
            print(f"\nStep 4: Building diff chunk {chunk_num} of {len(chunk_file_lists)}...")
            chunk_filename = (
                f"{output_filename_base}_part_{chunk_num}{output_ext}" if args.chunks > 1 else f"{output_filename_base}{output_ext}"
            )
            output_path = os.path.join(output_dir, chunk_filename)
            xml_content, chunk_stats = create_chunk_xml(
                chunk_files,
                new_report,
                abs_new_dir,
                notebooklm=args.notebooklm,
                dt=args.dt,
                output_filename=chunk_filename,
                chunk_num=chunk_num,
                total_chunks=len(chunk_file_lists),
                diff_contents=diff_contents,
            )
            with open(output_path, "w", encoding='utf-8') as f:
                f.write(xml_content)
            duration = time.time() - start_time
            final_report_stats.append({'path': output_path, 'files': chunk_stats['files'], 'loc': chunk_stats['loc'], 'duration': duration})
            print(f"Successfully created diff report: {output_path} (took {duration:.2f}s)")

        # Generate Mermaid diagram for diff mode, if requested, using the new report structure
        if args.mermaid:
            print("\nStep 5: Generating Mermaid diagram for diff...")
            mermaid_script = generate_mermaid_diagram(new_report, abs_new_dir)
            diagram_filename = f"{output_filename_base}_diagram.md"
            diagram_path = os.path.join(output_dir, diagram_filename)
            with open(diagram_path, "w", encoding='utf-8') as f:
                f.write("```mermaid\n")
                f.write(mermaid_script)
                f.write("\n```")
            print(f"Successfully created Mermaid diagram: {diagram_path}")
            final_report_stats.append({'path': diagram_path})

        print("\n--- DIFF CRAWL COMPLETE: FINAL REPORT ---")
        for stats in final_report_stats:
            if 'duration' in stats:
                print(f"  - Report: {stats['path']}")
                print(f"    Files:  {stats['files']}")
                print(f"    LOC:    {stats['loc']}")
            else:
                print(f"  - Diagram: {stats['path']}")
        print("------------------------------------------")
        return

    # -------------------------------------------------------------------------------------------------
    # Normal analysis mode (no diff)
    if not args.input:
        print("Error: --input is required unless --diff is specified with --new.")
        return
    abs_input_dir = os.path.abspath(args.input)
    RESULTS_DIR = "code_crawler_results"
    # Determine output file base name and extension
    if args.output:
        output_filename_base = os.path.splitext(os.path.basename(args.output))[0]
        output_ext = os.path.splitext(args.output)[1] or '.xml'
    else:
        output_filename_base = "default"
        output_ext = '.xml'
    output_dir = os.path.join(RESULTS_DIR, output_filename_base) if args.chunks > 1 else RESULTS_DIR
    os.makedirs(output_dir, exist_ok=True)

    # Perform analysis
    print("Step 1: Analyzing directory...")
    master_report = analyze_directory(args.input, ignore_patterns, see_ignored=args.seeignored, extract_pdfs=args.extract_pdfs)
    print("\nStep 2: Planning chunks...")
    chunk_file_lists = plan_chunks(master_report['files_metadata'], args.chunks, abs_input_dir)
    print(f"Planned {len(chunk_file_lists)} chunks.")

    final_report_stats = []
    for i, chunk_files in enumerate(chunk_file_lists):
        start_time = time.time()
        chunk_num = i + 1
        print(f"\nStep 3: Building chunk {chunk_num} of {len(chunk_file_lists)}...")
        chunk_filename = (
            f"{output_filename_base}_part_{chunk_num}{output_ext}" if args.chunks > 1 else f"{output_filename_base}{output_ext}"
        )
        output_path = os.path.join(output_dir, chunk_filename)
        xml_content, chunk_stats = create_chunk_xml(
            chunk_files,
            master_report,
            abs_input_dir,
            notebooklm=args.notebooklm,
            dt=args.dt,
            output_filename=chunk_filename,
            chunk_num=chunk_num,
            total_chunks=len(chunk_file_lists),
        )
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(xml_content)
        duration = time.time() - start_time
        final_report_stats.append({'path': output_path, 'files': chunk_stats['files'], 'loc': chunk_stats['loc'], 'duration': duration})
        print(f"Successfully created report: {output_path} (took {duration:.2f}s)")

    if args.mermaid:
        print("\nStep 4: Generating Mermaid diagram...")
        mermaid_script = generate_mermaid_diagram(master_report, abs_input_dir)
        diagram_filename = f"{output_filename_base}_diagram.md"
        diagram_path = os.path.join(output_dir, diagram_filename)
        with open(diagram_path, "w", encoding='utf-8') as f:
            f.write("```mermaid\n")
            f.write(mermaid_script)
            f.write("\n```")
        print(f"Successfully created Mermaid diagram: {diagram_path}")
        final_report_stats.append({'path': diagram_path})

    print("\n--- CRAWL COMPLETE: FINAL REPORT ---")
    for stats in final_report_stats:
        if 'duration' in stats:
            print(f"  - Report: {stats['path']}")
            print(f"    Files:  {stats['files']}")
            print(f"    LOC:    {stats['loc']}")
        else:
            print(f"  - Diagram: {stats['path']}")
    print("------------------------------------")

if __name__ == "__main__":
    main()