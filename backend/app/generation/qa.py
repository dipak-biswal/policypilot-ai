from collections.abc import Iterator

from langchain_openai import ChatOpenAI

from app.generation.citations import NOT_FOUND, build_context, extract_citations
from app.generation.prompts import QA_PROMPT
from app.retrieval.search import search
from app.utils.sse import sse
from app.agent.llm import llm

chain = QA_PROMPT | llm


def answer_question(question: str) -> dict:
    docs = search(question)
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
