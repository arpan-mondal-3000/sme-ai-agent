from app.agent import agent_executor

print("SME AI Business Consultant")

while True:

    query = input("Ask: ")

    if query == "exit":
        break

    result = agent_executor.invoke(
        {"input": query}
    )

    print(result["output"])