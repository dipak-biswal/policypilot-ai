from fastapi.testclient import TestClient
from app.auth.deps import get_current_user_id
from app.main import app
import json

client = TestClient(app)
TEST_USER = "test-user"


def _fake_user():
    return TEST_USER


app.dependency_overrides[get_current_user_id] = _fake_user


def test_resume_approve_returns_answer(monkeypatch):
    """Approve path: resume with action=approve should stream a final answer."""

    def fake_resume_agent(thread_id, decision):
        assert decision["action"] == "approve"
        yield f"event: token\ndata: {json.dumps({'text': '24 months [Page 12]'})}\n\n"
        yield f"event: done\ndata: {json.dumps({'answer': '24 months [Page 12]', 'pending': False})}\n\n"

    monkeypatch.setattr("app.routers.agent.resume_agent", fake_resume_agent)

    res = client.post(
        "/agent/resume",
        json={
            "thread_id": f"{TEST_USER}:t1",
            "action": "approve",
        },
    )
    assert res.status_code == 200
    body = res.text
    assert "24 months" in body
    assert "done" in body


def test_resume_edit_requires_text():
    res = client.post(
        "/agent/resume",
        json={"thread_id": "t1", "action": "edit"},
    )
    assert res.status_code == 400


def test_resume_reject_streams_discard(monkeypatch):
    def fake_resume_agent(thread_id, decision):
        assert decision["action"] == "reject"
        yield (
            "event: done\n"
            f"data: {json.dumps({'answer': 'Okay - I discarded that draft.', 'pending': False})}\n\n"
        )

    monkeypatch.setattr("app.routers.agent.resume_agent", fake_resume_agent)

    res = client.post(
        "/agent/resume",
        json={"thread_id": "t1", "action": "reject"},
    )
    assert res.status_code == 200
    assert "discarded" in res.text
