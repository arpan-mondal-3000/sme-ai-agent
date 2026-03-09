from langchain_community.llms import Ollama
from app.config import LLM_MODEL


def load_llm():

    llm = Ollama(model=LLM_MODEL)

    return llm