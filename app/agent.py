from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from models.llm_loader import load_llm
from app.tools import tools

llm = load_llm()

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)