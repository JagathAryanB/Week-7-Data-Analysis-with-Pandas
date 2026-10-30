"""
main.py - Main entry point and CLI for the Sales Data Analysis Dashboard.
Provides command-line arguments to execute specific analysis tasks or run
the entire end-to-end data analysis pipeline.
"""

import os
import sys
import argparse
from typing import Optional

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure package is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from sales_analyzer import DataLoader, DataCleaner, SalesAnalyzer, SalesVisualizer, ReportGenerator


def run_pipeline(
    data_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    charts_dir: Optional[str] = None,
    clean_export_path: Optional[str] = None,
    export_excel: bool = True,
    export_csv: bool = True,
    export_html: bool = True,
    generate_charts: bool = True,
    print_summary: bool = True,
) -> None:
    """
    Execute full end-to-end sales analysis pipeline:
    1. Load raw dataset
    2. Inspect data quality
    3. Clean and preprocess data
    4. Export cleaned dataset
    5. Perform comprehensive analysis
    6. Generate visualizations and executive dashboard
    7. Export Excel, CSV, and HTML reports
    8. Print executive summary to console
    """
    data_path = data_path or os.path.join(SCRIPT_DIR, "data", "raw", "sales_data.csv")
    if not os.path.isabs(data_path):
        data_path = os.path.join(SCRIPT_DIR, data_path)

    output_dir = output_dir or os.path.join(SCRIPT_DIR, "data", "reports")
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(SCRIPT_DIR, output_dir)

    charts_dir = charts_dir or os.path.join(output_dir, "charts")
    if not os.path.isabs(charts_dir):
        charts_dir = os.path.join(SCRIPT_DIR, charts_dir)

    clean_export_path = clean_export_path or os.path.join(SCRIPT_DIR, "data", "processed", "sales_data_cleaned.csv")
    if not os.path.isabs(clean_export_path):
        clean_export_path = os.path.join(SCRIPT_DIR, clean_export_path)
    print("\n" + "=" * 70)
    print("🚀 STARTING SALES DATA ANALYSIS PIPELINE (WEEK 7)")
    print("=" * 70)

    # 1. Load Data
    print(f"\n[Step 1/6] Loading sales dataset from: {data_path}")
    loader = DataLoader(data_path)
    df_raw = loader.auto_load()
    loader.display_info(df_raw)

    # 2. Quality Check
    print("\n[Step 2/6] Performing Data Quality Inspection...")
    quality_report = loader.check_data_quality(df_raw)

    # 3. Clean Data
    print("\n[Step 3/6] Preprocessing and Cleaning Data...")
    cleaner = DataCleaner(df_raw)
    df_cleaned = cleaner.clean()

    # 4. Export Cleaned Data
    print(f"\n[Step 4/6] Exporting Cleaned Data to: {clean_export_path}")
    cleaner.export_cleaned_data(clean_export_path)

    # 5. Core Analysis
    print("\n[Step 5/6] Performing Business Analytics...")
    analyzer = SalesAnalyzer(df=df_cleaned)
    stats = analyzer.calculate_basic_stats()
    cat_sales = analyzer.analyze_sales_by_category()
    monthly = analyzer.analyze_monthly_trends()
    cust_insights = analyzer.analyze_customer_purchase_patterns()
    peaks = analyzer.identify_peak_sales_periods()
    clv = analyzer.calculate_customer_lifetime_value()
    forecast = analyzer.generate_sales_forecast(periods=3)

    print(f"  ✓ Total Sales: ${stats.get('total_sales', 0):,.2f}")
    print(f"  ✓ Total Orders: {stats.get('total_orders', 0):,}")
    print(f"  ✓ Average Order Value: ${stats.get('average_order', 0):,.2f}")
    print(f"  ✓ Categories Analyzed: {len(cat_sales)}")
    print(f"  ✓ Months Analyzed: {len(monthly)}")
    print(f"  ✓ Repeat Customer Rate: {cust_insights.get('repeat_customers_pct', 0):.1f}%")

    # 6. Visualizations
    if generate_charts:
        print(f"\n[Step 6/6] Generating Charts and Dashboards in: {charts_dir}")
        visualizer = SalesVisualizer()
        visualizer.generate_all_visualizations(analyzer, output_dir=charts_dir)

    # 7. Reporting & Exports
    reporter = ReportGenerator(analyzer)
    os.makedirs(output_dir, exist_ok=True)

    if export_excel:
        excel_path = os.path.join(output_dir, "sales_report.xlsx")
        reporter.export_to_excel(output_path=excel_path)

    if export_csv:
        reporter.export_to_csv(output_dir=output_dir)

    if export_html:
        html_path = os.path.join(output_dir, "sales_report.html")
        reporter.generate_html_report(output_path=html_path)

    if print_summary:
        print("\n" + "=" * 70)
        print("EXECUTIVE SUMMARY REPORT")
        print("=" * 70 + "\n")
        reporter.print_report()
        print("\n" + "=" * 70)

    print("\n✅ Pipeline execution completed successfully!")


def main():
    """Command-line interface entry point."""
    parser = argparse.ArgumentParser(
        description="Sales Data Analysis Dashboard CLI (Pandas & Matplotlib)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--data",
        "-d",
        type=str,
        default="data/raw/sales_data.csv",
        help="Path to sales data file (CSV, Excel, JSON). Default: data/raw/sales_data.csv",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="data/reports",
        help="Directory to save exported reports. Default: data/reports",
    )
    parser.add_argument(
        "--charts-dir",
        type=str,
        default="data/reports/charts",
        help="Directory to save chart images. Default: data/reports/charts",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run complete end-to-end analysis, charts generation, and reporting pipeline.",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Compute and display basic sales statistics.",
    )
    parser.add_argument(
        "--category",
        action="store_true",
        help="Perform product category revenue and order analysis.",
    )
    parser.add_argument(
        "--monthly",
        action="store_true",
        help="Perform monthly sales trend and growth rate analysis.",
    )
    parser.add_argument(
        "--customer",
        action="store_true",
        help="Compute customer purchase patterns, repeat rates, and CLV.",
    )
    parser.add_argument(
        "--forecast",
        action="store_true",
        help="Generate 3-month simple moving average sales forecast.",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Generate all visualizations and executive dashboard.",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Export Excel, CSV, and HTML reports and print executive summary.",
    )

    args = parser.parse_args()

    # Determine absolute path to data if relative
    data_path = args.data
    if not os.path.isabs(data_path):
        data_path = os.path.join(SCRIPT_DIR, data_path)

    # Default to running full pipeline if no specific flag was selected
    if not any([args.stats, args.category, args.monthly, args.customer, args.forecast, args.visualize, args.report]):
        args.all = True

    if args.all:
        run_pipeline(
            data_path=data_path,
            output_dir=os.path.join(SCRIPT_DIR, args.output_dir),
            charts_dir=os.path.join(SCRIPT_DIR, args.charts_dir),
        )
        return

    # Partial execution based on flags
    loader = DataLoader(data_path)
    df = loader.auto_load()
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean()
    analyzer = SalesAnalyzer(df=cleaned_df)

    if args.stats:
        print("\n--- Basic Statistics ---")
        stats = analyzer.calculate_basic_stats()
        for k, v in stats.items():
            print(f"  {k}: {v}")

    if args.category:
        print("\n--- Sales by Category ---")
        cat_df = analyzer.analyze_sales_by_category()
        print(cat_df.to_string(index=False))

    if args.monthly:
        print("\n--- Monthly Trends & MoM Growth ---")
        monthly_df = analyzer.analyze_monthly_trends()
        print(monthly_df.to_string())

    if args.customer:
        print("\n--- Customer Insights & CLV ---")
        cust_patterns = analyzer.analyze_customer_purchase_patterns()
        for k, v in cust_patterns.items():
            print(f"  {k}: {v}")
        print("\n--- Customer Lifetime Value ---")
        clv = analyzer.calculate_customer_lifetime_value()
        for k, v in clv.items():
            print(f"  {k}: {v}")

    if args.forecast:
        print("\n--- Sales Forecast (Simple Moving Average) ---")
        fc_df = analyzer.generate_sales_forecast()
        print(fc_df.to_string())

    if args.visualize:
        print(f"\n--- Generating Visualizations into {args.charts_dir} ---")
        visualizer = SalesVisualizer()
        visualizer.generate_all_visualizations(analyzer, output_dir=os.path.join(SCRIPT_DIR, args.charts_dir))

    if args.report:
        print("\n--- Generating Reports ---")
        reporter = ReportGenerator(analyzer)
        reporter.print_report()
        reporter.export_to_excel(output_path=os.path.join(SCRIPT_DIR, args.output_dir, "sales_report.xlsx"))
        reporter.export_to_csv(output_dir=os.path.join(SCRIPT_DIR, args.output_dir))
        reporter.generate_html_report(output_path=os.path.join(SCRIPT_DIR, args.output_dir, "sales_report.html"))


if __name__ == "__main__":
    main()
