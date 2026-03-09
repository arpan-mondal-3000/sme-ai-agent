from langchain_core.tools import tool
from utils.financial_utils import calculate_profit, business_summary
from app.rag_pipeline import retrieve_data


@tool
def profit_tool(month: str) -> str:
    """
    Calculate the profit for a specific month.

    The input MUST be exactly one of the following formats:
    Jan-23, Feb-23, Mar-23, Apr-23, May-23, Jun-23, Jul-23, Aug-23, Sep-23, Oct-23
    """
    return calculate_profit(month)


@tool
def summary_tool(query: str) -> str:
    """
    Generate a summary of the overall business performance.
    Use this when the user asks for overall performance, trends, or summaries.
    """
    return business_summary(query)


@tool
def rag_tool(query: str) -> str:
    """
    Use this tool to retrieve financial records from the vector database.
    Always use this tool if the user asks about:
    - sales
    - expenses
    - customers
    - inventory
    - marketing spend
    """
    docs = retrieve_data(query)
    return "\n".join(docs)


tools = [
    profit_tool,
    summary_tool,
    rag_tool
]