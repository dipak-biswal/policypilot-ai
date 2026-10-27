from pydantic import BaseModel


class AgentRequest(BaseModel):
    question: str
    source: str | None = None
    thread_id: str | None = None
