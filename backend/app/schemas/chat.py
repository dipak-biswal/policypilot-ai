from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class ChatRequest(BaseModel):
    question: str


class Citations(BaseModel):
    source: str
    page: int
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citations]
