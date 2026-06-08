from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()

ROOT = Path(__file__).parent.parent

LLM_MODEL        = "llama-3.1-8b-instant"
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"
CHROMA_DB_DIR    = str(ROOT / "vectorstore" / "chroma_db")
COLLECTION_NAME = "sme_data"
DATA_PATH        = str(ROOT / "data" / "sme_sales_data.csv")
GROQ_API_KEY     = os.getenv("GROQ_API_KEY")
HF_TOKEN         = os.getenv("HF_TOKEN")