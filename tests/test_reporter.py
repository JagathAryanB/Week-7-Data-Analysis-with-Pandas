"""
Unit tests for ReportGenerator module.
"""

import os
import pytest
import pandas as pd
from sales_analyzer.analyzer import SalesAnalyzer
from sales_analyzer.reporter import ReportGenerator


@pytest.fixture
def sample_analyzer():
    df = pd.DataFrame({
        "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4"],
        "order_date": pd.to_datetime(["2024-01-10", "2024-02-15", "2024-03-20", "2024-04-25"]),
        "customer_id": ["CUST-1", "CUST-2", "CUST-1", "CUST-3"],
        "product_id": ["P-1", "P-2", "P-1", "P-3"],
        "product_name": ["Laptop", "Shirt", "Laptop", "Novel"],
        "category": ["Electronics", "Clothing", "Electronics", "Books"],
        "quantity": [1, 2, 1, 3],
        "total_amount": [500.0, 100.0, 500.0, 60.0],
        "region": ["North America", "Europe", "North America", "Asia"],
    })
    return SalesAnalyzer(df=df)


def test_generate_text_report(sample_analyzer):
    reporter = ReportGenerator(sample_analyzer)
    txt = reporter.generate_text_report()
    assert "SALES DATA ANALYSIS REPORT" in txt
    assert "BASIC STATISTICS" in txt
    assert "TOP PRODUCT CATEGORIES" in txt
    assert "RECOMMENDATIONS" in txt


def test_export_to_excel(sample_analyzer, tmp_path):
    reporter = ReportGenerator(sample_analyzer)
    excel_path = tmp_path / "report.xlsx"
    success = reporter.export_to_excel(output_path=str(excel_path))
    assert success is True
    assert os.path.exists(excel_path)
    assert os.path.getsize(excel_path) > 0


def test_export_to_csv(sample_analyzer, tmp_path):
    reporter = ReportGenerator(sample_analyzer)
    paths = reporter.export_to_csv(output_dir=str(tmp_path))
    assert "summary" in paths
    assert os.path.exists(paths["summary"])


def test_generate_html_report(sample_analyzer, tmp_path):
    reporter = ReportGenerator(sample_analyzer)
    html_path = tmp_path / "report.html"
    res = reporter.generate_html_report(output_path=str(html_path))
    assert os.path.exists(res)
    with open(res, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<title>Sales Data Analysis Report</title>" in content

