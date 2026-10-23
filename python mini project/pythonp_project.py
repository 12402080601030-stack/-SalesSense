"""
SalesSense - Command Line Runner
Runs the Level 1 & Level 2 analysis directly in your terminal.
"""

import os
from data_cleaning import clean_sales_data
from analysis import (
    get_overall_metrics,
    get_product_summary,
    get_category_summary,
    get_monthly_trends,
    generate_observations,
)


def main():
    # 1. Path to data
    data_path = os.path.join("data", "sample_sales.csv")

    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return

    print("=" * 60)
    print("       SALESSENSE - SALES INTELLIGENCE SYSTEM       ")
    print("=" * 60)

    # 2. Clean and load data
    print("\n[+] Loading and cleaning sales data...")
    df = clean_sales_data(data_path)
    print(f"    Loaded {len(df)} cleaned transaction records.\n")

    # 3. Overall KPI Metrics
    metrics = get_overall_metrics(df)
    print("-" * 60)
    print("EXECUTIVE SUMMARY (KPIs):")
    print(f"  • Total Revenue:       Rs {metrics['total_revenue']:,.2f}")
    print(f"  • Total Profit:        Rs {metrics['total_profit']:,.2f}")
    print(f"  • Profit Margin:       {metrics['overall_margin']}%")
    print(f"  • Total Orders:        {metrics['total_orders']}")
    print(f"  • Total Units Sold:    {metrics['total_units']}")
    print(f"  • Average Order Value: Rs {metrics['avg_order_value']:,.2f}")
    print("-" * 60)

    # 4. Top 3 Products
    print("\nTOP 3 PRODUCTS BY REVENUE:")
    top_products = get_product_summary(df).head(3)
    for idx, row in top_products.iterrows():
        print(f"  {idx+1}. {row['Product']} ({row['Category']})")
        print(f"     Revenue: Rs {row['Revenue']:,.2f} | Profit: Rs {row['Profit']:,.2f} | Margin: {row['Profit Margin (%)']}%")

    # 5. Monthly Trends
    print("\nMONTHLY REVENUE BREAKDOWN:")
    monthly = get_monthly_trends(df)
    for _, row in monthly.iterrows():
        growth_str = f"({row['Revenue Growth (%)']:+.1f}% vs prev month)" if pd.notna(row['Revenue Growth (%)']) else "(Base month)"
        print(f"  • {row['Month_Name']}: Rs {row['Revenue']:,.2f}  {growth_str}")

    # 6. Automated Observations
    print("\nBUSINESS OBSERVATIONS & ACTIONABLE INSIGHTS:")
    observations = generate_observations(df)
    for obs in observations:
        # Strip bold markdown asterisks for clean console printing
        clean_obs = obs.replace("**", "")
        print(f"  * {clean_obs}")

    print("\n" + "=" * 60)
    print("Analysis complete. To open the interactive dashboard, run:")
    print("    streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    import pandas as pd
    main()

