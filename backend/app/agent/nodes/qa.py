from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.config import get_stream_writer

from app.agent.llm import llm
from app.agent.state import AgentState
from app.agent.tools import calculator, date_calculator
from app.generation.citations import NOT_FOUND, build_context, extract_citations
from app.prompts.loader import load_prompt
from app.retrieval.search import search

QA_SYSTEM = load_prompt("qa_agent")
MAX_ROUNDS = 4
STEP_LABELS = {
    "search_document": "🔍 Searching the document",
    "calculator": "🧮 Calculating",
    "date_calculator": "📅 Working out dates",
}


def qa_node(state: AgentState) -> AgentState:
    emit = get_stream_writer()
    question = state.get("standalone_question") or state["question"]
    source = state.get("source")
    found_docs = list(state.get("docs", []))  # retrieval node results, first context

    @tool
    def search_document(query: str) -> str:
        """Search the uploaded document for passages about `query`. Returns text tagged with [Page N].
        Call it again with different words if the first results don't answer the question.
        """
        docs = search(query, source=source)
        found_docs.extend(docs)
        return build_context(docs) or "No matching passages."

    tools = {t.name: t for t in (search_document, calculator, date_calculator)}
    agent_llm = llm.bind_tools(list(tools.values()))

    if not found_docs:
        return {
            "answer": NOT_FOUND,
            "citations": [],
            "messages": [AIMessage(content=NOT_FOUND)],
        }

    hint = state.get("profile", {}).get("domain_hint", "")
    messages = [
        SystemMessage(
            QA_SYSTEM.replace("{domain_hint}", hint).replace(
                "{context}", build_context(found_docs)
            )
        ),
        HumanMessage(question),
    ]

    response = agent_llm.invoke(messages)
    for _ in range(MAX_ROUNDS):
        if not response.tool_calls:
            break
        messages.append(response)
        for call in response.tool_calls:
            emit(
                {
                    "step": STEP_LABELS.get(call["name"], call["name"]),
                    "detail": str(call["args"]),
                }
            )
            result = tools[call["name"]].invoke(call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
        response = agent_llm.invoke(messages)

    answer = response.content or NOT_FOUND
    return {
        "answer": answer,
        "citations": extract_citations(answer, found_docs),
        "messages": [AIMessage(content=answer)],
    }
