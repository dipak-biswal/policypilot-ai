import time
from collections.abc import Iterator

from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain_core.messages import AIMessageChunk

from app.agent.answer_blocks import pick_blocks
from app.agent.graph import graph
from app.core.metrics import estimate_cost
from app.generation.citations import NOT_FOUND
from app.guardrails.output import moderate_output
from app.guardrails.pipeline import run_input_guards
from app.utils.sse import sse

TEXT_NODES = {"qa", "summarizer"}
BLOCKED_REPLY = (
    "I can't help with that request. Ask a question about your uploaded document instead."
)


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
    streamed = False
    start = time.perf_counter()
    usage_cb = UsageMetadataCallbackHandler()
    config = {
        "configurable": {"thread_id": thread_id},
        "callbacks": [usage_cb],
    }

    guard = run_input_guards(question)
    if guard.pii_found:
        yield sse(
            "step",
            {"step": "🛡️ Redacted PII", "detail": ", ".join(guard.pii_found)},
        )
    if not guard.allowed:
        yield sse(
            "step",
            {
                "step": "🛡️ Blocked by guardrail",
                "detail": guard.blocked_reason or "injection",
            },
        )
        yield sse("intent", {"intent": "chat"})
        yield sse("token", {"text": BLOCKED_REPLY})
        yield sse("citations", [])
        yield sse("metrics", _build_metrics(start, {}))
        yield sse("done", {})
        return
    question = guard.question

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
                streamed = True
                yield sse("token", {"text": update["answer"]})

            final.update(update)

    answer = final.get("answer", "")
    if answer and answer != NOT_FOUND:
        safe, issues = moderate_output(answer)
        if issues:
            yield sse(
                "step",
                {"step": "🛡️ Output moderated", "detail": ", ".join(issues)},
            )
            yield sse("token", {"text": "\n\n" + safe})
            final["answer"] = safe
            answer = safe

    if final.get("report"):
        yield sse("report", final["report"])
    yield sse("citations", final.get("citations", []))

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