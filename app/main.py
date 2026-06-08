import app.warnings_config
from app.agent import agent_executor

print("SME AI Business Consultant")
print("Type 'exit' to quit.\n")

while True:
    query = input("Ask: ").strip()

    if not query:
        continue

    if query.lower() == "exit":
        break

    try:
        result = agent_executor.invoke({"input": query})
        output = result.get("output", "")

        # Detect if model dumped raw ReAct chain instead of clean answer
        if any(tag in output for tag in ["Action:", "Thought:", "Observation:"]):
            print("\n⚠ Agent couldn't form a clean answer. Try rephrasing.\n")
        else:
            print(f"\n💼 {output}\n")

    except Exception as e:
        print(f"\n[Error]: {e}\n")