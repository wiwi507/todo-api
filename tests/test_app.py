import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    res = client.get("/tasks")
    assert res.status_code == 200
    assert "tasks" in res.get_json()

def test_create_task(client):
    res = client.post("/tasks",
                      json={"title": "Nueva tarea"},
                      content_type="application/json")
    assert res.status_code == 201
    assert res.get_json()["title"] == "Nueva tarea"

def test_create_sin_titulo(client):
    res = client.post("/tasks", json={},
                      content_type="application/json")
    assert res.status_code == 400

def test_task_no_existe(client):
    res = client.get("/tasks/9999")
    assert res.status_code == 404

def test_delete_task(client):
    res = client.delete("/tasks/1")
    assert res.status_code == 200
    assert res.get_json()["result"] == "Task deleted"