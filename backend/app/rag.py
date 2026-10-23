import re
import json
from collections.abc import Iterator

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.vector_store import search

NOT_FOUND = "I couldn't find this in the uploaded policy."

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are PolicyPilot, an assistant that answers questions about insurance policies. "
            "Answer ONLY from the context below. If the answer is not in the context, say you don't know. "
            "Cite pages inline like [Page 12].\n\nContext:\n{context}",
        ),
        ("human", "{question}"),
    ]
)

chain = prompt | llm


def build_context(docs: list[Document]) -> str:
    return "\n\n".join(f"[Page {d.metadata['page']}] {d.page_content}" for d in docs)


def extract_citations(answer: str, docs: list[Document]) -> list[dict]:
    cited_pages = {int(p) for p in re.findall(r"\[Page (\d+)\]", answer)}
    citations: dict[int, dict] = {}

    for d in docs:
        page = d.metadata["page"]
        if page in cited_pages and page not in citations:
            citations[page] = {
                "source": d.metadata["source"],
                "page": d.metadata["page"],
                "snippet": d.page_content[:200],
            }
    return sorted(citations.values(), key=lambda c: c["page"])


def answer_question(question: str) -> dict:
    docs = search(question, k=4)

    if not docs:
        return {
            "answer": NOT_FOUND,
            "citations": [],
        }

    response = chain.invoke({"context": build_context(docs), "question": question})

    return {
        "answer": response.content,
        "citations": extract_citations(response.content, docs),
    }


def sse(event: str, data) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def stream_answer(question: str) -> Iterator[str]:
    docs = search(question)
    if not docs:
        yield sse("token", NOT_FOUND)
        yield sse("citations", [])
        yield sse("done", None)
        return
    full_answer = ""
    for chunk in chain.stream({"context": build_context(docs), "question": question}):
        if chunk.content:
            full_answer += chunk.content
            yield sse("token", chunk.content)
    yield sse("citations", extract_citations(full_answer, docs))
    yield sse("done", None)
