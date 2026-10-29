import time
from collections.abc import Iterator

from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain_core.messages import AIMessageChunk

from app.agent.answer_blocks import pick_blocks
from app.agent.graph import graph
from app.core.metrics import estimate_cost
from app.generation.citations import NOT_FOUND
from app.utils.sse import sse

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
    streamed = False  # did any text reach the client?
    start = time.perf_counter()
    usage_cb = UsageMetadataCallbackHandler()
    config = {
        "configurable": {"thread_id": thread_id},
        "callbacks": [usage_cb],
    }

    for mode, chunk in graph.stream(
        {"question": question, "source": source},
        config=config,
        stream_mode=["messages", "updates", "custom"],
    ):
        if mode == "custom":
            yield sse("step", chunk)
            continue

        if mode == "messages":
            msg, meta = chunk
            if (
                meta.get("langgraph_node") in TEXT_NODES
                and isinstance(msg, AIMessageChunk)
                and msg.content
            ):
                streamed = True
                yield sse("token", {"text": msg.content})
            continue

        for node, update in chunk.items():
            if not update:
                continue
            if node == "router":
                if update.get("intent") == "chat":
                    streamed = True
                    yield sse("token", {"text": update["answer"]})
                yield sse("intent", {"intent": update["intent"]})
            elif node in TEXT_NODES and not streamed and update.get("answer"):
                # node answered without calling the LLM (e.g. NOT_FOUND)
                streamed = True
                yield sse("token", {"text": update["answer"]})

            final.update(update)

    if final.get("report"):
        yield sse("report", final["report"])
    yield sse("citations", final.get("citations", []))

    answer = final.get("answer", "")
    if final.get("intent") == "qa" and answer and answer != NOT_FOUND:
        blocks = pick_blocks(
            final.get("standalone_question") or question,
            answer,
            final.get("profile", {}).get("domain_hint", ""),
        )
        if blocks:
            yield sse("blocks", blocks)

    metrics = _build_metrics(start, usage_cb.usage_metadata)
    print("METRICS", metrics, flush=True)
    yield sse("metrics", metrics)
    yield sse("done", {})
