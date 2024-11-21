import re

def is_empty(s: str) -> bool:
    """Check if string is empty or None."""
    return s is None or len(s.strip()) == 0

def to_camel_case(s: str) -> str:
    """Convert string to camelCase."""
    s = s.strip()
    if is_empty(s):
        return s
    parts = s.split('_')
    return parts[0].lower() + ''.join(p.title() for p in parts[1:])

def to_snake_case(s: str) -> str:
    """Convert string to snake_case."""
    s = s.strip()
    if is_empty(s):
        return s
    s = re.sub('([A-Z])', r'_\1', s)
    return s.lower().strip('_')

def to_kebab_case(s: str) -> str:
    """Convert string to kebab-case."""
    return to_snake_case(s).replace('_', '-')

def truncate(s: str, length: int, suffix: str = '...') -> str:
    """Truncate string to specified length with suffix."""
    if is_empty(s) or len(s) <= length:
        return s
    return s[:length] + suffix

def contains(s: str, sub: str, case_sensitive: bool = True) -> bool:
    """Check if string contains substring."""
    if not case_sensitive:
        s = s.lower()
        sub = sub.lower()
    return sub in s

def starts_with(s: str, prefix: str, case_sensitive: bool = True) -> bool:
    """Check if string starts with prefix."""
    if not case_sensitive:
        s = s.lower()
        prefix = prefix.lower()
    return s.startswith(prefix)

def ends_with(s: str, suffix: str, case_sensitive: bool = True) -> bool:
    """Check if string ends with suffix."""
    if not case_sensitive:
        s = s.lower()
        suffix = suffix.lower()
    return s.endswith(suffix)

def remove_prefix(s: str, prefix: str) -> str:
    """Remove prefix from string if it exists."""
    if s.startswith(prefix):
        return s[len(prefix):]
    return s

def remove_suffix(s: str, suffix: str) -> str:
    """Remove suffix from string if it exists."""
    if s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def split_by_delimiter(s: str, delimiter: str = ',', strip: bool = True) -> list:
    """Split string by delimiter and optionally strip whitespace."""
    if is_empty(s):
        return []
    parts = s.split(delimiter)
    if strip:
        return [p.strip() for p in parts]
    return parts

def join_with_delimiter(items: list, delimiter: str = ',') -> str:
    """Join list items with delimiter."""
    return delimiter.join(str(item) for item in items)

def extract_between(s: str, start: str, end: str) -> str:
    """Extract substring between start and end markers."""
    start_idx = s.find(start)
    if start_idx == -1:
        return ''
    start_idx += len(start)
    end_idx = s.find(end, start_idx)
    if end_idx == -1:
        return ''
    return s[start_idx:end_idx]