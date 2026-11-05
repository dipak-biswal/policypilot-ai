from dataclasses import dataclass

from app.guardrails.injection import check_injection
from app.guardrails.pii import redact_pii


@dataclass
class GuardResult:
    allowed: bool
    question: str  # possibly redacted
    blocked_reason: str | None = None
    pii_found: list[str] | None = None


def run_input_guards(question: str) -> GuardResult:
    clean, found = redact_pii(question)
    verdict = check_injection(clean)
    if verdict.is_injection:
        return GuardResult(
            allowed=False,
            question=clean,
            blocked_reason=verdict.reason,
            pii_found=found or None,
        )
    return GuardResult(allowed=True, question=clean, pii_found=found or None)
