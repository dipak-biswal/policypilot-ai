from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.agent.graph import graph, thread_config
from app.agent.stream import stream_agent
from app.auth.deps import get_current_user_id
from app.rate_limit import limiter
from app.routers.documents import scoped_source
from app.schemas.agent import AgentRequest

router = APIRouter(prefix="/agent", tags=["agent"])


def _scope(body: AgentRequest, user_id: str) -> tuple[str, str]:
    if not body.source:
        # no source = "search all documents", which would cross users
        raise HTTPException(status_code=400, detail="Select a document first")
    source = scoped_source(user_id, body.source)
    thread_id = f"{user_id}:{body.thread_id or 'default'}"
    return source, thread_id


@router.post("")
@limiter.limit("10/minute")
def run_agent(
    request: Request,
    body: AgentRequest,
    user_id: str = Depends(get_current_user_id),
) -> dict:
    source, thread_id = _scope(body, user_id)
    result = graph.invoke(
        {"question": body.question, "source": source},
        config=thread_config(thread_id),
    )
    return {
        "intent": result.get("intent"),
        "answer": result.get("answer"),
        "citations": result.get("citations", []),
        "report": result.get("report"),
        "follow_up_questions": result.get("follow_up_questions", []),
    }


@router.post("/stream")
@limiter.limit("10/minute")
def agent_stream(
    request: Request,
    body: AgentRequest,
    user_id: str = Depends(get_current_user_id),
):
    source, thread_id = _scope(body, user_id)
    return StreamingResponse(
        stream_agent(body.question, source, thread_id),
        media_type="text/event-stream",
    )
