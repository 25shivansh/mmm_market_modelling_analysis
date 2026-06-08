"""
Baseline Model Training Module

This module contains functions for training baseline models
such as linear regression for MMM.
"""

import os
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pickle
from typing import Tuple, Dict, List
 
from feature_engineering import prepare_feature_importance_data


def train_linear_regression(X: pd.DataFrame, y: pd.Series, 
                           test_size: float = 0.2,
                           random_state: int = 42) -> Tuple[LinearRegression, Dict]:
    """
    Train a linear regression model.
    
    Args:
        X: Feature matrix
        y: Target variable
        test_size: Proportion of data for testing
        random_state: Random state for reproducibility
        
    Returns:
        Tuple of (trained model, evaluation metrics)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'train_r2': r2_score(y_train, y_pred_train),
        'test_r2': r2_score(y_test, y_pred_test),
        'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
        'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
        'train_mae': mean_absolute_error(y_train, y_pred_train),
        'test_mae': mean_absolute_error(y_test, y_pred_test)
    }
    
    return model, metrics


def save_model(model: LinearRegression, filepath: str) -> None:
    """
    Save trained model to disk.
    
    Args:
        model: Trained model
        filepath: Path to save the model
    """
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {filepath}")


def load_model(filepath: str) -> LinearRegression:
    """
    Load trained model from disk.
    
    Args:
        filepath: Path to the saved model
        
    Returns:
        Loaded model
    """
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded from {filepath}")
    return model


def coefficients_df(model: LinearRegression, feature_names: List[str]) -> pd.DataFrame:
    """
    Return a DataFrame of feature coefficients.
    """
    coefs = np.asarray(model.coef_).ravel()
    df = pd.DataFrame({
        'feature': feature_names,
        'coefficient': coefs,
        'abs_coefficient': np.abs(coefs)
    })
    df = df.sort_values('abs_coefficient', ascending=False).reset_index(drop=True)
    return df


def plot_feature_importance(coef_df: pd.DataFrame, output_path: str, top_n: int = 20) -> str:
    """
    Save a bar plot of top_n feature importances (by absolute coefficient).
    Returns the filepath of the saved image.
    """
    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_file = out_dir / 'feature_importance.png'

    top = coef_df.head(top_n).iloc[::-1]
    plt.figure(figsize=(8, max(4, top_n * 0.25)))
    colors = ['green' if v >= 0 else 'red' for v in top['coefficient']]
    plt.barh(top['feature'], top['coefficient'], color=colors)
    plt.xlabel('Coefficient')
    plt.title(f'Top {top_n} Feature Coefficients')
    plt.tight_layout()
    plt.savefig(plot_file, dpi=150)
    plt.close()
    return str(plot_file)


def train_baseline_pipeline(input_path: str,
                            output_dir: str,
                            target_col: str = 'Sales_Value',
                            id_columns: List[str] = None,
                            test_size: float = 0.2,
                            random_state: int = 42,
                            top_n_features: int = 20) -> Dict:
    """
    Complete baseline training pipeline using Linear Regression.

    Steps:
      - Load feature-engineered data
      - Prepare numeric features and target (uses prepare_feature_importance_data)
      - Train/test split
      - Fit LinearRegression
      - Compute R2, RMSE, MAE
      - Save model, coefficients CSV, importance plot, and interpretation text

    Returns a dictionary with paths and metrics.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    df = pd.read_csv(input_path)

    # Prepare numeric dataset
    id_columns = id_columns or ['Week', 'Geo', 'Brand', 'SKU']
    prepared, feature_columns = prepare_feature_importance_data(df, target_col=target_col, id_columns=id_columns)

    X = prepared[feature_columns].fillna(0)
    y = prepared[target_col].astype(float).fillna(0)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Metrics
    metrics = {
        'train_r2': float(r2_score(y_train, y_pred_train)),
        'test_r2': float(r2_score(y_test, y_pred_test)),
        'train_rmse': float(np.sqrt(mean_squared_error(y_train, y_pred_train))),
        'test_rmse': float(np.sqrt(mean_squared_error(y_test, y_pred_test))),
        'train_mae': float(mean_absolute_error(y_train, y_pred_train)),
        'test_mae': float(mean_absolute_error(y_test, y_pred_test))
    }

    # Coefficients
    coef_df = coefficients_df(model, feature_columns)
    coef_csv = output_dir / 'feature_coefficients.csv'
    coef_df.to_csv(coef_csv, index=False)

    # Plot
    plot_file = plot_feature_importance(coef_df, str(output_dir), top_n=top_n_features)

    # Save model
    model_file = output_dir / 'linear_regression_model.pkl'
    save_model(model, str(model_file))

    # Business interpretation (simple automated summary)
    top_pos = coef_df[coef_df['coefficient'] > 0].head(5)
    top_neg = coef_df[coef_df['coefficient'] < 0].head(5)

    total_abs = coef_df['abs_coefficient'].sum() if coef_df['abs_coefficient'].sum() != 0 else 1.0

    interpretation_lines = []
    interpretation_lines.append('Baseline Linear Regression — Business Interpretation')
    interpretation_lines.append('')
    interpretation_lines.append('Model performance:')
    for k, v in metrics.items():
        interpretation_lines.append(f'- {k}: {v:.4f}')
    interpretation_lines.append('')
    interpretation_lines.append('Top positive drivers:')
    for _, r in top_pos.iterrows():
        pct = 100.0 * r['abs_coefficient'] / total_abs
        interpretation_lines.append(f"- {r['feature']}: coef={r['coefficient']:.4f} ({pct:.2f}% of total impact)")
    interpretation_lines.append('')
    interpretation_lines.append('Top negative drivers:')
    for _, r in top_neg.iterrows():
        pct = 100.0 * r['abs_coefficient'] / total_abs
        interpretation_lines.append(f"- {r['feature']}: coef={r['coefficient']:.4f} ({pct:.2f}% of total impact)")
    interpretation_lines.append('')
    interpretation_lines.append('Notes: Coefficients are from an unconstrained linear model and represent short-term linear associations. Interpret with caution; run causal or experimental analysis for causal claims.')

    interp_file = output_dir / 'business_interpretation.txt'
    interp_file.write_text('\n'.join(interpretation_lines))

    # Save metrics
    metrics_file = output_dir / 'metrics.json'
    pd.Series(metrics).to_json(metrics_file)

    return {
        'model_file': str(model_file),
        'coefficients_csv': str(coef_csv),
        'plot_file': str(plot_file),
        'interpretation_file': str(interp_file),
        'metrics_file': str(metrics_file),
        'metrics': metrics
    }
