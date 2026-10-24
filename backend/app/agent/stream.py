from collections.abc import Iterator

from app.agent.graph import graph
from app.utils.sse import sse

TEXT_NODES = {"qa", "summarizer"}


def stream_agent(question: str, source: str | None = None) -> Iterator[str]:
    final: dict = {}

    for mode, chunk in graph.stream(
        {"question": question, "source": source}, stream_mode=["messages", "updates"]
    ):
        if mode == "messages":
            msg, meta = chunk
            if meta.get("langgraph_node") in TEXT_NODES and msg.content:
                yield sse("token", {"text": msg.content})
        else:
            for node, update in chunk.items():
                if not update:
                    continue
                if node == "router":
                    yield sse("intent", {"intent": update["intent"]})

                final.update(update)

    if final.get("report"):
        yield sse("report", final["report"])
    yield sse("citations", final.get("citations", []))
    yield sse("done", {})
