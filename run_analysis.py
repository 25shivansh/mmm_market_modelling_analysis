"""
Complete Market Mix Modeling Data Understanding Analysis
Generates comprehensive report and visualizations for dataset exploration
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from data_understanding import DataUnderstanding


def main():
    """
    Main execution function for complete data analysis.
    """
    
    # Define paths
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "raw" / "synthetic_mmm_weekly_india.csv"
    reports_dir = project_root / "reports"
    
    print("\n" + "=" * 80)
    print("MARKET MIX MODELING - COMPLETE DATA UNDERSTANDING ANALYSIS")
    print("=" * 80 + "\n")
    
    # Initialize analyzer
    analyzer = DataUnderstanding(str(data_path))
    
    # Load data
    print("Step 1: Loading dataset...")
    if analyzer.load_data() is None:
        print("✗ Failed to load dataset")
        return
    
    df = analyzer.df
    print(f"✓ Dataset loaded successfully\n")
    
    # === ANALYSIS 1: Dataset Shape ===
    print("Step 2: Dataset Shape")
    print("-" * 80)
    rows, cols = analyzer.get_shape()
    print(f"   Rows: {rows:,}")
    print(f"   Columns: {cols}")
    print()
    
    # === ANALYSIS 2: Data Types ===
    print("Step 3: Data Types")
    print("-" * 80)
    dtypes = analyzer.get_data_types()
    print(dtypes)
    print()
    
    # === ANALYSIS 3: Missing Values ===
    print("Step 4: Missing Values Analysis")
    print("-" * 80)
    missing = analyzer.get_missing_values()
    if len(missing) > 0:
        print(missing.to_string(index=False))
    else:
        print("✓ No missing values detected in the dataset")
    print()
    
    # === ANALYSIS 4: Duplicate Rows ===
    print("Step 5: Duplicate Rows Analysis")
    print("-" * 80)
    dup_count = analyzer.get_duplicate_rows()
    dup_pct = (dup_count / len(df) * 100)
    print(f"   Total Duplicate Rows: {dup_count}")
    print(f"   Percentage of Data: {dup_pct:.2f}%")
    print()
    
    # === ANALYSIS 5: Unique Values ===
    print("Step 6: Unique Values per Column")
    print("-" * 80)
    unique_vals = analyzer.get_unique_values()
    print(unique_vals.to_string(index=False))
    print()
    
    # === ANALYSIS 6: Summary Statistics ===
    print("Step 7: Summary Statistics (Numerical Columns)")
    print("-" * 80)
    summary_stats = analyzer.get_summary_statistics()
    print(summary_stats)
    print()
    
    # === ANALYSIS 7: Business Interpretation ===
    print("Step 8: Business Interpretation of Columns")
    print("-" * 80)
    interpretations = analyzer.get_business_interpretation()
    
    for column, interpretation in interpretations.items():
        if column in df.columns:
            print(f"\n   {column}:")
            print(f"   → {interpretation}")
    print()
    
    # === ADVANCED INSIGHTS ===
    print("Step 9: Advanced Data Insights")
    print("-" * 80)
    
    # Categorical columns analysis
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    print(f"\n   Categorical Columns ({len(categorical_cols)}):")
    for col in categorical_cols:
        unique_count = df[col].nunique()
        print(f"   • {col}: {unique_count} unique values")
        print(f"     Values: {', '.join(df[col].unique()[:5].astype(str))}")
    
    # Numerical columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"\n   Numerical Columns ({len(numeric_cols)}):")
    print(f"   • Columns: {', '.join(numeric_cols[:5])}")
    if len(numeric_cols) > 5:
        print(f"     ... and {len(numeric_cols) - 5} more")
    
    # Key statistics
    print("\n   Key Metrics:")
    if 'Sales_Value' in df.columns:
        print(f"   • Total Sales Value: ₹{df['Sales_Value'].sum():,.2f}")
        print(f"   • Average Sales Value: ₹{df['Sales_Value'].mean():,.2f}")
        print(f"   • Median Sales Value: ₹{df['Sales_Value'].median():,.2f}")
    
    if 'Sales_Units' in df.columns:
        print(f"   • Total Sales Units: {df['Sales_Units'].sum():,.0f}")
        print(f"   • Average Units per Record: {df['Sales_Units'].mean():.2f}")
    
    if 'Trade_Spend' in df.columns:
        print(f"   • Total Trade Spend: ₹{df['Trade_Spend'].sum():,.2f}")
        print(f"   • Average Trade Spend: ₹{df['Trade_Spend'].mean():,.2f}")
    
    # Distribution analysis
    if 'Geo' in df.columns:
        print(f"\n   Geographic Distribution:")
        geo_dist = df['Geo'].value_counts()
        for geo, count in geo_dist.items():
            pct = (count / len(df)) * 100
            print(f"   • {geo}: {count:,} records ({pct:.1f}%)")
    
    if 'Brand' in df.columns:
        print(f"\n   Brand Distribution:")
        brand_dist = df['Brand'].value_counts()
        for brand, count in brand_dist.items():
            pct = (count / len(df)) * 100
            print(f"   • {brand}: {count:,} records ({pct:.1f}%)")
    
    print("\n" + "-" * 80)
    
    # === GENERATE AND SAVE REPORT ===
    print("\nStep 10: Generating Report and Visualizations...")
    print("-" * 80)
    
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Save text report
    report_text = analyzer.save_report()
    
    # Create visualizations
    analyzer.create_visualizations(str(reports_dir))
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nGenerated Files:")
    print(f"  ✓ Report: {reports_dir / 'data_understanding_report.txt'}")
    print(f"  ✓ Visualizations: {reports_dir / 'data_understanding_visualizations.png'}")
    print(f"  ✓ Categorical Charts: {reports_dir / 'categorical_distribution.png'}")
    print("\n")


if __name__ == "__main__":
    main()
