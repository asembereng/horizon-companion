"""
Chapter 6: Data Modeling — Database Operations

SQLite-backed persistence for Horizon. Demonstrates:
- SQL schema creation (CREATE TABLE)
- Parameterised queries (no SQL injection)
- ORM-like repository pattern
"""

from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from .models import Task, TaskStatus, TaskPriority, User


# ── Schema ──────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT    NOT NULL UNIQUE,
    email       TEXT    NOT NULL,
    full_name   TEXT    DEFAULT '',
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    DEFAULT '',
    owner_id    INTEGER REFERENCES users(id),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    status      TEXT    NOT NULL DEFAULT 'to_do',
    priority    INTEGER NOT NULL DEFAULT 1,
    assignee_id INTEGER NOT NULL REFERENCES users(id),
    project_id  INTEGER REFERENCES projects(id),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""


# ── Database Connection ─────────────────────────────────────────

class Database:
    """Manages SQLite database connections and schema.

    Usage:
        db = Database(":memory:")  # or "horizon.db" for persistent storage
        db.initialize()
    """

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._conn: sqlite3.Connection | None = None

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create the database connection.

        For :memory: databases, we reuse the same connection
        (each new connection creates a separate empty database).
        """
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def initialize(self) -> None:
        """Create tables if they don't exist."""
        conn = self._get_connection()
        conn.executescript(SCHEMA)
        conn.commit()

    @contextmanager
    def connection(self):
        """Context manager for database connections.

        Chapter 11: Resource management — always close connections.
        For in-memory databases, we reuse the connection.
        For file databases, we create a new one each time.
        """
        if self.db_path == ":memory:":
            yield self._get_connection()
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()


# ── SQLite Task Repository ──────────────────────────────────────

class SQLiteTaskRepository:
    """Concrete TaskRepository backed by SQLite.

    Chapter 5 (DIP): This implements the same interface as
    InMemoryTaskRepository — TaskService doesn't know the difference.

    Chapter 10: All queries use parameterised inputs to prevent
    SQL injection.
    """

    def __init__(self, db: Database):
        self._db = db

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """Convert a database row to a Task object."""
        user = User(
            id=row["assignee_id"],
            username=f"user_{row['assignee_id']}",
            email=f"user_{row['assignee_id']}@horizon.app",
        )
        return Task(
            id=row["id"],
            title=row["title"],
            status=TaskStatus(row["status"]),
            priority=TaskPriority(row["priority"]),
            assignee=user,
            project_id=row["project_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def save(self, task: Task) -> Task:
        """Insert or update a task."""
        with self._db.connection() as conn:
            if task.id == 0:
                cursor = conn.execute(
                    """INSERT INTO tasks (title, status, priority,
                       assignee_id, project_id)
                       VALUES (?, ?, ?, ?, ?)""",
                    (task.title, task.status.value, task.priority.value,
                     task.assignee.id, task.project_id),
                )
                task.id = cursor.lastrowid
            else:
                conn.execute(
                    """UPDATE tasks SET title=?, status=?, priority=?,
                       assignee_id=?, project_id=? WHERE id=?""",
                    (task.title, task.status.value, task.priority.value,
                     task.assignee.id, task.project_id, task.id),
                )
        return task

    def find_by_id(self, task_id: int) -> Task | None:
        """Find a task by ID using a parameterised query."""
        with self._db.connection() as conn:
            row = conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            return self._row_to_task(row) if row else None

    def find_all(self, status: TaskStatus | None = None) -> list[Task]:
        """Return all tasks, optionally filtered. Ordered by priority DESC."""
        with self._db.connection() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM tasks WHERE status = ? ORDER BY priority DESC",
                    (status.value,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM tasks ORDER BY priority DESC"
                ).fetchall()
            return [self._row_to_task(r) for r in rows]

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID."""
        with self._db.connection() as conn:
            cursor = conn.execute(
                "DELETE FROM tasks WHERE id = ?", (task_id,)
            )
            return cursor.rowcount > 0
