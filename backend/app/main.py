from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.pdf_utils import extract_pages
from app.vector_store import index_pages, search
from app.rag import answer_question

app = FastAPI(title="PolicyPilot AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    service: str


class PageText(BaseModel):
    page: int
    text: str


class DocumentResponse(BaseModel):
    filename: str
    page_count: int
    chunks_indexed: int
    pages: list[PageText]


class ChatRequest(BaseModel):
    question: str


class Citations(BaseModel):
    source: str
    page: int
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citations]


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="policypilot-ai")


@app.post("/documents", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()
    pages = extract_pages(file_bytes)
    filename = file.filename or "unknown.pdf"
    chunks_indexed = index_pages(filename, pages)

    return DocumentResponse(
        filename=filename,
        page_count=len(pages),
        chunks_indexed=chunks_indexed,
        pages=[PageText(**p) for p in pages],
    )


@app.get("/search")
def search_chunks(q: str) -> list[dict]:
    results = search(q)

    return [{"text": d.page_content[:300], **d.metadata} for d in results]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    return ChatResponse(**answer_question(req.question))
