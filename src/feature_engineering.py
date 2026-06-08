"""
Feature Engineering Module

This module contains functions for creating and transforming features
for marketing mix modeling.
"""

from pathlib import Path

import pandas as pd
import numpy as np
from typing import List, Tuple


DEFAULT_MEDIA_COLUMNS = [
    'TV_Impressions',
    'YouTube_Impressions',
    'Facebook_Impressions',
    'Instagram_Impressions',
    'Print_Readership',
    'Radio_Listenership'
]

DEFAULT_PROMOTION_COLUMNS = [
    'Feature_Flag',
    'Display_Flag',
    'TPR_Flag'
]

DEFAULT_GROUP_COLUMNS = ['Geo', 'Brand', 'SKU']
DEFAULT_TIME_COLUMN = 'Week'


def _sort_for_time_series(df: pd.DataFrame,
                          time_col: str = DEFAULT_TIME_COLUMN,
                          group_cols: List[str] = None) -> pd.DataFrame:
    """Return a copy sorted so time-series transforms stay aligned."""
    working_df = df.copy()

    if time_col in working_df.columns:
        working_df[time_col] = pd.to_datetime(working_df[time_col], errors='coerce')

    sort_columns = []
    if group_cols:
        sort_columns.extend([col for col in group_cols if col in working_df.columns])
    if time_col in working_df.columns:
        sort_columns.append(time_col)

    if sort_columns:
        working_df = working_df.sort_values(sort_columns)

    return working_df


def _to_numeric_flag(series: pd.Series) -> pd.Series:
    """Convert boolean-like values to 0/1 integers."""
    if series.dtype == bool:
        return series.astype(int)

    normalized = series.astype(str).str.lower().str.strip()
    return normalized.map({'true': 1, 'false': 0, '1': 1, '0': 0}).fillna(0).astype(int)


def create_total_media_exposure(df: pd.DataFrame,
                                media_columns: List[str] = None,
                                output_col: str = 'Total_Media_Exposure') -> pd.DataFrame:
    """
    Create a total media exposure feature from all available media columns.
    """
    df_media = df.copy()
    media_columns = media_columns or DEFAULT_MEDIA_COLUMNS
    available_columns = [col for col in media_columns if col in df_media.columns]

    if not available_columns:
        df_media[output_col] = 0.0
        return df_media

    df_media[output_col] = df_media[available_columns].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)
    return df_media


def create_promotion_score(df: pd.DataFrame,
                           promotion_columns: List[str] = None,
                           spend_column: str = 'Trade_Spend',
                           output_col: str = 'Promotion_Score') -> pd.DataFrame:
    """
    Create a promotion score from promo flags and trade spend.
    """
    df_promo = df.copy()
    promotion_columns = promotion_columns or DEFAULT_PROMOTION_COLUMNS
    available_flags = [col for col in promotion_columns if col in df_promo.columns]

    flag_score = pd.Series(0.0, index=df_promo.index)
    if available_flags:
        flag_score = df_promo[available_flags].apply(_to_numeric_flag).mean(axis=1)

    if spend_column in df_promo.columns:
        spend_values = pd.to_numeric(df_promo[spend_column], errors='coerce').fillna(0)
        spend_score = np.log1p(spend_values)
        spend_min = spend_score.min()
        spend_max = spend_score.max()
        if spend_max > spend_min:
            spend_score = (spend_score - spend_min) / (spend_max - spend_min)
        else:
            spend_score = pd.Series(0.0, index=df_promo.index)
    else:
        spend_score = pd.Series(0.0, index=df_promo.index)

    df_promo[output_col] = 100.0 * (0.5 * flag_score + 0.5 * spend_score)
    return df_promo


def create_lagged_features(df: pd.DataFrame, columns: List[str], 
                          lags: List[int],
                          group_cols: List[str] = None,
                          time_col: str = DEFAULT_TIME_COLUMN) -> pd.DataFrame:
    """
    Create lagged features for time series data.
    
    Args:
        df: Input DataFrame
        columns: List of column names to create lags for
        lags: List of lag values
        
    Returns:
        DataFrame with lagged features added
    """
    df_lagged = _sort_for_time_series(df, time_col=time_col, group_cols=group_cols)
    available_columns = [col for col in columns if col in df_lagged.columns]

    if group_cols:
        group_keys = [col for col in group_cols if col in df_lagged.columns]
        grouped = df_lagged.groupby(group_keys, sort=False)
    else:
        grouped = None
    
    for col in available_columns:
        for lag in lags:
            lag_col = f'{col}_lag_{lag}'
            if grouped is not None:
                df_lagged[lag_col] = grouped[col].shift(lag)
            else:
                df_lagged[lag_col] = df_lagged[col].shift(lag)
    
    return df_lagged


def create_rolling_features(df: pd.DataFrame, columns: List[str], 
                           window_sizes: List[int],
                           group_cols: List[str] = None,
                           time_col: str = DEFAULT_TIME_COLUMN) -> pd.DataFrame:
    """
    Create rolling window features (mean, std, etc.).
    
    Args:
        df: Input DataFrame
        columns: List of column names to create rolling features for
        window_sizes: List of window sizes
        
    Returns:
        DataFrame with rolling features added
    """
    df_rolling = _sort_for_time_series(df, time_col=time_col, group_cols=group_cols)
    available_columns = [col for col in columns if col in df_rolling.columns]

    if group_cols:
        group_keys = [col for col in group_cols if col in df_rolling.columns]
        grouped = df_rolling.groupby(group_keys, sort=False)
    else:
        grouped = None
    
    for col in available_columns:
        for window in window_sizes:
            mean_col = f'{col}_rolling_mean_{window}'
            std_col = f'{col}_rolling_std_{window}'
            if grouped is not None:
                df_rolling[mean_col] = grouped[col].transform(lambda s: s.rolling(window=window, min_periods=1).mean())
                df_rolling[std_col] = grouped[col].transform(lambda s: s.rolling(window=window, min_periods=1).std())
            else:
                df_rolling[mean_col] = df_rolling[col].rolling(window=window, min_periods=1).mean()
                df_rolling[std_col] = df_rolling[col].rolling(window=window, min_periods=1).std()
    
    return df_rolling


def create_interaction_features(df: pd.DataFrame,
                                interaction_pairs: List[Tuple[str, str]] = None) -> pd.DataFrame:
    """
    Create interaction features between important MMM drivers.
    """
    df_interactions = df.copy()
    interaction_pairs = interaction_pairs or [
        ('Total_Media_Exposure', 'Promotion_Score'),
        ('Trade_Spend', 'Total_Media_Exposure'),
        ('Trade_Spend', 'Promotion_Score'),
        ('TV_Impressions', 'YouTube_Impressions')
    ]

    for left_col, right_col in interaction_pairs:
        if left_col in df_interactions.columns and right_col in df_interactions.columns:
            left_values = pd.to_numeric(df_interactions[left_col], errors='coerce').fillna(0)
            right_values = pd.to_numeric(df_interactions[right_col], errors='coerce').fillna(0)
            df_interactions[f'{left_col}_x_{right_col}'] = left_values * right_values

    return df_interactions


def prepare_feature_importance_data(df: pd.DataFrame,
                                    target_col: str = 'Sales_Value',
                                    id_columns: List[str] = None) -> Tuple[pd.DataFrame, List[str]]:
    """
    Prepare a numeric dataset for feature importance analysis.
    """
    id_columns = id_columns or ['Week', 'Geo', 'Brand', 'SKU']
    prepared_df = df.copy()

    for col in prepared_df.select_dtypes(include=['bool']).columns:
        prepared_df[col] = prepared_df[col].astype(int)

    numeric_df = prepared_df.select_dtypes(include=[np.number]).copy()
    if target_col not in numeric_df.columns and target_col in prepared_df.columns:
        numeric_df[target_col] = pd.to_numeric(prepared_df[target_col], errors='coerce')

    if target_col not in numeric_df.columns:
        raise ValueError(f"Target column '{target_col}' is required for feature importance preparation.")

    feature_columns = [
        col for col in numeric_df.columns
        if col != target_col and col not in id_columns
    ]

    return numeric_df[feature_columns + [target_col]].copy(), feature_columns


def build_feature_engineering_pipeline(input_path: str,
                                      output_path: str,
                                      target_col: str = 'Sales_Value',
                                      group_cols: List[str] = None,
                                      lag_columns: List[str] = None,
                                      rolling_columns: List[str] = None,
                                      lag_values: List[int] = None,
                                      rolling_windows: List[int] = None) -> Tuple[pd.DataFrame, List[str]]:
    """
    Run the complete feature-engineering pipeline and save the final dataset.
    """
    group_cols = group_cols or DEFAULT_GROUP_COLUMNS
    lag_values = lag_values or [1, 2, 4]
    rolling_windows = rolling_windows or [4, 12]

    df = pd.read_csv(input_path)
    df = _sort_for_time_series(df, group_cols=group_cols, time_col=DEFAULT_TIME_COLUMN)
    df = create_total_media_exposure(df)
    df = create_promotion_score(df)

    lag_columns = lag_columns or [
        target_col,
        'Total_Media_Exposure',
        'Promotion_Score',
        'Trade_Spend'
    ]
    rolling_columns = rolling_columns or [
        target_col,
        'Total_Media_Exposure',
        'Promotion_Score',
        'Trade_Spend'
    ]

    df = create_lagged_features(df, lag_columns, lag_values, group_cols=group_cols)
    df = create_rolling_features(df, rolling_columns, rolling_windows, group_cols=group_cols)
    df = create_interaction_features(df)

    feature_importance_df, feature_columns = prepare_feature_importance_data(df, target_col=target_col)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    return feature_importance_df, feature_columns


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
