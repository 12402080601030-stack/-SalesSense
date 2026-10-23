import pandas as pd


def get_overall_metrics(df):
    """
    Computes key executive KPIs from the sales data.
    """
    total_revenue = df['Revenue'].sum()
    total_cost = df['Total Cost'].sum()
    total_profit = df['Profit'].sum()

    # Overall profit margin
    overall_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0

    # Total units sold
    total_units = int(df['Quantity'].sum())

    # Total orders count: use 'Order ID' if available, otherwise total rows
    if 'Order ID' in df.columns:
        total_orders = df['Order ID'].nunique()
    else:
        total_orders = len(df)

    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "overall_margin": round(overall_margin, 2),
        "total_orders": total_orders,
        "total_units": total_units,
        "avg_order_value": round(avg_order_value, 2)
    }


def get_product_summary(df):
    """
    Groups sales performance by product.
    """
    summary = df.groupby('Product').agg(
        Category=('Category', 'first'),
        Units_Sold=('Quantity', 'sum'),
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()

    summary['Profit Margin (%)'] = (summary['Profit'] / summary['Revenue'] * 100).round(2)
    summary = summary.sort_values(by='Revenue', ascending=False).reset_index(drop=True)
    return summary


def get_category_summary(df):
    """
    Groups sales performance by category.
    """
    summary = df.groupby('Category').agg(
        Units_Sold=('Quantity', 'sum'),
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()

    summary['Profit Margin (%)'] = (summary['Profit'] / summary['Revenue'] * 100).round(2)
    summary['Revenue Share (%)'] = (summary['Revenue'] / summary['Revenue'].sum() * 100).round(2)
    summary = summary.sort_values(by='Revenue', ascending=False).reset_index(drop=True)
    return summary


def get_monthly_trends(df):
    """
    Groups data chronologically by month for trend charts.
    """
    monthly = df.groupby('Year-Month').agg(
        Month_Name=('Month Name', 'first'),
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Quantity', 'count')
    ).reset_index()

    # Calculate month-over-month growth rate
    monthly['Revenue Growth (%)'] = monthly['Revenue'].pct_change() * 100
    monthly['Revenue Growth (%)'] = monthly['Revenue Growth (%)'].round(2)

    return monthly


def generate_observations(df):
    """
    Generates rule-based, evidence-backed business insights without guesswork.
    """
    observations = []
    
    if df.empty:
        return ["Not enough data to generate observations."]

    # 1. Product Revenue vs Profit Margin comparison
    prod_df = get_product_summary(df)
    if not prod_df.empty:
        top_rev_item = prod_df.iloc[0]
        # Find item with highest margin among items with reasonable sales
        top_margin_item = prod_df.sort_values(by='Profit Margin (%)', ascending=False).iloc[0]

        if top_rev_item['Product'] == top_margin_item['Product']:
            observations.append(
                f"**Top Performer:** **{top_rev_item['Product']}** is your best-performing item overall, "
                f"generating the highest revenue (₹{top_rev_item['Revenue']:,.0f}) with a solid profit margin of {top_rev_item['Profit Margin (%)']}%."
            )
        else:
            observations.append(
                f"**Revenue vs Margin Opportunity:** **{top_rev_item['Product']}** generated the highest total revenue (₹{top_rev_item['Revenue']:,.0f}), "
                f"but **{top_margin_item['Product']}** delivered a higher profit margin ({top_margin_item['Profit Margin (%)']}% vs {top_rev_item['Profit Margin (%)']}%)."
            )

    # 2. Category Concentration
    cat_df = get_category_summary(df)
    if not cat_df.empty:
        lead_cat = cat_df.iloc[0]
        observations.append(
            f"**Category Concentration:** **{lead_cat['Category']}** brings in {lead_cat['Revenue Share (%)']}% of all revenue "
            f"(₹{lead_cat['Revenue']:,.0f})."
        )

    # 3. Month-over-month Trend & Notable Drops/Peaks
    monthly_df = get_monthly_trends(df)
    if len(monthly_df) >= 2:
        best_month = monthly_df.loc[monthly_df['Revenue'].idxmax()]
        worst_month = monthly_df.loc[monthly_df['Revenue'].idxmin()]
        
        observations.append(
            f"**Peak Period:** Peak revenue occurred in **{best_month['Month_Name']}** at ₹{best_month['Revenue']:,.0f}. "
            f"The lowest was **{worst_month['Month_Name']}** at ₹{worst_month['Revenue']:,.0f}."
        )

        # Check for significant monthly drops (> 10%)
        drops = monthly_df[monthly_df['Revenue Growth (%)'] < -10]
        if not drops.empty:
            worst_drop = drops.sort_values(by='Revenue Growth (%)').iloc[0]
            observations.append(
                f"**Noticeable Decline Detected:** Sales dipped by {abs(worst_drop['Revenue Growth (%)']):.1f}% in "
                f"**{worst_drop['Month_Name']}**. Review product-level volumes during this month to see which lines slowed down."
            )

    # 4. Low Margin Flag
    low_margin_items = prod_df[prod_df['Profit Margin (%)'] < 25]
    if not low_margin_items.empty:
        names = ", ".join(low_margin_items['Product'].head(3).tolist())
        observations.append(
            f"**Margin Watchlist:** Products with margins under 25%: **{names}**. Consider evaluating supplier costs or bundling them."
        )

    return observations

