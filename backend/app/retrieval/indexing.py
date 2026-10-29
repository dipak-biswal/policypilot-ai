import hashlib

from langchain_core.documents import Document

from app.retrieval import bm25
from app.retrieval.store import splitter, vector_store


def chunk_id(doc: Document) -> str:
    key = f"{doc.metadata['source']}|{doc.metadata['page']}|{doc.page_content}"
    return hashlib.sha256(key.encode()).hexdigest()


def load_chunks(source: str | None) -> list[Document]:
    kwargs = {"filter": {"source": {"$eq": source}}} if source else {}
    return vector_store.similarity_search("document", k=2000, **kwargs)


def index_pages(filename: str, pages: list[dict]) -> int:
    docs = [
        Document(
            page_content=p["text"], metadata={"source": filename, "page": p["page"]}
        )
        for p in pages
        if p["text"]
    ]
    chunks = splitter.split_documents(docs)
    unique = {chunk_id(c): c for c in chunks}
    vector_store.add_documents(list(unique.values()), ids=list(unique.keys()))
    bm25.invalidate()
    return len(unique)


def delete_document(source: str) -> int:
    chunks = load_chunks(source)
    if not chunks:
        return 0
    vector_store.delete(ids=[chunk_id(c) for c in chunks])
    bm25.invalidate()
    return len(chunks)
