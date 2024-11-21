import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional, Union, Dict, Any

class Logger:
    def __init__(self, name: str, log_dir: str = "logs"):
        """
        Initialize logger with name and log directory.
        
        Args:
            name: Logger name
            log_dir: Directory to store log files
        """
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup console and file handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_file = os.path.join(self.log_dir, f"{self.name}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, message, **kwargs)

    def _log(self, level: int, message: str, **kwargs):
        """Internal logging method with extra data handling."""
        if kwargs:
            message = f"{message} - Extra Data: {kwargs}"
        self.logger.log(level, message)

    def set_level(self, level: Union[int, str]):
        """Set logging level."""
        self.logger.setLevel(self._get_level(level))

    def _get_level(self, level: Union[int, str]) -> int:
        """Convert string level to logging level."""
        if isinstance(level, int):
            return level
        return getattr(logging, level.upper())

class DailyLogger(Logger):
    """Logger that creates new log file daily."""
    
    def _setup_handlers(self):
        """Setup console and daily rotating file handlers."""
        # Console handler (same as parent)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Daily rotating file handler
        log_file = os.path.join(self.log_dir, f"{self.name}.log")
        file_handler = TimedRotatingFileHandler(
            log_file,
            when='midnight',
            interval=1,
            backupCount=30  # Keep 30 days of logs
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

def create_logger(name: str, log_dir: str = "logs", daily: bool = False) -> Logger:
    """
    Create a new logger instance.
    
    Args:
        name: Logger name
        log_dir: Directory to store log files
        daily: If True, creates DailyLogger, otherwise creates standard Logger
    """
    logger_class = DailyLogger if daily else Logger
    return logger_class(name, log_dir)

# Default logger instance
default_logger = create_logger("default")

# Convenience functions using default logger
def debug(message: str, **kwargs):
    """Log debug message using default logger."""
    default_logger.debug(message, **kwargs)

def info(message: str, **kwargs):
    """Log info message using default logger."""
    default_logger.info(message, **kwargs)

def warning(message: str, **kwargs):
    """Log warning message using default logger."""
    default_logger.warning(message, **kwargs)

def error(message: str, **kwargs):
    """Log error message using default logger."""
    default_logger.error(message, **kwargs)

def critical(message: str, **kwargs):
    """Log critical message using default logger."""
    default_logger.critical(message, **kwargs)

def set_level(level: Union[int, str]):
    """Set logging level for default logger."""
    default_logger.set_level(level)

"""
# 1. Simple logging

from core.log import info, error, debug

# Simple logging
info("Application started")
error("An error occurred", error_code=500)
debug("Debug information", data={"key": "value"})

# 2. Create logger

from core.log import create_logger

# Create standard logger
logger = create_logger("myapp", log_dir="logs")
logger.info("Application started")
logger.error("Error occurred")

# Create daily rotating logger
daily_logger = create_logger("myapp", log_dir="logs", daily=True)
daily_logger.info("This will be in a daily rotating file")
"""