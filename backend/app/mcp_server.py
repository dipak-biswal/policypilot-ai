import os
from contextvars import ContextVar
from dotenv import load_dotenv

load_dotenv()

from mcp.server.mcpserver import MCPServer
from starlette.responses import JSONResponse

from app.core.security import decode_access_token
from app.guardrails.pii import redact_pii
from app.generation.qa import build_context, search
from app.routers.documents import scoped_source

mcp = MCPServer("Policypilot")

# request scoped "who is calling"
current_user: ContextVar[str | None] = ContextVar("current_user", default=None)


@mcp.tool()
def ping(name: str) -> str:
    """Say hello. Used to check the MCP server is reachable."""
    return f"Hello {name}, policyPilot MCP is alive"


@mcp.tool()
def search_policy(filename: str, query: str) -> str:
    """Search one of YOUR uploaded documents for passages about `query`.
    `filename` is the name you uploaded, e.g. 'optima-plus.pdf'.
    Returns text tagged with [Page N]."""
    user_id = current_user.get()
    if not user_id:
        return "Not authenticated."
    source = scoped_source(user_id, filename)  # server decides the namespace
    docs = search(query, source=source)
    raw = build_context(docs) or "No matching passages."
    clean, _ = redact_pii(raw)
    return clean


class BearerAuth:
    """ASGI middleware: reject requests without a valid PolicyPilot JWT."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope.get("headers") or [])
        auth = headers.get(b"authorization", b"").decode()
        token = auth.removeprefix("Bearer ").strip()
        user_id = decode_access_token(token) if token else None
        if not user_id:
            res = JSONResponse({"detail": "Unauthorized"}, status_code=401)
            return await res(scope, receive, send)
        reset = current_user.set(user_id)
        try:
            await self.app(scope, receive, send)
        finally:
            current_user.reset(reset)


if __name__ == "__main__":

    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "streamable-http":
        import uvicorn

        uvicorn.run(BearerAuth(mcp.streamable_http_app()), host="127.0.0.1", port=8001)
    else:
        current_user.set(os.getenv("MCP_LOCAL_USER_ID"))
        mcp.run()
