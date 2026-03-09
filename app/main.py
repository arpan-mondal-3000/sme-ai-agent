from app.agent import agent

print("SME Business AI Agent")

while True:

    query = input("Ask: ")

    if query == "exit":
        break

    response = agent.run(query)

    print(response)