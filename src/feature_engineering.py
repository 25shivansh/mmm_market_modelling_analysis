"""
Feature Engineering Module

This module contains functions for creating and transforming features
for marketing mix modeling.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple


def create_lagged_features(df: pd.DataFrame, columns: List[str], 
                          lags: List[int]) -> pd.DataFrame:
    """
    Create lagged features for time series data.
    
    Args:
        df: Input DataFrame
        columns: List of column names to create lags for
        lags: List of lag values
        
    Returns:
        DataFrame with lagged features added
    """
    df_lagged = df.copy()
    
    for col in columns:
        for lag in lags:
            df_lagged[f'{col}_lag_{lag}'] = df_lagged[col].shift(lag)
    
    return df_lagged


def create_rolling_features(df: pd.DataFrame, columns: List[str], 
                           window_sizes: List[int]) -> pd.DataFrame:
    """
    Create rolling window features (mean, std, etc.)
    
    Args:
        df: Input DataFrame
        columns: List of column names to create rolling features for
        window_sizes: List of window sizes
        
    Returns:
        DataFrame with rolling features added
    """
    df_rolling = df.copy()
    
    for col in columns:
        for window in window_sizes:
            df_rolling[f'{col}_rolling_mean_{window}'] = df_rolling[col].rolling(window).mean()
            df_rolling[f'{col}_rolling_std_{window}'] = df_rolling[col].rolling(window).std()
    
    return df_rolling


def normalize_features(df: pd.DataFrame, columns: List[str], 
                      method: str = 'minmax') -> Tuple[pd.DataFrame, dict]:
    """
    Normalize features using specified method.
    
    Args:
        df: Input DataFrame
        columns: List of column names to normalize
        method: Normalization method ('minmax', 'zscore')
        
    Returns:
        Tuple of (normalized DataFrame, scaling parameters)
    """
    df_normalized = df.copy()
    scaling_params = {}
    
    if method == 'minmax':
        for col in columns:
            min_val = df_normalized[col].min()
            max_val = df_normalized[col].max()
            df_normalized[col] = (df_normalized[col] - min_val) / (max_val - min_val)
            scaling_params[col] = {'min': min_val, 'max': max_val}
    
    return df_normalized, scaling_params
