"""
Dataset Profiler Service
Phase 1: File Upload & Dataset Profiling

This module provides dataset profiling capabilities:
- Load CSV and Excel files
- Extract metadata (rows, columns, data types)
- Generate data preview
- Handle errors gracefully

NO AI APIs are used - all logic is rule-based using pandas.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List


class DatasetProfiler:
    """
    A service class for profiling datasets.
    
    This class loads CSV/Excel files and extracts comprehensive
    metadata without using any AI APIs.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the profiler with a file path.
        
        Args:
            file_path: Path to the CSV or Excel file
        
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported
        """
        self.file_path = Path(file_path)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """
        Load the dataset based on file extension.
        
        Supports:
        - CSV files (.csv)
        - Excel files (.xlsx, .xls)
        
        Raises:
            ValueError: If file format is not supported
            Exception: If file cannot be read
        """
        file_extension = self.file_path.suffix.lower()
        
        try:
            if file_extension == '.csv':
                # Load CSV file
                self.df = pd.read_csv(self.file_path)
            
            elif file_extension in ['.xlsx', '.xls']:
                # Load Excel file
                self.df = pd.read_excel(self.file_path)
            
            else:
                raise ValueError(
                    f"Unsupported file format: {file_extension}. "
                    "Only .csv, .xlsx, and .xls files are supported."
                )
        
        except pd.errors.EmptyDataError:
            raise ValueError("The file is empty or contains no data.")
        
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing file: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Error loading file: {str(e)}")
    
    def get_basic_info(self) -> Dict[str, Any]:
        """
        Get basic dataset information.
        
        Returns:
            dict: Contains number of rows, columns, and file size
        """
        return {
            "num_rows": len(self.df),
            "num_columns": len(self.df.columns),
            "file_size_bytes": self.file_path.stat().st_size,
            "file_size_mb": round(self.file_path.stat().st_size / (1024 * 1024), 2)
        }
    
    def get_column_info(self) -> List[Dict[str, Any]]:
        """
        Get detailed information about each column.
        
        Returns:
            list: List of dictionaries containing column metadata
        """
        column_info = []
        
        for col in self.df.columns:
            col_data = {
                "name": col,
                "dtype": str(self.df[col].dtype),
                "non_null_count": int(self.df[col].count()),
                "null_count": int(self.df[col].isnull().sum()),
                "null_percentage": round((self.df[col].isnull().sum() / len(self.df)) * 100, 2)
            }
            
            # Add unique value count
            col_data["unique_count"] = int(self.df[col].nunique())
            
            # Determine semantic type
            col_data["semantic_type"] = self._determine_semantic_type(self.df[col])
            
            column_info.append(col_data)
        
        return column_info
    
    def _determine_semantic_type(self, series: pd.Series) -> str:
        """
        Determine the semantic type of a column using rule-based logic.
        
        Args:
            series: Pandas series (column)
        
        Returns:
            str: Semantic type (numerical, categorical, datetime, text, boolean)
        """
        dtype = series.dtype
        
        # Check for boolean
        if dtype == 'bool':
            return "boolean"
        
        # Check for datetime
        if pd.api.types.is_datetime64_any_dtype(dtype):
            return "datetime"
        
        # Check for numerical
        if pd.api.types.is_numeric_dtype(dtype):
            return "numerical"
        
        # For object types, determine if categorical or text
        if dtype == 'object':
            unique_ratio = series.nunique() / len(series)
            
            # If unique ratio is low, likely categorical
            if unique_ratio < 0.5:
                return "categorical"
            else:
                return "text"
        
        return "unknown"
    
    def get_preview(self, num_rows: int = 10) -> Dict[str, Any]:
        """
        Get a preview of the dataset.
        
        Args:
            num_rows: Number of rows to include in preview (default: 10)
        
        Returns:
            dict: Contains column names and preview data
        """
        preview_df = self.df.head(num_rows)
        
        # Convert to dictionary format suitable for JSON
        preview_data = {
            "columns": list(self.df.columns),
            "data": preview_df.replace({np.nan: None}).to_dict(orient='records')
        }
        
        return preview_data
    
    def get_profile(self) -> Dict[str, Any]:
        """
        Get complete dataset profile.
        
        This is the main method that combines all profiling information.
        
        Returns:
            dict: Complete dataset profile including:
                - Basic info (rows, columns, size)
                - Column information (types, nulls, etc.)
                - Data preview
        """
        try:
            profile = {
                "basic_info": self.get_basic_info(),
                "columns": self.get_column_info(),
                "preview": self.get_preview(num_rows=10),
                "status": "success"
            }
            
            return profile
        
        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e)
            }
