from app.agent.state import AgentState
from app.vector_store import search

SUMMARY_QUERY = "policy coverage benefits sum insured exclusions waiting periods claims"


def retrieval_node(state: AgentState) -> AgentState:
    source = state.get("source")
    if state["intent"] == "qa":
        docs = search(state["question"], k=4, source=source)
    else:
        docs = search(SUMMARY_QUERY, k=8, min_score=0.0, source=source)

    return {"docs": docs}
