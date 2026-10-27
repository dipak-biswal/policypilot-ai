from collections.abc import Iterator

from app.agent.graph import graph
from app.utils.sse import sse
from langchain_core.messages import AIMessageChunk

import time
from langchain_core.callbacks import UsageMetadataCallbackHandler
from app.core.metrics import estimate_cost

TEXT_NODES = {"qa", "summarizer"}


def _build_metrics(start: float, usage: dict) -> dict:
    return {
        "latency_ms": round((time.perf_counter() - start) * 1000),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage.values()),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage.values()),
        "cost_usd": estimate_cost(usage),
    }


def stream_agent(
    question: str, source: str | None = None, thread_id: str = "default"
) -> Iterator[str]:
    final: dict = {}
    start = time.perf_counter()
    usage_cb = UsageMetadataCallbackHandler()
    config = {
        "configurable": {"thread_id": thread_id},
        "callbacks": [usage_cb],
    }

    for mode, chunk in graph.stream(
        {"question": question, "source": source},
        config=config,
        stream_mode=["messages", "updates"],
    ):
        if mode == "messages":
            msg, meta = chunk
            if (
                meta.get("langgraph_node") in TEXT_NODES
                and isinstance(msg, AIMessageChunk)
                and msg.content
            ):
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

    metrics = _build_metrics(start, usage_cb.usage_metadata)
    print("METRICS", metrics, flush=True)
    yield sse("metrics", metrics)
    yield sse("done", {})
