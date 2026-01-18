# PolicyLens
**Turning complex policies into clear answers.**

PolicyLens is an AI-powered policy assistant that helps users ask natural language questions and receive grounded, context-aware answers from internal policy documents. Built using a Retrieval-Augmented Generation (RAG) architecture, it combines semantic search with large language models to deliver accurate, trustworthy responses.

---

## ✨ Key Features

- 🔍 **Semantic Policy Search** – FAISS vector indexing for fast, relevant retrieval
- 🤖 **LLM-Powered Answers** – Intelligent responses with robust fallback logic
- 📚 **Source Attribution** – Full transparency with cited policy references
- 🧠 **Context-Aware Responses** – Answers grounded strictly in policy text
- 🔒 **Secure & Reproducible** – No raw data or secrets in version control

---

## 🧠 How It Works

1. **Document Processing** – Policy documents are parsed, cleaned, and split into semantic chunks
2. **Embedding Generation** – Each chunk is converted into a vector embedding
3. **Vector Indexing** – Embeddings are indexed using FAISS for fast similarity search
4. **Query Processing**:
   - User submits a natural language question
   - System retrieves most relevant policy chunks
   - LLM generates response **only from retrieved context**
5. **Response Display**:
   - Clear, concise answer
   - Supporting policy sources
   - Model attribution

---

## 🏗️ Architecture Overview
```
User Query
    ↓
Frontend (Next.js)
    ↓
Backend (FastAPI)
    ├── FAISS Vector Search
    ├── Embedding Model
    └── LLM (OpenAI/Gemini with fallback)
```

---

## 🧰 Tech Stack

### Frontend
- **Next.js** – React framework for production
- **Tailwind CSS** – Utility-first styling

### Backend
- **FastAPI** – High-performance Python API framework
- **FAISS** – Efficient similarity search and clustering
- **OpenAI / Gemini** – LLM providers with automatic fallback

### ML/NLP
- **Text Embedding Models(Sentence Transformers / Gemini / OpenAI)** – Text embeddings
- **RAG Architecture** – Retrieval-Augmented Generation

---

## 📂 Repository Structure
```
policy_assistant/
│
├── backend/               # FastAPI backend & logic
│   ├── rag/               # RAG specific modules
│   ├── main.py            # API entry point
│   ├── rag_engine.py      # Core RAG logic integration
│   ├── config.py          # Configuration settings
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # Next.js frontend application
│   ├── src/               # Source code
│   │   └── app/           # App router pages & components
│   ├── public/            # Static assets
│   └── package.json       # Node dependencies
│
├── data_processing/       # Data ingestion & processing pipeline
│   ├── README.md          # Pipeline documentation
│   ├── chunk_splitter.py  # Text chunking logic
│   ├── build_faiss_index.py # Vector indexing script
│   └── query_faiss.py     # Search testing script
│
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

---

## 📊 Data & Reproducibility

> ⚠️ **Note:** Raw datasets, embeddings, and FAISS indexes are intentionally excluded from this repository.

**Why?**
- Large file sizes unsuitable for version control
- Security and licensing considerations
- Industry best practices for data management

**Good news:** The entire pipeline is **fully reproducible** using the scripts in `data_processing/`.

📄 See **[data_processing/README.md](data_processing/README.md)** for complete instructions.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- API keys for OpenAI and/or Google Gemini

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend will run on `http://localhost:3000`

### Environment Variables

Create a `.env` file in the `backend/` directory:
```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

---

## 💡 Use Case Examples

**Sample Questions:**
- "What is the company's termination policy?"
- "How does the remote work policy work?"
- "What are the guidelines for leave and benefits?"
- "Is there a dress code mentioned in the employee handbook?"

PolicyLens provides answers **only when supported by policy context**. If information isn't available in the documents, it clearly states this limitation rather than hallucinating.

---

## 🔮 Future Enhancements

- [ ] Multi-document upload support
- [ ] User feedback loop for improving responses
- [ ] Advanced filtering (by department, policy type, date)
- [ ] Conversation history and follow-up questions
- [ ] Export responses with citations

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

**Lakshya**

Questions or feedback? Feel free to open an issue or reach out!

---

## 🙏 Acknowledgments

Built with:
- [FAISS](https://github.com/facebookresearch/faiss) by Facebook Research
- [OpenAI API](https://openai.com/)
- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)