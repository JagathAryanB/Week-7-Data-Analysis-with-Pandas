"""
analyzer.py - Core sales data analysis engine.
Implements the SalesAnalyzer class with basic metrics, category performance,
monthly trend analysis, customer purchase pattern analysis, cohort tracking,
CLV calculation, and sales forecasting.
"""

import os
from typing import Optional, Dict, Any, Union, Tuple, List
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class SalesAnalyzer:
    """Analyzes sales data and generates insights"""

    def __init__(self, data_path: Optional[str] = None, df: Optional[pd.DataFrame] = None):
        """
        Initialize the analyzer with a data file path or an in-memory DataFrame.

        Args:
            data_path: Path to CSV or Excel file.
            df: Optional pre-loaded DataFrame.
        """
        self.data_path = data_path
        self.df: Optional[pd.DataFrame] = df.copy() if df is not None else None
        if self.df is None and self.data_path:
            self.load_data()

    def load_data(self) -> None:
        """Load sales data from CSV file"""
        if not self.data_path:
            print("No data_path provided.")
            return

        try:
            if self.data_path.endswith(".xlsx") or self.data_path.endswith(".xls"):
                self.df = pd.read_excel(self.data_path)
            else:
                self.df = pd.read_csv(self.data_path)

            # Convert date column to datetime
            if "order_date" in self.df.columns:
                self.df["order_date"] = pd.to_datetime(self.df["order_date"])
            print(f"Data loaded successfully. Shape: {self.df.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")

    def clean_data(self) -> None:
        """Clean the sales data"""
        if self.df is None:
            print("No data loaded")
            return

        # Remove duplicates
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_rows - len(self.df)
        print(f"Removed {removed} duplicate rows")

        # Handle missing values
        missing_values = self.df.isnull().sum()
        if missing_values.sum() > 0:
            print("Missing values found:")
            print(missing_values[missing_values > 0])
            # Fill numerical columns with median
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.df[col].isnull().sum() > 0:
                    self.df[col] = self.df[col].fillna(self.df[col].median())
            # Fill categorical columns with mode
            categorical_cols = self.df.select_dtypes(include=["object"]).columns
            for col in categorical_cols:
                if self.df[col].isnull().sum() > 0:
                    self.df[col] = self.df[col].fillna(self.df[col].mode()[0])

    def calculate_basic_stats(self) -> Dict[str, Any]:
        """Calculate basic sales statistics"""
        if self.df is None or self.df.empty:
            return {}

        stats = {
            "total_sales": round(float(self.df["total_amount"].sum()), 2),
            "average_order": round(float(self.df["total_amount"].mean()), 2),
            "total_orders": int(len(self.df)),
            "unique_customers": int(self.df["customer_id"].nunique()) if "customer_id" in self.df.columns else 0,
            "unique_products": int(self.df["product_id"].nunique()) if "product_id" in self.df.columns else 0,
        }

        # Add date range if available
        if "order_date" in self.df.columns and not self.df["order_date"].dropna().empty:
            stats["date_range"] = {
                "start": self.df["order_date"].min().strftime("%Y-%m-%d"),
                "end": self.df["order_date"].max().strftime("%Y-%m-%d"),
            }

        return stats

    def analyze_sales_by_category(self) -> pd.DataFrame:
        """Analyze sales by product category"""
        if self.df is None or "category" not in self.df.columns:
            return pd.DataFrame()

        agg_dict = {
            "total_amount": "sum",
            "quantity": "sum" if "quantity" in self.df.columns else "count",
            "order_id": "count" if "order_id" in self.df.columns else "size",
        }

        category_sales = self.df.groupby("category", as_index=False).agg(agg_dict)
        category_sales = category_sales.rename(columns={"order_id": "order_count"})

        total_rev = category_sales["total_amount"].sum()
        category_sales["percentage"] = (
            (category_sales["total_amount"] / total_rev * 100).round(1) if total_rev > 0 else 0.0
        )
        category_sales = category_sales.sort_values("total_amount", ascending=False).reset_index(drop=True)
        return category_sales

    def find_top_selling_products(self, n: int = 10) -> pd.DataFrame:
        """
        Identify top selling products by total revenue and unit sales.

        Args:
            n: Number of top products to return.
        """
        if self.df is None or "product_name" not in self.df.columns:
            return pd.DataFrame()

        agg_dict = {
            "total_amount": "sum",
            "quantity": "sum" if "quantity" in self.df.columns else "count",
            "order_id": "count" if "order_id" in self.df.columns else "size",
        }
        if "category" in self.df.columns:
            top_products = self.df.groupby(["product_id", "product_name", "category"], as_index=False).agg(agg_dict)
        else:
            top_products = self.df.groupby(["product_id", "product_name"], as_index=False).agg(agg_dict)

        top_products = top_products.rename(columns={"order_id": "order_count"})
        return top_products.sort_values("total_amount", ascending=False).head(n).reset_index(drop=True)

    def analyze_monthly_trends(self) -> pd.DataFrame:
        """Analyze monthly sales trends and growth rates"""
        if self.df is None or "order_date" not in self.df.columns:
            return pd.DataFrame()

        # Extract month-year
        self.df["month_year"] = self.df["order_date"].dt.to_period("M").astype(str)

        agg_dict = {
            "total_amount": "sum",
            "quantity": "sum" if "quantity" in self.df.columns else "count",
            "order_id": "count" if "order_id" in self.df.columns else "size",
        }
        if "customer_id" in self.df.columns:
            agg_dict["customer_id"] = "nunique"

        monthly_sales = self.df.groupby("month_year").agg(agg_dict)
        rename_map = {"order_id": "order_count"}
        if "customer_id" in agg_dict:
            rename_map["customer_id"] = "unique_customers"
        monthly_sales = monthly_sales.rename(columns=rename_map)

        # Calculate month-over-month growth
        monthly_sales["growth_rate"] = monthly_sales["total_amount"].pct_change() * 100

        # Month name representation for friendly display
        monthly_sales["month_name"] = pd.to_datetime(monthly_sales.index, format="%Y-%m").strftime("%B")

        return monthly_sales

    def identify_peak_sales_periods(self) -> Dict[str, Any]:
        """
        Identify highest and lowest sales months, peak growth month, and weekday patterns.
        """
        monthly = self.analyze_monthly_trends()
        if monthly.empty:
            return {}

        highest_month_idx = monthly["total_amount"].idxmax()
        lowest_month_idx = monthly["total_amount"].idxmin()

        # Find best growth month (excluding the first NaN month)
        valid_growth = monthly["growth_rate"].dropna()
        best_growth_idx = valid_growth.idxmax() if not valid_growth.empty else None

        peaks = {
            "highest_sales_month": {
                "period": highest_month_idx,
                "month_name": monthly.loc[highest_month_idx, "month_name"],
                "total_sales": round(float(monthly.loc[highest_month_idx, "total_amount"]), 2),
            },
            "lowest_sales_month": {
                "period": lowest_month_idx,
                "month_name": monthly.loc[lowest_month_idx, "month_name"],
                "total_sales": round(float(monthly.loc[lowest_month_idx, "total_amount"]), 2),
            },
            "average_monthly_sales": round(float(monthly["total_amount"].mean()), 2),
            "best_growth_month": {
                "period": best_growth_idx,
                "month_name": monthly.loc[best_growth_idx, "month_name"] if best_growth_idx else "N/A",
                "growth_rate_pct": round(float(valid_growth.max()), 1) if best_growth_idx else 0.0,
            }
            if best_growth_idx
            else None,
        }

        # Day of week analysis if dates available
        if "order_date" in self.df.columns:
            dow_sales = self.df.groupby(self.df["order_date"].dt.day_name())["total_amount"].sum()
            peaks["peak_day_of_week"] = dow_sales.idxmax()

        return peaks

    def analyze_customer_purchase_patterns(self) -> Dict[str, Any]:
        """
        Analyze customer purchase metrics:
        - Repeat customers count & percentage
        - Average customer value
        - Revenue share of top 10% customers
        """
        if self.df is None or "customer_id" not in self.df.columns:
            return {}

        customer_summary = self.df.groupby("customer_id").agg(
            total_spend=("total_amount", "sum"), order_count=("order_id" if "order_id" in self.df.columns else "total_amount", "count")
        )

        total_customers = len(customer_summary)
        if total_customers == 0:
            return {}

        repeat_customers = int((customer_summary["order_count"] > 1).sum())
        repeat_pct = round((repeat_customers / total_customers) * 100, 1)
        avg_cust_value = round(float(customer_summary["total_spend"].mean()), 2)

        # Revenue share of top 10% customers
        top_10_pct_count = max(1, int(np.ceil(total_customers * 0.10)))
        top_10_revenue = customer_summary["total_spend"].sort_values(ascending=False).head(top_10_pct_count).sum()
        total_revenue = customer_summary["total_spend"].sum()
        top_10_revenue_share = round((top_10_revenue / total_revenue) * 100, 1) if total_revenue > 0 else 0.0

        return {
            "total_customers": total_customers,
            "repeat_customers": repeat_customers,
            "repeat_customers_pct": repeat_pct,
            "average_customer_value": avg_cust_value,
            "top_10_pct_revenue_share": top_10_revenue_share,
        }

    def perform_cohort_analysis(self) -> pd.DataFrame:
        """
        Perform monthly customer cohort retention analysis.
        """
        if self.df is None or "customer_id" not in self.df.columns or "order_date" not in self.df.columns:
            return pd.DataFrame()

        df_cohort = self.df.copy()
        df_cohort["order_month"] = df_cohort["order_date"].dt.to_period("M")
        df_cohort["cohort_month"] = df_cohort.groupby("customer_id")["order_month"].transform("min")

        # Calculate period difference (cohort index in months)
        def get_date_int(df, column):
            year = df[column].dt.year
            month = df[column].dt.month
            return year, month

        order_year, order_month = get_date_int(df_cohort, "order_month")
        cohort_year, cohort_month = get_date_int(df_cohort, "cohort_month")
        years_diff = order_year - cohort_year
        months_diff = order_month - cohort_month
        df_cohort["cohort_index"] = years_diff * 12 + months_diff + 1

        cohort_data = df_cohort.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
        cohort_pivot = cohort_data.pivot(index="cohort_month", columns="cohort_index", values="customer_id")

        cohort_sizes = cohort_pivot.iloc[:, 0]
        retention_matrix = cohort_pivot.divide(cohort_sizes, axis=0).round(3) * 100
        return retention_matrix

    def calculate_customer_lifetime_value(self) -> Dict[str, float]:
        """
        Calculate Customer Lifetime Value (CLV) metrics:
        - Average Purchase Value (APV)
        - Average Purchase Frequency Rate (APFR)
        - Customer Value (CV)
        """
        if self.df is None or "customer_id" not in self.df.columns:
            return {}

        total_orders = len(self.df)
        unique_customers = self.df["customer_id"].nunique()
        total_revenue = self.df["total_amount"].sum()

        if unique_customers == 0 or total_orders == 0:
            return {}

        avg_purchase_value = total_revenue / total_orders
        avg_purchase_frequency = total_orders / unique_customers
        customer_value = avg_purchase_value * avg_purchase_frequency

        return {
            "average_purchase_value": round(float(avg_purchase_value), 2),
            "purchase_frequency_rate": round(float(avg_purchase_frequency), 2),
            "customer_value": round(float(customer_value), 2),
        }

    def generate_sales_forecast(self, periods: int = 3, window: int = 3) -> pd.DataFrame:
        """
        Generate simple moving average forecast for upcoming periods.

        Args:
            periods: Number of future months to forecast.
            window: Rolling window size for moving average.

        Returns:
            pd.DataFrame: Table containing historical and forecasted sales.
        """
        monthly = self.analyze_monthly_trends()
        if monthly.empty:
            return pd.DataFrame()

        series = monthly["total_amount"].copy()
        rolling_mean = series.rolling(window=window, min_periods=1).mean()

        last_date = pd.to_datetime(series.index[-1], format="%Y-%m")
        future_dates = [
            (last_date + pd.DateOffset(months=i)).strftime("%Y-%m")
            for i in range(1, periods + 1)
        ]

        forecast_vals = []
        hist_plus_forecast = list(series.values)
        for _ in range(periods):
            next_val = float(np.mean(hist_plus_forecast[-window:]))
            forecast_vals.append(next_val)
            hist_plus_forecast.append(next_val)

        forecast_df = pd.DataFrame(
            {
                "forecast_sales": forecast_vals,
                "method": f"{window}-Month Simple Moving Average",
            },
            index=future_dates,
        )
        return forecast_df

    def create_visualizations(self, output_dir: str = "output") -> None:
        """Create visualizations of sales data"""
        os.makedirs(output_dir, exist_ok=True)

        # 1. Monthly sales trend
        monthly_data = self.analyze_monthly_trends()
        if not monthly_data.empty:
            plt.figure(figsize=(12, 6))
            monthly_data["total_amount"].plot(kind="line", marker="o", color="#2563EB", linewidth=2.5)
            plt.title("Monthly Sales Trend", fontsize=14, fontweight="bold")
            plt.xlabel("Month", fontsize=11)
            plt.ylabel("Total Sales ($)", fontsize=11)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/monthly_trend.png", dpi=150)
            plt.close()

        # 2. Sales by category
        category_data = self.analyze_sales_by_category()
        if not category_data.empty:
            plt.figure(figsize=(10, 6))
            category_data.head(10).plot(x="category", y="total_amount", kind="bar", color="#10B981", legend=False)
            plt.title("Top 10 Product Categories by Sales", fontsize=14, fontweight="bold")
            plt.xlabel("Category", fontsize=11)
            plt.ylabel("Total Sales ($)", fontsize=11)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(f"{output_dir}/category_sales.png", dpi=150)
            plt.close()

        # 3. Order value distribution
        if self.df is not None and "total_amount" in self.df.columns:
            plt.figure(figsize=(10, 6))
            plt.hist(self.df["total_amount"], bins=30, edgecolor="black", color="#6366F1", alpha=0.85)
            plt.title("Order Value Distribution", fontsize=14, fontweight="bold")
            plt.xlabel("Order Value ($)", fontsize=11)
            plt.ylabel("Frequency", fontsize=11)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/order_distribution.png", dpi=150)
            plt.close()

        print(f"Visualizations saved to {output_dir}/")

    def generate_report(self, output_path: str = "sales_report.xlsx") -> bool:
        """Generate comprehensive sales report"""
        try:
            parent_dir = os.path.dirname(os.path.abspath(output_path))
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                # Basic stats sheet
                stats = self.calculate_basic_stats()
                stats_df = pd.DataFrame([stats])
                # Flatten date_range dict if present
                if "date_range" in stats_df.columns:
                    stats_df["date_range_start"] = stats.get("date_range", {}).get("start")
                    stats_df["date_range_end"] = stats.get("date_range", {}).get("end")
                    stats_df = stats_df.drop(columns=["date_range"])
                stats_df.to_excel(writer, sheet_name="Summary", index=False)

                # Monthly trends sheet
                monthly_data = self.analyze_monthly_trends()
                if not monthly_data.empty:
                    monthly_data.to_excel(writer, sheet_name="Monthly Trends")

                # Category analysis sheet
                category_data = self.analyze_sales_by_category()
                if not category_data.empty:
                    category_data.to_excel(writer, sheet_name="Category Analysis", index=False)

                # Customer Insights sheet
                cust_insights = self.analyze_customer_purchase_patterns()
                if cust_insights:
                    pd.DataFrame([cust_insights]).to_excel(writer, sheet_name="Customer Insights", index=False)

                # Raw data sample sheet
                if self.df is not None:
                    self.df.head(1000).to_excel(writer, sheet_name="Raw Data Sample", index=False)

            print(f"Report generated: {output_path}")
            return True
        except Exception as e:
            print(f"Error generating report: {e}")
            return False
