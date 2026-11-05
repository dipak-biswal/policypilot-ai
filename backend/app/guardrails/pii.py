import re

# Patterns are deliberately conservative — better to over-mask than leak
_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE = re.compile(
    r"(?<!\d)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}(?!\d)"
)
_AADHAAR = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
_PAN = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")


def redact_pii(text: str) -> tuple[str, list[str]]:
    """Return redacted text and a list of what was found (e.g. ['email', 'phone'])."""
    found: list[str] = []
    def mask(pattern: re.Pattern, label: str, replacement: str, s: str) -> str:
        if pattern.search(s):
            found.append(label)
            return pattern.sub(replacement, s)
        return s
    text = mask(_EMAIL, "email", "[EMAIL]", text)
    text = mask(_PHONE, "phone", "[PHONE]", text)
    text = mask(_AADHAAR, "aadhaar", "[AADHAAR]", text)
    text = mask(_PAN, "pan", "[PAN]", text)
    return text, found