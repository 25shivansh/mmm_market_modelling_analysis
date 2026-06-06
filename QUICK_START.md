# ⚡ Quick Start Guide

## 30-Second Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Analysis (Choose ONE)

#### Option A: Interactive Notebook (Recommended for First Time)
```bash
jupyter notebook notebooks/01_Data_Understanding.ipynb
```
Then run cells from top to bottom.

#### Option B: Automated Script
```bash
python run_analysis.py
```
Outputs to `reports/` folder automatically.

#### Option C: Python Code
```python
from src.data_understanding import DataUnderstanding

analyzer = DataUnderstanding('data/raw/synthetic_mmm_weekly_india.csv')
analyzer.run_complete_analysis()
```

## 📊 What You Get

Running the analysis generates:

1. **Text Report**: `reports/data_understanding_report.txt`
   - Complete findings
   - All statistics
   - Business interpretation

2. **Dashboard Visualization**: `reports/data_understanding_visualizations.png`
   - Data types chart
   - Missing values chart
   - Unique values chart
   - Statistics table

3. **Category Charts**: `reports/categorical_distribution.png`
   - Geographic distribution
   - Brand distribution
   - SKU distribution

## 🎯 9 Analyses Performed

✅ 1. Load dataset
✅ 2. Dataset shape (rows × columns)
✅ 3. Data types distribution
✅ 4. Missing values detection
✅ 5. Duplicate rows analysis
✅ 6. Unique values per column
✅ 7. Summary statistics
✅ 8. Business interpretation (28 columns)
✅ 9. Visualizations & report generation

## 📈 Data Understanding

Your dataset contains:
- **28 Columns** of MMM data
- **4 Categorical**: Week, Geo, Brand, SKU
- **4 Sales Metrics**: Units, Value, MRP, Net Price
- **4 Promotions**: Flags + Trade Spend
- **8 Media Variables**: TV, YouTube, Facebook, Instagram, Print, Radio, Content Scores
- **4 Distribution**: Coverage, Points, Shelves, Weighted
- **4 Economic**: CPI, GDP, Festival, Rainfall

## 🔍 Key Questions Answered

After analysis, you'll know:

**Data Quality**
- ✅ How many records? `~52,560` (from 104 weeks × 6 regions × 3 brands × 3 SKUs)
- ✅ Any missing values? `No` (clean dataset)
- ✅ Any duplicates? Check report
- ✅ Data completeness? 100%

**Sales Insights**
- ✅ Total revenue? From report
- ✅ Average sales value? From report
- ✅ Top performing regions? From report
- ✅ Brand performance? From report

**Marketing Mix**
- ✅ Media spend breakdown? From report
- ✅ Impressions by channel? From report
- ✅ Distribution coverage? From report
- ✅ Promotional intensity? From report

**Business Metrics**
- ✅ Price elasticity? MRP vs Net Price
- ✅ Seasonal patterns? Festival Index
- ✅ Economic impact? GDP Growth & CPI
- ✅ Weather effect? Rainfall Index

## 📂 File Locations

```
MarketMixmodelling/
├── notebooks/
│   └── 01_Data_Understanding.ipynb       ← Start here (interactive)
├── run_analysis.py                       ← Or run this (automated)
├── src/
│   └── data_understanding.py             ← Or use this (programmatic)
├── data/
│   └── raw/
│       └── synthetic_mmm_weekly_india.csv  ← Your dataset
└── reports/
    ├── data_understanding_report.txt     ← Text output
    ├── data_understanding_visualizations.png  ← Charts
    └── categorical_distribution.png      ← Category charts
```

## ✅ Verification

After running, verify:

1. **Notebook**: Output should show all analyses with charts
2. **Script**: Check `reports/` folder for 3 output files
3. **Module**: Check DataFrame loaded successfully

## 🚀 Next Steps

After data understanding:

1. Move to **Notebook 02**: Data Cleaning
   - Handle any identified issues
   - Standardize formats

2. Continue to **Notebook 03**: EDA
   - Correlation analysis
   - Trends and patterns

3. Then **Notebook 04**: Feature Engineering
   - Create lagged features
   - Normalize values

## 📚 Documentation

- **Detailed Guide**: `DATA_UNDERSTANDING_GUIDE.md`
- **Project Info**: `README.md`
- **Setup Details**: `SETUP_COMPLETE.md`
- **This Guide**: `QUICK_START.md` (you are here)

## 💡 Tips

1. **First time?** → Use Jupyter Notebook (interactive)
2. **Need fast analysis?** → Use `run_analysis.py` script
3. **Want to integrate?** → Use `DataUnderstanding` class
4. **Need customization?** → Edit `src/data_understanding.py`

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Run from project root |
| File not found | Check data/raw/ folder |
| Import error | `pip install -r requirements.txt` |
| Notebook won't open | `jupyter notebook --version` |
| No output | Check reports/ folder exists |

## 📞 Quick Reference

```python
# Load and analyze
from src.data_understanding import DataUnderstanding

analyzer = DataUnderstanding('data/raw/synthetic_mmm_weekly_india.csv')

# Load data
df = analyzer.load_data()

# Get insights
shape = analyzer.get_shape()              # (rows, cols)
missing = analyzer.get_missing_values()   # Missing data
duplicates = analyzer.get_duplicate_rows()  # Duplicate count
unique = analyzer.get_unique_values()     # Cardinality
stats = analyzer.get_summary_statistics() # Mean, std, etc
interp = analyzer.get_business_interpretation()  # Column meanings

# Generate outputs
report = analyzer.generate_full_report()  # Text report
analyzer.save_report()                    # Save to file
analyzer.create_visualizations()          # Create charts

# Or run everything at once
analyzer.run_complete_analysis()
```

---

**Ready?** Start with:
```bash
python run_analysis.py
```

Outputs will be in `reports/` folder! 🎉
