import re
from io import BytesIO

from pypdf import PdfReader

BOILERPLATE = [
    r"HDFC ERGO General Insurance Company Limited\.?\s*IRDAI Reg\..*?UIN:.*?(?=\n|$)",
    r"HDFC ERGO General Insurance Company Limited",
    r"Policy Wording",
    r"Optima Plus-?",
]


def clean_text(text: str) -> str:
    for pattern in BOILERPLATE:
        text = re.sub(pattern, " ", text, flags=re.DOTALL)
    text = re.sub(r"[ \t]+", " ", text)  # collapse spaces
    text = re.sub(r"\n\s*\n+", "\n", text)  # collapse blank lines
    return text.strip()


def extract_pages(file_bytes: bytes) -> list[dict]:
    reader = PdfReader(BytesIO(file_bytes))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")
        pages.append({"page": index, "text": text.strip()})

    return pages
