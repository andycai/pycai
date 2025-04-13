from core.svn import SVNClient
from core import ioutil
import os
import re
from typing import List, Dict, Tuple

class RepoSyncer:
    def __init__(self, repo1_path: str, repo2_path: str, username: str = None, password: str = None):
        """Initialize repository syncer."""
        self.repo1 = SVNClient(repo1_path, username, password)
        self.repo2 = SVNClient(repo2_path, username, password)
        self.repo1_path = repo1_path
        self.repo2_path = repo2_path

    def update_repos(self) -> bool:
        """Update both repositories to latest version."""
        return self.repo1.update() and self.repo2.update()

    def parse_log_entry(self, log_output: str) -> List[Dict[str, str]]:
        """Parse SVN log output to extract file changes."""
        changes = []
        current_revision = None
        
        for line in log_output.split('\n'):
            # Look for revision line
            rev_match = re.match(r'^r(\d+)', line)
            if rev_match:
                current_revision = rev_match.group(1)
                continue
            
            # Look for changed files
            if line.startswith('A ') or line.startswith('M ') or line.startswith('D '):
                action = line[0]
                path = line[2:].strip()
                changes.append({
                    'revision': current_revision,
                    'action': action,
                    'path': path
                })
        
        return changes

    def sync_changes(self) -> bool:
        """Sync changes from repo1 to repo2."""
        try:
            # Get recent changes from repo1
            log_output = self.repo1.log(limit=100)
            changes = self.parse_log_entry(log_output)
            
            # Track files for final commit
            files_to_commit = []
            
            for change in changes:
                src_path = os.path.join(self.repo1_path, change['path'])
                dst_path = os.path.join(self.repo2_path, change['path'])
                
                if change['action'] in ['A', 'M']:  # Add or Modify
                    # Ensure destination directory exists
                    dst_dir = os.path.dirname(dst_path)
                    ioutil.ensure_dir(dst_dir)
                    
                    # Copy file
                    ioutil.copy_file(src_path, dst_path)
                    
                    # Add to SVN if new file
                    if change['action'] == 'A':
                        self.repo2.add([dst_path])
                    
                    files_to_commit.append(dst_path)
                    
                elif change['action'] == 'D':  # Delete
                    if os.path.exists(dst_path):
                        self.repo2.delete([dst_path])
                        files_to_commit.append(dst_path)
            
            # Commit all changes
            if files_to_commit:
                return self.repo2.commit(
                    message="Synced changes from repo1",
                    paths=files_to_commit
                )
            
            return True
            
        except Exception as e:
            print(f"Error during sync: {e}")
            return False

def main():
    """Main function to run the sync operation."""
    # Replace these with actual repository paths and credentials
    repo1_path = "/path/to/repo1"
    repo2_path = "/path/to/repo2"
    username = "your_username"
    password = "your_password"
    
    syncer = RepoSyncer(repo1_path, repo2_path, username, password)
    
    print("Updating repositories...")
    if not syncer.update_repos():
        print("Failed to update repositories")
        return
    
    print("Syncing changes...")
    if syncer.sync_changes():
        print("Successfully synced changes")
    else:
        print("Failed to sync changes")

if __name__ == "__main__":
    main()
