"""
Unit tests for SalesAnalyzer module.
"""

import pytest
import pandas as pd
import numpy as np
from sales_analyzer.analyzer import SalesAnalyzer


@pytest.fixture
def clean_sales_data():
    return pd.DataFrame({
        "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4", "ORD-5"],
        "order_date": pd.to_datetime(["2024-01-15", "2024-01-20", "2024-02-14", "2024-02-28", "2024-03-10"]),
        "customer_id": ["CUST-1", "CUST-2", "CUST-1", "CUST-3", "CUST-2"],
        "product_id": ["P-1", "P-2", "P-1", "P-3", "P-2"],
        "product_name": ["Laptop", "Shirt", "Laptop", "Coffee Maker", "Shirt"],
        "category": ["Electronics", "Clothing", "Electronics", "Home & Garden", "Clothing"],
        "quantity": [1, 2, 1, 1, 3],
        "unit_price": [1000.0, 50.0, 1000.0, 150.0, 50.0],
        "total_amount": [1000.0, 100.0, 1000.0, 150.0, 150.0],
    })


def test_calculate_basic_stats(clean_sales_data):
    analyzer = SalesAnalyzer(df=clean_sales_data)
    stats = analyzer.calculate_basic_stats()
    assert stats["total_orders"] == 5
    assert stats["total_sales"] == 2400.0
    assert stats["average_order"] == 480.0
    assert stats["unique_customers"] == 3
    assert stats["unique_products"] == 3
    assert "date_range" in stats
    assert stats["date_range"]["start"] == "2024-01-15"
    assert stats["date_range"]["end"] == "2024-03-10"


def test_analyze_sales_by_category(clean_sales_data):
    analyzer = SalesAnalyzer(df=clean_sales_data)
    cat_df = analyzer.analyze_sales_by_category()
    assert len(cat_df) == 3
    # Top category should be Electronics (1000 + 1000 = 2000)
    assert cat_df.iloc[0]["category"] == "Electronics"
    assert cat_df.iloc[0]["total_amount"] == 2000.0
    assert cat_df.iloc[0]["order_count"] == 2


def test_analyze_monthly_trends(clean_sales_data):
    analyzer = SalesAnalyzer(df=clean_sales_data)
    monthly = analyzer.analyze_monthly_trends()
    assert len(monthly) == 3  # Jan, Feb, Mar
    assert "2024-01" in monthly.index
    assert monthly.loc["2024-01", "total_amount"] == 1100.0


def test_customer_purchase_patterns(clean_sales_data):
    analyzer = SalesAnalyzer(df=clean_sales_data)
    cust = analyzer.analyze_customer_purchase_patterns()
    assert cust["total_customers"] == 3
    # CUST-1 has 2 orders, CUST-2 has 2 orders, CUST-3 has 1 order -> 2 repeat customers
    assert cust["repeat_customers"] == 2
    assert cust["repeat_customers_pct"] == round((2 / 3) * 100, 1)


def test_generate_sales_forecast(clean_sales_data):
    analyzer = SalesAnalyzer(df=clean_sales_data)
    forecast = analyzer.generate_sales_forecast(periods=2, window=2)
    assert len(forecast) == 2
    assert "forecast_sales" in forecast.columns

