from langchain_core.documents import Document

from app.rag import extract_citations


def make_doc(page: int, text: str = "some text") -> Document:
    return Document(page_content=text, metadata={"source": "policy.pdf", "page": page})


def test_only_cited_pages_are_returned():
    docs = [make_doc(9), make_doc(10), make_doc(15)]
    result = extract_citations("Answer here [Page 10].", docs)
    assert [c["page"] for c in result] == [10]


def test_duplicates_removed_and_sorted():
    docs = [make_doc(17), make_doc(9), make_doc(9)]
    result = extract_citations("A [Page 17] and B [Page 9, Page 9].", docs)
    assert [c["page"] for c in result] == [9, 17]


def test_no_citations_when_answer_cites_nothing():
    assert extract_citations("I don't know.", [make_doc(1)]) == []
