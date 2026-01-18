import os
import json
import faiss
import numpy as np

# ---------------------------
# OPTIONAL: OpenAI
# ---------------------------
from openai import OpenAI

# ---------------------------
# OPTIONAL: Gemini
# ---------------------------
try:
    from google import genai
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False


class RAGEngine:
    def __init__(self):
        self.index = None
        self.metadata = None
        self.embedding_dim = None

        self.openai_client = (
            OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            if os.getenv("OPENAI_API_KEY")
            else None
        )

        self.gemini_client = (
            genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            if GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY")
            else None
        )

    # ---------------------------
    # LOAD FAISS + METADATA
    # ---------------------------
    def load_documents(self):
        INDEX_PATH = "backend/rag/faiss.index"
        META_PATH = "backend/rag/chunk_metadata.json"

        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.embedding_dim = self.index.d
        print(f"✅ FAISS loaded with {len(self.metadata)} chunks")

    # ---------------------------
    # EMBEDDING
    # ---------------------------
    def embed_query(self, text):
        if not self.gemini_client:
            # Fallback or Error. Since we need embeddings for search, and index likely depends on this model, we must error.
            raise ValueError("Gemini Client not initialized (Missing GEMINI_API_KEY). Cannot embed query.")
            
        response = self.gemini_client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return np.array(response.embeddings[0].values, dtype="float32")

    # ---------------------------
    # FAISS SEARCH
    # ---------------------------
    def search(self, question, top_k=5):
        query_vec = self.embed_query(question).reshape(1, -1)
        distances, indices = self.index.search(query_vec, top_k)
        
        results = []
        for j, i in enumerate(indices[0]):
            meta = self.metadata[i].copy()
            meta["score"] = float(distances[0][j])
            results.append(meta)
            
        return results

    # ---------------------------
    # PROMPT BUILDER
    # ---------------------------
    def build_prompt(self, question, chunks):
        context = "\n\n".join(
            f"[{i+1}] ({c['heading']} | {c['source']})\n{c['text']}"
            for i, c in enumerate(chunks)
        )

        return f"""
You are a policy assistant.

This is a POLICY QUESTION answering system.
Only describe explicit rules, requirements, or documented practices.
Do NOT give general opinions, benefits, or cultural explanations unless explicitly stated in policy documents.

Rules:
- Answer ONLY using the provided context
- If the answer is not present, say so clearly
- Be concise and factual

If no explicit policy rules are found in the context, respond:
"No specific policy guidance was found in the provided documents."

Question:
{question}

Context:
{context}

Answer:
""".strip()

    # ---------------------------
    # GPT-4o-mini
    # ---------------------------
    def answer_with_gpt4o_mini(self, question, chunks):
        prompt = self.build_prompt(question, chunks)

        resp = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300
        )

        return {
            "answer": resp.choices[0].message.content.strip(),
            "model_used": "gpt-4o-mini"
        }

    # ---------------------------
    # GEMINI
    # ---------------------------
    def answer_with_gemini(self, question, chunks):
        if not self.gemini_client:
            raise RuntimeError("Gemini not available")

        prompt = self.build_prompt(question, chunks)

        resp = self.gemini_client.models.generate_content(
            model="gemini-pro-latest",
            contents=prompt
        )

        return {
            "answer": resp.text.strip(),
            "model_used": "gemini-pro"
        }

    # ---------------------------
    # o4-mini
    # ---------------------------
    def answer_with_o4_mini(self, question, chunks):
        prompt = self.build_prompt(question, chunks)

        resp = self.openai_client.chat.completions.create(
            model="o4-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300
        )

        return {
            "answer": resp.choices[0].message.content.strip(),
            "model_used": "o4-mini"
        }

    # ---------------------------
    # EXTRACTIVE
    # ---------------------------
    def answer_extractively(self, question, chunks):
        joined = "\n\n".join(
            f"- {c['text'][:800]}" for c in chunks[:3]
        )

        return {
            "answer": "Based on the policy documents:\n\n" + joined,
            "model_used": "extractive-only"
        }

    # ---------------------------
    # PUBLIC API (USED BY FASTAPI)
    # ---------------------------
    def answer(self, question):
        chunks = self.search(question)

        engines = [
            self.answer_with_gpt4o_mini,
            self.answer_with_gemini,
            self.answer_with_o4_mini,
            self.answer_extractively
        ]

        for engine in engines:
            try:
                result = engine(question, chunks)
                if result["answer"]:
                    return result
            except Exception as e:
                print(f"⚠️ {engine.__name__} failed: {e}")

        return {
            "answer": "Unable to answer the question.",
            "model_used": "none"
        }


rag_engine = RAGEngine()