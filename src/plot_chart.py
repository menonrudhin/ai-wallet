import matplotlib.pyplot as plt
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def plot_pie_chart(df):
    # Convert amount to numeric (remove commas first)
    df["amount"] = df["amount"].astype(str).str.replace(",", "").apply(pd.to_numeric, errors="coerce")
    
    # Group by Category
    category_sum = df.groupby("category")["amount"].sum()

    logger.info(f"Category sums for pie chart: \n{category_sum}")

    # Remove zero values
    category_sum = category_sum[category_sum > 0]

    plt.figure(figsize=(8,8))
    plt.pie(category_sum, labels=category_sum.index, autopct="%1.1f%%")
    plt.title("Spending by Category")
    plt.show()

def plot_bar_chart(df):
    # Convert amount to numeric (remove commas first)
    df["amount"] = df["amount"].astype(str).str.replace(",", "").apply(pd.to_numeric, errors="coerce")
    
    # Group by MonthYear and Category
    monthly_data = (
        df.groupby(["date", "category"])["amount"]
        .sum()
        .reset_index()
    )

    # Convert MonthYear back to string for plotting
    monthly_data["date"] = monthly_data["date"].apply(lambda x: f"{x.month}/{x.year}")

    # Pivot table for grouped bar chart
    pivot_df = monthly_data.pivot_table(
        index="date",
        columns="category",
        values="amount",
        aggfunc="sum"
    ).fillna(0)

    pivot_df = pivot_df.sort_index()

    pivot_df.plot(kind="bar", figsize=(12,6))

    plt.xlabel("Month-Year")
    plt.ylabel("Amount Spent")
    plt.title("Monthly Spending Trend by Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()