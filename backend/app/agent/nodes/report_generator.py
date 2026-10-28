from langchain_core.prompts import ChatPromptTemplate

from app.agent.llm import llm
from app.agent.report_schema import Report
from app.agent.state import AgentState
from app.generation.citations import build_context

report_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You design a visual report about an insurance policy using ONLY the context.\n"
            "Pick the block type that best fits each piece of information:\n"
            "- stat: 2-4 headline numbers (sum insured, premium, co-pay, room rent cap)\n"
            "- callout (tone=warning): exclusions, gotchas, things NOT covered\n"
            "- callout (tone=info/success): helpful tips or good news\n"
            "- checklist: what is covered (covered=true) vs not covered (covered=false)\n"
            "- timeline: waiting periods, in order from shortest to longest\n"
            "- table: sub-limits or anything with rows and columns\n"
            "- progress: ONLY real percentages stated in the policy (e.g. 20% co-pay). Never for ranges or amounts.\n"
            "- accordion: long details like claim process steps or exclusion lists\n"
            "- bullets: anything else\n"
            "Use 4-8 blocks, don't repeat the same info in two blocks, and never invent numbers. "
            "Never output a block, stat or item with 'Not specified', 'N/A' or unknown values - just omit it. "
            "Fill `pages` on every block with source page numbers. "
            "Suggest 3 follow-up questions.\n\nContext:\n{context}",
        ),
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
        {"context": build_context(docs), "question": question}
    )

    pages = sorted({p for b in report.blocks for p in b.pages})

    citations = [
        {"source": docs[0].metadata["source"], "page": p, "snippet": ""} for p in pages
    ]

    return {
        "report": report.model_dump(),
        "answer": report.summary,
        "citations": citations,
    }
