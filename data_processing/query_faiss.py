import os
import json
import faiss
import numpy as np
from google import genai

# -------- CONFIG --------
INDEX_PATH = "faiss.index"
META_PATH = "chunk_metadata.json"
EMBED_MODEL = "models/text-embedding-004"
TOP_K = 5
# ------------------------

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def embed_query(text: str) -> np.ndarray:
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=text
    )
    return np.array(response.embeddings[0].values, dtype="float32")


# Load FAISS index
index = faiss.read_index(INDEX_PATH)

# Load metadata
with open(META_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

print("✅ FAISS index and metadata loaded")


def search(query: str, top_k: int = TOP_K):
    q_emb = embed_query(query).reshape(1, -1)
    distances, indices = index.search(q_emb, top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])

    return results


# -------- TEST --------
if __name__ == "__main__":
    query = input("\nAsk a question: ")
    results = search(query)

    print("\n🔍 Top results:\n")
    for i, r in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Heading: {r['heading']}")
        print(f"Source: {r['source']}")
        print(f"Path: {r['path']}")
        print(r['text'][:600])
        print()