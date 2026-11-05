from app.guardrails.pii import redact_pii

_LEAK_MARKERS = (
    "system prompt",
    "ignore previous instructions",
    "you are dan",
    "do anything now",
)


def moderate_output(answer: str) -> tuple[str, list[str]]:
    """Return (safe_answer, list of issues found). Empty issues = ok."""
    issues: list[str] = []
    clean, pii = redact_pii(answer)
    if pii:
        issues.append("pii:" + ",".join(pii))
    lower = clean.lower()
    if any(m in lower for m in _LEAK_MARKERS):
        issues.append("prompt_leak")
        return (
            "I can't share that. Ask a question about your uploaded document instead.",
            issues,
        )
    return clean, issues
