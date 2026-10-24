from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.generation.qa import answer_question, stream_answer
from app.schemas.chat import ChatRequest, ChatResponse
from app.retrieval.search import search

router = APIRouter(tags=["chat (legacy)"])


@router.get("/search")
def search_chunks(q: str) -> list[dict]:
    results = search(q)
    return [{"text": d.page_content[:300], **d.metadata} for d in results]


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    return ChatResponse(**answer_question(req.question))


@router.post("/chat/stream")
def chat_stream(req: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        stream_answer(req.question), media_type="text/event-stream"
    )
