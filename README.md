# Week 7: Sales Data Analysis Dashboard

A comprehensive sales data analysis system built using **Pandas**, **NumPy**, and **Matplotlib**. This project loads transactional sales data, cleans and preprocesses messy records, performs exploratory and advanced business analytics, produces publication-quality visualizations, and exports multi-format reports (Excel, CSV, HTML, and terminal).

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Project Architecture](#-project-architecture)
- [Folder Structure](#-folder-structure)
- [Key Features](#-key-features)
- [Installation & Setup](#-installation--setup)
- [Command-Line Interface (CLI) Usage](#-command-line-interface-cli-usage)
- [Modules Overview](#-modules-overview)
- [Jupyter Notebooks](#-jupyter-notebooks)
- [Sample Output](#-sample-output)
- [Running Automated Tests](#-running-automated-tests)

---

## 🎯 Overview
This project introduces foundational and advanced data analysis skills using Python and Pandas for real-world business scenarios:
- **Data Ingestion**: Loading from CSV, Excel, and JSON formats.
- **Data Preprocessing**: Handling missing values (median for numerical, mode for categorical), removing duplicates, and casting datatypes.
- **Business Analytics**: Total sales, average order value, top-performing product categories, peak demand periods, monthly trends, and growth rates.
- **Advanced Customer Analytics**: Customer lifetime value (CLV), purchase repeat rates, Pareto revenue concentration, cohort retention, and moving-average forecasting.
- **Visualization**: Line trends, category bar charts, revenue distribution pie charts, histogram distributions, and unified dashboards.
- **Multi-Format Reporting**: Multi-tab formatted Excel spreadsheets, raw CSVs, and modern HTML executive summaries.

---

## 📁 Folder Structure

```text
week7-sales-analysis/
├── sales_analyzer/
│   ├── __init__.py          # Package initialization and exports
│   ├── data_loader.py       # Data loading, structure exploration, quality checks
│   ├── data_cleaner.py      # Missing values, deduplication, type casting
│   ├── analyzer.py          # Core metrics, trends, customer patterns, forecasting
│   ├── visualizer.py        # Matplotlib charts, histograms, executive dashboard
│   └── reporter.py          # Terminal reports, Excel, CSV, and HTML exports
├── notebooks/
│   ├── exploration.ipynb    # Step 2: Exploratory data analysis (EDA)
│   └── analysis.ipynb       # Steps 3-7: Complete analysis and insights pipeline
├── data/
│   ├── raw/
│   │   └── sales_data.csv   # Raw transaction records (4,567 rows, 2024)
│   ├── processed/
│   │   └── sales_data_cleaned.csv # Cleaned dataset ready for modeling
│   └── reports/
│       ├── sales_report.xlsx      # Multi-sheet Excel report
│       ├── sales_report.html      # Interactive HTML executive summary
│       ├── summary_statistics.csv
│       ├── monthly_trends.csv
│       ├── category_analysis.csv
│       └── charts/                # Generated visualizations
│           ├── monthly_trend.png
│           ├── category_sales.png
│           ├── category_pie.png
│           ├── order_distribution.png
│           ├── geographical_sales.png
│           └── sales_dashboard.png
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_data_cleaner.py
│   ├── test_analyzer.py
│   ├── test_visualizer.py
│   └── test_reporter.py
├── requirements.txt         # Project dependencies
├── README.md                # Documentation
├── .gitignore               # Ignored development artifacts
└── main.py                  # CLI and automated pipeline runner
```

---

## 🛠 Installation & Setup

### Prerequisites
- Python 3.9+ (Python 3.10 - 3.14 supported)
- `pip` package manager

### 1. Clone or Navigate to Repository
```bash
cd week7-sales-analysis
```

### 2. (Optional) Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Command-Line Interface (CLI) Usage

The project includes an extensible CLI in `main.py`.

### 1. Run Complete End-to-End Pipeline
Executes loading, cleaning, analytics, visualization, and report generation:
```bash
python main.py
```
*(or explicitly with `--all`)*
```bash
python main.py --all
```

### 2. Inspect Specific Metrics
- **Basic Statistics**:
  ```bash
  python main.py --stats
  ```
- **Category Sales Breakdown**:
  ```bash
  python main.py --category
  ```
- **Monthly Trends & Growth Rates**:
  ```bash
  python main.py --monthly
  ```
- **Customer Insights & CLV**:
  ```bash
  python main.py --customer
  ```
- **3-Month Simple Moving Average Forecast**:
  ```bash
  python main.py --forecast
  ```
- **Generate All Visualizations Only**:
  ```bash
  python main.py --visualize
  ```
- **Export Reports (Excel, CSV, HTML)**:
  ```bash
  python main.py --report
  ```

### 3. Custom Input or Output Paths
```bash
python main.py --data path/to/custom_sales.csv --output-dir custom_reports/
```

---

## 📦 Modules Overview

### 1. `data_loader.py`
- `DataLoader`: Loads CSV, Excel, and JSON data.
- `DataLoader.display_info()`: Outputs `.head()`, `.info()`, and `.describe()`.
- `DataLoader.check_data_quality()`: Scans missing counts, null percentages, and duplicate records.
- `DataLoader.identify_data_types()`: Inferred vs detected column types.

### 2. `data_cleaner.py`
- `DataCleaner.remove_duplicates()`: Drops duplicate records and logs row delta.
- `DataCleaner.handle_missing_values()`: Fills numerical columns with **median** and categorical columns with **mode** (standard data science best practice).
- `DataCleaner.fix_data_types()`: Converts date columns to `datetime64[ns]` and string categories to `category`.
- `DataCleaner.validate_business_rules()`: Verifies `total_amount == quantity * unit_price` and positive values.
- `DataCleaner.clean()`: One-shot end-to-end cleaning pipeline.

### 3. `analyzer.py`
- `SalesAnalyzer`: The core analytics engine implementing:
  - `calculate_basic_stats()`: Total sales, average order value, order volume, unique customers/products, and date range.
  - `analyze_sales_by_category()`: Category revenue, unit sales, order count, and revenue share %.
  - `find_top_selling_products(n=10)`: Top products ranked by sales.
  - `analyze_monthly_trends()`: Monthly revenue, orders, and Month-over-Month (MoM) growth rates.
  - `identify_peak_sales_periods()`: Highest/lowest sales months, peak growth period, and best day of week.
  - `analyze_customer_purchase_patterns()`: Repeat buyer rates, average customer spend, and top 10% revenue contribution.
  - `perform_cohort_analysis()`: Monthly customer retention matrix.
  - `calculate_customer_lifetime_value()`: Average purchase value, purchase frequency, and customer value.
  - `generate_sales_forecast()`: Simple moving average forecast.

### 4. `visualizer.py`
- `SalesVisualizer`: Generates publication-ready charts using the `Agg` backend:
  - `plot_monthly_sales_trend()`: Line chart with markers and currency formatting.
  - `plot_category_sales()`: Horizontal or vertical bar chart with exact value callouts.
  - `plot_category_pie_chart()`: Percentage share of top product categories.
  - `plot_order_value_distribution()`: 30-bin histogram.
  - `plot_geographical_distribution()`: Sales distribution by global region.
  - `create_dashboard()`: 4-in-1 multi-panel executive dashboard.

### 5. `reporter.py`
- `ReportGenerator`:
  - `generate_text_report()`: Generates the exact executive summary text matching the project specification.
  - `export_to_excel()`: Creates a styled multi-sheet Excel workbook (`Summary`, `Monthly Trends`, `Category Analysis`, `Customer Insights`, `Raw Data Sample`).
  - `export_to_csv()`: Saves individual summary CSV files.
  - `generate_html_report()`: Creates a standalone HTML report with responsive KPI cards and tables.

---

## 📊 Sample Output

Running `python main.py` outputs the executive report:

```text
📊 SALES DATA ANALYSIS REPORT
========================================

📅 Analysis Period: Jan 2024 - Dec 2024

📈 BASIC STATISTICS:
- Total Sales: $1,245,678.90
- Total Orders: 4,567
- Average Order Value: $272.76
- Unique Customers: 1,234
- Unique Products: 555

🏆 TOP PRODUCT CATEGORIES:
1. Electronics: $456,789 (36.7%)
2. Clothing: $234,567 (18.8%)
3. Home & Garden: $198,765 (16.0%)
4. Books: $123,456 (9.9%)
5. Sports: $98,765 (7.9%)

📅 MONTHLY TRENDS:
- Highest Sales Month: November ($144,794)
- Lowest Sales Month: February ($86,152)
- Average Monthly Sales: $103,806.57
- Best Growth Month: November (+30.7%)

👥 CUSTOMER INSIGHTS:
- Repeat Customers: 345 (28.0%)
- Average Customer Value: $1,009.46
- Top 10% Customers Generate: 38.0% of revenue

💡 RECOMMENDATIONS:
1. Focus marketing on Electronics category
2. Improve customer retention programs
3. Consider seasonal promotions in Q4
4. Expand product range in high-performing categories
```

---

## 🧪 Running Automated Tests

A comprehensive unit test suite is included under `tests/` covering every component:

```bash
python -m pytest tests/ -v
```

Output:
```text
tests/test_analyzer.py::test_calculate_basic_stats PASSED
tests/test_analyzer.py::test_analyze_sales_by_category PASSED
tests/test_analyzer.py::test_analyze_monthly_trends PASSED
tests/test_analyzer.py::test_customer_purchase_patterns PASSED
tests/test_analyzer.py::test_generate_sales_forecast PASSED
tests/test_data_cleaner.py::test_remove_duplicates PASSED
tests/test_data_cleaner.py::test_handle_missing_values PASSED
tests/test_data_cleaner.py::test_full_clean_pipeline PASSED
tests/test_data_cleaner.py::test_export_cleaned_data PASSED
tests/test_data_loader.py::test_load_csv_success PASSED
tests/test_data_loader.py::test_load_csv_file_not_found PASSED
tests/test_data_loader.py::test_auto_load PASSED
tests/test_data_loader.py::test_check_data_quality PASSED
tests/test_data_loader.py::test_identify_data_types PASSED
tests/test_reporter.py::test_generate_text_report PASSED
tests/test_reporter.py::test_export_to_excel PASSED
tests/test_reporter.py::test_export_to_csv PASSED
tests/test_reporter.py::test_generate_html_report PASSED
tests/test_visualizer.py::test_plot_monthly_sales_trend PASSED
tests/test_visualizer.py::test_plot_category_sales PASSED
tests/test_visualizer.py::test_plot_order_value_distribution PASSED
tests/test_visualizer.py::test_create_dashboard PASSED

============================= 22 passed in 4.37s ==============================
```

