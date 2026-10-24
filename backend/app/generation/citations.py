import re

from langchain_core.documents import Document

NOT_FOUND = "I couldn't find this in the uploaded policy."


def build_context(docs: list[Document]) -> str:
    """Join chunks into one prompt string, each tagged with its page so the LLM can cite it."""
    return "\n\n".join(f"[Page {d.metadata['page']}] {d.page_content}" for d in docs)


def extract_citations(answer: str, docs: list[Document]) -> list[dict]:
    """Find [Page N] mentions in the answer and return one citation per cited page."""
    cited_pages = {int(p) for p in re.findall(r"Page (\d+)", answer)}
    citations: dict[int, dict] = {}
    for d in docs:
        page = d.metadata["page"]
        if page in cited_pages and page not in citations:
            citations[page] = {
                "source": d.metadata["source"],
                "page": page,
                "snippet": d.page_content[:200],
            }
    return sorted(citations.values(), key=lambda c: c["page"])
