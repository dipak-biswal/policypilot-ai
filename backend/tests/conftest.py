import os

os.environ.setdefault("OPENAI_API_KEY", "sk-test-not-real")

import pytest


class _SafeVerdict:
    is_injection = False
    reason = "test stub"


class _FakeClassifier:
    def invoke(self, _messages):
        return _SafeVerdict()


@pytest.fixture(autouse=True)
def _no_llm_injection_check(monkeypatch):
    """Unit tests never call OpenAI for the injection check."""
    monkeypatch.setattr("app.guardrails.injection._classifier", _FakeClassifier())
