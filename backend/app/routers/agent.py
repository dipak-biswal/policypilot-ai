from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.schemas.agent import AgentRequest
from app.agent.graph import graph, thread_config
from app.agent.stream import stream_agent
from app.rate_limit import limiter

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("")
@limiter.limit("10/minute")
def run_agent(request: Request, body: AgentRequest) -> dict:
    # `request` is only for slowapi (to read the client IP); `body` is the JSON payload
    result = graph.invoke(
        {"question": body.question, "source": body.source},
        config=thread_config(body.thread_id),
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
def agent_stream(request: Request, body: AgentRequest):
    return StreamingResponse(
        stream_agent(body.question, body.source),
        media_type="text/event-stream",
    )
