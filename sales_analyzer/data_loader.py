"""
data_loader.py - Module for loading and exploring sales datasets.
Supports loading data from CSV, Excel, and JSON files, displaying dataset
structure, and performing data quality checks.
"""

import os
from typing import Optional, Dict, Any, Union
import pandas as pd
import numpy as np


class DataLoader:
    """Handles data loading and initial exploratory inspection for sales data."""

    def __init__(self, filepath: Optional[str] = None):
        """
        Initialize DataLoader with an optional file path.

        Args:
            filepath: Path to the data file (CSV, Excel, or JSON).
        """
        self.filepath = filepath
        self.df: Optional[pd.DataFrame] = None

    def load_csv(self, filepath: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Load sales data from a CSV file.

        Args:
            filepath: Path to the CSV file. Defaults to self.filepath.
            **kwargs: Additional parameters passed to pd.read_csv.

        Returns:
            pd.DataFrame: Loaded DataFrame.
        """
        path = filepath or self.filepath
        if not path:
            raise ValueError("No file path provided for CSV loading.")
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        try:
            self.df = pd.read_csv(path, **kwargs)
            # Auto-convert order_date if present
            if "order_date" in self.df.columns:
                self.df["order_date"] = pd.to_datetime(self.df["order_date"], errors="coerce")
            print(f"[DataLoader] Successfully loaded CSV from {path}. Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"[DataLoader] Error loading CSV from {path}: {e}")
            raise

    def load_excel(self, filepath: Optional[str] = None, sheet_name: Union[str, int] = 0, **kwargs) -> pd.DataFrame:
        """
        Load sales data from an Excel file (.xlsx, .xls).

        Args:
            filepath: Path to Excel file.
            sheet_name: Sheet name or index to read.
            **kwargs: Extra arguments for pd.read_excel.

        Returns:
            pd.DataFrame: Loaded DataFrame.
        """
        path = filepath or self.filepath
        if not path:
            raise ValueError("No file path provided for Excel loading.")
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        try:
            self.df = pd.read_excel(path, sheet_name=sheet_name, **kwargs)
            if "order_date" in self.df.columns:
                self.df["order_date"] = pd.to_datetime(self.df["order_date"], errors="coerce")
            print(f"[DataLoader] Successfully loaded Excel from {path}. Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"[DataLoader] Error loading Excel from {path}: {e}")
            raise

    def load_json(self, filepath: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Load sales data from a JSON file.

        Args:
            filepath: Path to JSON file.
            **kwargs: Extra arguments for pd.read_json.

        Returns:
            pd.DataFrame: Loaded DataFrame.
        """
        path = filepath or self.filepath
        if not path:
            raise ValueError("No file path provided for JSON loading.")
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        try:
            self.df = pd.read_json(path, **kwargs)
            if "order_date" in self.df.columns:
                self.df["order_date"] = pd.to_datetime(self.df["order_date"], errors="coerce")
            print(f"[DataLoader] Successfully loaded JSON from {path}. Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"[DataLoader] Error loading JSON from {path}: {e}")
            raise

    def auto_load(self, filepath: Optional[str] = None) -> pd.DataFrame:
        """
        Automatically detect file format by extension and load into DataFrame.

        Args:
            filepath: File path to load.
        """
        path = filepath or self.filepath
        if not path:
            raise ValueError("No file path provided.")
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            return self.load_csv(path)
        elif ext in [".xlsx", ".xls"]:
            return self.load_excel(path)
        elif ext == ".json":
            return self.load_json(path)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Expected .csv, .xlsx, or .json")

    def display_info(self, df: Optional[pd.DataFrame] = None) -> None:
        """
        Display basic information about the dataset using head(), info(), describe().

        Args:
            df: Optional DataFrame. Defaults to self.df.
        """
        data = df if df is not None else self.df
        if data is None:
            print("[DataLoader] No dataset currently loaded.")
            return

        print("=" * 60)
        print("DATASET STRUCTURE OVERVIEW")
        print("=" * 60)
        print(f"Shape: {data.shape[0]} rows, {data.shape[1]} columns\n")
        print("--- Head (First 5 Rows) ---")
        print(data.head())
        print("\n--- DataFrame Info ---")
        data.info()
        print("\n--- Summary Statistics (Numeric) ---")
        print(data.describe())
        print("=" * 60)

    def check_data_quality(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Inspect dataset for quality issues: missing values, duplicate records,
        and unexpected value ranges.

        Args:
            df: Optional DataFrame. Defaults to self.df.

        Returns:
            dict: Summary report of data quality metrics.
        """
        data = df if df is not None else self.df
        if data is None:
            return {"error": "No data loaded"}

        missing_counts = data.isnull().sum()
        missing_pct = (missing_counts / len(data)) * 100
        missing_summary = {
            col: {"count": int(missing_counts[col]), "percentage": round(float(missing_pct[col]), 2)}
            for col in data.columns if missing_counts[col] > 0
        }

        duplicate_count = int(data.duplicated().sum())

        quality_report = {
            "total_rows": len(data),
            "total_columns": len(data.columns),
            "duplicate_rows": duplicate_count,
            "columns_with_missing_values": missing_summary,
            "has_missing_values": len(missing_summary) > 0,
            "memory_usage_bytes": int(data.memory_usage(deep=True).sum()),
        }

        print("\n[DataLoader] Data Quality Check:")
        print(f"  - Total records: {quality_report['total_rows']}")
        print(f"  - Duplicate rows: {duplicate_count}")
        if quality_report["has_missing_values"]:
            print(f"  - Columns with missing values: {list(missing_summary.keys())}")
        else:
            print("  - No missing values found.")

        return quality_report

    def identify_data_types(self, df: Optional[pd.DataFrame] = None) -> Dict[str, str]:
        """
        Identify and summarize data types for each column in the dataset.

        Args:
            df: Optional DataFrame. Defaults to self.df.

        Returns:
            dict: Column names mapped to their inferred string data type.
        """
        data = df if df is not None else self.df
        if data is None:
            return {}
        dtypes_map = {col: str(dtype) for col, dtype in data.dtypes.items()}
        return dtypes_map


def load_sales_data(filepath: str) -> pd.DataFrame:
    """
    Convenience function to quickly load a sales dataset from disk.

    Args:
        filepath: Path to CSV, Excel, or JSON sales file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    loader = DataLoader(filepath)
    return loader.auto_load()

