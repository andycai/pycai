import os
import zipfile
from typing import List, Optional

def create_zip(zip_file: str, files: List[str], base_dir: Optional[str] = None):
    """
    Create a ZIP file from a list of files.
    
    Args:
        zip_file: Path to the output ZIP file
        files: List of files to include in the ZIP
        base_dir: Optional base directory for relative paths in the ZIP
    """
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            if base_dir:
                arcname = os.path.relpath(file, base_dir)
            else:
                arcname = os.path.basename(file)
            zf.write(file, arcname)

def extract_zip(zip_file: str, extract_path: str):
    """
    Extract a ZIP file to specified path.
    
    Args:
        zip_file: Path to the ZIP file to extract
        extract_path: Directory to extract files to
    """
    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(extract_path)

def list_zip_contents(zip_file: str) -> List[str]:
    """
    List contents of a ZIP file.
    
    Args:
        zip_file: Path to the ZIP file
    
    Returns:
        List of file names in the ZIP
    """
    with zipfile.ZipFile(zip_file, 'r') as zf:
        return zf.namelist()

def add_to_zip(zip_file: str, files: List[str], base_dir: Optional[str] = None):
    """
    Add files to an existing ZIP file.
    
    Args:
        zip_file: Path to the ZIP file
        files: List of files to add
        base_dir: Optional base directory for relative paths in the ZIP
    """
    with zipfile.ZipFile(zip_file, 'a', zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            if base_dir:
                arcname = os.path.relpath(file, base_dir)
            else:
                arcname = os.path.basename(file)
            zf.write(file, arcname)

def is_zip_file(file_path: str) -> bool:
    """
    Check if a file is a valid ZIP file.
    
    Args:
        file_path: Path to the file to check
    
    Returns:
        True if file is a valid ZIP file, False otherwise
    """
    return zipfile.is_zipfile(file_path)

def get_zip_info(zip_file: str) -> List[dict]:
    """
    Get detailed information about files in a ZIP archive.
    
    Args:
        zip_file: Path to the ZIP file
    
    Returns:
        List of dictionaries containing file information
    """
    info_list = []
    with zipfile.ZipFile(zip_file, 'r') as zf:
        for info in zf.infolist():
            info_dict = {
                'filename': info.filename,
                'file_size': info.file_size,
                'compress_size': info.compress_size,
                'date_time': info.date_time,
                'compress_type': info.compress_type
            }
            info_list.append(info_dict)
    return info_list

def extract_single_file(zip_file: str, file_name: str, extract_path: str):
    """
    Extract a single file from a ZIP archive.
    
    Args:
        zip_file: Path to the ZIP file
        file_name: Name of the file to extract
        extract_path: Directory to extract the file to
    """
    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extract(file_name, extract_path)

"""
# Create a ZIP file
files = ['file1.txt', 'file2.txt']
create_zip('archive.zip', files)

# Extract ZIP contents
extract_zip('archive.zip', 'extract_folder')

# List ZIP contents
contents = list_zip_contents('archive.zip')

# Get detailed ZIP info
info = get_zip_info('archive.zip')
"""