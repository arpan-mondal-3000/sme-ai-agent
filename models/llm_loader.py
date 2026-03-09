from langchain_community.chat_models import ChatOllama


def load_llm():

    llm = ChatOllama(
        model="llama3.1:latest",
        temperature=0
    )

    return llm