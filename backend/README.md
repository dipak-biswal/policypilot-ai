# PolicyPilot AI

Agentic RAG app: upload insurance/health policy PDFs, chat with them, and get cited answers and AI-generated summary reports.

## Tech Stack

- Frontend: React + TypeScript + Vite
- Backend: Python, FastAPI, uv
- AI: LangChain, LangGraph, OpenAI
- Vector DB: ChromaDB → PostgreSQL + pgvector
- Quality: LangSmith, RAGAS, pytest
- DevOps: Docker, GitHub Actions

## Progress

- [x] Milestone 0: Repo + Python env setup with uv
- [x] Milestone 1: FastAPI server with typed /health endpoint
- [x] Milestone 2: PDF upload endpoint with page-wise text extraction (pypdf)
- [x] Milestone 3: Chunking (RecursiveCharacterTextSplitter), OpenAI embeddings, ChromaDB vector search with page metadata
- [x] Milestone 4: RAG /chat endpoint with grounded answers, relevance-score filtering and page citations
