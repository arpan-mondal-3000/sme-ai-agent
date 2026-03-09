import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

df = pd.read_csv("data/sme_sales_data.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="vectorstore/chroma_db")

collection = client.get_or_create_collection("sme_data")

for i, row in df.iterrows():

    text = f"""
Month: {row['Month']}
Sales: {row['Sales']}
Expenses: {row['Expenses']}
Customers: {row['Customers']}
Inventory Cost: {row['InventoryCost']}
Marketing Spend: {row['MarketingSpend']}
"""

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[text]
    )

print("Embeddings stored.")