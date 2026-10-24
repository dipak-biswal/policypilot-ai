from pydantic import BaseModel


class PageText(BaseModel):
    page: int
    text: str


class DocumentResponse(BaseModel):
    filename: str
    page_count: int
    chunks_indexed: int
    pages: list[PageText]


class DeleteResponse(BaseModel):
    filename: str
    chunks_deleted: int
