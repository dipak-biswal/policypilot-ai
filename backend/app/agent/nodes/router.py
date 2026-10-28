import re

from pydantic import BaseModel, Field

from app.agent.llm import llm
from app.agent.state import AgentState, Intent
from langchain_core.messages import AIMessage


class RouteDecision(BaseModel):
    intent: Intent = Field(
        description=(
            "qa: a specific question about the policy; "
            "summary: wants a short overview of the policy; "
            "report: wants a detailed structured report or comparison"
            "chat: greetings, thanks or small talk not about the policy; "
        )
    )


router_llm = llm.with_structured_output(RouteDecision, method="function_calling")

REPORT_WORDS = re.compile(r"\b(report|compare|comparison|detailed|breakdown)\b", re.I)
SUMMARY_WORDS = re.compile(
    r"\b(summary|summari[sz]e|overview|tl;?dr|key points)\b", re.I
)
QA_START = re.compile(
    r"^(is|are|does|do|can|will|what|when|how|which|who|am i|my)\b", re.I
)

GREETING = re.compile(
    r"^\s*(hi|hello|hey|thanks|thank you|ok|okay|bye)\b[\s!.]*$", re.I
)


def fast_route(question: str) -> Intent | None:
    """Cheap keyword rules for obvious cases; None means 'not sure, ask the LLM'."""
    if REPORT_WORDS.search(question):
        return "report"
    if SUMMARY_WORDS.search(question):
        return "summary"
    if QA_START.match(question.strip()):
        return "qa"
    return None


def router_node(state: AgentState) -> AgentState:

    if GREETING.match(state["question"]):
        reply = "Hi! 👋 Ask me anything about your policy, like coverage, waiting periods or exclusions, or ask for a full report."
        return {
            "intent": "chat",
            "answer": reply,
            "citations": [],
            "messages": [AIMessage(reply)],
        }
    question = state.get("standalone_question") or state["question"]

    intent = fast_route(question)
    if intent is None:
        decision = router_llm.invoke(
            f"Classify the user's request about an insurance policy.\n\nRequest: {question}"
        )
        intent = decision.intent

    return {"intent": intent}
