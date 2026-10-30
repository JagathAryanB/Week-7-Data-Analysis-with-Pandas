"""
Unit tests for DataLoader module.
"""

import os
import pytest
import pandas as pd
from sales_analyzer.data_loader import DataLoader, load_sales_data


@pytest.fixture
def sample_csv(tmp_path):
    csv_file = tmp_path / "sample_sales.csv"
    data = {
        "order_id": ["ORD-1", "ORD-2", "ORD-3"],
        "order_date": ["2024-01-15", "2024-02-10", "2024-03-05"],
        "customer_id": ["CUST-1", "CUST-2", "CUST-1"],
        "product_id": ["P-1", "P-2", "P-1"],
        "product_name": ["Laptop", "Shirt", "Laptop"],
        "category": ["Electronics", "Clothing", "Electronics"],
        "quantity": [1, 2, 1],
        "unit_price": [1000.0, 50.0, 1000.0],
        "total_amount": [1000.0, 100.0, 1000.0],
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    return str(csv_file)


def test_load_csv_success(sample_csv):
    loader = DataLoader(sample_csv)
    df = loader.load_csv()
    assert df is not None
    assert len(df) == 3
    assert "order_date" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["order_date"])


def test_load_csv_file_not_found():
    loader = DataLoader("non_existent_file.csv")
    with pytest.raises(FileNotFoundError):
        loader.load_csv()


def test_auto_load(sample_csv):
    df = load_sales_data(sample_csv)
    assert len(df) == 3
    assert "category" in df.columns


def test_check_data_quality(sample_csv):
    loader = DataLoader(sample_csv)
    df = loader.load_csv()
    report = loader.check_data_quality(df)
    assert report["total_rows"] == 3
    assert report["duplicate_rows"] == 0
    assert report["has_missing_values"] is False


def test_identify_data_types(sample_csv):
    loader = DataLoader(sample_csv)
    df = loader.load_csv()
    dtypes = loader.identify_data_types(df)
    assert "quantity" in dtypes
    assert "total_amount" in dtypes

