"""Cheap, non-LLM checks: retrieval hit rate, off-topic refusal, router accuracy."""


def doc_page(d) -> int:
    # search() may return Documents or (Document, score) tuples
    doc = d[0] if isinstance(d, tuple) else d
    return int(doc.metadata["page"])


def doc_text(d) -> str:
    doc = d[0] if isinstance(d, tuple) else d
    return doc.page_content


def page_hit(docs, expected_pages: list[int]) -> bool:
    """True if at least one expected page was retrieved."""
    retrieved = {doc_page(d) for d in docs}
    return bool(retrieved & set(expected_pages))


def is_refusal(result: dict, not_found: str) -> bool:
    """Off-topic answers should be the NOT_FOUND message with no citations."""
    answer = (result.get("answer") or "").strip().lower()
    return not_found.strip().lower() in answer and not result.get("citations")
