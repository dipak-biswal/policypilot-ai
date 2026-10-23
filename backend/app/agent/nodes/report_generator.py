from langchain_core.prompts import ChatPromptTemplate

from app.agent.llm import llm
from app.agent.report_schema import Report
from app.agent.state import AgentState
from app.rag import build_context

report_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Create a structured report about this insurance policy using ONLY the context. "
            "Choose the best layout per section: table for limits/waiting periods, bullets for "
            "coverages/exclusions, keyValue for short facts. Fill `pages` with source page numbers. "
            "Suggest 3 follow-up questions.\n\nContext:\n{context}",
        ),
        "human",
        "{question}",
    ]
)

report_chain = report_prompt | llm.with_structured_output(Report)


def report_node(state: AgentState) -> AgentState:
    docs = state["docs"]
    report: Report = report_chain.invoke(
        {"context": build_context(docs), "question": state["question"]}
    )

    pages = sorted({p for s in report.sections for p in s.pages})

    citations = [
        {"source": docs[0].metadata["source"], "page": p, "snippet": ""} for p in pages
    ]

    return {
        "report": report.model_dump(),
        "answer": report.summary,
        "citations": citations,
    }
