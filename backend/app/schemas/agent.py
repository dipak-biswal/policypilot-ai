from typing import Literal
from pydantic import BaseModel


class AgentRequest(BaseModel):
    question: str
    source: str | None = None
    thread_id: str | None = None


class ResumeRequest(BaseModel):
    thread_id: str | None = None
    action: Literal["approve", "edit", "reject"]
    text: str | None = None  # used when action == "edit"
