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
- [x] Milestone 5: Modular React + TypeScript UI (api/hooks/components) with PDF upload and citation chips
- [x] Milestone 5b: Token streaming over SSE (FastAPI StreamingResponse + fetch ReadableStream in React)
- [x] Milestone 6: LangGraph agent (router → retrieval → qa / summarizer / report generator) with structured-output reports and follow-up suggestions
- [x] Milestone 7: Dynamic report rendering (layout-driven components) + clickable follow-up suggestions
- [x] Milestone 8a: LangSmith tracing of every graph run (router decision, retrieved chunks, latency, tokens)
