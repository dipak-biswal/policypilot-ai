import re

from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field

from app.agent.llm import llm
from app.agent.state import AgentState, Intent
from app.core.config import settings
from app.ingestion.profile_store import get_profile
from app.prompts.loader import load_prompt


class RouteDecision(BaseModel):
    intent: Intent = Field(
        description=(
            "qa: a specific question about the document; "
            "summary: wants a short overview of the document; "
            "report: wants a detailed structured report or comparison; "
            "chat: greetings, thanks or small talk not about the document"
        )
    )


router_llm = llm.with_structured_output(RouteDecision, method="function_calling")
ROUTER_PROMPT = load_prompt("router")

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
    # load this document's profile once per question; later nodes read it from state
    profile = get_profile(state.get("source")).model_dump()

    if GREETING.match(state["question"]):
        reply = settings.greeting_reply
        return {
            "intent": "chat",
            "answer": reply,
            "citations": [],
            "messages": [AIMessage(reply)],
            "profile": profile,
        }

    question = state.get("standalone_question") or state["question"]

    intent = fast_route(question)
    if intent is None:
        prompt = ROUTER_PROMPT.replace("{question}", question).replace(
            "{domain_hint}", profile["domain_hint"]
        )
        try:
            intent = router_llm.invoke(prompt).intent
        except Exception as e:  # malformed tool call -> safest default
            print("ROUTER fallback to qa:", e, flush=True)
            intent = "qa"

    return {"intent": intent, "profile": profile}
