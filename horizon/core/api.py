"""
Chapter 7: APIs — REST API for Horizon

A lightweight REST-like API using Python's built-in http.server.
No external frameworks required — demonstrates HTTP concepts directly.
"""

from __future__ import annotations
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from .models import User, TaskPriority
from .services import TaskService, InMemoryTaskRepository


class HorizonAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the Horizon API.

    Chapter 7: RESTful conventions:
    - GET    /tasks       → List tasks
    - GET    /tasks/1     → Get task by ID
    - POST   /tasks       → Create a task
    - DELETE /tasks/1     → Delete a task
    - GET    /health      → Health check
    """

    # Shared service instance (set by create_app)
    service: TaskService = None  # type: ignore
    default_user: User = None  # type: ignore

    def _send_json(self, status: int, data: dict | list) -> None:
        """Send a JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def _read_body(self) -> dict:
        """Read and parse the JSON request body."""
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length).decode()
        return json.loads(body)

    def do_GET(self) -> None:
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/health":
            self._send_json(200, {"status": "ok", "service": "horizon"})
            return

        if path == "/tasks":
            query = parse_qs(parsed.query)
            status_filter = query.get("status", [None])[0]
            tasks = self.service.list_tasks()
            task_dicts = [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status.value,
                    "priority": t.priority.value,
                    "assignee": t.assignee.username,
                    "project_id": t.project_id,
                    "created_at": str(t.created_at),
                }
                for t in tasks
            ]
            self._send_json(200, task_dicts)
            return

        # GET /tasks/<id>
        if path.startswith("/tasks/"):
            try:
                task_id = int(path.split("/")[-1])
                task = self.service.get_task(task_id)
                if task is None:
                    self._send_json(404, {"detail": "Not found"})
                    return
                self._send_json(200, {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status.value,
                    "priority": task.priority.value,
                    "assignee": task.assignee.username,
                })
            except ValueError:
                self._send_json(400, {"detail": "Invalid task ID"})
            return

        self._send_json(404, {"detail": "Not found"})

    def do_POST(self) -> None:
        """Handle POST requests."""
        path = urlparse(self.path).path.rstrip("/")

        if path == "/tasks":
            try:
                body = self._read_body()
                title = body.get("title", "")
                assignee_name = body.get("assignee", "")
                priority = body.get("priority", 1)

                user = User(
                    id=self.default_user.id,
                    username=assignee_name or self.default_user.username,
                    email=self.default_user.email,
                )
                task = self.service.create_task(
                    title=title,
                    assignee=user,
                    priority=TaskPriority(priority),
                )
                self._send_json(201, {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status.value,
                    "assignee": task.assignee.username,
                })
            except (ValueError, KeyError) as e:
                self._send_json(400, {"detail": str(e)})
            return

        self._send_json(404, {"detail": "Not found"})

    def do_DELETE(self) -> None:
        """Handle DELETE requests."""
        path = urlparse(self.path).path.rstrip("/")

        if path.startswith("/tasks/"):
            try:
                task_id = int(path.split("/")[-1])
                deleted = self.service.delete_task(
                    task_id, self.default_user
                )
                if deleted:
                    self._send_json(204, {})
                else:
                    self._send_json(404, {"detail": "Not found"})
            except KeyError:
                self._send_json(404, {"detail": "Not found"})
            except PermissionError as e:
                self._send_json(403, {"detail": str(e)})
            return

        self._send_json(404, {"detail": "Not found"})

    def log_message(self, format, *args):
        """Suppress default logging to keep test output clean."""
        pass


def create_app(
    host: str = "localhost",
    port: int = 8000,
) -> HTTPServer:
    """Create and configure the Horizon API server.

    Args:
        host: Server hostname.
        port: Server port.

    Returns:
        Configured HTTPServer instance.
    """
    repo = InMemoryTaskRepository()
    default_user = User(id=1, username="admin", email="admin@horizon.app")

    HorizonAPIHandler.service = TaskService(repo=repo)
    HorizonAPIHandler.default_user = default_user

    server = HTTPServer((host, port), HorizonAPIHandler)
    return server


if __name__ == "__main__":
    print("🏗️  Horizon API starting on http://localhost:8000")
    print("   GET  /health  → Health check")
    print("   GET  /tasks   → List tasks")
    print("   POST /tasks   → Create task")
    print("   Press Ctrl+C to stop")
    server = create_app()
    server.serve_forever()
