import os
import hashlib
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app import bm25

import warnings

warnings.filterwarnings("ignore", message="Relevance scores must be between 0 and 1")

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def build_vector_store():
    if os.getenv("VECTOR_BACKEND", "CHROMA") == "pgvector":
        return PGVector(
            embeddings=embeddings,
            collection_name="policies",
            connection=os.environ["DATABASE_URL"],
            use_jsonb=True,
        )
    return Chroma(
        collection_name="policies",
        embedding_function=embeddings,
        persist_directory="./chroma_db",
    )


vector_store = build_vector_store()

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=250)


def chunk_id(doc: Document) -> str:
    key = f"{doc.metadata['source']}|{doc.metadata['page']}|{doc.page_content}"
    return hashlib.sha256(key.encode()).hexdigest()


def index_pages(filename: str, pages: list[dict]) -> int:
    docs = [
        Document(
            page_content=p["text"], metadata={"source": filename, "page": p["page"]}
        )
        for p in pages
        if p["text"]
    ]

    chunks = splitter.split_documents(docs)
    ids = list(dict.fromkeys(chunk_id(c) for c in chunks))

    unique = {chunk_id(c): c for c in chunks}

    vector_store.add_documents([unique[i] for i in ids], ids=ids)

    bm25.invalidate()
    return len(chunks)


def _load_chunks(source: str | None) -> list[Document]:
    kwargs = {"filter": {"source": {"$eq": source}}} if source else {}

    return vector_store.similarity_search("insurance policy", k=2000, **kwargs)


def expand_with_page(
    docs: list[Document], source: str | None, max_docs: int = 10
) -> list[Document]:
    """Small-to-big: for the top hits, add sibling chunks from the same page and the page before,
    so rules that start on one page and list items on the next stay together."""
    key = source or "__all__"
    all_chunks = bm25.all_docs(key)
    seen = {bm25.doc_key(d) for d in docs}
    expanded = list(docs)

    for d in docs[:2]:  # only expand the strongest hits to keep the prompt small
        page = d.metadata.get("page")
        wanted = {page, page - 1} if isinstance(page, int) else {page}
        for sib in all_chunks:
            if (
                sib.metadata.get("source") == d.metadata.get("source")
                and sib.metadata.get("page") in wanted
                and bm25.doc_key(sib) not in seen
                and len(expanded) < max_docs
            ):
                expanded.append(sib)
                seen.add(bm25.doc_key(sib))
    return expanded


def search(
    query: str, k: int = 6, min_score: float = 0.2, source: str | None = None
) -> list[Document]:
    kwargs = {"filter": {"source": {"$eq": source}}} if source else {}
    results = vector_store.similarity_search_with_relevance_scores(query, k=k, **kwargs)
    vector_docs = [doc for doc, score in results if score >= min_score]

    if not vector_docs:
        return []
    key = source or "__all__"

    if not bm25.has_index(key):
        bm25.build_index(key, _load_chunks(source))
    keyword_docs = bm25.bm25_search(key, query, k * 2)

    top = rrf_top(vector_docs, keyword_docs, k)
    return expand_with_page(top, source)


def rrf_top(
    vector_docs: list[Document], keyword_docs: list[Document], k: int
) -> list[Document]:
    merged = bm25.rrf([vector_docs, keyword_docs])

    must_keep = keyword_docs[:2]
    keys = {bm25.doc_key(d) for d in must_keep}
    rest = [d for d in merged if bm25.doc_key(d) not in keys]

    return (must_keep + rest)[:k]


def delete_document(source: str) -> int:
    """Delete every chunk of one document. Returns how many chunks were removed."""
    chunks = _load_chunks(source)
    if not chunks:
        return 0
    # chunk ids are deterministic hashes, so we can rebuild them from the chunks themselves
    vector_store.delete(ids=[chunk_id(c) for c in chunks])
    bm25.invalidate()
    return len(chunks)
