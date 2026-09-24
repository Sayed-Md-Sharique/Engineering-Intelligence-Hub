import os
from pathlib import Path
from dotenv import load_dotenv

# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "engineering_knowledge"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

GROQ_MODEL = "openai/gpt-oss-20b"