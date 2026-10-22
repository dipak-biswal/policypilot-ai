from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.pdf_utils import extract_pages

app = FastAPI(title="PolicyPilot AI")


class PageText(BaseModel):
    page: int
    text: str


class DocumentResponse(BaseModel):
    filename: str
    page_count: int
    pages: list[PageText]


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="policypilot-ai")


@app.post("/documents", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()
    pages = extract_pages(file_bytes)

    return DocumentResponse(
        filename=file.filename or "unknown.pdf",
        page_count=len(pages),
        pages=[PageText(**p) for p in pages],
    )
