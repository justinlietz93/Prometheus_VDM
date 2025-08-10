import os
import argparse
import tempfile
import time
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict
from datetime import datetime

# Imports from our rewritten analyzer
from analyzer import analyze_directory, save_analysis, load_analysis
from config import ignore_patterns

def get_file_content(path):
    """Safely reads the content of a file."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def plan_chunks(files_metadata, num_chunks, root_dir):
    """
    Intelligently plans the distribution of files into a specific number of chunks.
    It prioritizes creating the correct number of chunks while keeping files from
    the same directory together where possible. Large directories are automatically
    subdivided and distributed.
    """
    file_paths = list(files_metadata.keys())
    if not file_paths or num_chunks <= 0:
        return []
    if num_chunks == 1:
        return [file_paths]
    
    # 1. Group files by their top-level directory
    files_by_dir = defaultdict(list)
    for path in file_paths:
        relative_path = os.path.relpath(path, root_dir)
        path_parts = relative_path.split(os.sep)
        top_level = path_parts[0] if len(path_parts) > 1 else '<root>'
        files_by_dir[top_level].append(path)
    
    # Sort files within each directory to ensure deterministic order
    for key in files_by_dir:
        files_by_dir[key].sort()

    # 2. Identify "mega" directories and subdivide them
    total_files = len(file_paths)
    avg_chunk_size = total_files / num_chunks
    
    distributable_groups = []
    # Sort directories by name for deterministic processing
    for dirname, files in sorted(files_by_dir.items()):
        
        # If a directory is larger than the average, split it.
        # The 1.5* multiplier is a heuristic to avoid splitting directories that are only slightly larger.
        if len(files) > avg_chunk_size * 1.5:
            num_splits = round(len(files) / avg_chunk_size)
            split_size = -(-len(files) // num_splits) # Ceiling division
            for i in range(0, len(files), split_size):
                distributable_groups.append(files[i:i + split_size])
        else:
            distributable_groups.append(files)
            
    # 3. Distribute the groups into the final chunks
    chunks = [[] for _ in range(num_chunks)]
    # Sort groups by size (desc) to place largest groups first, leading to a better-balanced result
    distributable_groups.sort(key=len, reverse=True)
    
    for group in distributable_groups:
        # Always add the next group to the chunk that is currently the smallest
        smallest_chunk = min(chunks, key=len)
        smallest_chunk.extend(group)
        
    # Filter out any empty chunks, though this is less likely with the new logic
    return [chunk for chunk in chunks if chunk]

def create_chunk_xml(chunk_files, master_report, root_dir, notebooklm=False, dt=False, output_filename="", chunk_num=1, total_chunks=1):
    """
    Builds a complete XML report for a single chunk using the minidom library
    to correctly handle CDATA sections.
    """
    doc = minidom.Document()
    root_element = doc.createElement("fum_code_report")
    doc.appendChild(root_element)

    # Helper function to create text-containing elements
    def create_text_element(parent, name, text):
        elem = doc.createElement(name)
        elem.appendChild(doc.createTextNode(str(text)))
        parent.appendChild(elem)

    # --- Add Date/Time as first XML element if requested (only when notebooklm is NOT used) ---
    if dt and not notebooklm:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_text_element(root_element, "generated_timestamp", current_datetime)

    # --- 1. Add Metadata ---
    metadata_element = doc.createElement("metadata")
    root_element.appendChild(metadata_element)
    
    # Global stats for the entire project
    global_stats = master_report['global_stats']
    global_elem = doc.createElement("global_stats")
    metadata_element.appendChild(global_elem)
    create_text_element(global_elem, "total_files", global_stats.get('total_files', 0))
    create_text_element(global_elem, "total_size_bytes", global_stats.get('total_size', 0))
    create_text_element(global_elem, "total_loc", global_stats.get('total_loc', 0))
    
    # Stats for this specific chunk
    chunk_stats = {'files': len(chunk_files), 'size': 0, 'loc': 0}
    for f_path in chunk_files:
        stats = master_report['files_metadata'].get(f_path, {})
        chunk_stats['size'] += stats.get('size', 0)
        chunk_stats['loc'] += stats.get('loc', 0)
    
    chunk_elem = doc.createElement("chunk_stats")
    metadata_element.appendChild(chunk_elem)
    create_text_element(chunk_elem, "files_in_chunk", chunk_stats['files'])
    create_text_element(chunk_elem, "size_in_chunk_bytes", chunk_stats['size'])
    create_text_element(chunk_elem, "loc_in_chunk", chunk_stats['loc'])

    # --- 2. Add Highlighted ASCII Map ---
    ascii_map_element = doc.createElement("ascii_map")
    root_element.appendChild(ascii_map_element)
    
    path_to_line_num = master_report['path_to_line_num']
    highlight_lines = {path_to_line_num.get(f) for f in chunk_files if path_to_line_num.get(f) is not None}
    
    highlighted_map_lines = []
    for i, line in enumerate(master_report['ascii_map_lines']):
        if i in highlight_lines:
            highlighted_map_lines.append(f">> {line}")
        else:
            highlighted_map_lines.append(f"   {line}")
    
    cdata_map = doc.createCDATASection("\n".join(highlighted_map_lines))
    ascii_map_element.appendChild(cdata_map)

    # --- 3. Add File Contents ---
    files_element = doc.createElement("files")
    root_element.appendChild(files_element)

    for file_path in sorted(chunk_files):
        file_element = doc.createElement("file")
        files_element.appendChild(file_element)
        
        relative_path = os.path.relpath(file_path, root_dir)
        create_text_element(file_element, "path", relative_path)
        
        content_element = doc.createElement("content")
        file_element.appendChild(content_element)
        file_content = get_file_content(file_path)
        # CDATA sections cannot contain ']]>'. To handle this, we split the content
        # by this sequence, and re-insert the delimiter as a properly-escaped text node.
        parts = file_content.split(']]>')
        for i, part in enumerate(parts):
            if part:
                content_element.appendChild(doc.createCDATASection(part))
            if i < len(parts) - 1:
                content_element.appendChild(doc.createTextNode(']]>'))

    final_xml = doc.toprettyxml(indent="  ")
    
    # Add headers for NotebookLM and/or date/time compatibility if requested
    header_parts = []
    
    # NotebookLM header takes priority (goes first)
    if notebooklm:
        base_name = os.path.splitext(os.path.basename(output_filename))[0]
        if total_chunks > 1:
            header_parts.append(f"# {base_name}_part_{chunk_num} of {total_chunks}")
        else:
            header_parts.append(f"# {base_name}")
    
    # Add date/time as markdown subsection only if notebooklm is used
    if dt and notebooklm:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_parts.append(f"Generated on: {current_datetime}")
    
    # Combine headers if any exist
    if header_parts:
        header = "\n\n".join(header_parts) + "\n\n"
        final_xml = header + final_xml
    
    return final_xml, chunk_stats


def main():
    parser = argparse.ArgumentParser(description="Code crawler for FUM project.")
    parser.add_argument("--input", required=True, help="Root directory to scan.")
    parser.add_argument("--output", required=True, help="Base path for the output report file(s).")
    parser.add_argument("--chunks", type=int, default=1, help="Number of chunks to split the report into.")
    parser.add_argument("--notebooklm", action="store_true", help="Add markdown header for NotebookLM compatibility.")
    parser.add_argument("--dt", action="store_true", help="Add date/time information to the output.")
    args = parser.parse_args()

    # --- Overwrite Feature: Clean up old report files before starting ---
    print("Checking for and removing old report files to ensure a clean run...")
    output_base, output_ext = os.path.splitext(args.output)
    if args.chunks > 1:
        import glob
        pattern = f"{output_base}_part_*{output_ext}"
        old_files = glob.glob(pattern)
        for f in old_files:
            try:
                os.remove(f)
                print(f"Removed old report: {f}")
            except OSError as e:
                print(f"Error removing file {f}: {e}")
    else:
        if os.path.exists(args.output):
            try:
                os.remove(args.output)
                print(f"Removed old report: {args.output}")
            except OSError as e:
                print(f"Error removing file {args.output}: {e}")
    print("Cleanup complete.")
    # --- End Overwrite Feature ---

    # --- Step 1: Perform a single analysis and save the master report ---
    print("Step 1: Analyzing directory...")
    master_report = analyze_directory(args.input, ignore_patterns)
    
    # Use a temporary file for the master report to ensure clean data passage
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as temp_f:
        temp_report_path = temp_f.name
        save_analysis(master_report, temp_report_path)
    print(f"Master analysis report saved to temporary file: {temp_report_path}")


    # --- Step 2: Plan the chunks based on the master report ---
    print("\nStep 2: Planning chunks...")
    # Load the pristine data back for planning
    loaded_report = load_analysis(temp_report_path)
    chunk_file_lists = plan_chunks(loaded_report['files_metadata'], args.chunks, args.input)
    print(f"Planned {len(chunk_file_lists)} chunks.")
    
    # --- Step 3: Build each chunk report ---
    output_base, output_ext = os.path.splitext(args.output)
    final_report_stats = []

    for i, chunk_files in enumerate(chunk_file_lists):
        start_time = time.time()
        chunk_num = i + 1
        print(f"\nStep 3: Building chunk {chunk_num} of {len(chunk_file_lists)}...")
        
        if args.chunks > 1:
            output_path = f"{output_base}_part_{chunk_num}{output_ext}"
        else:
            output_path = args.output
        
        # Always use the pristine loaded_report as the source of truth
        xml_content, chunk_stats = create_chunk_xml(
            chunk_files, 
            loaded_report, 
            args.input,
            notebooklm=args.notebooklm,
            dt=args.dt,
            output_filename=output_path,
            chunk_num=chunk_num,
            total_chunks=len(chunk_file_lists)
        )
            
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(xml_content)
        
        end_time = time.time()
        duration = end_time - start_time
        
        final_report_stats.append({
            'path': output_path,
            'files': chunk_stats['files'],
            'loc': chunk_stats['loc'],
            'duration': duration
        })
        print(f"Successfully created report: {output_path} (took {duration:.2f}s)")

    # --- Cleanup ---
    os.remove(temp_report_path)
    print(f"\nCleanup: Removed temporary file {temp_report_path}")
    
    # --- Final Summary ---
    print("\n--- CRAWL COMPLETE: FINAL REPORT ---")
    for stats in final_report_stats:
        print(f"  - Chunk: {os.path.basename(stats['path'])}")
        print(f"    Files: {stats['files']}")
        print(f"    LOC:   {stats['loc']}")
        print(f"    Time:  {stats['duration']:.2f} seconds")
    print("------------------------------------")


if __name__ == "__main__":
    main()