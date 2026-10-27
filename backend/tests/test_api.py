from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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

    res = client.post("/agent", json={"question": "waiting period?"})
    assert res.status_code == 200
    assert res.json()["intent"] == "qa"
    assert "36 months" in res.json()["answer"]
