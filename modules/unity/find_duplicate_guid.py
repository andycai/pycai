from core import ioutil
import os
import re
from collections import defaultdict
from typing import Dict, List, Set

def find_meta_files(directory: str) -> List[str]:
    """Find all .meta files in the given directory and its subdirectories."""
    return ioutil.list_files(directory, pattern=".meta")

def extract_guid(file_path: str) -> str:
    """Extract GUID from a .meta file."""
    content = ioutil.read_file(file_path)
    # Look for "guid: " followed by alphanumeric characters
    match = re.search(r'guid:\s*([a-zA-Z0-9]+)', content)
    if match:
        return match.group(1)
    return ""

def find_duplicate_guids(directory: str, output_file: str):
    """
    Find and report duplicate GUIDs in Unity meta files.
    
    Args:
        directory: Root directory to search for .meta files
        output_file: Path to output report file
    """
    # Dictionary to store GUID -> list of files mapping
    guid_files: Dict[str, Set[str]] = defaultdict(set)
    
    # Find all meta files
    meta_files = find_meta_files(directory)
    
    # Extract GUIDs from each file
    for meta_file in meta_files:
        guid = extract_guid(meta_file)
        if guid:
            # Store the original asset path (without .meta extension)
            asset_path = meta_file[:-5]  # Remove .meta extension
            guid_files[guid].add(asset_path)
    
    # Filter for duplicates and write report
    duplicates = {guid: files for guid, files in guid_files.items() if len(files) > 1}
    
    if duplicates:
        # Prepare report content
        report_lines = ["Unity Duplicate GUID Report", "=" * 25, ""]
        
        for guid, files in duplicates.items():
            report_lines.append(f"GUID: {guid}")
            report_lines.append("-" * 20)
            for file_path in sorted(files):
                report_lines.append(f"  - {file_path}")
            report_lines.append("")
        
        # Write report
        ioutil.write_file(output_file, "\n".join(report_lines))
        print(f"Found {len(duplicates)} duplicate GUIDs. Report written to: {output_file}")
    else:
        print("No duplicate GUIDs found.")

if __name__ == "__main__":
    # Example usage
    project_dir = "."  # Current directory
    output_file = "duplicate_guids_report.txt"
    find_duplicate_guids(project_dir, output_file)
