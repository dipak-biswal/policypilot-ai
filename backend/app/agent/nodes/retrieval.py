from app.agent.state import AgentState
from app.core.config import settings
from app.retrieval.search import search


def retrieval_node(state: AgentState) -> AgentState:
    source = state.get("source")
    if state["intent"] == "qa":
        docs = search(
            state.get("standalone_question") or state["question"], source=source
        )
    else:
        query = state.get("profile", {}).get("summary_query") or settings.summary_query
        docs = search(query, k=8, min_score=0.0, source=source)

    return {"docs": docs}
