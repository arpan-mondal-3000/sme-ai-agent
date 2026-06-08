from langchain_core.tools import tool
from utils.financial_utils import (
    calculate_profit,
    business_summary,
    compare_periods,
    top_months,
)
from app.rag_pipeline import retrieve_data


@tool
def profit_tool(month: str) -> str:
    """
    Calculate a detailed profit breakdown for a specific month.
    Accepts flexible input: 'Jul-23', 'July 2023', 'jul 23'.
    Use this when the user asks about profit, revenue, or expenses for ONE month.
    """
    return calculate_profit(month)


@tool
def summary_tool(query: str) -> str:
    """
    Summarise overall business performance for a period.
    Pass the user's original query — it detects year, quarter automatically.
    Use for: overall performance, trends, advice, improvement suggestions.
    Examples: 'how did we do in 2023', 'Q2 2022 performance', 'how can I improve sales'
    """
    return business_summary(query)


@tool
def compare_tool(periods: str) -> str:
    """
    Compare two time periods side by side.
    Input format: '<period1> vs <period2>'
    Examples: '2022 vs 2023', 'Q1 2022 vs Q1 2023'
    Use when the user asks to compare years, quarters, or periods.
    """
    parts = [p.strip() for p in periods.split("vs")]
    if len(parts) != 2:
        return "Please provide two periods separated by 'vs'. Example: '2022 vs 2023'"
    return compare_periods(parts[0], parts[1])


@tool
def top_months_tool(query: str) -> str:
    """
    Find the top performing months for a given metric.
    Detects metric from query: Sales, Expenses, Customers, InventoryCost, MarketingSpend.
    Use when user asks: 'best months for sales', 'top 3 months by customers', etc.
    Defaults to top 5 by Sales if nothing specific is mentioned.
    """
    query_lower = query.lower()

    metric = "Sales"
    for m in ["expenses", "customers", "inventorycost", "marketingspend", "sales"]:
        if m in query_lower.replace(" ", ""):
            metric = m.capitalize()
            break

    import re
    n_match = re.search(r"\b(\d+)\b", query)
    n = int(n_match.group(1)) if n_match else 5

    return top_months(metric=metric, n=n)


@tool
def rag_tool(query: str) -> str:
    """
    Retrieve raw financial records from the vector database.
    Use for specific data lookups: sales figures, expenses, customer counts,
    inventory cost, or marketing spend for any month or period.
    Input should be a short descriptive phrase. Example: 'sales July 2023', 'expenses Q1'.
    """
    docs = retrieve_data(query)
    return "\n\n".join(docs)


tools = [
    profit_tool,
    summary_tool,
    compare_tool,
    top_months_tool,
    rag_tool,
]