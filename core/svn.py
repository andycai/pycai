import os
import subprocess
from typing import List, Optional, Dict, Tuple

class SVNClient:
    def __init__(self, working_dir: str, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize SVN client.
        
        Args:
            working_dir: SVN working directory
            username: SVN username
            password: SVN password
        """
        self.working_dir = working_dir
        self.username = username
        self.password = password

    def _run_command(self, command: List[str]) -> Tuple[str, str, int]:
        """
        Run SVN command and return output.
        
        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        if self.username:
            command.extend(['--username', self.username])
        if self.password:
            command.extend(['--password', self.password])
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.working_dir,
            text=True
        )
        stdout, stderr = process.communicate()
        return stdout.strip(), stderr.strip(), process.returncode

    def checkout(self, url: str, path: Optional[str] = None) -> bool:
        """
        Checkout SVN repository.
        
        Args:
            url: Repository URL
            path: Local path (optional)
        """
        command = ['svn', 'checkout', url]
        if path:
            command.append(path)
        
        _, stderr, code = self._run_command(command)
        return code == 0

    def update(self, path: Optional[str] = None) -> bool:
        """Update working copy."""
        command = ['svn', 'update']
        if path:
            command.append(path)
        
        _, stderr, code = self._run_command(command)
        return code == 0

    def commit(self, message: str, paths: Optional[List[str]] = None) -> bool:
        """
        Commit changes.
        
        Args:
            message: Commit message
            paths: List of paths to commit (optional)
        """
        command = ['svn', 'commit', '-m', message]
        if paths:
            command.extend(paths)
        
        _, stderr, code = self._run_command(command)
        return code == 0

    def add(self, paths: List[str]) -> bool:
        """Add files/directories to version control."""
        command = ['svn', 'add'] + paths
        _, stderr, code = self._run_command(command)
        return code == 0

    def delete(self, paths: List[str], force: bool = False) -> bool:
        """Delete files/directories from version control."""
        command = ['svn', 'delete']
        if force:
            command.append('--force')
        command.extend(paths)
        
        _, stderr, code = self._run_command(command)
        return code == 0

    def status(self, path: Optional[str] = None) -> str:
        """Get status of working copy."""
        command = ['svn', 'status']
        if path:
            command.append(path)
        
        stdout, _, _ = self._run_command(command)
        return stdout

    def log(self, limit: Optional[int] = None, path: Optional[str] = None) -> str:
        """Get commit log."""
        command = ['svn', 'log']
        if limit:
            command.extend(['-l', str(limit)])
        if path:
            command.append(path)
        
        stdout, _, _ = self._run_command(command)
        return stdout

    def diff(self, path: Optional[str] = None, revision: Optional[str] = None) -> str:
        """Get differences."""
        command = ['svn', 'diff']
        if revision:
            command.extend(['-r', revision])
        if path:
            command.append(path)
        
        stdout, _, _ = self._run_command(command)
        return stdout

    def revert(self, paths: List[str], recursive: bool = False) -> bool:
        """Revert changes."""
        command = ['svn', 'revert']
        if recursive:
            command.append('-R')
        command.extend(paths)
        
        _, stderr, code = self._run_command(command)
        return code == 0

    def cleanup(self) -> bool:
        """Clean up working copy."""
        command = ['svn', 'cleanup']
        _, stderr, code = self._run_command(command)
        return code == 0

    def info(self, path: Optional[str] = None) -> str:
        """Get repository information."""
        command = ['svn', 'info']
        if path:
            command.append(path)
        
        stdout, _, _ = self._run_command(command)
        return stdout

    def list_files(self, url: Optional[str] = None) -> str:
        """List files in repository."""
        command = ['svn', 'list']
        if url:
            command.append(url)
        
        stdout, _, _ = self._run_command(command)
        return stdout

def create_client(working_dir: str, username: Optional[str] = None, 
                 password: Optional[str] = None) -> SVNClient:
    """Create a new SVN client instance."""
    return SVNClient(working_dir, username, password)

"""
from core.svn import create_client

# Create SVN client
svn = create_client(
    working_dir='/path/to/working/dir',
    username='your_username',  # optional
    password='your_password'   # optional
)

# Checkout repository
svn.checkout('https://svn.example.com/repo')

# Update working copy
svn.update()

# Add files
svn.add(['file1.txt', 'file2.txt'])

# Commit changes
svn.commit('Added new files')

# Get status
status = svn.status()
print(status)
"""