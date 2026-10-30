"""
Unit tests for SalesVisualizer module.
"""

import os
import pytest
import pandas as pd
from sales_analyzer.analyzer import SalesAnalyzer
from sales_analyzer.visualizer import SalesVisualizer


@pytest.fixture
def sample_analyzer():
    df = pd.DataFrame({
        "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4"],
        "order_date": pd.to_datetime(["2024-01-10", "2024-02-15", "2024-03-20", "2024-04-25"]),
        "customer_id": ["CUST-1", "CUST-2", "CUST-1", "CUST-3"],
        "product_id": ["P-1", "P-2", "P-1", "P-3"],
        "category": ["Electronics", "Clothing", "Electronics", "Books"],
        "quantity": [1, 2, 1, 3],
        "total_amount": [500.0, 100.0, 500.0, 60.0],
        "region": ["North America", "Europe", "North America", "Asia"],
    })
    return SalesAnalyzer(df=df)


def test_plot_monthly_sales_trend(sample_analyzer, tmp_path):
    vis = SalesVisualizer()
    monthly = sample_analyzer.analyze_monthly_trends()
    out = tmp_path / "trend.png"
    vis.plot_monthly_sales_trend(monthly, output_path=str(out))
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0


def test_plot_category_sales(sample_analyzer, tmp_path):
    vis = SalesVisualizer()
    cats = sample_analyzer.analyze_sales_by_category()
    out = tmp_path / "cats.png"
    vis.plot_category_sales(cats, output_path=str(out))
    assert os.path.exists(out)


def test_plot_order_value_distribution(sample_analyzer, tmp_path):
    vis = SalesVisualizer()
    out = tmp_path / "hist.png"
    vis.plot_order_value_distribution(sample_analyzer.df, output_path=str(out))
    assert os.path.exists(out)


def test_create_dashboard(sample_analyzer, tmp_path):
    vis = SalesVisualizer()
    out = tmp_path / "dashboard.png"
    vis.create_dashboard(sample_analyzer, output_path=str(out))
    assert os.path.exists(out)

