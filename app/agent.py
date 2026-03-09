from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from models.llm_loader import load_llm
from app.tools import tools

llm = load_llm()
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    early_stopping_method="generate",
    agent_kwargs={
        "prefix": """
You are an SME business analyst.

Use tools to retrieve or compute financial data.

IMPORTANT:
When you have enough information from tool observations,
you MUST output:

Final Answer: <your answer>

Do not call more tools if the answer is already available.
"""
    }
)