from fastapi import APIRouter, HTTPException, File, Request, UploadFile

from app.ingestion.pdf import extract_pages
from app.rate_limit import limiter
from app.schemas.documents import DeleteResponse, DocumentResponse, PageText
from app.retrieval.indexing import delete_document, index_pages

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
    chunks_indexed = index_pages(filename, pages)

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
    return DeleteResponse(filename=filename, chunks_deleted=deleted)
