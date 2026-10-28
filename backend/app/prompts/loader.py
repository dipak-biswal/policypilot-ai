from functools import lru_cache
from pathlib import Path
from app.core.config import settings

PROMPT_DIR = Path(__file__).parent


def load_prompt(name: str) -> str:
    text = (PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8")
    return text.replace("{{app_name}}", settings.app_name).replace(
        "{{domain_hint}}", settings.domain_hint
    )
