import sys
import subprocess
from app.warnings_config import *

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "ui"

    if mode == "ui":
        subprocess.run(["streamlit", "run", "frontend/ui.py"], check=True)
    elif mode == "cli":
        from app.agent import agent_executor
        print("SME AI Business Consultant (CLI)\nType 'exit' to quit.\n")
        while True:
            query = input("Ask: ").strip()
            if not query:
                continue
            if query.lower() == "exit":
                break
            result = agent_executor.invoke({"input": query})
            print(f"\n{result.get('output', '')}\n")
    elif mode == "ingest":
        import embeddings.embed_data 
        print("Data ingested into ChromaDB.")
    else:
        print(f"Unknown mode: {mode}. Use: ui | cli | ingest")

if __name__ == "__main__":
    main()