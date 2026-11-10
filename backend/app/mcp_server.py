from dotenv import load_dotenv

load_dotenv()

from mcp.server.mcpserver import MCPServer
from app.guardrails.pii import redact_pii
from app.generation.qa import build_context, search

mcp = MCPServer("Policypilot")


@mcp.tool()
def ping(name: str) -> str:
    """Say hello. Used to check the MCP server is reachable."""
    return f"Hello {name}, policyPilot MCP is alive"


@mcp.tool()
def search_policy(source: str, query: str) -> str:
    """Search an uploaded policy document for passages about `query`.
    `source` is the internal document key, e.g. 'user-id/policy.pdf'.
    Returns text tagged with [Page N]."""
    docs = search(query, source=source)
    raw = build_context(docs) or "No matching passages."
    clean, _ = redact_pii(raw)
    return clean


if __name__ == "__main__":
    mcp.run()
