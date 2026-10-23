import pandas as pd


def clean_sales_data(file_source):
    """
    Loads and cleans sales dataset from a CSV file path or uploaded file buffer.
    Returns:
        pd.DataFrame: Cleaned dataframe with calculated financial columns.
    """
    # 1. Read CSV
    df = pd.read_csv(file_source)

    # 2. Standardize column names (trim spaces)
    df.columns = [col.strip() for col in df.columns]

    # Required columns check
    required_cols = ['Order Date', 'Product', 'Category', 'Quantity', 'Unit Price']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in CSV: {', '.join(missing_cols)}")

    # 3. Remove duplicate rows if any
    df = df.drop_duplicates()

    # 4. Convert date column to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

    # Drop rows where Order Date, Product, or Category is invalid / missing
    df = df.dropna(subset=['Order Date', 'Product', 'Category'])

    # 5. Clean numeric columns
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce').fillna(0)

    # Filter out non-positive quantities or prices
    df = df[(df['Quantity'] > 0) & (df['Unit Price'] > 0)]

    # 6. Core financial calculations
    df['Revenue'] = df['Quantity'] * df['Unit Price']

    # If Unit Cost column exists, calculate Profit and Profit Margin
    if 'Unit Cost' in df.columns:
        df['Unit Cost'] = pd.to_numeric(df['Unit Cost'], errors='coerce').fillna(0)
        df['Total Cost'] = df['Quantity'] * df['Unit Cost']
        df['Profit'] = df['Revenue'] - df['Total Cost']
        # Profit Margin % (avoid zero division)
        df['Profit Margin (%)'] = (df['Profit'] / df['Revenue']) * 100
        df['Profit Margin (%)'] = df['Profit Margin (%)'].round(2)
    else:
        df['Unit Cost'] = 0.0
        df['Total Cost'] = 0.0
        df['Profit'] = 0.0
        df['Profit Margin (%)'] = 0.0

    # 7. Helper date columns for easy grouping
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Month Name'] = df['Order Date'].dt.strftime('%b %Y')

    # Sort chronologically
    df = df.sort_values(by='Order Date').reset_index(drop=True)

    return df

