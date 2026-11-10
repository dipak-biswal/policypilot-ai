import re
from langgraph.types import interrupt
from app.agent.state import AgentState

_HIGH_STAKES = re.compile(
    r"\b(waiting period|exclusion|excluded|not covered|pre-?existing|"
    r"maternity|claim|deductible|co-?pay|limit|sub-?limit|"
    r"cancellation|refund|premium)\b",
    re.IGNORECASE,
)


def needs_approval(question: str, answer: str) -> bool:
    blob = f"{question}\n{answer}"
    return bool(_HIGH_STAKES.search(blob))


def approval_node(state: AgentState) -> AgentState:
    """Pause only for high-stakes drafts; otherwise auto-pass."""
    draft = state.get("answer", "")
    question = state.get("standalone_question") or state.get("question", "")

    if not needs_approval(question, draft):
        return {}

    decision = interrupt(
        {
            "type": "approve_answer",
            "draft": draft,
            "question": question,
        }
    )
    action = (decision or {}).get("action", "approve")
    if action == "reject":
        return {
            "answer": "Okay - I discarded that draft. Ask another question whenever you're ready.",
            "citations": [],
        }
    if action == "edit":
        edited = (decision or {}).get("text") or draft
        return {"answer": edited}
    return {}
