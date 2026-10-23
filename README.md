# SalesSense — Sales Intelligence & Decision Support System

A clean, practical sales analysis tool and interactive dashboard that turns raw CSV transaction records into actionable business insights.

Built with **Python**, **pandas**, **Plotly**, and **Streamlit**.

---

## 🎯 What it Does

- **Cleans & Validates Data**: Automatically trims messy headers, handles missing dates, drops duplicates, and standardizes numeric columns.
- **Calculates Key Financials**:
  - Revenue = Quantity × Unit Price
  - Profit = Revenue − (Quantity × Unit Cost)
  - Profit Margin (%) = (Profit ÷ Revenue) × 100
  - Average Order Value (AOV)
- **Visualizes Performance**: Interactive Plotly charts for monthly sales trends, category revenue breakdown, and top products.
- **Evidence-Based Observations**: Detects notable monthly drops, flags low-margin items, and highlights revenue-versus-margin trade-offs with concrete figures.

---

## 📁 Project Structure

```text
├── data/
│   └── sample_sales.csv     # 50-row realistic store transaction dataset
├── data_cleaning.py         # CSV cleaning & column validation logic
├── analysis.py              # Financial metrics & rule-based observations
├── pythonp_project.py       # Quick terminal runner (Week 1 deliverable)
├── app.py                   # Streamlit interactive dashboard (Week 3 deliverable)
├── tests/
│   └── test_analysis.py     # Simple unit tests for calculations
├── requirements.txt         # Required Python packages
└── README.md
```

---

## 🚀 How to Run

### 1. Install Dependencies
Open your terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### 2. Option A: Run Terminal Analysis (Quick Check)
```bash
python pythonp_project.py
```

### 3. Option B: Launch Interactive Web Dashboard
```bash
streamlit run app.py
```
This opens the dashboard in your web browser. You can use the built-in sample data or upload your own sales CSV file via the sidebar.

### 4. Run Tests (Optional)
```bash
pytest
```

