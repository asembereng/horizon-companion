"""
Chapter 3: Programming Fundamentals — Command-Line Task Creator

This is Horizon's first script: a CLI tool that lets you create,
list, and manage tasks from the terminal.

Usage:
    python -m horizon.cli
"""

import json
import os
from datetime import datetime

# ── In-memory task storage ──────────────────────────────────────
tasks: list[dict] = []
_next_id: int = 1


# ── Core Functions ──────────────────────────────────────────────

def validate_title(title: str) -> bool:
    """Validate that a task title is non-empty and under 200 characters.

    Chapter 3: Input validation — always verify before processing.

    Args:
        title: The proposed task title.

    Returns:
        True if valid, False otherwise.
    """
    if not title or not title.strip():
        return False
    if len(title) > 200:
        return False
    return True


def create_task(title: str, assignee: str, priority: int = 0) -> dict:
    """Create a new task and add it to the task list.

    Chapter 3: Functions should do one thing well.

    Args:
        title: The task title (1–200 characters).
        assignee: The person responsible for the task.
        priority: Task priority (0 = normal, higher = more urgent).

    Returns:
        The created task dictionary.

    Raises:
        ValueError: If title is empty or exceeds 200 characters.
    """
    global _next_id

    if not validate_title(title):
        raise ValueError(
            f"Title cannot be empty or exceed 200 characters. Got: '{title}'"
        )

    task = {
        "id": _next_id,
        "title": title.strip(),
        "assignee": assignee,
        "status": "to_do",
        "priority": priority,
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(task)
    _next_id += 1
    return task


def list_tasks(status: str | None = None) -> list[dict]:
    """Return all tasks, optionally filtered by status.

    Args:
        status: Filter by status ('to_do', 'in_progress', 'complete').
                None returns all tasks.

    Returns:
        List of matching task dictionaries.
    """
    if status is None:
        return list(tasks)
    return [t for t in tasks if t["status"] == status]


def update_status(task_id: int, new_status: str) -> dict:
    """Update a task's status.

    Args:
        task_id: The ID of the task to update.
        new_status: The new status ('to_do', 'in_progress', 'complete').

    Returns:
        The updated task dictionary.

    Raises:
        ValueError: If the status is not valid.
        KeyError: If no task with the given ID exists.
    """
    valid_statuses = {"to_do", "in_progress", "complete"}
    if new_status not in valid_statuses:
        raise ValueError(
            f"Invalid status '{new_status}'. Must be one of: {valid_statuses}"
        )

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            return task

    raise KeyError(f"Task with id {task_id} not found")


def delete_task(task_id: int) -> dict:
    """Delete a task by ID.

    Args:
        task_id: The ID of the task to delete.

    Returns:
        The deleted task dictionary.

    Raises:
        KeyError: If no task with the given ID exists.
    """
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            return tasks.pop(i)
    raise KeyError(f"Task with id {task_id} not found")


def reset_tasks() -> None:
    """Clear all tasks and reset the ID counter. Used in tests."""
    global _next_id
    tasks.clear()
    _next_id = 1


# ── CLI Interface ───────────────────────────────────────────────

def print_tasks(task_list: list[dict]) -> None:
    """Pretty-print a list of tasks."""
    if not task_list:
        print("  No tasks found.")
        return
    for t in task_list:
        status_icon = {"to_do": "⬜", "in_progress": "🔷", "complete": "✅"}
        icon = status_icon.get(t["status"], "❓")
        print(f"  {icon} [{t['id']}] {t['title']} → {t['assignee']} "
              f"(priority: {t['priority']})")


def main():
    """Interactive CLI loop for Horizon task management."""
    print("=" * 50)
    print("  🏗️  HORIZON — Task Manager CLI")
    print("  Chapter 3: Your First Program")
    print("=" * 50)

    while True:
        print("\nCommands: [a]dd  [l]ist  [u]pdate  [d]elete  [q]uit")
        choice = input("→ ").strip().lower()

        if choice in ("q", "quit"):
            print("Goodbye! 👋")
            break

        elif choice in ("a", "add"):
            title = input("  Task title: ").strip()
            assignee = input("  Assignee: ").strip()
            priority = input("  Priority (0=normal): ").strip()
            try:
                task = create_task(
                    title, assignee, int(priority) if priority else 0
                )
                print(f"  ✅ Created task #{task['id']}: {task['title']}")
            except ValueError as e:
                print(f"  ❌ Error: {e}")

        elif choice in ("l", "list"):
            print_tasks(list_tasks())

        elif choice in ("u", "update"):
            try:
                tid = int(input("  Task ID: ").strip())
                status = input("  New status (to_do/in_progress/complete): ").strip()
                task = update_status(tid, status)
                print(f"  ✅ Task #{task['id']} → {task['status']}")
            except (ValueError, KeyError) as e:
                print(f"  ❌ Error: {e}")

        elif choice in ("d", "delete"):
            try:
                tid = int(input("  Task ID: ").strip())
                task = delete_task(tid)
                print(f"  🗑️  Deleted task #{task['id']}: {task['title']}")
            except KeyError as e:
                print(f"  ❌ Error: {e}")

        else:
            print("  Unknown command. Try again.")


if __name__ == "__main__":
    main()
