import base64
import hashlib
import hmac
import secrets
from typing import Union, Optional

def base64_encode(data: Union[str, bytes]) -> str:
    """
    Encode data to base64.
    
    Args:
        data: String or bytes to encode
    
    Returns:
        Base64 encoded string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')

def base64_decode(data: str) -> str:
    """
    Decode base64 data.
    
    Args:
        data: Base64 encoded string
    
    Returns:
        Decoded string
    """
    return base64.b64decode(data).decode('utf-8')

def md5(data: Union[str, bytes]) -> str:
    """
    Calculate MD5 hash.
    
    Args:
        data: String or bytes to hash
    
    Returns:
        MD5 hash string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.md5(data).hexdigest()

def sha1(data: Union[str, bytes]) -> str:
    """
    Calculate SHA1 hash.
    
    Args:
        data: String or bytes to hash
    
    Returns:
        SHA1 hash string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha1(data).hexdigest()

def sha256(data: Union[str, bytes]) -> str:
    """
    Calculate SHA256 hash.
    
    Args:
        data: String or bytes to hash
    
    Returns:
        SHA256 hash string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def sha512(data: Union[str, bytes]) -> str:
    """
    Calculate SHA512 hash.
    
    Args:
        data: String or bytes to hash
    
    Returns:
        SHA512 hash string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha512(data).hexdigest()

def hmac_sha256(key: Union[str, bytes], data: Union[str, bytes]) -> str:
    """
    Calculate HMAC using SHA256.
    
    Args:
        key: Secret key
        data: Data to hash
    
    Returns:
        HMAC hash string
    """
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hmac.new(key, data, hashlib.sha256).hexdigest()

def generate_random_string(length: int = 32) -> str:
    """
    Generate cryptographically strong random string.
    
    Args:
        length: Length of string to generate
    
    Returns:
        Random string
    """
    return secrets.token_hex(length // 2)

def generate_random_bytes(length: int = 32) -> bytes:
    """
    Generate cryptographically strong random bytes.
    
    Args:
        length: Length of bytes to generate
    
    Returns:
        Random bytes
    """
    return secrets.token_bytes(length)

def url_safe_base64_encode(data: Union[str, bytes]) -> str:
    """
    URL-safe base64 encode.
    
    Args:
        data: String or bytes to encode
    
    Returns:
        URL-safe base64 encoded string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).decode('utf-8')

def url_safe_base64_decode(data: str) -> str:
    """
    URL-safe base64 decode.
    
    Args:
        data: URL-safe base64 encoded string
    
    Returns:
        Decoded string
    """
    return base64.urlsafe_b64decode(data).decode('utf-8')

def compare_digest(a: Union[str, bytes], b: Union[str, bytes]) -> bool:
    """
    Constant time comparison to prevent timing attacks.
    
    Args:
        a: First string/bytes to compare
        b: Second string/bytes to compare
    
    Returns:
        True if equal, False otherwise
    """
    if isinstance(a, str):
        a = a.encode('utf-8')
    if isinstance(b, str):
        b = b.encode('utf-8')
    return hmac.compare_digest(a, b)