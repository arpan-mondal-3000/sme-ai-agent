from langchain_groq import ChatGroq
from core.config import LLM_MODEL, LLM_TEMPERATURE

def load_llm():
    return ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE
    )