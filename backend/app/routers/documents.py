from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from app.ingestion.pdf import extract_pages
from app.ingestion.profile import detect_profile
from app.ingestion.profile_store import delete_profile, save_profile
from app.rate_limit import limiter
from app.retrieval.indexing import delete_document, index_pages
from app.schemas.documents import DeleteResponse, DocumentResponse, PageText

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse)
@limiter.limit("5/hour")
async def upload_document(
    request: Request, file: UploadFile = File(...)
) -> DocumentResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()
    pages = extract_pages(file_bytes)
    filename = file.filename or "unknown.pdf"

    save_profile(
        filename, detect_profile(pages)
    )  # profile first, so BM25 rebuild sees its stopwords
    chunks_indexed = index_pages(filename, pages)  # clears the BM25 cache

    return DocumentResponse(
        filename=filename,
        page_count=len(pages),
        chunks_indexed=chunks_indexed,
        pages=[PageText(**p) for p in pages],
    )


@router.delete("/{filename}", response_model=DeleteResponse)
@limiter.limit("10/hour")
def remove_document(request: Request, filename: str) -> DeleteResponse:
    deleted = delete_document(filename)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    delete_profile(filename)
    return DeleteResponse(filename=filename, chunks_deleted=deleted)
