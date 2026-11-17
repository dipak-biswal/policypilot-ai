from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing import Annotated

load_dotenv()


# 1. @tool builds the JSON schema from type hints + docstring (no manual TOOLS list)
@tool
def get_copay(
    amount: Annotated[float, "Bill amont in INR, e.g. 250000"],
    percent: Annotated[float, "Co-pay percentage as a number, e.g. 20 for 20%"],
) -> dict:
    """Calculate the co-pay amount for a hospital bill in INR."""
    return {"copay": round(amount * percent / 100, 2)}


@tool
def get_waiting_period(topic: str) -> dict:
    """Look up the waiting period for a topic, e.g. illness, maternity."""
    fake = {"illness": "30 days", "maternity": "excluded"}
    return {"topic": topic, "waiting_period": fake.get(topic.lower(), "not stated")}


TOOLS = {t.name: t for t in [get_copay, get_waiting_period]}
print("SCHEMA:", get_copay.args)  # the schema LangChain generated

# 2. bind_tools = passing tools=[...] to the raw API
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(list(TOOLS.values()))

messages = [
    SystemMessage(
        "Answer only from tool results, Copy facts exactly. "
        "If a tool says 'excluded', say it is NOT covered at all. "
        "Never add a time period or 'might' that the tool did not return. "
    ),
    HumanMessage(
        "Waiting periods for illness and maternity, and 20% co-pay on 250000?"
    ),
]

# 3. The agent loop, with a round limit like qa.py
for round_no in range(1, 5):
    ai = llm.invoke(messages)
    messages.append(ai)
    print(
        f"ROUND {round_no}: tool_calls={[(c['name'], c['args']) for c in ai.tool_calls]}"
    )

    if not ai.tool_calls:  # check tool_calls, not finish_reason
        break

    for call in ai.tool_calls:  # args are already a dict, no json.loads
        selected_tool = TOOLS[call["name"]]
        result = selected_tool.invoke(call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

print("FINAL:", ai.content)
print("MESSAGE TYPES:", [type(m).__name__ for m in messages])
