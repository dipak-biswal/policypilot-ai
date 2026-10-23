from pydantic import BaseModel, Field

from app.agent.llm import llm
from app.agent.state import AgentState, Intent


class RouteDecesion(BaseModel):
    intent: Intent = Field(
        description=(
            "qa: a specific question about the policy; "
            "summary: wants a short overview of the policy; "
            "report: wants a detailed structured report or comparison"
        )
    )


router_llm = llm.with_structured_output(RouteDecesion)


def router_node(state: AgentState) -> AgentState:
    decision = router_llm.invoke(
        f"Classify the user's request about an insurance policy.\n\nRequest: {state["question"]}"
    )

    return {"intent": decision.intent}
