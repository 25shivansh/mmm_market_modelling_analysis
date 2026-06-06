"""
Robyn Pipeline Module

This module contains functions for preparing data and running
Robyn Marketing Mix Model analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


def prepare_robyn_input(df: pd.DataFrame, 
                       date_column: str = 'date',
                       target_column: str = 'sales',
                       media_columns: List[str] = None) -> pd.DataFrame:
    """
    Prepare data for Robyn MMM model.
    
    Args:
        df: Input DataFrame
        date_column: Name of date column
        target_column: Name of target/sales column
        media_columns: List of media spend columns
        
    Returns:
        DataFrame formatted for Robyn MMM
    """
    robyn_df = df.copy()
    
    # Ensure date column is datetime
    if date_column in robyn_df.columns:
        robyn_df[date_column] = pd.to_datetime(robyn_df[date_column])
    
    return robyn_df


def validate_robyn_data(df: pd.DataFrame, 
                       required_columns: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that data meets Robyn requirements.
    
    Args:
        df: Input DataFrame
        required_columns: List of required column names
        
    Returns:
        Tuple of (is_valid, list of missing columns)
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    is_valid = len(missing_columns) == 0
    
    return is_valid, missing_columns


def calculate_adstock(media_spend: np.ndarray, 
                     decay_rate: float = 0.5,
                     adstock_length: int = 13) -> np.ndarray:
    """
    Calculate adstock effect for media spend.
    
    Args:
        media_spend: Array of media spend values
        decay_rate: Decay rate for adstock effect
        adstock_length: Length of adstock effect
        
    Returns:
        Array of adstocked media values
    """
    adstocked = np.zeros_like(media_spend)
    
    for i in range(len(media_spend)):
        for lag in range(min(adstock_length, i + 1)):
            adstocked[i] += media_spend[i - lag] * (decay_rate ** lag)
    
    return adstocked
