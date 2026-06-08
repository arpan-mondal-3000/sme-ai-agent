import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import chromadb
from sentence_transformers import SentenceTransformer
from core.config import EMBEDDING_MODEL, CHROMA_DB_DIR, COLLECTION_NAME

model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_or_create_collection(COLLECTION_NAME)

def retrieve_data(query: str):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    return results["documents"][0]