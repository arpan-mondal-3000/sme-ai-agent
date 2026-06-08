import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="vectorstore/chroma_db")
collection = client.get_or_create_collection("sme_data")

df = pd.read_csv("data/sme_sales_data.csv")

docs, embeddings, ids = [], [], []

for _, row in df.iterrows():
    # Rich text format so RAG retrieval carries full context
    text = (
        f"Month: {row['Month']}\n"
        f"Sales: {row['Sales']}\n"
        f"Expenses: {row['Expenses']}\n"
        f"Customers: {row['Customers']}\n"
        f"Inventory Cost: {row['InventoryCost']}\n"
        f"Marketing Spend: {row['MarketingSpend']}"
    )
    docs.append(text)
    embeddings.append(model.encode(text).tolist())
    ids.append(f"record_{row['Month']}")

collection.add(documents=docs, embeddings=embeddings, ids=ids)
print(f"Ingested {len(docs)} records into ChromaDB")