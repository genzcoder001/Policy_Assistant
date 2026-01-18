import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATA_DIRECTORY = os.getenv("DATA_DIRECTORY", "../data")
    EMBEDDING_MODEL = "all-MiniLM-L6-v2" # Lightweight, good for local testing
    
    # Safety keywords for simple heuristic check (can be improved with LLM)
    SENSITIVE_KEYWORDS = ["harassment", "discrimination", "termination", "legal", "compliance", "salary", "bonus"]

settings = Settings()
