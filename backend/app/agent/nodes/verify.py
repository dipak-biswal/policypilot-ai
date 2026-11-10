from app.agent.state import AgentState
from app.agent.subagents.citation_checker import citation_checker
from app.generation.citations import (
    NOT_FOUND,
)

import re

_ABSTAIN = re.compile(
    r"\b(i don'?t know|does not (state|specify|mention)|not (stated|specified|mentioned))\b",
    re.I,
)
_HAS_FACT = re.compile(r"\d")  # numbers usually mean a factual claim


def _is_pure_abstain(answer: str) -> bool:
    return bool(_ABSTAIN.search(answer)) and not _HAS_FACT.search(answer)


def verify_node(state: AgentState) -> dict:
    answer = state.get("answer", "")
    if not answer or answer == NOT_FOUND or _is_pure_abstain(answer):
        return {"verified": True, "citation_issues": []}
    result = citation_checker.invoke(
        {"answer": answer, "context": state.get("context", "")}
    )
    return {"verified": result["verified"], "citation_issues": result["issues"]}
