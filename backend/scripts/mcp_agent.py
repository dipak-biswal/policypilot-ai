import asyncio
import json
import os
import sys

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"
FILENAME = os.environ.get("MCP_TEST_FILE", "sample-policy.pdf")  # a file you uploaded

SERVER = StdioServerParameters(command=sys.executable, args=["-m", "app.mcp_server"])


def to_openai_tool(t) -> dict:
    """MCP tool -> OpenAI tool schema (same JSON Schema underneath)."""
    return {
        "type": "function",
        "function": {
            "name": t.name,
            "description": t.description or "",
            "parameters": t.input_schema,
        },
    }


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            tools = [to_openai_tool(t) for t in mcp_tools if t.name == "search_policy"]

            messages = [
                {
                    "role": "system",
                    "content": f"Answer only from search_policy results for file '{FILENAME}'. "
                    "Cite pages. If not found, say you don't know.",
                },
                {
                    "role": "user",
                    "content": "What is the waiting period for pre-existing diseases?",
                },
            ]

            for round_no in range(1, 5):
                r = await client.chat.completions.create(
                    model=MODEL, messages=messages, tools=tools
                )
                msg = r.choices[0].message
                messages.append(msg)
                print(
                    f"ROUND {round_no}: {[(c.function.name, c.function.arguments) for c in msg.tool_calls or []]}"
                )
                if not msg.tool_calls:
                    break

                for call in msg.tool_calls:
                    args = json.loads(call.function.arguments)
                    res = await session.call_tool(
                        call.function.name, args
                    )  # <-- via MCP
                    text = "\n".join(c.text for c in res.content if hasattr(c, "text"))
                    print(
                        f"  MCP {call.function.name} -> {len(text)} chars, is_error={res.is_error}"
                    )
                    messages.append(
                        {"role": "tool", "tool_call_id": call.id, "content": text}
                    )

            print("FINAL:", msg.content)


asyncio.run(main())
