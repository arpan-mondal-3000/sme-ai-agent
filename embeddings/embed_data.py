import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

df = pd.read_csv("data/sme_sales_data.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection("sme_data")

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
        documents=[text],
        embeddings=[embedding],
        ids=[str(i)]
    )

print("Data Embedded Successfully")