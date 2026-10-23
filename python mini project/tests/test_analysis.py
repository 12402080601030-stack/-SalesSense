import pandas as pd
import pytest
from data_cleaning import clean_sales_data
from analysis import get_overall_metrics, get_product_summary


def test_calculations():
    # Create simple sample data
    test_df = pd.DataFrame({
        "Order Date": ["2026-01-01", "2026-01-02"],
        "Product": ["Notebook", "Pen"],
        "Category": ["Stationery", "Stationery"],
        "Quantity": [10, 5],
        "Unit Price": [50.0, 20.0],
        "Unit Cost": [30.0, 10.0]
    })

    # Calculations
    test_df["Revenue"] = test_df["Quantity"] * test_df["Unit Price"]
    test_df["Total Cost"] = test_df["Quantity"] * test_df["Unit Cost"]
    test_df["Profit"] = test_df["Revenue"] - test_df["Total Cost"]

    metrics = get_overall_metrics(test_df)

    # 10 * 50 = 500, 5 * 20 = 100 -> Total Revenue = 600
    assert metrics["total_revenue"] == 600.0
    # Cost: 10 * 30 = 300, 5 * 10 = 50 -> Total Cost = 350 -> Profit = 250
    assert metrics["total_profit"] == 250.0
    # Margin: 250 / 600 * 100 = 41.67%
    assert metrics["overall_margin"] == 41.67


def test_missing_required_column():
    bad_df = pd.DataFrame({
        "Product": ["Notebook"],
        "Quantity": [10]
    })
    # Save temporary CSV
    import io
    csv_buffer = io.StringIO(bad_df.to_csv(index=False))

    with pytest.raises(ValueError):
        clean_sales_data(csv_buffer)

