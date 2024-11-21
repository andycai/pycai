import os
import shutil

def read_file(path):
    """Read entire file content."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_lines(path):
    """Read file content as lines."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

def read_bytes(path):
    """Read file as bytes."""
    with open(path, 'rb') as f:
        return f.read()

def write_file(path, content):
    """Write content to file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def write_lines(path, lines):
    """Write lines to file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def write_bytes(path, data):
    """Write bytes to file."""
    with open(path, 'wb') as f:
        f.write(data)

def append_file(path, content):
    """Append content to file."""
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)

def ensure_dir(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def copy_file(src, dst):
    """Copy file from src to dst."""
    shutil.copy2(src, dst)

def move_file(src, dst):
    """Move file from src to dst."""
    shutil.move(src, dst)

def remove_file(path):
    """Remove a file."""
    if os.path.exists(path):
        os.remove(path)

def remove_dir(path):
    """Remove a directory and its contents."""
    if os.path.exists(path):
        shutil.rmtree(path)

def list_files(path, pattern=None):
    """List all files in directory."""
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if pattern is None or pattern in filename:
                files.append(os.path.join(root, filename))
    return files

def file_exists(path):
    """Check if file exists."""
    return os.path.exists(path)

def get_file_size(path):
    """Get file size in bytes."""
    return os.path.getsize(path)

def get_file_modified_time(path):
    """Get file last modified time."""
    return os.path.getmtime(path)
