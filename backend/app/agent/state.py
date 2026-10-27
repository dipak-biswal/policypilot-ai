from typing import Annotated, Literal, TypedDict

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

Intent = Literal["qa", "summary", "report"]


class AgentState(TypedDict, total=False):
    question: str
    standalone_question: str
    messages: Annotated[list[BaseMessage], add_messages]
    intent: Intent
    docs: list[Document]
    answer: str
    citations: list[dict]
    report: dict
    source: str | None
