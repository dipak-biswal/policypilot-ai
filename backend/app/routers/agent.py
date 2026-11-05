from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.agent.graph import graph, thread_config
from app.agent.stream import BLOCKED_REPLY, resume_agent, stream_agent
from app.auth.deps import get_current_user_id
from app.guardrails.pipeline import run_input_guards
from app.rate_limit import limiter
from app.routers.documents import scoped_source
from app.schemas.agent import AgentRequest, ResumeRequest

router = APIRouter(prefix="/agent", tags=["agent"])


def _scope_source(user_id: str, source: str | None) -> str:
    if not source:
        raise HTTPException(status_code=400, detail="Select a document first")
    return scoped_source(user_id, source)


def _thread(user_id: str, thread_id: str | None) -> str:
    return f"{user_id}:{thread_id or 'default'}"


@router.post("")
@limiter.limit("10/minute")
def run_agent(
    request: Request,
    body: AgentRequest,
    user_id: str = Depends(get_current_user_id),
) -> dict:
    source = _scope_source(user_id, body.source)
    thread_id = _thread(user_id, body.thread_id)
    guard = run_input_guards(body.question)
    if not guard.allowed:
        return {
            "intent": "chat",
            "answer": BLOCKED_REPLY,
            "citations": [],
            "report": None,
            "follow_up_questions": [],
            "guardrail": {
                "blocked": True,
                "reason": guard.blocked_reason,
                "pii": guard.pii_found,
            },
        }
    result = graph.invoke(
        {"question": guard.question, "source": source},
        config=thread_config(thread_id),
    )
    return {
        "intent": result.get("intent"),
        "answer": result.get("answer"),
        "citations": result.get("citations", []),
        "report": result.get("report"),
        "follow_up_questions": result.get("follow_up_questions", []),
        "guardrail": (
            {"blocked": False, "pii": guard.pii_found} if guard.pii_found else None
        ),
    }


@router.post("/stream")
@limiter.limit("10/minute")
def agent_stream(
    request: Request,
    body: AgentRequest,
    user_id: str = Depends(get_current_user_id),
):
    source = _scope_source(user_id, body.source)
    thread_id = _thread(user_id, body.thread_id)
    return StreamingResponse(
        stream_agent(body.question, source, thread_id),
        media_type="text/event-stream",
    )


@router.post("/resume")
@limiter.limit("10/minute")
def agent_resume(
    request: Request,
    body: ResumeRequest,
    user_id: str = Depends(get_current_user_id),
):
    if body.action == "edit" and not (body.text or "").strip():
        raise HTTPException(status_code=400, detail="Edited text is required")
    thread_id = _thread(user_id, body.thread_id)
    return StreamingResponse(
        resume_agent(thread_id, {"action": body.action, "text": body.text}),
        media_type="text/event-stream",
    )
