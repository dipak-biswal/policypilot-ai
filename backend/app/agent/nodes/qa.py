from app.agent.state import AgentState
from app.rag import NOT_FOUND, build_context, chain, extract_citations


def qa_node(state: AgentState) -> AgentState:
    docs = state.get("docs", [])

    if not docs:
        return {"answer": NOT_FOUND, "citations": []}

    response = chain.invoke(
        {"context": build_context(docs), "question": state["question"]}
    )

    return {
        "answer": response.content,
        "citations": extract_citations(response.content, docs),
    }
