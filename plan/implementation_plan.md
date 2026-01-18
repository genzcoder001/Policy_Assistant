# Implementation Plan - AI-Powered Policy Assistant

This plan outlines the development of an internal company policy assistant using FastAPI, React/Next.js, and a RAG pipeline (FAISS + Embeddings + LLM).

## User Review Required
> [!IMPORTANT]
> **API Keys**: The application requires an LLM provider API key (e.g., OPENAI_API_KEY) to function. Please ensure this is available in the run environment.
> **Mock Data**: We will create dummy "Company Policies" to populate the knowledge base for demonstration purposes.

## Proposed Changes

### Project Structure
Root: `/Users/satya_lakshya/.gemini/antigravity/scratch/policy_assistant`

### Backend (`/backend`)
We will use **FastAPI**.
#### [NEW] `main.py`
- Initialize FastAPI app.
- CORS middleware for Frontend connection.
- Endpoints:
  - `POST /query`: Accepts natural language questions, returns policy-aware answers.
  - `POST /upload-policy`: (Optional for v1) To add new documents.
  - `GET /health`: Health check.

#### [NEW] `rag_engine.py`
- **Embeddings**: Use standard embeddings (e.g., `sentence-transformers` or OpenAI Embeddings) to vectorize text.
- **Vector Store**: FAISS (Facebook AI Similarity Search) to store and retrieve policy chunks.
- **LLM Interface**: Connect to LLM (e.g., via LangChain or direct API) to generate answers based on retrieved context.
- **Logic**:
  - Context retrieval.
  - Prompt engineering for "safe", "ambiguity-aware", and "sensitive" responses.

#### [NEW] `models.py`
- Pydantic models for request/response validation.

#### [NEW] `config.py`
- Environment variable loading (API keys, settings).

### Frontend (`/frontend`)
We will use **Next.js**.
#### [NEW] `pages/index.js`
- Minimal Chat UI.
- Input field for questions.
- Display area for chat history (User + Bot).
- "Thinking" state indicator.

#### [NEW] `styles/globals.css`
- Basic clean styling (Vanilla CSS as per guidelines).

### Data (`/data`)
#### [NEW] `sample_policies.txt`
- A text file containing dummy corporate policies (HR, IT, Remote Work) to index on startup.

## Verification Plan

### Automated Tests
- **Backend Tests**:
  - Run `pytest` to check `/health` and mock `/query` endpoints.
  - Verify Pydantic validation rejects invalid inputs.

### Manual Verification
1. **Startup**: Run backend (`uvicorn`) and frontend (`npm run dev`).
2. **Indexing Check**: Verify console logs show policies are indexed on startup.
3. **Query Implementation**:
   - Ask: "What is the remote work policy?" -> Expect detailed answer citing the sample policy.
   - Ask: "Can I ignore security updates?" -> Expect cautious/refusal response (Sensitive topic).
   - Ask something without context -> Expect "I don't have information on that in the policies."
4. **UI Check**: Verify chat flows smoothly and looks clean.
