from app.agent.state import AgentState
from app.generation.citations import NOT_FOUND, build_context, extract_citations
from app.generation.qa import chain
from langchain_core.messages import AIMessage


def qa_node(state: AgentState) -> AgentState:
    docs = state.get("docs", [])

    if not docs:
        return {
            "answer": NOT_FOUND,
            "citations": [],
            "messages": [AIMessage(content=NOT_FOUND)],
        }

    response = chain.invoke(
        {
            "context": build_context(docs),
            "question": state.get("standalone_quetion") or state["question"],
        }
    )

    return {
        "answer": response.content,
        "citations": extract_citations(response.content, docs),
        "messages": [AIMessage(content=response.content)],
    }
