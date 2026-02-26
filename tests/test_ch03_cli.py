"""Tests for Chapter 3: CLI Task Creator"""
import pytest
from horizon.cli import (
    create_task, validate_title, list_tasks,
    update_status, delete_task, reset_tasks, tasks,
)


@pytest.fixture(autouse=True)
def clean_tasks():
    """Reset task state before each test."""
    reset_tasks()
    yield
    reset_tasks()


# ── validate_title ──────────────────────────────────────────────

class TestValidateTitle:
    def test_rejects_empty_string(self):
        assert validate_title("") is False

    def test_rejects_whitespace_only(self):
        assert validate_title("   ") is False

    def test_rejects_too_long(self):
        assert validate_title("x" * 201) is False

    def test_accepts_valid_title(self):
        assert validate_title("Fix login bug") is True

    def test_accepts_exactly_200_chars(self):
        assert validate_title("x" * 200) is True


# ── create_task ─────────────────────────────────────────────────

class TestCreateTask:
    def test_returns_dict_with_required_fields(self):
        task = create_task("Fix bug", "Amara")
        assert isinstance(task, dict)
        assert task["title"] == "Fix bug"
        assert task["assignee"] == "Amara"
        assert task["status"] == "to_do"

    def test_assigns_incrementing_ids(self):
        t1 = create_task("Task A", "Amara")
        t2 = create_task("Task B", "Ben")
        assert t1["id"] == 1
        assert t2["id"] == 2

    def test_strips_whitespace_from_title(self):
        task = create_task("  Deploy v2  ", "Carol")
        assert task["title"] == "Deploy v2"

    def test_raises_on_empty_title(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            create_task("", "Amara")

    def test_raises_on_too_long_title(self):
        with pytest.raises(ValueError):
            create_task("x" * 201, "Amara")

    def test_default_priority_is_zero(self):
        task = create_task("Task", "Amara")
        assert task["priority"] == 0

    def test_custom_priority(self):
        task = create_task("Urgent task", "Amara", priority=3)
        assert task["priority"] == 3

    def test_includes_created_at(self):
        task = create_task("Task", "Amara")
        assert "created_at" in task


# ── list_tasks ──────────────────────────────────────────────────

class TestListTasks:
    def test_returns_empty_list_initially(self):
        assert list_tasks() == []

    def test_returns_all_tasks(self):
        create_task("A", "Amara")
        create_task("B", "Ben")
        assert len(list_tasks()) == 2

    def test_filters_by_status(self):
        create_task("A", "Amara")
        t2 = create_task("B", "Ben")
        update_status(t2["id"], "complete")
        assert len(list_tasks(status="complete")) == 1
        assert len(list_tasks(status="to_do")) == 1


# ── update_status ───────────────────────────────────────────────

class TestUpdateStatus:
    def test_updates_status(self):
        task = create_task("Task", "Amara")
        updated = update_status(task["id"], "in_progress")
        assert updated["status"] == "in_progress"

    def test_raises_on_invalid_status(self):
        task = create_task("Task", "Amara")
        with pytest.raises(ValueError, match="Invalid status"):
            update_status(task["id"], "banana")

    def test_raises_on_missing_task(self):
        with pytest.raises(KeyError):
            update_status(999, "complete")


# ── delete_task ─────────────────────────────────────────────────

class TestDeleteTask:
    def test_deletes_existing_task(self):
        task = create_task("Task", "Amara")
        deleted = delete_task(task["id"])
        assert deleted["id"] == task["id"]
        assert len(tasks) == 0

    def test_raises_on_missing_task(self):
        with pytest.raises(KeyError):
            delete_task(999)
