from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from app.agent.llm import llm


class CheckerState(TypedDict):
    answer: str
    context: str
    verified: bool
    issues: list[str]


class Verdict(BaseModel):
    verified: bool = Field(
        description="True only if every claim is supported by the context"
    )
    issues: list[str] = Field(
        description="Each unsupported or wrongly-cited claim, one line each"
    )


_SYSTEM = """You verify a drafted answer against the retrieved context.

Check ONLY factual claims that assert something IS in the policy
(numbers, durations, amounts, coverage, exclusions, conditions).

Rules:
- A claim is supported if the context states it or clearly implies it.
- A number or condition is supported ONLY if the context links it to the
  SAME subject. A figure stated for one topic (e.g. "any illness") does
  NOT support the same figure for another topic (e.g. "maternity").
- Do NOT flag statements that information is missing or unknown
  (e.g. "the document does not specify X", "I don't know").
- Do NOT flag wording, tone, or completeness. Only unsupported facts.
- Each issue must quote the unsupported claim and say what the context says instead.
- If every factual claim is supported, return verified=true and issues=[].

Examples:

Context: "[Page 12] Maternity expenses are excluded."
Answer: "The document does not state a maternity waiting period."
Verdict: verified=true, issues=[]
(Reason: saying something is not stated is not a factual claim.)

Context: "[Page 12] Maternity expenses are excluded."
Answer: "Maternity is covered after 9 months."
Verdict: verified=false, issues=["'covered after 9 months' is unsupported; context says maternity is excluded."]

Context: "[Page 9] 30-day waiting period for any illness. [Page 12] Maternity expenses are excluded."
Answer: "Maternity has a 30-day waiting period."
Verdict: verified=false, issues=["'30-day waiting period' for maternity is unsupported; Page 9 gives 30 days for illness, and Page 12 says maternity is excluded."]
(Reason: the number belongs to a different subject.)
"""


_checker = llm.with_structured_output(Verdict)


def check(state: CheckerState) -> dict:
    v = _checker.invoke(
        [
            SystemMessage(_SYSTEM),
            HumanMessage(f"ANSWER:\n{state['answer']}\n\nCONTEXT:\n{state['context']}"),
        ]
    )
    return {"verified": v.verified, "issues": v.issues}


_g = StateGraph(CheckerState)
_g.add_node("check", check)
_g.set_entry_point("check")
_g.add_edge("check", END)
citation_checker = _g.compile()
