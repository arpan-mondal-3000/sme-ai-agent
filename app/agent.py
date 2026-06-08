from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from models.llm_loader import load_llm
from app.tools import tools

llm = load_llm()

PREFIX = """
You are an SME business analyst AI assistant.
You have access to tools to retrieve and compute financial data.

STRICT FORMAT RULES — you MUST follow these exactly:

1. "Action:" must contain ONLY the tool name. Nothing else.
   CORRECT ->   Action: rag_tool
   WRONG   ->   Action: Use the rag_tool to retrieve financial records.

2. After receiving an Observation, analyse it and write your Final Answer.
   Do NOT call the same tool again if you already have the data.

3. For greetings or vague inputs that need no data, reply directly:
   Final Answer: <your conversational reply>

EXAMPLE (follow this format exactly):
---
Question: What were the sales in January?
Thought: The user wants sales data. I should use rag_tool to retrieve it.
Action: rag_tool
Action Input: January sales
Observation: Month: Jan-23, Sales: 500000, Expenses: 300000
Thought: I now have the sales data for January. I can answer directly.
Final Answer: In January 2023, sales were ₹5,00,000 with expenses of ₹3,00,000.
---
"""

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors="Check your output format. Action must be only the tool name: profit_tool, summary_tool, or rag_tool.",
    max_iterations=5,
    early_stopping_method="generate",
    agent_kwargs={
        "prefix": PREFIX,
    }
)