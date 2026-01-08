"""
File Validation Utilities
Phase 1: File Upload & Dataset Profiling

This module provides utilities for validating uploaded files.
All validation is rule-based - no AI APIs are used.
"""

from pathlib import Path
from typing import List


# Allowed file extensions
ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls'}

# Maximum file size (100 MB)
MAX_FILE_SIZE_MB = 100
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def validate_file_extension(filename: str) -> bool:
    """
    Validate if the file has an allowed extension.
    
    Args:
        filename: Name of the file to validate
    
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    if not filename:
        return False
    
    file_path = Path(filename)
    extension = file_path.suffix.lower()
    
    return extension in ALLOWED_EXTENSIONS


def validate_file_size(file_size_bytes: int) -> bool:
    """
    Validate if the file size is within allowed limits.
    
    Args:
        file_size_bytes: Size of the file in bytes
    
    Returns:
        bool: True if size is acceptable, False otherwise
    """
    return 0 < file_size_bytes <= MAX_FILE_SIZE_BYTES


def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename.
    
    Args:
        filename: Name of the file
    
    Returns:
        str: File extension (lowercase, with dot)
    """
    return Path(filename).suffix.lower()


def is_csv_file(filename: str) -> bool:
    """
    Check if the file is a CSV file.
    
    Args:
        filename: Name of the file
    
    Returns:
        bool: True if CSV file, False otherwise
    """
    return get_file_extension(filename) == '.csv'


def is_excel_file(filename: str) -> bool:
    """
    Check if the file is an Excel file.
    
    Args:
        filename: Name of the file
    
    Returns:
        bool: True if Excel file, False otherwise
    """
    return get_file_extension(filename) in {'.xlsx', '.xls'}


def get_allowed_extensions_string() -> str:
    """
    Get a human-readable string of allowed extensions.
    
    Returns:
        str: Comma-separated list of allowed extensions
    """
    return ", ".join(sorted(ALLOWED_EXTENSIONS))
