"""
Logger for Paper Daily

Handles application logging with different levels and file output.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """Manages logging for the application"""
    
    def __init__(self, log_file: str = "paper_daily.log", level: str = "INFO"):
        """
        Initialize the logger
        
        Args:
            log_file: Path to the log file
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_file = log_file
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with file and console handlers"""
        
        # Create logger
        logger = logging.getLogger("paper_daily")
        logger.setLevel(self.level)
        
        # Remove existing handlers to avoid duplication
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create and setup file handler
        if self.log_file:
            # Create logs directory if it doesn't exist
            log_dir = os.path.dirname(self.log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Create and setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def log(self, message: str, level: str = "INFO", extra_data: Optional[dict] = None) -> None:
        """
        Log a message
        
        Args:
            message: Message to log
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            extra_data: Additional data to include in log
        """
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        if extra_data:
            message = f"{message} | Extra: {extra_data}"
        
        self.logger.log(log_level, message)
    
    def debug(self, message: str, extra_data: Optional[dict] = None) -> None:
        """Log debug message"""
        self.log(message, "DEBUG", extra_data)
    
    def info(self, message: str, extra_data: Optional[dict] = None) -> None:
        """Log info message"""
        self.log(message, "INFO", extra_data)
    
    def warning(self, message: str, extra_data: Optional[dict] = None) -> None:
        """Log warning message"""
        self.log(message, "WARNING", extra_data)
    
    def error(self, message: str, extra_data: Optional[dict] = None) -> None:
        """Log error message"""
        self.log(message, "ERROR", extra_data)
    
    def critical(self, message: str, extra_data: Optional[dict] = None) -> None:
        """Log critical message"""
        self.log(message, "CRITICAL", extra_data)
    
    def log_function_call(self, function_name: str, args: dict = None) -> None:
        """
        Log a function call with its arguments
        
        Args:
            function_name: Name of the function being called
            args: Arguments passed to the function
        """
        message = f"Calling function: {function_name}"
        if args:
            message += f" with args: {args}"
        self.debug(message)
    
    def log_performance(self, operation: str, duration: float, extra_info: dict = None) -> None:
        """
        Log performance metrics
        
        Args:
            operation: Name of the operation
            duration: Duration in seconds
            extra_info: Additional performance info
        """
        message = f"Performance: {operation} took {duration:.2f}s"
        if extra_info:
            message += f" | {extra_info}"
        self.info(message) 