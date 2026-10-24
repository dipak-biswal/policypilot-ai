from pathlib import Path

from app.ingestion.pdf import extract_pages

SAMPLE = Path(__file__).parent.parent.parent / "sample-data" / "optima-plus.pdf"


def test_extracts_all_pages_with_numbers():
    pages = extract_pages(SAMPLE.read_bytes())
    assert len(pages) == 29
    assert pages[0]["page"] == 1
    assert len(pages[0]["text"]) > 0
