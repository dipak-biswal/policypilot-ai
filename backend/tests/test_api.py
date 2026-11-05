from fastapi.testclient import TestClient
from app.auth.deps import get_current_user_id
from app.main import app
from app.routers.documents import scoped_source

client = TestClient(app)

TEST_USER = "test-user"


def _fake_user():
    return TEST_USER


app.dependency_overrides[get_current_user_id] = _fake_user


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_upload_rejects_non_pdf():
    res = client.post(
        "/documents", files={"file": ("note.txt", b"hello", "text/plain")}
    )
    assert res.status_code == 400


def test_agent_endpoint_returns_graph_result(monkeypatch):
    fake_result = {
        "intent": "qa",
        "answer": "36 months [Page 10]",
        "citations": [],
        "report": None,
    }
    monkeypatch.setattr(
        "app.routers.agent.graph.invoke", lambda state, config=None: fake_result
    )

    res = client.post(
        "/agent", json={"question": "waiting period?", "source": "optima-plus.pdf"}
    )
    assert res.status_code == 200
    assert res.json()["intent"] == "qa"
    assert "36 months" in res.json()["answer"]


def test_routes_require_auth():
    app.dependency_overrides.pop(get_current_user_id, None)
    try:
        res = client.post("/agent", json={"question": "hi", "source": "x.pdf"})
        assert res.status_code == 401
    finally:
        app.dependency_overrides[get_current_user_id] = _fake_user


def test_scoped_source_isolates_users():
    a = scoped_source("user-a", "policy.pdf")
    b = scoped_source("user-b", "policy.pdf")
    assert a == "user-a/policy.pdf"
    assert b == "user-b/policy.pdf"
    assert a != b


def test_delete_other_users_doc_is_404(monkeypatch):
    """User B deleting user A's filename must not hit A's source."""
    seen = {}

    def fake_delete(source: str) -> int:
        seen["source"] = source
        return 0  # not found for this user

    monkeypatch.setattr("app.routers.documents.delete_document", fake_delete)
    monkeypatch.setattr("app.routers.documents.delete_profile", lambda s: None)

    # client already overrides get_current_user_id -> test-user
    res = client.delete("/documents/policy.pdf")
    assert res.status_code == 404
    assert seen["source"] == f"{TEST_USER}/policy.pdf"
