"""
visualizer.py - Module for generating visual charts and dashboards.
Implements line charts, bar charts, pie charts, histograms, geographical maps/charts,
and an integrated executive dashboard.
"""

import os
from typing import Optional, Union
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


class SalesVisualizer:
    """Creates publication-ready visualizations and charts for sales analysis."""

    def __init__(self, style: str = "seaborn-v0_8-whitegrid"):
        """
        Initialize the visualizer with a styling preference.
        """
        # Apply standard clean styling
        try:
            plt.style.use(style)
        except Exception:
            try:
                plt.style.use("default")
            except Exception:
                pass

        # Color palette for charts
        self.colors = [
            "#2563EB",  # Blue
            "#10B981",  # Green
            "#F59E0B",  # Amber
            "#EF4444",  # Red
            "#8B5CF6",  # Purple
            "#EC4899",  # Pink
            "#14B8A6",  # Teal
            "#F97316",  # Orange
        ]

    def plot_monthly_sales_trend(self, monthly_data: pd.DataFrame, output_path: Optional[str] = None) -> plt.Figure:
        """
        Create sales trend line chart over time.

        Args:
            monthly_data: DataFrame indexed or containing 'month_year' and 'total_amount'.
            output_path: Optional path to save the generated image.
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        x_vals = monthly_data.index if "month_year" not in monthly_data.columns else monthly_data["month_year"]
        y_vals = monthly_data["total_amount"]

        ax.plot(x_vals, y_vals, marker="o", color=self.colors[0], linewidth=2.5, markersize=7, label="Monthly Sales")
        ax.set_title("Monthly Sales Trend (2024)", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Month", fontsize=11, labelpad=10)
        ax.set_ylabel("Total Sales ($)", fontsize=11, labelpad=10)
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        ax.grid(True, linestyle="--", alpha=0.5)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            fig.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close(fig)

        return fig

    def plot_category_sales(self, category_data: pd.DataFrame, top_n: int = 10, output_path: Optional[str] = None) -> plt.Figure:
        """
        Generate bar chart of top selling product categories.

        Args:
            category_data: DataFrame with 'category' and 'total_amount'.
            top_n: Number of categories to display.
            output_path: Optional path to save image.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        data = category_data.head(top_n)

        bars = ax.bar(data["category"], data["total_amount"], color=self.colors[1], edgecolor="#065F46", width=0.6)
        ax.set_title(f"Top {len(data)} Product Categories by Sales", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Category", fontsize=11, labelpad=10)
        ax.set_ylabel("Total Sales ($)", fontsize=11, labelpad=10)
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        plt.xticks(rotation=45, ha="right")

        # Value labels above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"${height:,.0f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="medium",
            )

        plt.tight_layout()

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            fig.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close(fig)

        return fig

    def plot_category_pie_chart(self, category_data: pd.DataFrame, output_path: Optional[str] = None) -> plt.Figure:
        """
        Generate product category pie chart showing revenue share percentage.

        Args:
            category_data: DataFrame with 'category' and 'total_amount'.
            output_path: Optional save path.
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        data = category_data.copy()

        # If too many categories, group small ones into 'Other'
        if len(data) > 6:
            top5 = data.head(5)
            other_amt = data.iloc[5:]["total_amount"].sum()
            other_row = pd.DataFrame([{"category": "Other", "total_amount": other_amt}])
            data = pd.concat([top5, other_row], ignore_index=True)

        wedges, texts, autotexts = ax.pie(
            data["total_amount"],
            labels=data["category"],
            autopct="%1.1f%%",
            startangle=140,
            colors=self.colors[: len(data)],
            wedgeprops={"edgecolor": "white", "linewidth": 2},
            textprops={"fontsize": 11},
        )
        for at in autotexts:
            at.set_color("white")
            at.set_fontweight("bold")

        ax.set_title("Product Category Revenue Distribution", fontsize=14, fontweight="bold", pad=15)
        plt.tight_layout()

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            fig.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close(fig)

        return fig

    def plot_order_value_distribution(self, df: pd.DataFrame, bins: int = 30, output_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize order value distribution using a histogram.

        Args:
            df: Sales DataFrame containing 'total_amount'.
            bins: Number of histogram bins.
            output_path: Optional save path.
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.hist(df["total_amount"], bins=bins, edgecolor="black", color=self.colors[4], alpha=0.8)
        ax.set_title("Order Value Distribution", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Order Value ($)", fontsize=11, labelpad=10)
        ax.set_ylabel("Frequency", fontsize=11, labelpad=10)
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        ax.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            fig.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close(fig)

        return fig

    def plot_geographical_distribution(self, df: pd.DataFrame, region_col: str = "region", output_path: Optional[str] = None) -> Optional[plt.Figure]:
        """
        Visualize sales distribution across geographical regions.

        Args:
            df: Sales DataFrame.
            region_col: Column indicating geographic region or country.
            output_path: Optional save path.
        """
        if region_col not in df.columns:
            return None

        fig, ax = plt.subplots(figsize=(10, 6))
        geo_sales = df.groupby(region_col)["total_amount"].sum().sort_values(ascending=False)

        bars = ax.bar(geo_sales.index, geo_sales.values, color=self.colors[2], edgecolor="#B45309", width=0.6)
        ax.set_title("Geographical Sales Distribution", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Region", fontsize=11, labelpad=10)
        ax.set_ylabel("Total Sales ($)", fontsize=11, labelpad=10)
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        plt.xticks(rotation=30, ha="right")

        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"${height:,.0f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        plt.tight_layout()

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            fig.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close(fig)

        return fig

    def create_dashboard(self, analyzer: Any, output_path: Optional[str] = None) -> plt.Figure:
        """
        Create a 4-panel executive dashboard combining:
        1. Monthly Sales Trend (Line)
        2. Category Sales (Bar)
        3. Category Distribution (Pie)
        4. Order Value Distribution (Hist)

        Args:
            analyzer: SalesAnalyzer instance.
            output_path: Optional save path.
        """
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle("Sales Performance & Business Insights Dashboard", fontsize=18, fontweight="bold", y=0.98)

        monthly = analyzer.analyze_monthly_trends()
        categories = analyzer.analyze_sales_by_category()
        df = analyzer.df

        # Panel 1: Monthly Trend
        ax1 = axes[0, 0]
        if not monthly.empty:
            ax1.plot(monthly.index, monthly["total_amount"], marker="o", color=self.colors[0], linewidth=2.5)
            ax1.set_title("Monthly Sales Trend", fontsize=13, fontweight="bold")
            ax1.set_xlabel("Month")
            ax1.set_ylabel("Sales ($)")
            ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
            ax1.grid(True, linestyle="--", alpha=0.4)
            ax1.tick_params(axis="x", rotation=45)

        # Panel 2: Category Sales
        ax2 = axes[0, 1]
        if not categories.empty:
            top_cats = categories.head(6)
            ax2.bar(top_cats["category"], top_cats["total_amount"], color=self.colors[1], edgecolor="#065F46")
            ax2.set_title("Top Product Categories by Revenue", fontsize=13, fontweight="bold")
            ax2.set_xlabel("Category")
            ax2.set_ylabel("Sales ($)")
            ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
            ax2.grid(axis="y", linestyle="--", alpha=0.4)
            ax2.tick_params(axis="x", rotation=30)

        # Panel 3: Category Pie Share
        ax3 = axes[1, 0]
        if not categories.empty:
            top5 = categories.head(5)
            other_sum = categories.iloc[5:]["total_amount"].sum() if len(categories) > 5 else 0
            pie_data = top5.copy()
            if other_sum > 0:
                pie_data = pd.concat([pie_data, pd.DataFrame([{"category": "Other", "total_amount": other_sum}])], ignore_index=True)

            ax3.pie(
                pie_data["total_amount"],
                labels=pie_data["category"],
                autopct="%1.1f%%",
                startangle=140,
                colors=self.colors[: len(pie_data)],
            )
            ax3.set_title("Revenue Share by Category", fontsize=13, fontweight="bold")

        # Panel 4: Order Value Distribution
        ax4 = axes[1, 1]
        if df is not None and "total_amount" in df.columns:
            ax4.hist(df["total_amount"], bins=30, edgecolor="black", color=self.colors[4], alpha=0.85)
            ax4.set_title("Order Value Distribution", fontsize=13, fontweight="bold")
            ax4.set_xlabel("Order Value ($)")
            ax4.set_ylabel("Frequency")
            ax4.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
            ax4.grid(True, linestyle="--", alpha=0.4)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            fig.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close(fig)

        return fig

    def generate_all_visualizations(self, analyzer: Any, output_dir: str = "data/reports/charts") -> None:
        """
        Generate and save all charts and the combined dashboard.

        Args:
            analyzer: Configured SalesAnalyzer instance.
            output_dir: Output directory to store images.
        """
        os.makedirs(output_dir, exist_ok=True)

        monthly = analyzer.analyze_monthly_trends()
        categories = analyzer.analyze_sales_by_category()
        df = analyzer.df

        if not monthly.empty:
            self.plot_monthly_sales_trend(monthly, output_path=f"{output_dir}/monthly_trend.png")
            print(f"[SalesVisualizer] Saved: {output_dir}/monthly_trend.png")

        if not categories.empty:
            self.plot_category_sales(categories, output_path=f"{output_dir}/category_sales.png")
            print(f"[SalesVisualizer] Saved: {output_dir}/category_sales.png")
            self.plot_category_pie_chart(categories, output_path=f"{output_dir}/category_pie.png")
            print(f"[SalesVisualizer] Saved: {output_dir}/category_pie.png")

        if df is not None and "total_amount" in df.columns:
            self.plot_order_value_distribution(df, output_path=f"{output_dir}/order_distribution.png")
            print(f"[SalesVisualizer] Saved: {output_dir}/order_distribution.png")

        if df is not None and "region" in df.columns:
            self.plot_geographical_distribution(df, output_path=f"{output_dir}/geographical_sales.png")
            print(f"[SalesVisualizer] Saved: {output_dir}/geographical_sales.png")

        self.create_dashboard(analyzer, output_path=f"{output_dir}/sales_dashboard.png")
        print(f"[SalesVisualizer] Saved: {output_dir}/sales_dashboard.png")
