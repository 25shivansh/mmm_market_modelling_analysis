"""
Baseline Model Training Module

This module contains functions for training baseline models
such as linear regression for MMM.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pickle
from typing import Tuple, Dict


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
