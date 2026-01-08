"""
Insight Rules Engine Service
Phase 4: Pattern Detection & Data Understanding

This module generates deterministic, rule-based insights from data profiling,
statistics, and trends. No AI APIs are used.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class InsightEngine:
    """
    A service class for generating data insights based on deterministic rules.
    """

    def __init__(self, df: pd.DataFrame, profile_data: Dict[str, Any], stats_data: Optional[Dict[str, Any]] = None):
        """
        Initialize the insight engine.

        Args:
            df: Pandas DataFrame containing the dataset
            profile_data: Profile metadata from the profiler service
            stats_data: Statistics metadata from the statistics service (optional)
        """
        self.df = df
        self.profile_data = profile_data
        self.stats_data = stats_data or {}
        self.insights = []

    def generate_insights(self) -> List[Dict[str, Any]]:
        """
        Generate all applicable insights based on hardcoded rules.

        Returns:
            list: List of insight objects
        """
        self.insights = []

        # 1. Data Quality Insights
        self._check_missing_data()
        self._check_constant_columns()
        self._check_sparse_columns()

        # 2. Distribution & Variance Insights
        self._check_high_variability()
        self._check_zero_variance()

        # 3. Category Dominance Insights
        self._check_dominant_categories()
        self._check_high_cardinality()

        # 4. Statistical Anomalies
        self._check_outliers()

        # Rank insights by severity (High -> Medium -> Low)
        severity_map = {"high": 0, "medium": 1, "low": 2}
        self.insights.sort(key=lambda x: severity_map.get(x["severity"], 3))

        return self.insights

    def _add_insight(self, i_type: str, severity: str, title: str, description: str, columns: List[str], metric: str, value: Any, threshold: Any):
        """Helper to add an insight object."""
        self.insights.append({
            "type": i_type,
            "severity": severity,
            "title": title,
            "description": description,
            "columns": columns,
            "evidence": {
                "metric": metric,
                "value": value,
                "threshold": threshold
            }
        })

    # --- Insight Rule Implementations ---

    def _check_missing_data(self):
        """Rule: null_percentage > 30%"""
        for col_info in self.profile_data.get('columns', []):
            null_pct = col_info.get('null_percentage', 0)
            if null_pct > 30:
                self._add_insight(
                    i_type="data_quality",
                    severity="high",
                    title="High Missing Data",
                    description=f"Column '{col_info['name']}' has a significant amount of missing values ({null_pct}%). This may impact the reliability of analysis for this specific attribute.",
                    columns=[col_info['name']],
                    metric="null_percentage",
                    value=null_pct,
                    threshold=30
                )

    def _check_constant_columns(self):
        """Rule: unique_count == 1"""
        for col_info in self.profile_data.get('columns', []):
            if col_info.get('unique_count') == 1:
                self._add_insight(
                    i_type="data_quality",
                    severity="high",
                    title="Constant Column Detected",
                    description=f"Column '{col_info['name']}' contains the same value for every record. It provides no predictive value or differentiation and can likely be removed.",
                    columns=[col_info['name']],
                    metric="unique_count",
                    value=1,
                    threshold=1
                )

    def _check_sparse_columns(self):
        """Rule: non_null_count < 10% of rows"""
        total_rows = self.profile_data.get('total_rows', 1)
        for col_info in self.profile_data.get('columns', []):
            fill_rate = (col_info.get('non_null_count', 0) / total_rows) * 100
            if fill_rate < 10 and col_info.get('unique_count', 0) > 0:
                self._add_insight(
                    i_type="data_quality",
                    severity="medium",
                    title="Sparse Data Column",
                    description=f"Column '{col_info['name']}' is very sparse, with less than 10% of records populated. Analysis on this column might be statistically insignificant.",
                    columns=[col_info['name']],
                    metric="fill_rate",
                    value=round(fill_rate, 2),
                    threshold=10
                )

    def _check_high_variability(self):
        """Rule: std_dev > (mean * 2.0)"""
        col_stats = self.stats_data.get('column_statistics', {})
        for col, stats in col_stats.items():
            mean = stats.get('mean', 0)
            std = stats.get('std', 0)
            if mean != 0 and std > (abs(mean) * 2.0):
                self._add_insight(
                    i_type="distribution",
                    severity="medium",
                    title="High Variability",
                    description=f"Numerical values in '{col}' show extreme dispersion. The standard deviation is more than twice the size of the mean, indicating highly volatile data.",
                    columns=[col],
                    metric="coefficient_of_variation",
                    value=round(std / abs(mean), 2),
                    threshold=2.0
                )

    def _check_zero_variance(self):
        """Rule: variance == 0 for numerical"""
        col_stats = self.stats_data.get('column_statistics', {})
        for col, stats in col_stats.items():
            if stats.get('variance') == 0:
                self._add_insight(
                    i_type="distribution",
                    severity="high",
                    title="Zero Variance",
                    description=f"Numerical column '{col}' has zero variance. All populated values are identical, making it redundant for most statistical models.",
                    columns=[col],
                    metric="variance",
                    value=0,
                    threshold=0
                )

    def _check_dominant_categories(self):
        """Rule: Top category > 70% of rows"""
        # This requires looking at top frequencies in categorical columns
        for col_info in self.profile_data.get('columns', []):
            if col_info.get('semantic_type') == 'categorical':
                # Since profiler might not give frequencies directly per-category in metadata yet,
                # we do a quick check on the DF if possible.
                counts = self.df[col_info['name']].value_counts(normalize=True)
                if not counts.empty and counts.iloc[0] > 0.7:
                    self._add_insight(
                        i_type="category",
                        severity="medium",
                        title="Dominant Category",
                        description=f"In column '{col_info['name']}', the category '{counts.index[0]}' accounts for over 70% of the data, potentially creating class imbalance.",
                        columns=[col_info['name']],
                        metric="top_category_share",
                        value=round(counts.iloc[0] * 100, 2),
                        threshold=70
                    )

    def _check_high_cardinality(self):
        """Rule: unique_count > 90% of rows"""
        total_rows = self.profile_data.get('total_rows', 1)
        if total_rows < 10: return # Skip for tiny datasets

        for col_info in self.profile_data.get('columns', []):
            if col_info.get('semantic_type') == 'categorical':
                unique_pct = (col_info.get('unique_count', 0) / total_rows) * 100
                if unique_pct > 90:
                    self._add_insight(
                        i_type="category",
                        severity="low",
                        title="High Cardinality",
                        description=f"'{col_info['name']}' has almost as many unique values as there are rows. This suggests it might be an ID or a unique identifier rather than a grouping category.",
                        columns=[col_info['name']],
                        metric="uniqueness_ratio",
                        value=round(unique_pct, 2),
                        threshold=90
                    )

    def _check_outliers(self):
        """Rule: Values outside 1.5 * IQR"""
        col_stats = self.stats_data.get('column_statistics', {})
        for col, stats in col_stats.items():
            # Get IQR if available
            q1 = stats.get('q1')
            q3 = stats.get('q3')
            count = stats.get('count', 0)
            
            if q1 is not None and q3 is not None and count > 0:
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                # Check for values in DF
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col].dropna()
                if not outliers.empty:
                    outlier_pct = (len(outliers) / count) * 100
                    self._add_insight(
                        i_type="anomaly",
                        severity="medium",
                        title="Potential Outliers",
                        description=f"Numerical column '{col}' contains values that are statistically significant outliers (falling outside 1.5x the Interquartile Range).",
                        columns=[col],
                        metric="outlier_percentage",
                        value=round(outlier_pct, 2),
                        threshold="1.5 * IQR"
                    )

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of insight counts."""
        summary = {"total_insights": len(self.insights), "high": 0, "medium": 0, "low": 0}
        for insight in self.insights:
            summary[insight["severity"]] += 1
        return summary
