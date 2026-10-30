"""
Unit tests for DataCleaner module.
"""

import os
import pytest
import pandas as pd
import numpy as np
from sales_analyzer.data_cleaner import DataCleaner


@pytest.fixture
def messy_dataframe():
    return pd.DataFrame({
        "order_id": ["ORD-1", "ORD-1", "ORD-2", "ORD-3", "ORD-4"],
        "order_date": ["2024-01-01", "2024-01-01", "2024-02-01", "2024-03-01", None],
        "category": ["Electronics", "Electronics", "Clothing", None, "Books"],
        "quantity": [2, 2, np.nan, 1, 3],
        "unit_price": [100.0, 100.0, 50.0, 20.0, 15.0],
        "total_amount": [200.0, 200.0, np.nan, 20.0, 45.0],
    })


def test_remove_duplicates(messy_dataframe):
    cleaner = DataCleaner(messy_dataframe)
    initial_len = len(messy_dataframe)
    cleaner.remove_duplicates()
    assert len(cleaner.df) == initial_len - 1


def test_handle_missing_values(messy_dataframe):
    cleaner = DataCleaner(messy_dataframe)
    cleaner.remove_duplicates()
    cleaner.handle_missing_values()
    # No NaNs in quantity or category
    assert cleaner.df["quantity"].isnull().sum() == 0
    assert cleaner.df["category"].isnull().sum() == 0


def test_full_clean_pipeline(messy_dataframe):
    cleaner = DataCleaner(messy_dataframe)
    cleaned = cleaner.clean()
    assert len(cleaned) == 4  # one duplicate removed
    assert cleaned["quantity"].isna().sum() == 0
    assert cleaned["category"].isna().sum() == 0


def test_export_cleaned_data(messy_dataframe, tmp_path):
    cleaner = DataCleaner(messy_dataframe)
    cleaner.clean()
    out_file = tmp_path / "cleaned.csv"
    res = cleaner.export_cleaned_data(str(out_file))
    assert os.path.exists(res)
    loaded = pd.read_csv(res)
    assert len(loaded) == len(cleaner.df)
