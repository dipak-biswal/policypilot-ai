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
- [x] Milestone 8b: pytest suite (citation logic, PDF extraction, API endpoints with mocked agent)
- [x] Milestone 8c: RAGAS evaluation (16-question golden set, retrieval hit rate, off-topic refusal, router accuracy)
- [x] Milestone 8d: Agent streaming (POST /agent/stream, SSE with intent/token/report/citations events via LangGraph stream_mode)
- [x] Milestone 9a/9b: Postgres + pgvector via docker-compose, switchable VECTOR_BACKEND (chroma | pgvector); eval parity (recall 0.95)
- [x] Milestone 9c: Full stack in Docker (backend uv image, frontend multi-stage Vite + nginx, one-command `docker compose up`)

## Design decisions

### Evaluation-driven tuning

| Change                                          | Hit rate | Faithfulness | Relevancy | Recall |
| ----------------------------------------------- | -------- | ------------ | --------- | ------ |
| Baseline (k=4, min_score 0.3, 1000/200 chunks)  | 0.69     | 0.62         | 0.57      | 0.62   |
| k=6, min_score 0.2                              | 1.00     | 0.91         | 0.71      | 0.85   |
| Strip header/footer boilerplate, 800/150 chunks | 1.00     | 0.96         | 0.81      | 0.95   |

Off-topic refusal 2/2 and router accuracy 5/5 throughout.

## Run with Docker

1. Copy `backend/.env.example` to `backend/.env` and add your OpenAI key
2. `docker compose up -d --build`
3. Open http://localhost:5173
