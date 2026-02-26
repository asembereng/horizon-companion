"""Tests for Chapter 7: REST API"""
import json
import threading
import urllib.request
import pytest
from horizon.api import create_app


@pytest.fixture
def server():
    """Start the API server on a random port in a background thread."""
    srv = create_app(host="localhost", port=0)
    _, port = srv.server_address
    thread = threading.Thread(target=srv.serve_forever)
    thread.daemon = True
    thread.start()
    yield f"http://localhost:{port}"
    srv.shutdown()


def _get(url: str) -> tuple[int, dict | list]:
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def _post(url: str, data: dict) -> tuple[int, dict]:
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


class TestHealthEndpoint:
    def test_health_check(self, server):
        status, body = _get(f"{server}/health")
        assert status == 200
        assert body["status"] == "ok"


class TestTasksAPI:
    def test_list_tasks_empty(self, server):
        status, body = _get(f"{server}/tasks")
        assert status == 200
        assert body == []

    def test_create_and_list_task(self, server):
        # Create
        status, created = _post(
            f"{server}/tasks",
            {"title": "Fix bug", "assignee": "Amara"},
        )
        assert status == 201
        assert created["title"] == "Fix bug"

        # List
        status, tasks = _get(f"{server}/tasks")
        assert status == 200
        assert len(tasks) == 1

    def test_create_task_empty_title_rejected(self, server):
        status, body = _post(
            f"{server}/tasks",
            {"title": "", "assignee": "Amara"},
        )
        assert status == 400

    def test_get_task_by_id(self, server):
        _post(f"{server}/tasks", {"title": "Task", "assignee": "Amara"})
        status, body = _get(f"{server}/tasks/1")
        assert status == 200
        assert body["title"] == "Task"

    def test_get_missing_task(self, server):
        status, body = _get(f"{server}/tasks/999")
        assert status == 404

    def test_not_found_route(self, server):
        status, body = _get(f"{server}/nonexistent")
        assert status == 404
