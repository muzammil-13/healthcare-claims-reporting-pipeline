"""
Logger utility module for Healthcare Claims Auto-Adjudication Pipeline.

This module provides centralized logging configuration with support for:
- File logging with rotation
- Console logging
- Different log levels
- Structured log formatting
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(
    name='pipeline',
    log_file='logs/pipeline.log',
    level=logging.INFO,
    console_output=True,
    max_bytes=10485760,  # 10MB
    backup_count=5
):
    """
    Configure and return a logger instance with file and optional console handlers.
    
    Args:
        name (str): Logger name (default: 'pipeline')
        log_file (str): Path to log file (default: 'logs/pipeline.log')
        level (int): Logging level (default: logging.INFO)
        console_output (bool): Enable console output (default: True)
        max_bytes (int): Max log file size before rotation (default: 10MB)
        backup_count (int): Number of backup files to keep (default: 5)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler (optional)
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name='pipeline'):
    """
    Get an existing logger instance by name.
    
    Args:
        name (str): Logger name (default: 'pipeline')
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


def log_function_call(logger, func_name, **kwargs):
    """
    Log a function call with its parameters.
    
    Args:
        logger: Logger instance
        func_name (str): Name of the function being called
        **kwargs: Function parameters to log
    """
    params = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
    logger.info(f"Calling {func_name}({params})")


def log_dataframe_info(logger, df, df_name='DataFrame'):
    """
    Log information about a pandas DataFrame.
    
    Args:
        logger: Logger instance
        df: pandas DataFrame
        df_name (str): Name/description of the DataFrame
    """
    logger.info(f"{df_name} - Shape: {df.shape}, Columns: {list(df.columns)}")
    logger.info(f"{df_name} - Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")


def log_section_start(logger, section_name):
    """
    Log the start of a major section/phase.
    
    Args:
        logger: Logger instance
        section_name (str): Name of the section
    """
    separator = "=" * 60
    logger.info(separator)
    logger.info(f"START: {section_name}")
    logger.info(separator)


def log_section_end(logger, section_name, success=True):
    """
    Log the end of a major section/phase.
    
    Args:
        logger: Logger instance
        section_name (str): Name of the section
        success (bool): Whether the section completed successfully
    """
    status = "SUCCESS" if success else "FAILED"
    separator = "=" * 60
    logger.info(f"END: {section_name} - {status}")
    logger.info(separator)


def log_metrics(logger, metrics_dict, prefix=''):
    """
    Log metrics in a structured format.
    
    Args:
        logger: Logger instance
        metrics_dict (dict): Dictionary of metrics to log
        prefix (str): Optional prefix for metric names
    """
    logger.info(f"Metrics{' - ' + prefix if prefix else ''}:")
    for key, value in metrics_dict.items():
        logger.info(f"  {key}: {value}")


def log_error_with_context(logger, error, context=''):
    """
    Log an error with additional context information.
    
    Args:
        logger: Logger instance
        error (Exception): The exception that occurred
        context (str): Additional context about where/why the error occurred
    """
    error_msg = f"Error: {type(error).__name__}: {str(error)}"
    if context:
        error_msg = f"{context} - {error_msg}"
    logger.error(error_msg, exc_info=True)


# Example usage and testing
if __name__ == "__main__":
    # Test the logger
    test_logger = setup_logger(
        name='test',
        log_file='logs/test.log',
        console_output=True
    )
    
    test_logger.info("Logger module test started")
    log_section_start(test_logger, "Test Section")
    
    # Test logging metrics
    test_metrics = {
        'total_records': 100,
        'processed': 95,
        'errors': 5
    }
    log_metrics(test_logger, test_metrics, prefix='Test Run')
    
    log_section_end(test_logger, "Test Section", success=True)
    test_logger.info("Logger module test completed")

# Made with Bob
