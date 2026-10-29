import re

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from app.ingestion.profile_store import get_profile

# key -> (index, docs, stopwords used for that index)
_cache: dict[str, tuple[BM25Okapi, list[Document], set[str]]] = {}

BASE_STOPWORDS = {
    "a",
    "an",
    "the",
    "is",
    "are",
    "was",
    "be",
    "i",
    "my",
    "me",
    "can",
    "do",
    "does",
    "for",
    "in",
    "of",
    "on",
    "to",
    "and",
    "or",
    "if",
    "it",
    "what",
    "when",
    "how",
    "will",
    "with",
    "under",
    "this",
    "that",
    "there",
    "any",
    "by",
    "as",
    "at",
    "from",
}


def stopwords_for(key: str) -> set[str]:
    """Base English words + this document's own frequent words (from its profile)."""
    source = key if key and key != "all" else None
    return BASE_STOPWORDS | {w.lower() for w in get_profile(source).stopwords}


def tokenize(text: str, stopwords: set[str] = BASE_STOPWORDS) -> list[str]:
    return [w for w in re.findall(r"\w+", text.lower()) if w not in stopwords]


def has_index(key: str) -> bool:
    return key in _cache


def build_index(key: str, docs: list[Document]) -> None:
    sw = stopwords_for(key)
    _cache[key] = (BM25Okapi([tokenize(d.page_content, sw) for d in docs]), docs, sw)


def invalidate() -> None:
    _cache.clear()


def all_docs(key: str) -> list[Document]:
    return _cache[key][1] if key in _cache else []


def bm25_search(key: str, query: str, k: int) -> list[Document]:
    if key not in _cache:
        return []
    index, docs, sw = _cache[key]

    scores = index.get_scores(tokenize(query, sw))  # same stopwords as the index

    top = sorted(range(len(docs)), key=lambda i: scores[i], reverse=True)[:k]
    return [docs[i] for i in top if scores[i] > 0]


def doc_key(d: Document) -> str:
    return f"{d.metadata.get('source')}|{d.metadata.get('page')}|{d.page_content}"


def rrf(result_lists: list[list[Document]], k: int = 60) -> list[Document]:
    """Reciprocal Rank Fusion: score = sum of 1 / (k + rank) across lists."""
    scores: dict[str, float] = {}
    by_key: dict[str, Document] = {}

    for results in result_lists:
        for rank, d in enumerate(results, start=1):
            key = doc_key(d)
            scores[key] = scores.get(key, 0.0) + 1 / (k + rank)
            by_key[key] = d
    return [by_key[key] for key in sorted(scores, key=scores.get, reverse=True)]
