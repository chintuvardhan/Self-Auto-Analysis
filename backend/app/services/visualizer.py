"""
Visualization Engine Service
Phase 3: Automatic Chart Generation

This module generates visualizations using rule-based logic.
All chart types are determined by hardcoded rules - NO AI APIs.

Charts are generated using Plotly for interactive visualizations.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
from collections import Counter


class VisualizationEngine:
    """
    A service class for generating data visualizations.
    
    This class applies hardcoded rules to automatically select and generate
    appropriate charts based on column types and data characteristics.
    """
    
    def __init__(self, df: pd.DataFrame, profile_data: Dict[str, Any], statistics_data: Optional[Dict[str, Any]] = None):
        """
        Initialize the visualization engine.
        
        Args:
            df: Pandas DataFrame containing the dataset
            profile_data: Profile metadata from the profiler service
            statistics_data: Statistics metadata from the statistics service (optional)
        """
        self.df = df
        self.profile_data = profile_data
        self.statistics_data = statistics_data or {}
        self.charts = []
        
        # Light mode color scheme
        self.colors = {
            'primary': '#0ea5e9',
            'secondary': '#8b5cf6',
            'accent': '#ec4899',
            'success': '#10b981'
        }
    
    def _get_columns_by_type(self, semantic_type: str) -> List[str]:
        """
        Get list of columns with a specific semantic type.
        
        Args:
            semantic_type: The semantic type to filter by
        
        Returns:
            list: Column names matching the semantic type
        """
        columns = []
        for col_info in self.profile_data.get('columns', []):
            if col_info.get('semantic_type') == semantic_type:
                columns.append(col_info['name'])
        return columns
    
    def generate_histogram(self, column: str) -> Dict[str, Any]:
        """
        Generate a histogram for a numerical column.
        
        Rule: Show distribution of values
        
        Args:
            column: Name of the numerical column
        
        Returns:
            dict: Chart configuration
        """
        data = self.df[column].dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data,
            marker_color=self.colors['primary'],
            opacity=0.8,
            name=column
        ))
        
        fig.update_layout(
            title=f"{column} Distribution",
            xaxis_title=column,
            yaxis_title="Frequency",
            template="plotly_white",
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='rgba(248,250,252,1)',
            font=dict(color='#0f172a')
        )
        
        return {
            'id': f"{column}_histogram",
            'type': 'histogram',
            'columns': [column],
            'title': f"{column} Distribution",
            'plotly_config': fig.to_dict()
        }
    
    def generate_boxplot(self, column: str) -> Dict[str, Any]:
        """
        Generate a box plot for a numerical column.
        
        Rule: Show spread, quartiles, and outliers
        
        Args:
            column: Name of the numerical column
        
        Returns:
            dict: Chart configuration
        """
        data = self.df[column].dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=data,
            name=column,
            marker_color=self.colors['secondary'],
            boxmean='sd'  # Show mean and standard deviation
        ))
        
        fig.update_layout(
            title=f"{column} Box Plot",
            yaxis_title=column,
            template="plotly_white",
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='rgba(248,250,252,1)',
            font=dict(color='#0f172a'),
            showlegend=False
        )
        
        return {
            'id': f"{column}_boxplot",
            'type': 'boxplot',
            'columns': [column],
            'title': f"{column} Box Plot",
            'plotly_config': fig.to_dict()
        }
    
    def generate_bar_chart(self, column: str) -> Dict[str, Any]:
        """
        Generate a bar chart for a categorical column.
        
        Rule: Show top 10 categories by frequency
        
        Args:
            column: Name of the categorical column
        
        Returns:
            dict: Chart configuration
        """
        # Count value frequencies
        value_counts = self.df[column].value_counts().head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=value_counts.index.astype(str),
            y=value_counts.values,
            marker_color=self.colors['accent'],
            text=value_counts.values,
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f"Top 10 {column} Categories",
            xaxis_title=column,
            yaxis_title="Count",
            template="plotly_white",
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='rgba(248,250,252,1)',
            font=dict(color='#0f172a')
        )
        
        return {
            'id': f"{column}_bar",
            'type': 'bar',
            'columns': [column],
            'title': f"Top 10 {column} Categories",
            'plotly_config': fig.to_dict()
        }
    
    def generate_line_chart(self, column: str) -> Dict[str, Any]:
        """
        Generate a line chart for a datetime column.
        
        Rule: Show record count over time
        
        Args:
            column: Name of the datetime column
        
        Returns:
            dict: Chart configuration
        """
        # Convert to datetime if not already
        try:
            datetime_data = pd.to_datetime(self.df[column], errors='coerce')
            datetime_data = datetime_data.dropna()
            
            # Group by date and count
            counts = datetime_data.value_counts().sort_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=counts.index,
                y=counts.values,
                mode='lines+markers',
                line=dict(color=self.colors['primary'], width=2),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title=f"{column} Over Time",
                xaxis_title=column,
                yaxis_title="Count",
                template="plotly_white",
                paper_bgcolor='rgba(255,255,255,0)',
                plot_bgcolor='rgba(248,250,252,1)',
                font=dict(color='#0f172a')
            )
            
            return {
                'id': f"{column}_line",
                'type': 'line',
                'columns': [column],
                'title': f"{column} Over Time",
                'plotly_config': fig.to_dict()
            }
        except Exception as e:
            return None
    
    def generate_scatter_plot(self, col1: str, col2: str) -> Optional[Dict[str, Any]]:
        """
        Generate a scatter plot for two numerical columns.
        
        Rule: Only if both columns have > 30 non-null values
        
        Args:
            col1: First numerical column
            col2: Second numerical column
        
        Returns:
            dict: Chart configuration, or None if criteria not met
        """
        # Check if both columns have enough data
        data1 = self.df[col1].dropna()
        data2 = self.df[col2].dropna()
        
        if len(data1) < 30 or len(data2) < 30:
            return None
        
        # Get common indices (rows where both columns have values)
        common_data = self.df[[col1, col2]].dropna()
        
        if len(common_data) < 30:
            return None
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=common_data[col1],
            y=common_data[col2],
            mode='markers',
            marker=dict(
                color=self.colors['secondary'],
                size=8,
                opacity=0.6
            )
        ))
        
        fig.update_layout(
            title=f"{col1} vs {col2}",
            xaxis_title=col1,
            yaxis_title=col2,
            template="plotly_white",
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='rgba(248,250,252,1)',
            font=dict(color='#0f172a')
        )
        
        return {
            'id': f"{col1}_{col2}_scatter",
            'type': 'scatter',
            'columns': [col1, col2],
            'title': f"{col1} vs {col2}",
            'plotly_config': fig.to_dict()
        }
    
    def generate_missing_values_chart(self) -> Dict[str, Any]:
        """
        Generate a bar chart showing missing values per column.
        
        Dataset-level chart.
        
        Returns:
            dict: Chart configuration
        """
        missing_counts = self.df.isnull().sum()
        missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=False)
        
        if len(missing_counts) == 0:
            # No missing values
            return None
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=missing_counts.index.astype(str),
            y=missing_counts.values,
            marker_color=self.colors['success'],
            text=missing_counts.values,
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Missing Values by Column",
            xaxis_title="Column",
            yaxis_title="Missing Count",
            template="plotly_white",
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='rgba(248,250,252,1)',
            font=dict(color='#0f172a')
        )
        
        return {
            'id': 'missing_values_chart',
            'type': 'bar',
            'columns': list(missing_counts.index),
            'title': 'Missing Values by Column',
            'plotly_config': fig.to_dict()
        }
    
    def generate_datatype_distribution(self) -> Dict[str, Any]:
        """
        Generate a pie chart showing distribution of semantic data types.
        
        Dataset-level chart.
        
        Returns:
            dict: Chart configuration
        """
        # Count semantic types
        type_counts = {}
        for col_info in self.profile_data.get('columns', []):
            semantic_type = col_info.get('semantic_type', 'unknown')
            type_counts[semantic_type] = type_counts.get(semantic_type, 0) + 1
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=list(type_counts.keys()),
            values=list(type_counts.values()),
            marker=dict(colors=[
                self.colors['primary'],
                self.colors['secondary'],
                self.colors['accent'],
                self.colors['success']
            ])
        ))
        
        fig.update_layout(
            title="Data Type Distribution",
            template="plotly_white",
            paper_bgcolor='rgba(255,255,255,0)',
            font=dict(color='#0f172a')
        )
        
        return {
            'id': 'datatype_distribution',
            'type': 'pie',
            'columns': [],
            'title': 'Data Type Distribution',
            'plotly_config': fig.to_dict()
        }
    
    def generate_all_charts(self) -> List[Dict[str, Any]]:
        """
        Generate all applicable charts based on hardcoded rules.
        
        This is the main method that applies all visualization rules.
        
        Returns:
            list: List of chart configurations
        """
        charts = []
        
        # Rule 1: Histograms and Box Plots for numerical columns
        numerical_cols = self._get_columns_by_type('numerical')
        for col in numerical_cols:
            # Histogram
            charts.append(self.generate_histogram(col))
            # Box plot
            charts.append(self.generate_boxplot(col))
        
        # Rule 2: Bar charts for categorical columns
        categorical_cols = self._get_columns_by_type('categorical')
        for col in categorical_cols:
            charts.append(self.generate_bar_chart(col))
        
        # Rule 3: Line charts for datetime columns
        datetime_cols = self._get_columns_by_type('datetime')
        for col in datetime_cols:
            line_chart = self.generate_line_chart(col)
            if line_chart:
                charts.append(line_chart)
        
        # Rule 4: Scatter plots for numerical column pairs (max 3 pairs)
        if len(numerical_cols) >= 2:
            pair_count = 0
            for i in range(len(numerical_cols)):
                for j in range(i + 1, len(numerical_cols)):
                    if pair_count >= 3:
                        break
                    scatter = self.generate_scatter_plot(numerical_cols[i], numerical_cols[j])
                    if scatter:
                        charts.append(scatter)
                        pair_count += 1
                if pair_count >= 3:
                    break
        
        # Rule 5: Dataset-level charts
        missing_chart = self.generate_missing_values_chart()
        if missing_chart:
            charts.append(missing_chart)
        
        charts.append(self.generate_datatype_distribution())
        
        return charts
    
    def get_visualizations(self) -> Dict[str, Any]:
        """
        Get all visualizations for the dataset.
        
        Returns:
            dict: Complete visualization data
        """
        try:
            charts = self.generate_all_charts()
            
            return {
                'status': 'success',
                'chart_count': len(charts),
                'charts': charts
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'error_message': str(e),
                'charts': []
            }
