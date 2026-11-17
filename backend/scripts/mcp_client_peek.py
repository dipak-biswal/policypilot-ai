import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(
    command=sys.executable,  # the same venv Python
    args=["-m", "app.mcp_server"],
)


async def main():
    # 1. Start the server as a subprocess and open stdin/stdout pipes
    async with stdio_client(SERVER) as (read, write):
        # 2. A session speaks MCP JSON-RPC over those pipes
        async with ClientSession(read, write) as session:
            await session.initialize()  # handshake
            # 3. tools/list
            listed = await session.list_tools()
            for t in listed.tools:
                print("TOOL:", t.name, "|", (t.description or "")[:60])
                print("  SCHEMA:", t.input_schema)
            # 4. tools/call
            result = await session.call_tool("ping", {"name": "Dipak"})
            print("PING:", [c.text for c in result.content if hasattr(c, "text")])
            print("IS ERROR:", result.is_error)


asyncio.run(main())
