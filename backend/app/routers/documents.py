from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

from app.auth.deps import get_current_user_id
from app.ingestion.pdf import extract_pages
from app.ingestion.profile import detect_profile
from app.ingestion.profile_store import delete_profile, save_profile
from app.rate_limit import limiter
from app.retrieval.indexing import delete_document, index_pages
from app.schemas.documents import DeleteResponse, DocumentResponse, PageText

router = APIRouter(prefix="/documents", tags=["documents"])


def scoped_source(user_id: str, filename: str) -> str:
    """Internal key for a user's document. Same filename for 2 users = 2 docs."""
    return f"{user_id}/{filename}"


@router.post("", response_model=DocumentResponse)
@limiter.limit("5/hour")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
) -> DocumentResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()
    pages = extract_pages(file_bytes)
    filename = file.filename or "unknown.pdf"
    source = scoped_source(user_id, filename)

    save_profile(
        source, detect_profile(pages)
    )  # profile first, so BM25 rebuild sees its stopwords
    chunks_indexed = index_pages(source, pages)  # clears the BM25 cache

    return DocumentResponse(
        filename=filename,  # the UI still sees the plain name
        page_count=len(pages),
        chunks_indexed=chunks_indexed,
        pages=[PageText(**p) for p in pages],
    )


@router.delete("/{filename}", response_model=DeleteResponse)
@limiter.limit("10/hour")
def remove_document(
    request: Request,
    filename: str,
    user_id: str = Depends(get_current_user_id),
) -> DeleteResponse:
    source = scoped_source(user_id, filename)
    deleted = delete_document(source)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    delete_profile(source)
    return DeleteResponse(filename=filename, chunks_deleted=deleted)
