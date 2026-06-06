"""
Data Preprocessing Module

This module contains functions for loading, cleaning, and preprocessing
marketing mix modeling data.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data from CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the loaded data
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None


def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df: Input DataFrame
        strategy: Strategy for handling missing values ('mean', 'median', 'drop')
        
    Returns:
        DataFrame with missing values handled
    """
    if strategy == 'drop':
        return df.dropna()
    elif strategy in ['mean', 'median']:
        return df.fillna(df.agg(strategy))
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def remove_outliers(df: pd.DataFrame, columns: list, method: str = 'iqr') -> pd.DataFrame:
    """
    Remove outliers from specified columns.
    
    Args:
        df: Input DataFrame
        columns: List of column names to check for outliers
        method: Method for outlier detection ('iqr', 'zscore')
        
    Returns:
        DataFrame with outliers removed
    """
    df_clean = df.copy()
    
    if method == 'iqr':
        for col in columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            df_clean = df_clean[(df_clean[col] >= Q1 - 1.5 * IQR) & 
                               (df_clean[col] <= Q3 + 1.5 * IQR)]
    
    return df_clean
