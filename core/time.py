from datetime import datetime, timedelta
from typing import Union, Optional
import time

# Common format strings
FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S"
FORMAT_DATE = "%Y-%m-%d"
FORMAT_TIME = "%H:%M:%S"
FORMAT_DATETIME_MS = "%Y-%m-%d %H:%M:%S.%f"
FORMAT_ISO = "%Y-%m-%dT%H:%M:%S.%fZ"

def now() -> datetime:
    """Get current datetime."""
    return datetime.now()

def timestamp() -> float:
    """Get current timestamp in seconds."""
    return time.time()

def timestamp_ms() -> int:
    """Get current timestamp in milliseconds."""
    return int(time.time() * 1000)

def format_datetime(dt: Optional[datetime] = None, fmt: str = FORMAT_DATETIME) -> str:
    """
    Format datetime to string.
    
    Args:
        dt: Datetime to format (default: current datetime)
        fmt: Format string (default: YYYY-MM-DD HH:MM:SS)
    """
    if dt is None:
        dt = now()
    return dt.strftime(fmt)

def parse_datetime(dt_str: str, fmt: str = FORMAT_DATETIME) -> datetime:
    """
    Parse datetime from string.
    
    Args:
        dt_str: Datetime string
        fmt: Format string (default: YYYY-MM-DD HH:MM:SS)
    """
    return datetime.strptime(dt_str, fmt)

def to_timestamp(dt: Optional[datetime] = None) -> float:
    """Convert datetime to timestamp in seconds."""
    if dt is None:
        dt = now()
    return dt.timestamp()

def from_timestamp(ts: Union[int, float]) -> datetime:
    """Convert timestamp to datetime."""
    return datetime.fromtimestamp(ts)

def add_days(dt: Optional[datetime] = None, days: int = 1) -> datetime:
    """Add days to datetime."""
    if dt is None:
        dt = now()
    return dt + timedelta(days=days)

def add_hours(dt: Optional[datetime] = None, hours: int = 1) -> datetime:
    """Add hours to datetime."""
    if dt is None:
        dt = now()
    return dt + timedelta(hours=hours)

def add_minutes(dt: Optional[datetime] = None, minutes: int = 1) -> datetime:
    """Add minutes to datetime."""
    if dt is None:
        dt = now()
    return dt + timedelta(minutes=minutes)

def add_seconds(dt: Optional[datetime] = None, seconds: int = 1) -> datetime:
    """Add seconds to datetime."""
    if dt is None:
        dt = now()
    return dt + timedelta(seconds=seconds)

def get_date_range(start_date: Union[str, datetime], 
                  end_date: Union[str, datetime], 
                  fmt: str = FORMAT_DATE) -> list:
    """
    Get list of dates between start and end date.
    
    Args:
        start_date: Start date (string or datetime)
        end_date: End date (string or datetime)
        fmt: Format string for input/output dates
    """
    if isinstance(start_date, str):
        start_date = parse_datetime(start_date, fmt)
    if isinstance(end_date, str):
        end_date = parse_datetime(end_date, fmt)
    
    date_list = []
    current = start_date
    while current <= end_date:
        date_list.append(format_datetime(current, fmt))
        current = add_days(current)
    return date_list

def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    """Check if two datetimes are on the same day."""
    return dt1.date() == dt2.date()

def is_weekend(dt: Optional[datetime] = None) -> bool:
    """Check if datetime is weekend (Saturday or Sunday)."""
    if dt is None:
        dt = now()
    return dt.weekday() >= 5

def get_month_start(dt: Optional[datetime] = None) -> datetime:
    """Get start of month for datetime."""
    if dt is None:
        dt = now()
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

def get_month_end(dt: Optional[datetime] = None) -> datetime:
    """Get end of month for datetime."""
    if dt is None:
        dt = now()
    next_month = dt.replace(day=28) + timedelta(days=4)
    return next_month.replace(day=1, hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=1)

def time_since(dt: datetime) -> str:
    """
    Get human readable time since datetime.
    Example: "2 days ago", "3 hours ago", etc.
    """
    now_ts = now()
    diff = now_ts - dt
    
    seconds = diff.total_seconds()
    if seconds < 60:
        return "just now"
    
    minutes = seconds // 60
    if minutes < 60:
        return f"{int(minutes)} minutes ago"
    
    hours = minutes // 60
    if hours < 24:
        return f"{int(hours)} hours ago"
    
    days = hours // 24
    if days < 30:
        return f"{int(days)} days ago"
    
    months = days // 30
    if months < 12:
        return f"{int(months)} months ago"
    
    years = months // 12
    return f"{int(years)} years ago"

"""
from core.time import (
    now, timestamp, format_datetime, parse_datetime,
    add_days, get_date_range, time_since
)

# Get current time
current = now()
ts = timestamp()  # Unix timestamp

# Format and parse
date_str = format_datetime(current)  # "2023-12-25 10:30:45"
dt = parse_datetime("2023-12-25 10:30:45")

# Date arithmetic
tomorrow = add_days(days=1)
next_week = add_days(days=7)

# Date ranges
dates = get_date_range("2023-12-01", "2023-12-31")

# Human readable time
time_ago = time_since(some_date)  # "2 days ago"
"""