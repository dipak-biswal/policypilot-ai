import re
from collections import Counter

from pydantic import BaseModel, Field

from app.agent.llm import llm
from app.prompts.loader import load_prompt


class DocProfile(BaseModel):
    domain: str = Field(
        description="One or two words, e.g. 'health insurance', 'rental contract', 'research paper'"
    )
    domain_hint: str = Field(
        description=(
            "1-2 sentences of INSTRUCTIONS to an assistant answering questions about this document, "
            "e.g. which sections override others (exclusions, exceptions, waiting periods), "
            "what special codes or terms mean, and which numbers matter most. "
            "Do not describe the document; tell the assistant how to read it."
        )
    )
    summary_query: str = Field(
        description="8-12 search keywords that would retrieve the most important sections"
    )
    stopwords: list[str] = []  # filled by code, not the LLM


profile_llm = llm.with_structured_output(DocProfile, method="function_calling")
PROFILE_PROMPT = load_prompt("profile")
KEEP = {"not", "no", "excluded", "except", "without"}  # never drop negations

GENERIC = DocProfile(
    domain="general",
    domain_hint="",
    summary_query="overview purpose key points terms conditions exceptions limits",
)


def frequent_words(pages: list[dict], ratio: float = 0.5, limit: int = 20) -> list[str]:
    """Words on more than `ratio` of pages carry little meaning for search."""
    if len(pages) < 3:
        return []
    df = Counter()  # document frequency: how many pages each word appears on
    for p in pages:
        df.update(set(re.findall(r"[a-z]{4,}", p["text"].lower())))
    common = [
        w for w, n in df.most_common() if n / len(pages) > ratio and w not in KEEP
    ]
    return common[:limit]


def detect_profile(pages: list[dict], max_chars: int = 6000) -> DocProfile:
    sample = "\n\n".join(p["text"] for p in pages[:4])[:max_chars]
    try:
        profile = profile_llm.invoke(PROFILE_PROMPT.replace("{sample}", sample))
    except Exception:
        profile = GENERIC.model_copy()
    profile.stopwords = frequent_words(pages)
    return profile
