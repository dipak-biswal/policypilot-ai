from langchain_core.documents import Document

from app.retrieval import bm25
from app.retrieval.indexing import load_chunks
from app.retrieval.store import vector_store


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
        bm25.build_index(key, load_chunks(source))
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


def warm_up() -> None:
    """Build the default BM25 index and open DB + embedding connections at startup."""
    try:
        vector_store.similarity_search("warm up", k=1)  # opens DB pool + OpenAI client
        if not bm25.has_index("__all__"):
            bm25.build_index("__all__", load_chunks(None))
        print(
            f"WARMUP done: {len(bm25.all_docs('__all__'))} chunks indexed", flush=True
        )
    except Exception as e:  # empty DB or no key shouldn't stop the server
        print(f"WARMUP skipped: {e}", flush=True)
