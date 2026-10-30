"""
data_cleaner.py - Module for data cleaning and preprocessing.
Implements duplicate removal, missing value imputation (median for numerical,
mode for categorical), data type conversion, and exporting cleaned datasets.
"""

import os
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np


class DataCleaner:
    """Preprocesses and cleans sales data according to project standards."""

    def __init__(self, df: Optional[pd.DataFrame] = None):
        """
        Initialize DataCleaner with an optional DataFrame.

        Args:
            df: Optional pandas DataFrame to clean.
        """
        self.df: Optional[pd.DataFrame] = df.copy() if df is not None else None
        self.cleaning_log: List[str] = []

    def set_data(self, df: pd.DataFrame) -> "DataCleaner":
        """Set or update the target DataFrame for cleaning."""
        self.df = df.copy()
        self.cleaning_log = []
        return self

    def remove_duplicates(self, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows from the dataset.

        Args:
            subset: Optional column names to consider for identifying duplicates.

        Returns:
            pd.DataFrame: Deduplicated DataFrame.
        """
        if self.df is None:
            raise ValueError("No DataFrame available to clean.")

        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset)
        removed = initial_rows - len(self.df)
        msg = f"Removed {removed} duplicate rows"
        self.cleaning_log.append(msg)
        print(f"[DataCleaner] {msg}")
        return self.df

    def handle_missing_values(
        self,
        strategy: str = "auto",
        numeric_fill: str = "median",
        categorical_fill: str = "mode",
        custom_numeric_values: Optional[Dict[str, float]] = None,
        custom_cat_values: Optional[Dict[str, str]] = None,
    ) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        By default:
          - Numerical columns are imputed with their median.
          - Categorical (object) columns are imputed with their mode.

        Args:
            strategy: 'auto' (median for numbers, mode for text) or 'drop' (drop NA rows).
            numeric_fill: 'median', 'mean', or 'zero'.
            categorical_fill: 'mode' or 'unknown'.
            custom_numeric_values: Dictionary mapping column name to fill value.
            custom_cat_values: Dictionary mapping column name to fill value.

        Returns:
            pd.DataFrame: DataFrame with missing values addressed.
        """
        if self.df is None:
            raise ValueError("No DataFrame available to clean.")

        missing_values = self.df.isnull().sum()
        if missing_values.sum() == 0:
            msg = "No missing values found in dataset."
            self.cleaning_log.append(msg)
            print(f"[DataCleaner] {msg}")
            return self.df

        print("[DataCleaner] Missing values found:")
        print(missing_values[missing_values > 0])

        if strategy == "drop":
            before = len(self.df)
            self.df = self.df.dropna()
            msg = f"Dropped {before - len(self.df)} rows containing missing values."
            self.cleaning_log.append(msg)
            print(f"[DataCleaner] {msg}")
            return self.df

        # Fill numerical columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].isnull().sum() > 0:
                if custom_numeric_values and col in custom_numeric_values:
                    fill_val = custom_numeric_values[col]
                elif numeric_fill == "mean":
                    fill_val = self.df[col].mean()
                elif numeric_fill == "zero":
                    fill_val = 0.0
                else:  # default 'median'
                    fill_val = self.df[col].median()
                self.df[col] = self.df[col].fillna(fill_val)
                self.cleaning_log.append(f"Filled missing in numeric '{col}' with {numeric_fill} ({fill_val})")

        # Fill categorical columns
        categorical_cols = self.df.select_dtypes(include=["object", "string"]).columns
        for col in categorical_cols:
            if self.df[col].isnull().sum() > 0:
                if custom_cat_values and col in custom_cat_values:
                    fill_val = custom_cat_values[col]
                elif categorical_fill == "unknown":
                    fill_val = "Unknown"
                else:  # default 'mode'
                    mode_series = self.df[col].mode()
                    fill_val = mode_series[0] if not mode_series.empty else "Unknown"
                self.df[col] = self.df[col].fillna(fill_val)
                self.cleaning_log.append(f"Filled missing in categorical '{col}' with {fill_val}")

        # Check any remaining datetime columns
        date_cols = self.df.select_dtypes(include=["datetime64[ns]", "datetime64"]).columns
        for col in date_cols:
            if self.df[col].isnull().sum() > 0:
                self.df[col] = self.df[col].bfill().ffill()
                self.cleaning_log.append(f"Backfilled/Forward-filled missing dates in '{col}'")

        print("[DataCleaner] Successfully handled all missing values.")
        return self.df

    def fix_data_types(
        self,
        date_columns: Optional[List[str]] = None,
        numeric_columns: Optional[List[str]] = None,
        category_columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Fix data type issues by casting columns to appropriate formats.

        Args:
            date_columns: List of columns to convert to datetime.
            numeric_columns: List of columns to convert to float/numeric.
            category_columns: List of columns to convert to categorical/string.

        Returns:
            pd.DataFrame: DataFrame with updated data types.
        """
        if self.df is None:
            raise ValueError("No DataFrame available.")

        # Default detection if not explicitly passed
        date_cols = date_columns or [col for col in self.df.columns if "date" in col.lower() or "time" in col.lower()]
        for col in date_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
                self.cleaning_log.append(f"Converted '{col}' to datetime")

        if numeric_columns:
            for col in numeric_columns:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
                    self.cleaning_log.append(f"Converted '{col}' to numeric")

        if category_columns:
            for col in category_columns:
                if col in self.df.columns:
                    self.df[col] = self.df[col].astype("category")
                    self.cleaning_log.append(f"Converted '{col}' to category")

        return self.df

    def validate_business_rules(self) -> pd.DataFrame:
        """
        Ensure business logic holds:
        - total_amount should equal quantity * unit_price (if present and total_amount is zero or missing)
        - quantity should be positive (> 0)
        - unit_price should be positive (>= 0)
        """
        if self.df is None:
            raise ValueError("No DataFrame available.")

        if "quantity" in self.df.columns and "unit_price" in self.df.columns:
            # Fix total_amount if missing or inconsistent
            if "total_amount" in self.df.columns:
                mask_invalid = (self.df["total_amount"].isna()) | (self.df["total_amount"] <= 0)
                if mask_invalid.any():
                    recalc = self.df.loc[mask_invalid, "quantity"] * self.df.loc[mask_invalid, "unit_price"]
                    self.df.loc[mask_invalid, "total_amount"] = recalc.round(2)
                    self.cleaning_log.append(f"Recalculated {mask_invalid.sum()} total_amount values from quantity*unit_price")

        return self.df

    def clean(self) -> pd.DataFrame:
        """
        Execute full cleaning pipeline:
        1. Remove duplicate records
        2. Fix data types
        3. Handle missing values appropriately
        4. Validate business rules

        Returns:
            pd.DataFrame: Cleaned DataFrame ready for analysis.
        """
        if self.df is None:
            raise ValueError("No DataFrame available to clean.")

        print("[DataCleaner] Starting complete data cleaning pipeline...")
        self.remove_duplicates()
        self.fix_data_types()
        self.handle_missing_values()
        self.validate_business_rules()
        print(f"[DataCleaner] Cleaning complete. Cleaned shape: {self.df.shape}")
        return self.df

    def export_cleaned_data(self, output_path: str, format: str = "csv") -> str:
        """
        Export cleaned dataset to disk.

        Args:
            output_path: Destination file path.
            format: 'csv', 'excel', or 'json'.

        Returns:
            str: Absolute path to written file.
        """
        if self.df is None:
            raise ValueError("No cleaned DataFrame to export.")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        fmt = format.lower()

        if fmt == "csv" or output_path.endswith(".csv"):
            self.df.to_csv(output_path, index=False)
        elif fmt in ["excel", "xlsx"] or output_path.endswith(".xlsx"):
            self.df.to_excel(output_path, index=False, engine="openpyxl")
        elif fmt == "json" or output_path.endswith(".json"):
            self.df.to_json(output_path, orient="records", date_format="iso", indent=2)
        else:
            self.df.to_csv(output_path, index=False)

        print(f"[DataCleaner] Cleaned data exported successfully to: {output_path}")
        return os.path.abspath(output_path)

