from dotenv import load_dotenv

load_dotenv()

import json

from langchain_core.messages import HumanMessage
from langchain_core.utils.function_calling import convert_to_openai_tool

from app.agent.llm import llm
from app.agent.tools import calculator, date_calculator
from langchain_core.messages import ToolMessage

tools = [calculator, date_calculator]

# 1. What the model actually sees
for t in tools:
    print(json.dumps(convert_to_openai_tool(t), indent=2))

# 2. What the model sends back
agent_llm = llm.bind_tools(tools)
msg = agent_llm.invoke(
    [
        HumanMessage(
            "I bought the policy on 2025-03-01. When does the 24-month waiting period end, and what is 18% of 50000?"
        )
    ]
)
print("content:", repr(msg.content))
print("tool_calls:", json.dumps(msg.tool_calls, indent=2))

# A. Force a tool even for a question that doesn't need one
forced = llm.bind_tools(tools, tool_choice="calculator")
m = forced.invoke([HumanMessage("Hi there!")])
print("\nFORCED:", json.dumps(m.tool_calls, indent=2))
# B. Feed a tool error back and watch the model recover
q = HumanMessage("What is 18% of 50000?")
first = agent_llm.invoke([q])
call = first.tool_calls[0]
err = ToolMessage(
    content="Error: expression must use only numbers and + - * / ( ). Got invalid syntax.",
    tool_call_id=call["id"],
)
retry = agent_llm.invoke([q, first, err])
print("\nRETRY content:", repr(retry.content))
print("RETRY tool_calls:", json.dumps(retry.tool_calls, indent=2))
