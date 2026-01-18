# Policy Assistant - Project Walkthrough

## How It Works (The "Zero-Training" Magic)

You asked if you need to "train" the model. The answer is **NO**.
We are using a technique called **RAG (Retrieval-Augmented Generation)**.

### 1. Traditional Training vs. RAG
- **Training**: Teaching a model everything by showing it millions of books. It takes weeks and costs customized hardware. If you change a policy, you have to re-train.
- **RAG (Our Approach)**: We keep the "Brain" (LLM) generic (like GPT-4). We give it a "Library" (your policy files). When you ask a question, the Brain looks up the relevant page in the Library and reads it to you.
    - **Advantage**: If you update a policy today, the system knows it immediately. No re-training required.

### 2. The Architecture Steps

#### Step A: Ingestion (The Library)
1. You place `.txt` files in `data/`.
2. **Standardization**: `rag_engine.py` reads them.
3. **Chunking**: It splits long text into smaller "chunks" (paragraphs).
4. **Embedding**: It uses a *local AI model* (`all-MiniLM-L6-v2`) to turn these chunks into lists of numbers (vectors).
5. **Indexing**: These vectors are stored in **FAISS**, which is like a super-fast search engine for meanings, not just keywords.

#### Step B: The Query Loop (The Assistant)
1. **User asks**: "Can I work from home?"
2. **Search**: The system converts your question into numbers and asks FAISS: "Which policy chunks are mathematically closest to this question?"
3. **Retrieval**: FAISS returns the specific snippets about "Remote Work".
4. **Generation**: We send a prompt to the LLM (OpenAI) that looks like this:
   > "Here is some context: [Remote Work Policy Text...]
   > User Question: Can I work from home?
   > Answer the user using ONLY the context above."
5. **Answer**: The LLM writes a natural language response.

## Project Structure

### Backend (`/backend`)
- **`main.py`**: The API Server. It receives the question from the frontend.
- **`rag_engine.py`**: The Core. Handles loading files, searching FAISS, and talking to OpenAI.
- **`config.py`**: Settings. Where you put your API Keys.
- **`models.py`**: Definitions of what a "Question" and "Answer" look like for the API.

### Frontend (`/frontend`)
- **`page.tsx`**: The Chat Interface. It sends your text to the backend and displays the reply.
- **`globals.css`**: The styling (Dark mode, animations).

## How to Run It

### Prerequisites
1. **OpenAI API Key**: You need this for the "Generation" step. Without it, the system can find the documents but can't write the answer.
   - Set it in `backend/.env` or export it: `export OPENAI_API_KEY=sk-...`

### commands
1. **Start Backend**:
   ```bash
   source dev_env/bin/activate
   uvicorn backend.main:app --reload --port 8000
   ```
2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
3. **Open Browser**: Go to `http://localhost:3000`

## Verification Results
- **Ingestion**: Verified that `rag_engine` loads `.txt` files from `data/`.
- **Retrieval**: The local embedding model works without an API key. It can find relevant policies.
- **Interface**: The Chat UI connects to the backend and displays responses.
