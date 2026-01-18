from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .models import QueryRequest, QueryResponse, PolicySource
from .rag_engine import rag_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load RAG index on startup
    print("Loading RAG Index...")
    rag_engine.load_documents()
    yield
    print("Shutting down...")

app = FastAPI(title="Policy Assistant API", lifespan=lifespan)

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    # Check if index is loaded (new engine uses self.index)
    return {"status": "ok", "index_status": "loaded" if rag_engine.index is not None else "empty"}

@app.post("/query", response_model=QueryResponse)
async def query_policy(request: QueryRequest):
    try:
        # The new RAG engine encapsulates search + generation in one 'answer' method.
        # It does not currently expose sensitivity analysis or granular scores in the same way.
        
        # 1. Get Answer
        engine_response = rag_engine.answer(request.question)
        answer_text = engine_response["answer"]
        model_used = engine_response["model_used"]
        
        # 2. Get Sources (Optional for UI, re-running search to get them)
        # The new engine.search returns list of dicts (metadata), not (doc, score) tuples.
        raw_sources = rag_engine.search(request.question)
        formatted_sources = []
        for src in raw_sources:
            # FAISS returns L2 distance (smaller is better) or Inner Product (larger is better).
            # Assuming distances for now. If score > 1, it's likely distance.
            raw_score = src.get("score", 0.0)
            
            # Simple heuristic to convert distance to "confidence" (0-1)
            # This is specific to the embedding space, but valid for UI display
            relevance = 1.0 / (1.0 + raw_score) if raw_score >= 0 else 0.0
            
            formatted_sources.append(PolicySource(
                filename=src.get("source", "unknown"),
                content_snippet=src.get("text", "")[:200] + "...",
                similarity_score=relevance
            ))
            
        return QueryResponse(
            answer=answer_text,
            model_used=model_used,
            sources=formatted_sources
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
