from io import BytesIO

from pypdf import PdfReader


def extract_pages(file_bytes: bytes) -> list[dict]:
    reader = PdfReader(BytesIO(file_bytes))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({"page": index, "text": text.strip()})

    return pages
