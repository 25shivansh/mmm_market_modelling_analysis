# Marketing Intelligence System - Marketing Mix Modeling (MMM)

## Overview
This project implements a comprehensive Marketing Mix Modeling (MMM) system to analyze the impact of various marketing channels on sales performance in India.

## Project Structure

```
Marketing-Intelligence-System/
│
├── data/
│   ├── raw/
│   │   └── synthetic_mmm_weekly_india.csv
│   └── processed/
│       ├── cleaned_data.csv
│       ├── feature_engineered_data.csv
│       └── robyn_input.csv
│
├── notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_Feature_Engineering.ipynb
│   ├── 05_Baseline_Model.ipynb
│   ├── 06_Robyn_Preparation.ipynb
│   └── 07_Robyn_MMM.ipynb
│
├── reports/
│   ├── dataset_report.pdf
│   ├── eda_report.pdf
│   ├── correlation_analysis.pdf
│   ├── baseline_model_report.pdf
│   └── mmm_report.pdf
│
├── models/
│   ├── linear_regression.pkl
│   └── robyn_model/
│
├── src/
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── train_baseline.py
│   └── robyn_pipeline.py
│
└── README.md
```

## Notebooks

### 01_Data_Understanding
Initial exploration of the synthetic MMM dataset including shape, data types, and basic statistics.

### 02_Data_Cleaning
Data cleaning and preprocessing including handling missing values, outliers, and data validation.

### 03_EDA
Exploratory Data Analysis with visualizations, correlation analysis, and distribution plots.

### 04_Feature_Engineering
Creation of advanced features including lagged variables, rolling averages, and normalized features.

### 05_Baseline_Model
Training and evaluation of baseline linear regression model to establish performance benchmarks.

### 06_Robyn_Preparation
Preparation of data for Robyn MMM including adstock calculations and data formatting.

### 07_Robyn_MMM
Implementation and analysis of Robyn Marketing Mix Model with advanced insights.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Start with `01_Data_Understanding.ipynb` to explore the data
2. Run `02_Data_Cleaning.ipynb` to preprocess the data
3. Continue through the notebooks sequentially for EDA, feature engineering, and modeling

## Data

- **Raw Data**: `data/raw/synthetic_mmm_weekly_india.csv`
  - Contains weekly marketing spend and sales data for multiple channels
  - Marketing channels: TV, Radio, Digital, Out-of-Home (OOP)

## Technologies

- Python 3.8+
- Pandas, NumPy for data manipulation
- Scikit-learn for baseline modeling
- Robyn for advanced MMM
- Matplotlib, Seaborn for visualization

## Authors

Marketing Intelligence Team

## License

MIT License
