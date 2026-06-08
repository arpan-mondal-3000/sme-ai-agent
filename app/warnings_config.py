import warnings
import logging
import os

# Suppress CUDA probe warning
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Suppress HuggingFace Hub unauthenticated warning  
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Suppress sentence-transformers BertModel load report
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)