from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.graph import graph

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentRequest(BaseModel):
    question: str


@router.post("")
def run_agent(req: AgentRequest) -> dict:
    result = graph.invoke({"question": req.question})

    return {
        "intent": result["intent"],
        "answer": result.get("answer", ""),
        "citations": result.get("citations", []),
        "report": result.get("report"),
    }
