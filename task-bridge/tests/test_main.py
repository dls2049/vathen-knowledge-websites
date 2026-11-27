from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_reports_scaffold():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "scaffold"

def test_task_update_disabled_without_key(monkeypatch):
    monkeypatch.delenv("TASK_BRIDGE_API_KEY", raising=False)
    response = client.post("/tasks/update", json={"task_id":"T-1","status":"Done","evidence":"Verified artifact and test output"})
    assert response.status_code == 503

def test_task_update_rejects_bad_status():
    response = client.post("/tasks/update", headers={"Authorization":"Bearer x"}, json={"task_id":"T-1","status":"finished","evidence":"Verified artifact and test output"})
    assert response.status_code == 422
