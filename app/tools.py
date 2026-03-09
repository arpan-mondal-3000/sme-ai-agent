from langchain.tools import Tool
from utils.financial_utils import calculate_profit, quarterly_summary
from app.rag_pipeline import retrieve_financial_records


financial_retriever = Tool(
    name="Financial Retriever",
    func=retrieve_financial_records,
    description="Retrieve financial records for a specific month"
)

profit_tool = Tool(
    name="Profit Calculator",
    func=calculate_profit,
    description="Calculate profit for a given month"
)

summary_tool = Tool(
    name="Business Summary",
    func=quarterly_summary,
    description="Generate business performance summary"
)

tools = [
    financial_retriever,
    profit_tool,
    summary_tool
]