import time
from collections.abc import Iterator

from langchain_core.callbacks import UsageMetadataCallbackHandler
from langgraph.types import Command

from app.agent.answer_blocks import pick_blocks
from app.agent.graph import graph
from app.core.metrics import estimate_cost
from app.generation.citations import NOT_FOUND
from app.guardrails.output import moderate_output
from app.guardrails.pipeline import run_input_guards
from app.utils.sse import sse

BLOCKED_REPLY = "I can't help with that request. Ask a question about your uploaded document instead."

# Usage from the first half of a HITL run, waiting for /resume.
# In-memory: fine for one container; use Redis/Postgres for multiple replicas.
_pending_usage: dict[str, dict] = {}


def _merge_usage(a: dict, b: dict) -> dict:
    """Add per-model usage dicts: {'gpt-4o-mini': {'input_tokens': .., ...}}."""
    out = {m: dict(u) for m, u in a.items()}
    for model, u in b.items():
        cur = out.setdefault(model, {})
        for k, v in u.items():
            if isinstance(v, (int, float)):
                cur[k] = cur.get(k, 0) + v
    return out


def _build_metrics(start: float, usage: dict) -> dict:
    return {
        "latency_ms": round((time.perf_counter() - start) * 1000),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage.values()),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage.values()),
        "cost_usd": estimate_cost(usage),
    }


def _payload_from_interrupts(interrupts) -> dict | None:
    if not interrupts:
        return None
    first = interrupts[0]
    value = getattr(first, "value", first)
    return value if isinstance(value, dict) else None


def _interrupt_payload(config: dict, final: dict, question: str) -> dict | None:
    snap = graph.get_state(config)
    if not snap:
        return None

    payload = _payload_from_interrupts(getattr(snap, "interrupts", None))
    if not payload:
        for task in getattr(snap, "tasks", ()) or ():
            payload = _payload_from_interrupts(getattr(task, "interrupts", None))
            if payload:
                break
    if not payload:
        return None

    payload.setdefault("type", "approve_answer")
    payload.setdefault("draft", final.get("answer", ""))
    payload.setdefault("question", question)
    return payload


def _finish(final: dict, question: str, start: float, usage: dict) -> Iterator[str]:
    answer = final.get("answer", "")
    if answer and answer != NOT_FOUND:
        safe, issues = moderate_output(answer)
        if issues:
            yield sse(
                "step",
                {"step": "Output moderated", "detail": ", ".join(issues)},
            )
            answer = safe
            final["answer"] = safe
        yield sse("token", {"text": answer})

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

    yield sse("metrics", _build_metrics(start, usage))
    yield sse("done", {})


def stream_agent(
    question: str, source: str | None = None, thread_id: str = "default"
) -> Iterator[str]:
    final: dict = {}
    start = time.perf_counter()
    usage_cb = UsageMetadataCallbackHandler()
    config = {"configurable": {"thread_id": thread_id}, "callbacks": [usage_cb]}

    guard = run_input_guards(question)
    if guard.pii_found:
        yield sse(
            "step",
            {"step": "Redacted PII", "detail": ", ".join(guard.pii_found)},
        )
    if not guard.allowed:
        yield sse(
            "step",
            {
                "step": "Blocked by guardrail",
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
        stream_mode=["updates", "custom"],
    ):
        if mode == "custom":
            yield sse("step", chunk)
            continue

        if not isinstance(chunk, dict):
            continue

        # LangGraph emits: {'__interrupt__': (Interrupt(...),)}
        if "__interrupt__" in chunk:
            payload = _payload_from_interrupts(chunk["__interrupt__"]) or {
                "type": "approve_answer",
                "draft": final.get("answer", ""),
                "question": question,
            }
            payload.setdefault("draft", final.get("answer", ""))
            payload.setdefault("question", question)
            payload.setdefault("type", "approve_answer")
            yield sse(
                "step",
                {
                    "step": "Waiting for your approval",
                    "detail": "approve / edit / reject",
                },
            )
            yield sse("interrupt", payload)
            yield sse("done", {"pending": True})
            _pending_usage[thread_id] = dict(usage_cb.usage_metadata)  # NEW
            return

        for node, update in chunk.items():
            if not update or not isinstance(update, dict):
                continue
            if node == "router":
                yield sse("intent", {"intent": update["intent"]})
                if update.get("intent") == "chat" and update.get("answer"):
                    yield sse("token", {"text": update["answer"]})
            final.update(update)

    # Fallback if interrupt was not in the stream chunks
    payload = _interrupt_payload(config, final, question)
    if payload:
        yield sse(
            "step",
            {
                "step": "Waiting for your approval",
                "detail": "approve / edit / reject",
            },
        )
        yield sse("interrupt", payload)
        yield sse("done", {"pending": True})
        _pending_usage[thread_id] = dict(usage_cb.usage_metadata)  # NEW
        return

    yield from _finish(final, question, start, usage_cb.usage_metadata)  # CHANGED


def resume_agent(
    thread_id: str,
    decision: dict,
) -> Iterator[str]:
    """Continue after the user approves / edits / rejects."""
    final: dict = {}
    start = time.perf_counter()
    usage_cb = UsageMetadataCallbackHandler()
    config = {"configurable": {"thread_id": thread_id}, "callbacks": [usage_cb]}

    for mode, chunk in graph.stream(
        Command(resume=decision),
        config=config,
        stream_mode=["updates", "custom"],
    ):
        if mode == "custom":
            yield sse("step", chunk)
            continue
        if isinstance(chunk, dict):
            for node, update in chunk.items():
                if node == "__interrupt__" or not isinstance(update, dict):
                    continue
                if update:
                    final.update(update)

    snap = graph.get_state(config)
    if snap and snap.values:
        final = {**final, **snap.values}

    question = final.get("standalone_question") or final.get("question", "")

    # NEW: add usage from before the interrupt to this request's usage
    saved = _pending_usage.pop(thread_id, {})
    usage = _merge_usage(saved, usage_cb.usage_metadata)
    yield from _finish(final, question, start, usage)
