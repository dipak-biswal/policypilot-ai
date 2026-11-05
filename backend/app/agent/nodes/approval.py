from langgraph.types import interrupt

from app.agent.state import AgentState


def approval_node(state: AgentState) -> AgentState:
    """Pause and ask the user to approve / edit / reject the draft answer."""
    draft = state.get("answer", "")
    decision = interrupt(
        {
            "type": "approve_answer",
            "draft": draft,
            "question": state.get("standalone_question") or state.get("question", ""),
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
