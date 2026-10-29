from langchain_core.prompts import ChatPromptTemplate

from app.agent.llm import llm
from app.agent.report_schema import Report
from app.agent.state import AgentState
from app.generation.citations import build_context
from app.prompts.loader import load_prompt

report_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", load_prompt("report")),
        ("human", "{question}"),
    ]
)

report_chain = report_prompt | llm.with_structured_output(
    Report, method="function_calling"
)


def report_node(state: AgentState) -> AgentState:
    docs = state["docs"]
    question = state.get("standalone_question") or state["question"]

    report: Report = report_chain.invoke(
        {
            "context": build_context(docs),
            "question": question,
            "domain_hint": state.get("profile", {}).get("domain_hint", ""),
        }
    )

    pages = sorted({p for b in report.blocks for p in b.pages})
    source = docs[0].metadata["source"] if docs else state.get("source")
    citations = [
        {
            "source": source,
            "page": p,
            "snippet": "",
        }
        for p in pages
    ]

    return {
        "report": report.model_dump(),
        "answer": report.summary,
        "citations": citations,
    }
