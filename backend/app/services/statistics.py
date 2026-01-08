"""
Statistics Engine Service
Phase 2: Descriptive Statistical Analysis

This module computes descriptive statistics for numerical columns.
All calculations are performed MANUALLY - no pandas .describe() shortcuts.

NO AI APIs are used - all logic is rule-based using numpy and pandas.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
from collections import Counter


class StatisticsEngine:
    """
    A service class for computing descriptive statistics on datasets.
    
    This class performs manual statistical calculations on numerical columns
    identified by the dataset profiler.
    """
    
    def __init__(self, df: pd.DataFrame, profile_data: Dict[str, Any]):
        """
        Initialize the statistics engine.
        
        Args:
            df: Pandas DataFrame containing the dataset
            profile_data: Profile metadata from the profiler service
        """
        self.df = df
        self.profile_data = profile_data
        self.numerical_columns = self._identify_numerical_columns()
    
    def _identify_numerical_columns(self) -> List[str]:
        """
        Identify numerical columns from profile data.
        
        Returns:
            list: Names of columns with semantic_type == "numerical"
        """
        numerical_cols = []
        
        for col_info in self.profile_data.get('columns', []):
            if col_info.get('semantic_type') == 'numerical':
                numerical_cols.append(col_info['name'])
        
        return numerical_cols
    
    def compute_count(self, series: pd.Series) -> int:
        """
        Compute count of non-null values.
        
        Args:
            series: Pandas series (column)
        
        Returns:
            int: Count of non-null values
        """
        return int(series.count())
    
    def compute_mean(self, series: pd.Series) -> Optional[float]:
        """
        Compute arithmetic mean manually.
        
        Args:
            series: Pandas series (column)
        
        Returns:
            float: Mean value, or None if no valid data
        """
        clean_data = series.dropna()
        
        if len(clean_data) == 0:
            return None
        
        # Manual calculation: sum / count
        total = float(np.sum(clean_data))
        count = len(clean_data)
        
        return round(total / count, 2)
    
    def compute_median(self, series: pd.Series) -> Optional[float]:
        """
        Compute median manually.
        
        Args:
            series: Pandas series (column)
        
        Returns:
            float: Median value, or None if no valid data
        """
        clean_data = series.dropna().sort_values()
        
        if len(clean_data) == 0:
            return None
        
        n = len(clean_data)
        
        # Manual calculation
        if n % 2 == 0:
            # Even number of elements: average of two middle values
            median = (clean_data.iloc[n//2 - 1] + clean_data.iloc[n//2]) / 2
        else:
            # Odd number of elements: middle value
            median = clean_data.iloc[n//2]
        
        return round(float(median), 2)
    
    def compute_mode(self, series: pd.Series) -> Optional[Union[int, float]]:
        """
        Compute mode (most frequent value) manually.
        
        Args:
            series: Pandas series (column)
        
        Returns:
            int/float: Mode value, or None if no valid data
        """
        clean_data = series.dropna()
        
        if len(clean_data) == 0:
            return None
        
        # Manual calculation using Counter
        counter = Counter(clean_data)
        
        if len(counter) == 0:
            return None
        
        # Get most common value
        mode_value, mode_count = counter.most_common(1)[0]
        
        # Return as int if it's a whole number, otherwise float
        if isinstance(mode_value, (int, np.integer)):
            return int(mode_value)
        else:
            return round(float(mode_value), 2)
    
    def compute_min(self, series: pd.Series) -> Optional[float]:
        """
        Compute minimum value manually.
        
        Args:
            series: Pandas series (column)
        
        Returns:
            float: Minimum value, or None if no valid data
        """
        clean_data = series.dropna()
        
        if len(clean_data) == 0:
            return None
        
        return round(float(np.min(clean_data)), 2)
    
    def compute_max(self, series: pd.Series) -> Optional[float]:
        """
        Compute maximum value manually.
        
        Args:
            series: Pandas series (column)
        
        Returns:
            float: Maximum value, or None if no valid data
        """
        clean_data = series.dropna()
        
        if len(clean_data) == 0:
            return None
        
        return round(float(np.max(clean_data)), 2)
    
    def compute_std_dev(self, series: pd.Series) -> Optional[float]:
        """
        Compute standard deviation manually (sample std dev, n-1).
        
        Args:
            series: Pandas series (column)
        
        Returns:
            float: Standard deviation, or None if insufficient data
        """
        clean_data = series.dropna()
        
        if len(clean_data) < 2:
            return None
        
        # Manual calculation
        mean = np.mean(clean_data)
        squared_diffs = [(x - mean) ** 2 for x in clean_data]
        variance = sum(squared_diffs) / (len(clean_data) - 1)  # Sample variance (n-1)
        std_dev = np.sqrt(variance)
        
        return round(float(std_dev), 2)
    
    def compute_variance(self, series: pd.Series) -> Optional[float]:
        """
        Compute variance manually (sample variance, n-1).
        
        Args:
            series: Pandas series (column)
        
        Returns:
            float: Variance, or None if insufficient data
        """
        clean_data = series.dropna()
        
        if len(clean_data) < 2:
            return None
        
        # Manual calculation
        mean = np.mean(clean_data)
        squared_diffs = [(x - mean) ** 2 for x in clean_data]
        variance = sum(squared_diffs) / (len(clean_data) - 1)  # Sample variance (n-1)
        
        return round(float(variance), 2)
    
    def compute_percentile(self, series: pd.Series, percentile: float) -> Optional[float]:
        """
        Compute percentile manually using linear interpolation.
        
        Args:
            series: Pandas series (column)
            percentile: Percentile to compute (0-100)
        
        Returns:
            float: Percentile value, or None if no valid data
        """
        clean_data = series.dropna().sort_values()
        
        if len(clean_data) == 0:
            return None
        
        # Manual calculation with linear interpolation
        n = len(clean_data)
        
        if n == 1:
            return round(float(clean_data.iloc[0]), 2)
        
        # Calculate position
        position = (percentile / 100) * (n - 1)
        lower_index = int(np.floor(position))
        upper_index = int(np.ceil(position))
        
        # Linear interpolation
        if lower_index == upper_index:
            result = clean_data.iloc[lower_index]
        else:
            lower_value = clean_data.iloc[lower_index]
            upper_value = clean_data.iloc[upper_index]
            fraction = position - lower_index
            result = lower_value + fraction * (upper_value - lower_value)
        
        return round(float(result), 2)
    
    def compute_range(self, series: pd.Series) -> Optional[float]:
        """
        Compute range (max - min) manually.
        
        Args:
            series: Pandas series (column)
        
        Returns:
            float: Range value, or None if no valid data
        """
        min_val = self.compute_min(series)
        max_val = self.compute_max(series)
        
        if min_val is None or max_val is None:
            return None
        
        return round(max_val - min_val, 2)
    
    def compute_column_statistics(self, column_name: str) -> Dict[str, Any]:
        """
        Compute all statistics for a single column.
        
        Args:
            column_name: Name of the column
        
        Returns:
            dict: Dictionary containing all computed statistics
        """
        series = self.df[column_name]
        
        stats = {
            'count': self.compute_count(series),
            'mean': self.compute_mean(series),
            'median': self.compute_median(series),
            'mode': self.compute_mode(series),
            'min': self.compute_min(series),
            'max': self.compute_max(series),
            'std_dev': self.compute_std_dev(series),
            'variance': self.compute_variance(series),
            'q1': self.compute_percentile(series, 25),
            'q2': self.compute_percentile(series, 50),
            'q3': self.compute_percentile(series, 75),
            'range': self.compute_range(series)
        }
        
        return stats
    
    def compute_dataset_summary(self) -> Dict[str, Any]:
        """
        Compute dataset-level statistics.
        
        Returns:
            dict: Dataset summary statistics
        """
        total_columns = len(self.df.columns)
        numeric_columns = len(self.numerical_columns)
        
        # Calculate overall missing percentage
        total_cells = self.df.shape[0] * self.df.shape[1]
        missing_cells = self.df.isnull().sum().sum()
        overall_missing_percentage = round((missing_cells / total_cells * 100), 2) if total_cells > 0 else 0
        
        # Identify zero variance and high variance columns
        zero_variance_columns = []
        high_variance_columns = []
        
        # Define high variance threshold (arbitrary: variance > 10000)
        HIGH_VARIANCE_THRESHOLD = 10000
        
        for col in self.numerical_columns:
            variance = self.compute_variance(self.df[col])
            
            if variance is not None:
                if variance == 0:
                    zero_variance_columns.append(col)
                elif variance > HIGH_VARIANCE_THRESHOLD:
                    high_variance_columns.append(col)
        
        summary = {
            'total_columns': total_columns,
            'numeric_columns': numeric_columns,
            'overall_missing_percentage': overall_missing_percentage,
            'zero_variance_columns': len(zero_variance_columns),
            'high_variance_columns': len(high_variance_columns),
            'zero_variance_column_names': zero_variance_columns,
            'high_variance_column_names': high_variance_columns
        }
        
        return summary
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get complete statistics for the dataset.
        
        This is the main method that computes all statistics.
        
        Returns:
            dict: Complete statistics including dataset summary and column statistics
        """
        try:
            # Check if there are any numerical columns
            if len(self.numerical_columns) == 0:
                return {
                    'status': 'no_numerical_columns',
                    'message': 'No numerical columns found in the dataset.',
                    'dataset_summary': {
                        'total_columns': len(self.df.columns),
                        'numeric_columns': 0
                    },
                    'column_statistics': {}
                }
            
            # Compute dataset summary
            dataset_summary = self.compute_dataset_summary()
            
            # Compute statistics for each numerical column
            column_statistics = {}
            
            for col in self.numerical_columns:
                column_statistics[col] = self.compute_column_statistics(col)
            
            return {
                'status': 'success',
                'dataset_summary': dataset_summary,
                'column_statistics': column_statistics
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'error_message': str(e)
            }
