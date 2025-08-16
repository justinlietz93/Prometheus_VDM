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

def create_chunk_xml(chunk_files, master_report, root_dir, notebooklm=False, dt=False, output_filename="", chunk_num=1, total_chunks=1):
    """
    Builds a complete XML report for a single chunk.
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
    parser = argparse.ArgumentParser(description="Code crawler for FUM project.")
    parser.add_argument("--input", required=True, help="Root directory to scan.")
    parser.add_argument("--output", help="Base path for the output report file(s).")
    parser.add_argument("--chunks", type=int, default=1, help="Number of chunks to split the report into.")
    parser.add_argument("--notebooklm", action="store_true", help="Add markdown header for NotebookLM compatibility.")
    parser.add_argument("--dt", action="store_true", help="Add date/time information to the output.")
    parser.add_argument("--mermaid", action="store_true", help="Generate a Mermaid diagram of the file structure.")
    parser.add_argument("--seeignored", action="store_true", help="Include ignored files and directories in the ASCII map.")
    parser.add_argument("--extract-pdfs", action="store_true", help="Extract text from PDFs during analysis.")

    args = parser.parse_args()

    abs_input_dir = os.path.abspath(args.input)

    RESULTS_DIR = "code_crawler_results"
    output_filename_base = os.path.splitext(os.path.basename(args.output or "default"))[0] if args.output else "default"
    output_ext = os.path.splitext(args.output)[1] or '.xml' if args.output else '.xml'
    
    output_dir = os.path.join(RESULTS_DIR, output_filename_base) if args.chunks > 1 else RESULTS_DIR
    os.makedirs(output_dir, exist_ok=True)

    # If --extract-pdfs is set and no --output, run extraction-only mode
    if args.extract_pdfs and not args.output:
        print("Running extraction-only mode for PDFs...")
        extraction_only_walk(args.input, ignore_patterns)  # Call the new function
        print("Extraction complete.")
        return  # Exit without generating reports

    # Otherwise, proceed with full analysis
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
        
        chunk_filename = f"{output_filename_base}_part_{chunk_num}{output_ext}" if args.chunks > 1 else f"{output_filename_base}{output_ext}"
        output_path = os.path.join(output_dir, chunk_filename)
        
        xml_content, chunk_stats = create_chunk_xml(
            chunk_files, master_report, abs_input_dir,
            notebooklm=args.notebooklm, dt=args.dt, output_filename=chunk_filename,
            chunk_num=chunk_num, total_chunks=len(chunk_file_lists)
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