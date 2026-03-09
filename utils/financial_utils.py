import pandas as pd
from utils.data_loader import load_data

df = load_data()


def calculate_profit(month):

    row = df[df["Month"] == month]

    if len(row) == 0:
        return "Month not found."

    sales = int(row["Sales"].values[0])
    expenses = int(row["Expenses"].values[0])

    profit = sales - expenses

    return f"Profit in {month} = ₹{profit}"


def quarterly_summary():

    total_sales = df["Sales"].sum()
    total_expenses = df["Expenses"].sum()

    profit = total_sales - total_expenses

    avg_customers = df["Customers"].mean()

    return f"""
    Total Sales: ₹{total_sales}
    Total Expenses: ₹{total_expenses}
    Net Profit: ₹{profit}
    Average Customers: {avg_customers}
    """