from typing import Literal, TypedDict

from langchain_core.documents import Document

Intent = Literal["qa", "summary", "report"]


class AgentState(TypedDict, total=False):
    question: str
    intent: Intent
    docs: list[Document]
    answer: str
    citations: list[dict]
    report: dict
