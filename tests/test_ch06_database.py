"""Tests for Chapter 6: Database Operations"""
import pytest
from horizon.models import User, Task, TaskStatus, TaskPriority
from horizon.database import Database, SQLiteTaskRepository


@pytest.fixture
def db():
    database = Database(":memory:")
    database.initialize()
    return database


@pytest.fixture
def repo(db):
    return SQLiteTaskRepository(db)


@pytest.fixture
def amara():
    return User(id=1, username="amara", email="amara@horizon.app")


@pytest.fixture
def seeded_db(db):
    """Insert a test user into the database."""
    with db.connection() as conn:
        conn.execute(
            "INSERT INTO users (id, username, email) VALUES (?, ?, ?)",
            (1, "amara", "amara@horizon.app"),
        )
    return db


class TestDatabase:
    def test_initialize_creates_tables(self, db):
        with db.connection() as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            names = [t["name"] for t in tables]
        assert "tasks" in names
        assert "users" in names
        assert "projects" in names


class TestSQLiteTaskRepository:
    def test_save_assigns_id(self, repo, amara):
        task = Task(id=0, title="Fix bug", assignee=amara)
        saved = repo.save(task)
        assert saved.id > 0

    def test_find_by_id(self, repo, amara):
        task = Task(id=0, title="Fix bug", assignee=amara)
        saved = repo.save(task)
        found = repo.find_by_id(saved.id)
        assert found is not None
        assert found.title == "Fix bug"

    def test_find_by_id_returns_none(self, repo):
        assert repo.find_by_id(999) is None

    def test_find_all(self, repo, amara):
        repo.save(Task(id=0, title="A", assignee=amara))
        repo.save(Task(id=0, title="B", assignee=amara))
        all_tasks = repo.find_all()
        assert len(all_tasks) == 2

    def test_find_all_filters_by_status(self, repo, amara):
        repo.save(Task(id=0, title="A", assignee=amara, status=TaskStatus.TO_DO))
        repo.save(Task(id=0, title="B", assignee=amara, status=TaskStatus.COMPLETE))
        todo = repo.find_all(status=TaskStatus.TO_DO)
        assert len(todo) == 1
        assert todo[0].title == "A"

    def test_delete(self, repo, amara):
        task = repo.save(Task(id=0, title="A", assignee=amara))
        assert repo.delete(task.id) is True
        assert repo.find_by_id(task.id) is None

    def test_delete_nonexistent(self, repo):
        assert repo.delete(999) is False

    def test_update_existing(self, repo, amara):
        task = repo.save(Task(id=0, title="A", assignee=amara))
        task.title = "Updated"
        repo.save(task)
        found = repo.find_by_id(task.id)
        assert found.title == "Updated"
