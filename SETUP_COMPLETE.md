# Market Mix Modeling - Data Understanding Analysis Package

## 📋 Summary

Complete Python code package for comprehensive data understanding and exploratory analysis of your Market Mix Modeling dataset. Includes reusable modules, executable scripts, interactive notebooks, and detailed documentation.

## 📦 What's Included

### 1. **Python Modules** (`src/`)

#### `data_understanding.py`
- **Class**: `DataUnderstanding`
- **Features**:
  - Load and validate datasets
  - Analyze dataset shape and dimensions
  - Examine data types and distributions
  - Detect missing values and duplicates
  - Calculate unique values per column
  - Generate summary statistics
  - Create business interpretations
  - Produce comprehensive reports
  - Generate visualizations
  
- **Usage**:
  ```python
  from src.data_understanding import DataUnderstanding
  
  analyzer = DataUnderstanding('data/raw/synthetic_mmm_weekly_india.csv')
  analyzer.run_complete_analysis()
  ```

#### `data_preprocessing.py` (Existing)
- Data loading utilities
- Missing value handling
- Outlier removal

#### `feature_engineering.py` (Existing)
- Lagged feature creation
- Rolling statistics
- Feature normalization

#### `train_baseline.py` (Existing)
- Linear regression baseline
- Model evaluation metrics
- Model persistence

#### `robyn_pipeline.py` (Existing)
- Robyn MMM preparation
- Adstock calculations

### 2. **Executable Scripts**

#### `run_analysis.py`
**Purpose**: Standalone script to run complete analysis
**Execution**: `python run_analysis.py`
**Output**:
- Console output of all analyses
- `reports/data_understanding_report.txt`
- `reports/data_understanding_visualizations.png`
- `reports/categorical_distribution.png`

### 3. **Interactive Notebook**

#### `notebooks/01_Data_Understanding.ipynb`
**Purpose**: Jupyter notebook for interactive analysis
**Cells Included** (11 sections):
1. Import required libraries
2. Load dataset
3. Dataset shape analysis
4. Data types distribution
5. Missing values analysis
6. Duplicate rows detection
7. Unique values analysis
8. Summary statistics
9. Business interpretation
10. Categorical distributions
11. Numerical distributions
12. Report generation and saving

**Features**:
- Step-by-step analysis
- Interactive visualizations
- Inline markdown documentation
- Easy to modify and extend

### 4. **Documentation**

#### `DATA_UNDERSTANDING_GUIDE.md`
- Comprehensive analysis guide
- Usage instructions (3 methods)
- Detailed component explanations
- Key metrics definitions
- Business insights
- Output file descriptions
- Next steps for modeling
- Troubleshooting guide

#### `README.md` (Updated)
- Project overview
- Directory structure
- Notebook descriptions
- Installation instructions
- Technology stack

#### `requirements.txt`
- All Python dependencies
- Version specifications
- Easy installation: `pip install -r requirements.txt`

## 🎯 9 Comprehensive Analyses Included

1. **Load Dataset** - CSV import and validation
2. **Dataset Shape** - Dimensions, memory usage, preview
3. **Data Types** - Type distribution and categorization
4. **Missing Values** - Null detection and percentage
5. **Duplicate Rows** - Exact and partial duplicate detection
6. **Unique Values** - Cardinality analysis per column
7. **Summary Statistics** - Mean, median, std, percentiles
8. **Business Interpretation** - Context for each column
9. **Visualizations** - Multiple chart types

## 📊 Output Artifacts

### Text Reports
```
reports/
├── data_understanding_report.txt      # Comprehensive findings
├── data_understanding_visualizations.png # 4-part dashboard
└── categorical_distribution.png       # Category value charts
```

### Notebook Output
- Inline charts and statistics
- Summary tables
- Distribution plots

## 🚀 Three Ways to Use

### Method 1: Jupyter Notebook (Recommended for Exploration)
```bash
cd notebooks
jupyter notebook 01_Data_Understanding.ipynb
```
✅ Interactive, step-by-step
✅ Visualizations in real-time
✅ Easy to modify and experiment

### Method 2: Python Script (Recommended for Automation)
```bash
python run_analysis.py
```
✅ Single command execution
✅ Generates all reports automatically
✅ Scheduled batch analysis

### Method 3: Python Module (Recommended for Integration)
```python
from src.data_understanding import DataUnderstanding

analyzer = DataUnderstanding('data/raw/synthetic_mmm_weekly_india.csv')
df = analyzer.load_data()
report = analyzer.run_complete_analysis()
```
✅ Programmatic control
✅ Integrate into pipelines
✅ Reusable in other projects

## 📈 Visualizations Generated

### 1. **Data Understanding Dashboard** (4 panels)
- Data types distribution (bar chart)
- Top 15 unique value columns (horizontal bars)
- Missing values analysis (bar chart or "No issues" message)
- Numerical summary statistics (table)

### 2. **Categorical Distribution** (6 panels)
- Geographic regions distribution
- Brand distribution
- SKU distribution
- Other categorical variables (top 10 values each)

### 3. **Numerical Distribution** (8 panels)
- Histograms of key metrics:
  - Sales_Units
  - Sales_Value
  - Trade_Spend
  - TV_Impressions
  - YouTube_Impressions
  - Distribution metrics
  - Economic indicators

## 📊 Data Elements Analyzed

### Categorical Variables (4)
- Week, Geo, Brand, SKU

### Sales Metrics (4)
- Sales_Units, Sales_Value, MRP, Net_Price

### Promotional Variables (4)
- Feature_Flag, Display_Flag, TPR_Flag, Trade_Spend

### Media/Advertising (8)
- TV_Impressions, YouTube_Impressions, Facebook_Impressions
- Instagram_Impressions, Print_Readership, Radio_Listenership
- FB_Banner_Content_Score, IG_Banner_Content_Score

### Distribution (4)
- Weighted_Distribution, Numeric_Distribution, TDP, NOS

### Economic/Contextual (4)
- CPI, GDP_Growth, Festival_Index, Rainfall_Index

**Total: 28 Columns Analyzed**

## 💡 Key Features

✅ **Comprehensive**: All 9 required analyses included
✅ **Reusable**: Object-oriented design for code reuse
✅ **Well-documented**: Inline comments and docstrings
✅ **Business-focused**: Each column interpreted in business context
✅ **Visualization-rich**: Multiple chart types for different insights
✅ **Report generation**: Automatic text reports
✅ **Flexible**: 3 different usage methods
✅ **Production-ready**: Error handling and validation

## 🔧 Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run analysis** (choose one method):
   - Notebook: `jupyter notebook notebooks/01_Data_Understanding.ipynb`
   - Script: `python run_analysis.py`
   - Module: See examples above

## 📚 Project Structure

```
MarketMixmodelling/
├── data/
│   ├── raw/
│   │   └── synthetic_mmm_weekly_india.csv
│   └── processed/
├── notebooks/
│   ├── 01_Data_Understanding.ipynb    ← USE THIS
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_EDA.ipynb
│   └── ... (other notebooks)
├── src/
│   ├── data_understanding.py          ← Main module
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── train_baseline.py
│   └── robyn_pipeline.py
├── reports/                           ← Outputs saved here
│   ├── data_understanding_report.txt
│   ├── data_understanding_visualizations.png
│   └── categorical_distribution.png
├── run_analysis.py                    ← Main script
├── requirements.txt                   ← Dependencies
├── README.md                          ← Project overview
└── DATA_UNDERSTANDING_GUIDE.md        ← This guide
```

## 🎓 What You'll Learn

By using this package, you'll understand:

1. **Data Structure**: How many records, variables, and their types
2. **Data Quality**: Missing values, duplicates, completeness
3. **Variable Distributions**: Ranges, patterns, outliers
4. **Business Metrics**: Sales trends, promotional activity, media spend
5. **Geographic Insights**: Regional performance differences
6. **Marketing Mix**: Media channel reach and effectiveness
7. **Economic Context**: External factors affecting sales

## 🚀 Next Steps

After completing this analysis:

1. **Data Cleaning** (Notebook 02)
   - Handle identified issues
   - Standardize and format data
   - Treat outliers

2. **Exploratory Data Analysis** (Notebook 03)
   - Correlation analysis
   - Trend analysis
   - Seasonal patterns

3. **Feature Engineering** (Notebook 04)
   - Create derived features
   - Lag variables
   - Aggregations

4. **Baseline Model** (Notebook 05)
   - Simple linear regression
   - Establish performance baseline

5. **Robyn MMM** (Notebooks 06-07)
   - Advanced marketing mix modeling
   - Media effectiveness analysis

## 📞 Support & Troubleshooting

### Common Issues

**"Module not found"**
- Run from project root directory
- Ensure Python path includes `src/`

**"File not found"**
- Check CSV file location: `data/raw/synthetic_mmm_weekly_india.csv`
- Verify relative paths from working directory

**"Import Error"**
- Install requirements: `pip install -r requirements.txt`
- Update pip: `pip install --upgrade pip`

## 📝 File Manifest

### Created Files
- ✅ `src/data_understanding.py` - Main analysis module
- ✅ `run_analysis.py` - Executable script
- ✅ `notebooks/01_Data_Understanding.ipynb` - Interactive notebook
- ✅ `DATA_UNDERSTANDING_GUIDE.md` - Comprehensive guide
- ✅ `requirements.txt` - Python dependencies

### Updated Files
- ✅ `README.md` - Project documentation
- ✅ `notebooks/02_Data_Cleaning.ipynb` - Skeleton notebook
- ✅ `notebooks/03_EDA.ipynb` - Skeleton notebook
- ✅ And 4 other notebooks

### Output Files (Generated)
- 📊 `reports/data_understanding_report.txt` - Text report
- 📈 `reports/data_understanding_visualizations.png` - Charts
- 📊 `reports/categorical_distribution.png` - Category charts

## ✨ Ready to Use!

You can now:
- ✅ Load and explore your dataset
- ✅ Understand all 28 columns in business context
- ✅ Generate comprehensive reports and visualizations
- ✅ Validate data quality
- ✅ Identify insights for further analysis
- ✅ Share findings with stakeholders

---

**Start Analysis**: Run `python run_analysis.py` or open the Jupyter notebook!
