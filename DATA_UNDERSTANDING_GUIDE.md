# Data Understanding Analysis Guide

## Overview

This guide explains how to perform comprehensive data understanding analysis on your Market Mix Modeling dataset using the provided Python code.

## Quick Start

### Option 1: Run Jupyter Notebook (Interactive)

1. Open the notebook:
   ```bash
   jupyter notebook notebooks/01_Data_Understanding.ipynb
   ```

2. Run cells sequentially to perform all analyses

3. Generate visualizations and reports automatically

### Option 2: Run Python Script

1. From the project root directory:
   ```bash
   python run_analysis.py
   ```

2. The script will:
   - Load your dataset
   - Perform all 9 analyses
   - Generate visualizations
   - Save findings to `reports/data_understanding_report.txt`

### Option 3: Use Python Module Directly

```python
from src.data_understanding import DataUnderstanding

# Initialize analyzer
analyzer = DataUnderstanding('data/raw/synthetic_mmm_weekly_india.csv')

# Run complete analysis
analyzer.run_complete_analysis('reports')
```

## Analysis Components

### 1. **Load Dataset**
- Reads CSV file into pandas DataFrame
- Validates file and displays basic info
- Checks memory usage

**Output**: DataFrame object ready for analysis

### 2. **Dataset Shape**
- Shows total rows and columns
- Displays memory consumption
- Previews first few records

**Output**: 
- Rows: Number of transactions/records
- Columns: Number of variables
- Memory: Size in MB

### 3. **Data Types**
- Identifies data type of each column
- Categorizes into numeric and categorical
- Shows type distribution

**Output**:
- Object (Categorical): Week, Geo, Brand, SKU
- Float64 (Continuous): Sales, Spend, Impressions
- Int64 (Integer): Flag variables

**Visualization**: Bar chart of data type distribution

### 4. **Missing Values**
- Checks for null/empty values
- Calculates percentage missing
- Identifies columns with data quality issues

**Output**:
- If no missing values: ✓ Clean dataset
- If missing values exist: Lists affected columns

**Business Impact**: Missing values affect model accuracy

### 5. **Duplicate Rows**
- Detects exact duplicate records
- Checks for duplicates by key columns
- Calculates percentage of duplicates

**Output**:
- Total duplicates: Count
- Percentage: Of total dataset
- Duplicate analysis by Week-Geo-Brand-SKU

**Business Impact**: Duplicates inflate apparent sales

### 6. **Unique Values per Column**
- Counts distinct values in each column
- Shows cardinality ratio
- Helps identify categorical vs numeric

**Output**:
- Column names
- Unique value counts
- Data types
- Unique percentage

**Business Interpretation**:
- High unique count → Continuous variable
- Low unique count → Categorical variable

**Visualization**: Bar chart of top 15 columns

### 7. **Summary Statistics**
- Mean, Median, Std Deviation for numeric columns
- Min, Max, 25%, 50%, 75% percentiles
- Identifies outliers and distribution shapes

**Output**: 
- Count: Non-null observations
- Mean: Average value
- Std: Standard deviation
- Min/Max: Range of values
- Percentiles: Distribution quartiles

**Business Interpretation**:
- Sales_Value Mean: Average transaction value
- Standard Deviation: Sales volatility
- Min/Max: Sales range across periods/regions

### 8. **Business Interpretation of Each Column**

Each column is interpreted in business context:

#### **Sales & Revenue Columns**
- `Sales_Units`: Volume metric (units sold)
- `Sales_Value`: Revenue metric (₹)
- `MRP`: List price
- `Net_Price`: Actual selling price (price elasticity)

#### **Promotional Columns**
- `Feature_Flag`: In-store feature presence
- `Display_Flag`: POS display availability
- `TPR_Flag`: Temporary price reduction
- `Trade_Spend`: Trade promotion investment

#### **Media/Advertising Columns**
- `TV_Impressions`: Traditional media reach
- `YouTube_Impressions`: Digital video reach
- `Facebook_Impressions`: Social media reach
- `Instagram_Impressions`: Visual platform reach
- `Print_Readership`: Print media reach
- `Radio_Listenership`: Audio media reach
- `FB_Banner_Content_Score`: Ad quality score
- `IG_Banner_Content_Score`: Ad effectiveness

#### **Distribution Columns**
- `Weighted_Distribution`: Importance-adjusted availability
- `Numeric_Distribution`: % stores stocking
- `TDP`: Total distribution points (count)
- `NOS`: Shelf count (shelf space)

#### **Contextual Columns**
- `CPI`: Inflation/economic context
- `GDP_Growth`: Macroeconomic indicator
- `Festival_Index`: Seasonal demand factor
- `Rainfall_Index`: Weather impact factor

### 9. **Categorical Distribution**
- Value counts for categorical variables
- Percentage distribution
- Bar charts for each category

**Business Insights**:
- Geographic regions: Market coverage
- Brands: Portfolio representation
- SKUs: Product mix diversity

**Visualization**: Bar charts for each categorical column

### 10. **Numerical Distribution**
- Histograms for key metrics
- Distribution shape (normal, skewed, etc.)
- Identifies potential outliers

**Visualization**: Histograms of 8 key numerical variables

### 11. **Generate Report**
- Comprehensive text report
- Saves to `reports/data_understanding_report.txt`
- Contains all findings and metrics

## Key Metrics Explained

### Sales Metrics
- **Total Sales Value**: Cumulative revenue
- **Average Sales Value**: Mean transaction
- **Sales Range**: Min to Max sales

### Media Metrics
- **TV Impressions**: Traditional advertising reach
- **Digital Impressions**: YouTube/Facebook/Instagram combined
- **Total Media Investment**: Sum of all media spends

### Distribution Metrics
- **Numeric Distribution**: Market penetration (%)
- **TDP**: Store count (actual distribution points)
- **Shelf Space**: NOS (shelf allocation)

### Economic Indicators
- **GDP Growth**: Economic cycle phase
- **CPI**: Inflation level
- **Festival Index**: Seasonal factor
- **Rainfall**: Weather impact

## Output Files

### 1. Text Report
**Location**: `reports/data_understanding_report.txt`

**Contents**:
- Executive summary
- Data quality metrics
- Key statistics
- Column interpretations
- Geographic & brand analysis

### 2. Visualizations
**Location**: `reports/data_understanding_visualizations.png`

**Charts**:
- Data types distribution
- Missing values analysis
- Unique values by column
- Numerical summary statistics

**Location**: `reports/categorical_distribution.png`

**Charts**:
- Value distributions for categorical variables
- Geographic regions breakdown
- Brand distribution
- SKU representation

## Usage Example in Your Analysis

```python
# Step 1: Exploratory Analysis
from src.data_understanding import DataUnderstanding

analyzer = DataUnderstanding('data/raw/synthetic_mmm_weekly_india.csv')
df = analyzer.load_data()

# Step 2: Check Quality
print(f"Rows: {analyzer.get_shape()[0]}")
print(f"Missing: {len(analyzer.get_missing_values())} columns affected")
print(f"Duplicates: {analyzer.get_duplicate_rows()}")

# Step 3: Understand Variables
unique_vals = analyzer.get_unique_values()
interpretations = analyzer.get_business_interpretation()

# Step 4: Generate Report
analyzer.run_complete_analysis()
```

## Business Questions Answered

### Market Understanding
- ✓ How many regions do we operate in?
- ✓ What's the sales range across different periods?
- ✓ Which brands perform best?

### Data Quality
- ✓ Are there any data issues (missing/duplicates)?
- ✓ What's the data completeness percentage?
- ✓ Is the dataset suitable for modeling?

### Variable Analysis
- ✓ Which variables are continuous vs categorical?
- ✓ What are the typical values for each variable?
- ✓ Are there any unusual distributions?

### Marketing Mix
- ✓ How much is spent on each media channel?
- ✓ How many impressions do we get?
- ✓ What's the promotional activity level?

## Next Steps

After completing data understanding:

1. **Move to Data Cleaning** → Notebook 02
   - Handle any identified issues
   - Standardize formats
   - Handle outliers

2. **Proceed to EDA** → Notebook 03
   - Correlation analysis
   - Trend analysis
   - Seasonal patterns

3. **Feature Engineering** → Notebook 04
   - Create derived features
   - Time lags and rolling averages
   - Feature scaling

## Tips & Best Practices

1. **Always start with data understanding** - Never skip this step
2. **Review missing values first** - Critical for model building
3. **Check data types** - Ensures correct analysis
4. **Understand business context** - Essential for interpretation
5. **Save reports** - Document all findings for reference
6. **Visualize distributions** - Spot patterns visually

## Troubleshooting

### Issue: Module not found error
**Solution**: Add `src/` to Python path or run from project root

### Issue: File not found error
**Solution**: Ensure CSV file is at `data/raw/synthetic_mmm_weekly_india.csv`

### Issue: Memory error with large dataset
**Solution**: Read data in chunks or increase available memory

### Issue: Visualization not displaying
**Solution**: Ensure matplotlib backend is set correctly: `matplotlib.use('TkAgg')`

## Support

For issues or questions about the analysis:
1. Check the generated report for insights
2. Review visualizations for patterns
3. Examine individual column statistics
4. Refer to business interpretations for context
