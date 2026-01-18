# Data Processing & Indexing Pipeline

This directory contains all scripts used to transform raw policy documents
into a searchable vector index for the PolicyLens RAG system.

Due to size and security constraints, raw datasets, generated chunks,
and FAISS indexes are not included in the repository. All artifacts can be
reproduced using the scripts below.

---

## Pipeline Overview

The data processing workflow follows these steps:

1. **Raw Document Parsing**
   - Source policy documents are cleaned and normalized.
   - Metadata such as source file and path are preserved.

2. **Filtering & Structuring**
   - Documents are filtered to retain policy-relevant sections.
   - Structured representations are created for downstream processing.

3. **Chunking**
   - Large documents are split into semantically coherent chunks.
   - Chunk sizes are chosen to balance retrieval accuracy and context length.

4. **Embedding & Indexing**
   - Each chunk is converted into a vector embedding.
   - Embeddings are indexed using FAISS for fast similarity search.

5. **Query & Retrieval**
   - User queries are embedded and matched against the FAISS index.
   - Top-k relevant chunks are retrieved and passed to the RAG engine.

---

## Script Descriptions

- **create_parsed_sources.py**  
  Parses and structures raw policy documents while preserving metadata.

- **create_filtered_sources.py**  
  Filters parsed documents to retain relevant policy content.

- **chunk_splitter.py**  
  Splits filtered documents into semantically meaningful chunks.

- **build_faiss_index.py**  
  Generates embeddings for all chunks and builds the FAISS vector index.

- **query_faiss.py**  
  Performs similarity search over the FAISS index for a given query.

---

## Reproducibility

To fully reproduce the data pipeline:
1. Provide the raw policy documents as input.
2. Run the scripts in the order described above.
3. Generate the FAISS index before starting the backend server.

All scripts are deterministic and can be re-run without manual intervention.
