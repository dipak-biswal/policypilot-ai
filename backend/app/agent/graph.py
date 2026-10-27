import uuid

from langgraph.graph import END, START, StateGraph

from app.agent.nodes.qa import qa_node
from app.agent.nodes.retrieval import retrieval_node
from app.agent.nodes.router import router_node
from app.agent.nodes.summarizer import summarizer_node
from app.agent.state import AgentState
from app.agent.nodes.report_generator import report_node
from app.agent.nodes.rewriter import rewriter_node
from langgraph.checkpoint.memory import MemorySaver


def pick_next(state: AgentState) -> str:
    return {"qa": "qa", "summary": "summarizer", "report": "report"}[state["intent"]]


def thread_config(thread_id: str | None = None) -> dict:
    return {"configurable": {"thread_id": thread_id or str(uuid.uuid4())}}


builder = StateGraph(AgentState)
builder.add_node("router", router_node)
builder.add_node("retrieval", retrieval_node)
builder.add_node("qa", qa_node)
builder.add_node("summarizer", summarizer_node)
builder.add_node("report", report_node)
builder.add_node("rewriter", rewriter_node)

builder.add_edge(START, "rewriter")
builder.add_edge("rewriter", "router")
builder.add_edge("router", "retrieval")

builder.add_conditional_edges(
    "retrieval", pick_next, {"qa": "qa", "summarizer": "summarizer", "report": "report"}
)
builder.add_edge("qa", END)
builder.add_edge("summarizer", END)
builder.add_edge("report", END)

graph = builder.compile(checkpointer=MemorySaver())
