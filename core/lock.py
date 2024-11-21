import os
import time
import fcntl
import errno
import atexit
from contextlib import contextmanager
from typing import Optional, Union, Callable
from datetime import datetime

class FileLock:
    """A file locking mechanism."""
    
    def __init__(self, file_path: str, timeout: float = -1):
        """
        Initialize file lock.
        
        Args:
            file_path: Path to the lock file
            timeout: Maximum time to wait for lock acquisition (-1 for infinite)
        """
        self.file_path = file_path
        self.timeout = timeout
        self.fd = None
        self.pid = os.getpid()
        
        # Register cleanup on process exit
        atexit.register(self.release)

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire the lock.
        
        Args:
            timeout: Override default timeout
        
        Returns:
            True if lock was acquired, False if not
        """
        timeout = timeout if timeout is not None else self.timeout
        start_time = time.time()
        
        while True:
            try:
                # Open the lock file
                self.fd = os.open(self.file_path, os.O_CREAT | os.O_RDWR)
                
                # Try to acquire lock
                fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                
                # Write PID to lock file
                os.truncate(self.fd, 0)
                os.write(self.fd, f"{self.pid}\n".encode())
                
                return True
                
            except (IOError, OSError) as e:
                if self.fd:
                    os.close(self.fd)
                    self.fd = None
                
                if e.errno != errno.EAGAIN:
                    raise
                
                if timeout >= 0 and time.time() - start_time >= timeout:
                    return False
                
                time.sleep(0.1)

    def release(self):
        """Release the lock."""
        if self.fd is not None:
            try:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
                os.close(self.fd)
            except (IOError, OSError):
                pass
            finally:
                self.fd = None

    def is_locked(self) -> bool:
        """Check if file is currently locked."""
        try:
            fd = os.open(self.file_path, os.O_RDWR)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(fd, fcntl.LOCK_UN)
                return False
            except (IOError, OSError) as e:
                if e.errno != errno.EAGAIN:
                    raise
                return True
            finally:
                os.close(fd)
        except (IOError, OSError):
            return False

    def get_owner_pid(self) -> Optional[int]:
        """Get PID of process holding the lock."""
        try:
            with open(self.file_path, 'r') as f:
                pid = int(f.readline().strip())
                return pid
        except (IOError, ValueError):
            return None

    def __enter__(self):
        """Context manager entry."""
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()

@contextmanager
def file_lock(file_path: str, timeout: float = -1):
    """
    Context manager for file locking.
    
    Args:
        file_path: Path to lock file
        timeout: Maximum time to wait for lock
    
    Example:
        with file_lock('myfile.lock'):
            # Do something with exclusive access
    """
    lock = FileLock(file_path, timeout)
    try:
        lock.acquire()
        yield lock
    finally:
        lock.release()

class LockTimeout(Exception):
    """Exception raised when lock acquisition times out."""
    pass

def with_file_lock(lock_path: str, timeout: float = -1):
    """
    Decorator for functions requiring file lock.
    
    Args:
        lock_path: Path to lock file
        timeout: Maximum time to wait for lock
    
    Example:
        @with_file_lock('myfile.lock')
        def my_function():
            # Do something with exclusive access
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            with file_lock(lock_path, timeout) as lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator

"""
# 1. Manual lock/unlock

from core.lock import FileLock

# Create lock
lock = FileLock("myfile.lock", timeout=10)

# Manual lock/unlock
if lock.acquire():
    try:
        # Do something with exclusive access
        pass
    finally:
        lock.release()

# 2. Using context manager

from core.lock import file_lock

# Using with statement
with file_lock("myfile.lock", timeout=10) as lock:
    # Do something with exclusive access
    pass

# 3. Using decorator:

from core.lock import with_file_lock

@with_file_lock("myfile.lock", timeout=10)
def my_function():
    # Do something with exclusive access
    pass
"""