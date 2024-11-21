import json
import requests
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin

class HTTPClient:
    def __init__(self, base_url: str = "", timeout: int = 30):
        """
        Initialize HTTP client with base URL and default timeout.
        
        Args:
            base_url: Base URL for all requests
            timeout: Default timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.headers: Dict[str, str] = {}

    def set_header(self, key: str, value: str):
        """Set a header for all requests."""
        self.headers[key] = value

    def set_headers(self, headers: Dict[str, str]):
        """Set multiple headers for all requests."""
        self.headers.update(headers)

    def get(self, url: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """
        Send GET request.
        
        Args:
            url: Request URL
            params: URL parameters
            **kwargs: Additional arguments for requests
        """
        full_url = urljoin(self.base_url, url)
        return self.session.get(
            full_url,
            params=params,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

    def post(self, url: str, data: Optional[Union[Dict, str]] = None, 
             json_data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """
        Send POST request.
        
        Args:
            url: Request URL
            data: Form data or raw string data
            json_data: JSON data (will be converted to string)
            **kwargs: Additional arguments for requests
        """
        full_url = urljoin(self.base_url, url)
        return self.session.post(
            full_url,
            data=data,
            json=json_data,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

    def put(self, url: str, data: Optional[Union[Dict, str]] = None,
            json_data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Send PUT request."""
        full_url = urljoin(self.base_url, url)
        return self.session.put(
            full_url,
            data=data,
            json=json_data,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

    def delete(self, url: str, **kwargs) -> requests.Response:
        """Send DELETE request."""
        full_url = urljoin(self.base_url, url)
        return self.session.delete(
            full_url,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

    def download_file(self, url: str, filepath: str, chunk_size: int = 8192) -> bool:
        """
        Download file from URL to local path.
        
        Args:
            url: File URL
            filepath: Local file path
            chunk_size: Size of chunks for streaming
        
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            response = self.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            return True
        except Exception:
            return False

    def upload_file(self, url: str, filepath: str, file_param_name: str = 'file',
                   additional_data: Optional[Dict] = None) -> requests.Response:
        """
        Upload file to URL.
        
        Args:
            url: Upload URL
            filepath: Path to file to upload
            file_param_name: Name of the file parameter
            additional_data: Additional form data
        """
        files = {file_param_name: open(filepath, 'rb')}
        data = additional_data or {}
        
        try:
            return self.post(url, data=data, files=files)
        finally:
            for f in files.values():
                f.close()

def create_client(base_url: str = "", timeout: int = 30) -> HTTPClient:
    """Create a new HTTP client instance."""
    return HTTPClient(base_url, timeout)

# Convenience functions using a default client
_default_client = HTTPClient()

def get(url: str, **kwargs) -> requests.Response:
    """Send GET request using default client."""
    return _default_client.get(url, **kwargs)

def post(url: str, **kwargs) -> requests.Response:
    """Send POST request using default client."""
    return _default_client.post(url, **kwargs)

def put(url: str, **kwargs) -> requests.Response:
    """Send PUT request using default client."""
    return _default_client.put(url, **kwargs)

def delete(url: str, **kwargs) -> requests.Response:
    """Send DELETE request using default client."""
    return _default_client.delete(url, **kwargs)

def download_file(url: str, filepath: str) -> bool:
    """Download file using default client."""
    return _default_client.download_file(url, filepath)

def upload_file(url: str, filepath: str, **kwargs) -> requests.Response:
    """Upload file using default client."""
    return _default_client.upload_file(url, filepath, **kwargs)

"""
# 1. Create a custom client

from core.http import HTTPClient

# Create client with base URL
client = HTTPClient('https://api.example.com')

# Set headers if needed
client.set_header('Authorization', 'Bearer token123')

# Make requests
response = client.get('/users')
response = client.post('/users', json_data={'name': 'John'})

# 2. Create a default client

from core.http import get, post, download_file

# Simple requests
response = get('https://api.example.com/users')
response = post('https://api.example.com/users', json_data={'name': 'John'})

# Download file
success = download_file('https://example.com/file.pdf', 'local_file.pdf')
"""