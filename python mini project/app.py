import os
import streamlit as st
import plotly.express as px
from data_cleaning import clean_sales_data
from analysis import (
    get_overall_metrics,
    get_product_summary,
    get_category_summary,
    get_monthly_trends,
    generate_observations,
)

# Page configuration
st.set_page_config(
    page_title="SalesSense | Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 SalesSense — Sales Intelligence & Decision Support")
st.markdown("Transform raw sales records into understandable business performance metrics, trends, and actionable observations.")

# -------------------------------------------------------------
# SIDEBAR: Data Upload & Filters
# -------------------------------------------------------------
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload sales CSV", type=["csv"])

sample_file_path = os.path.join(os.path.dirname(__file__), "data", "sample_sales.csv")

try:
    if uploaded_file is not None:
        raw_df = clean_sales_data(uploaded_file)
        st.sidebar.success("Custom dataset loaded successfully!")
    elif os.path.exists(sample_file_path):
        raw_df = clean_sales_data(sample_file_path)
        st.sidebar.info("Viewing sample demo dataset. Upload your own CSV anytime!")
    else:
        st.error("No dataset available. Please upload a CSV file with sales records.")
        st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Date & Category filters
st.sidebar.header("🔍 Filter Data")

# Date range filter
min_date = raw_df['Order Date'].min().date()
max_date = raw_df['Order Date'].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Category filter
all_categories = sorted(raw_df['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Categories",
    options=all_categories,
    default=all_categories
)

# Apply filters
df = raw_df.copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_d, end_d = selected_dates
    df = df[(df['Order Date'].dt.date >= start_d) & (df['Order Date'].dt.date <= end_d)]

if selected_categories:
    df = df[df['Category'].isin(selected_categories)]

if df.empty:
    st.warning("No sales records match the selected filters. Please expand your filter criteria.")
    st.stop()

# -------------------------------------------------------------
# TOP ROW: Key Performance Indicators (KPIs)
# -------------------------------------------------------------
metrics = get_overall_metrics(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{metrics['total_revenue']:,.2f}")
col2.metric("Total Profit", f"₹{metrics['total_profit']:,.2f}")
col3.metric("Profit Margin", f"{metrics['overall_margin']}%")
col4.metric("Avg Order Value", f"₹{metrics['avg_order_value']:,.2f}")

st.markdown("---")

# -------------------------------------------------------------
# MAIN CONTENT TABS
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Sales & Trends",
    "📦 Product Performance",
    "💡 Business Observations",
    "📋 Cleaned Data & Export"
])

# TAB 1: Trends & Category Analysis
with tab1:
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Monthly Revenue & Profit Trend")
        monthly_df = get_monthly_trends(df)
        fig_trend = px.line(
            monthly_df,
            x="Month_Name",
            y=["Revenue", "Profit"],
            markers=True,
            title="Revenue vs Profit Over Time",
            labels={"value": "Amount (₹)", "Month_Name": "Month", "variable": "Metric"},
            color_discrete_map={"Revenue": "#1f77b4", "Profit": "#2ca02c"}
        )
        fig_trend.update_layout(legend_title_text="")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        st.subheader("Revenue by Category")
        cat_df = get_category_summary(df)
        fig_cat = px.bar(
            cat_df,
            x="Category",
            y="Revenue",
            color="Category",
            text_auto=True,
            title="Total Sales by Category"
        )
        st.plotly_chart(fig_cat, use_container_width=True)

# TAB 2: Product Performance
with tab2:
    prod_df = get_product_summary(df)

    st.subheader("Top Products by Revenue")
    fig_prod = px.bar(
        prod_df.head(8),
        x="Revenue",
        y="Product",
        orientation="h",
        color="Profit Margin (%)",
        color_continuous_scale="Viridis",
        title="Top Products (Colored by Profit Margin %)",
        text_auto=True
    )
    fig_prod.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_prod, use_container_width=True)

    st.subheader("Detailed Product Breakdown")
    formatted_prod_df = prod_df.copy()
    formatted_prod_df['Revenue'] = formatted_prod_df['Revenue'].apply(lambda x: f"₹{x:,.2f}")
    formatted_prod_df['Profit'] = formatted_prod_df['Profit'].apply(lambda x: f"₹{x:,.2f}")
    formatted_prod_df['Profit Margin (%)'] = formatted_prod_df['Profit Margin (%)'].apply(lambda x: f"{x:.1f}%")
    st.dataframe(formatted_prod_df, use_container_width=True)

# TAB 3: Evidence-Based Business Observations
with tab3:
    st.subheader("Evidence-Based Business Observations")
    st.markdown("These findings are automatically derived from the concrete figures in your dataset.")

    observations = generate_observations(df)
    for obs in observations:
        st.info(obs)

# TAB 4: Raw / Cleaned Data & Download
with tab4:
    st.subheader("Processed Dataset Preview")
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned Data as CSV",
        data=csv_data,
        file_name="cleaned_sales_data.csv",
        mime="text/csv"
    )
