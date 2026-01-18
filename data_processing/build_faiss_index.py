import os
import json
import time
import faiss
import numpy as np
from tqdm import tqdm
from google import genai

# ---------------- CONFIG ----------------
CHUNKS_DIR = "chunks"
INDEX_OUT = "faiss.index"
META_OUT = "chunk_metadata.json"

EMBED_MODEL = "models/text-embedding-004"
SLEEP_SEC = 0.05  # rate-limit safety (important for free tier)
# ---------------------------------------

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def embed_text(text: str) -> np.ndarray:
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=text
    )
    return np.array(response.embeddings[0].values, dtype="float32")


vectors = []
metadata = []

files = sorted(os.listdir(CHUNKS_DIR))

print(f"Embedding {len(files)} chunks...")

for fname in tqdm(files):
    with open(os.path.join(CHUNKS_DIR, fname), "r", encoding="utf-8") as f:
        chunk = json.load(f)

    text = chunk["text"]

    try:
        emb = embed_text(text)
    except Exception as e:
        print(f"⚠️ Skipping {fname}: {e}")
        continue

    vectors.append(emb)
    metadata.append({
        "chunk_id": chunk["chunk_id"],
        "source": chunk["source"],
        "path": chunk["path"],
        "heading": chunk["heading"],
        "text": chunk["text"]
    })

    time.sleep(SLEEP_SEC)

vectors = np.vstack(vectors)
dim = vectors.shape[1]

# Build FAISS index
index = faiss.IndexFlatL2(dim)
index.add(vectors)

faiss.write_index(index, INDEX_OUT)

with open(META_OUT, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"\n✅ FAISS index built with {index.ntotal} vectors")
print(f"Saved: {INDEX_OUT}, {META_OUT}")