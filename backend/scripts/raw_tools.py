import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"


# 1. A plain Python function: the "real" tool
def get_copay(amount: float, percent: float) -> dict:
    return {"copay": round(amount * percent / 100, 2)}


def get_waiting_period(topic: str) -> dict:
    fake_policy = {
        "illness": "30 days",
        "specified diseases": "24 months",
        "maternity": "excluded",
    }
    return {
        "topic": topic,
        "waiting_period": fake_policy.get(topic.lower(), "not stated"),
    }


# 2. The JSON schema the model sees (LangChain builds this from your docstring)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_copay",
            "description": "Calculate the co-pay amount for a hospital bill.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Bill amount in INR"},
                    "percent": {"type": "number", "description": "Co-pay percentage"},
                },
                "required": ["amount", "percent"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_waiting_period",
            "description": "Look up the waiting period for a topic in the policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "e.g. illness, maternity, specified diseases",
                    },
                },
                "required": ["topic"],
            },
        },
    },
]


REGISTRY = {"get_copay": get_copay, "get_waiting_period": get_waiting_period}

# messages = [
#     {
#         "role": "user",
#         "content": "My bill is 250000 INR with 20% co-pay. How much do I pay?",
#     }
# ]

messages = [
    {
        "role": "user",
        "content": "What are the waiting periods for illness and maternity, and what is 20% co-pay on 250000 INR?",
    }
]


# 3. First call: the model decides whether to use a tool
first = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
msg = first.choices[0].message
print("FINISH REASON:", first.choices[0].finish_reason)
print(
    "TOOL CALLS:",
    [(c.function.name, c.function.arguments) for c in msg.tool_calls or []],
)
# 4. Run each requested tool and send the result back
messages.append(msg)  # the assistant message containing tool_calls
for call in msg.tool_calls or []:
    args = json.loads(call.function.arguments)
    result = REGISTRY[call.function.name](**args)
    print("  RUN:", call.id, call.function.name, args, "->", result)
    messages.append(
        {"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)}
    )

# 5. Second call: the model writes the final answer using the tool result
second = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
print("FINAL:", second.choices[0].message.content)
print("TOTAL MESSAGES:", len(messages))

print("\n--- tool_choice experiments ---")
hello = [{"role": "user", "content": "Hello, how are you?"}]

for choice in [
    "auto",
    "none",
    "required",
    {"type": "function", "function": {"name": "get_copay"}},
]:
    r = client.chat.completions.create(
        model=MODEL, messages=hello, tools=TOOLS, tool_choice=choice
    )
    m = r.choices[0].message
    label = choice if isinstance(choice, str) else "forced:get_copay"
    print(
        f"{label:18} finish={r.choices[0].finish_reason:10} tools={[(c.function.name, c.function.arguments) for c in m.tool_calls or []]}"
    )


# ---------------- Lesson 4 ----------------
print("\n--- strict + structured output ---")

# A. Strict tool schema: the model must output exactly this shape
STRICT_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "get_copay",
            "description": "Calculate the co-pay amount for a hospital bill.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "percent": {"type": "number"},
                },
                "required": ["amount", "percent"],
                "additionalProperties": False,
            },
        },
    }
]
q = [
    {
        "role": "user",
        "content": "Co-pay is twenty percent on a bill of two lakh fifty thousand rupees.",
    }
]
r = client.chat.completions.create(model=MODEL, messages=q, tools=STRICT_TOOL)
print(
    "STRICT TOOL:",
    [c.function.arguments for c in r.choices[0].message.tool_calls or []],
)


# B. Structured output: the ANSWER itself is typed JSON (no tool runs)
from pydantic import BaseModel


class CoverageAnswer(BaseModel):
    topic: str
    covered: bool
    waiting_period: str | None
    page: int | None


context = (
    "[Page 9] 30-day waiting period for any illness. "
    "[Page 12] Maternity expenses are excluded."
)
r2 = client.beta.chat.completions.parse(
    model=MODEL,
    messages=[
        {"role": "system", "content": f"Answer only from this context:\n{context}"},
        {"role": "user", "content": "Is maternity covered?"},
    ],
    response_format=CoverageAnswer,
)
parsed = r2.choices[0].message.parsed
print("STRUCTURED:", parsed)
print(
    "TYPE:",
    type(parsed).__name__,
    "| covered is bool:",
    isinstance(parsed.covered, bool),
)
