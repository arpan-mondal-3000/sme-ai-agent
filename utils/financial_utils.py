import pandas as pd
import re

df = pd.read_csv("data/sme_sales_data.csv")


def calculate_profit(month: str):

    month = month.strip().lower()

    df["Month_norm"] = df["Month"].str.lower()

    row = df[df["Month_norm"].str.contains(month)]

    if row.empty:
        return "Month not found in dataset."

    row = row.iloc[0]

    profit = float(row["Sales"]) - float(row["Expenses"])

    return f"Profit in {row['Month']} = ₹{int(profit)}"

def business_summary(query: str):

    query = query.lower()

    # detect quarter
    quarter_match = re.search(r"q([1-4])", query)

    # detect year
    year_match = re.search(r"(20\d{2})", query)

    df_copy = df.copy()
    df_copy["Month"] = pd.to_datetime(df_copy["Month"], format="%b-%y")

    if quarter_match and year_match:

        quarter = int(quarter_match.group(1))
        year = int(year_match.group(1))

        df_copy = df_copy[df_copy["Month"].dt.year == year]
        df_copy = df_copy[df_copy["Month"].dt.quarter == quarter]

    data = df_copy

    if data.empty:
        return "No data found for that period."

    total_sales = data["Sales"].sum()
    total_expenses = data["Expenses"].sum()
    profit = total_sales - total_expenses
    avg_customers = data["Customers"].mean()

    return f"""
Business Performance Summary

Total Sales: ₹{int(total_sales)}
Total Expenses: ₹{int(total_expenses)}
Net Profit: ₹{int(profit)}
Average Customers: {int(avg_customers)}
"""