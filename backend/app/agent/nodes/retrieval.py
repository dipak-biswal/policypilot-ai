from app.agent.state import AgentState
from app.retrieval.search import search
from app.core.config import settings

SUMMARY_QUERY = settings.summary_query


def retrieval_node(state: AgentState) -> AgentState:
    source = state.get("source")
    if state["intent"] == "qa":
        docs = search(
            state.get("standalone_question") or state["question"], source=source
        )

    else:
        docs = search(SUMMARY_QUERY, k=8, min_score=0.0, source=source)

    return {"docs": docs}
