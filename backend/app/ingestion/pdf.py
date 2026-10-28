import re
from collections import Counter
from io import BytesIO

from pypdf import PdfReader

from app.core.config import settings


def _norm(line: str) -> str:
    """Normalise a line so 'Page 3 of 20' and 'Page 4 of 20' count as the same line."""
    return re.sub(r"\d+", "#", line.strip().lower())


def find_repeated_lines(raw_pages: list[str]) -> set[str]:
    """Lines that appear on most pages are headers or footers."""
    if len(raw_pages) < 3:  # too few pages to tell
        return set()
    counts = Counter()
    for text in raw_pages:
        # set(): count each line once per page, like new Set() in JS
        counts.update({_norm(l) for l in text.splitlines() if l.strip()})
    threshold = len(raw_pages) * settings.boilerplate_min_ratio
    return {line for line, n in counts.items() if n >= threshold}


def clean_text(text: str, repeated: set[str]) -> str:
    lines = [l for l in text.splitlines() if _norm(l) not in repeated]
    text = "\n".join(lines)
    for pattern in settings.boilerplate_patterns:
        text = re.sub(pattern, " ", text, flags=re.DOTALL)
    text = re.sub(r"[ \t]+", " ", text)  # collapse spaces
    text = re.sub(r"\n\s*\n+", "\n", text)  # collapse blank lines
    return text.strip()


def extract_pages(file_bytes: bytes) -> list[dict]:
    reader = PdfReader(BytesIO(file_bytes))
    raw = [page.extract_text() or "" for page in reader.pages]
    repeated = find_repeated_lines(raw)
    return [
        {"page": i, "text": clean_text(text, repeated)}
        for i, text in enumerate(raw, start=1)
    ]
