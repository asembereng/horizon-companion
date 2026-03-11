"""
Chapter 5: Design Principles — Service Layer

Services coordinate domain operations. Each service has a single
responsibility and depends on abstractions (protocols), not concrete
implementations.
"""

from __future__ import annotations
from .models import (
    Task, TaskStatus, TaskPriority, User,
    TaskRepository, NotificationService,
)


# ── In-Memory Repository (Chapter 5: OCP + DIP) ────────────────

class InMemoryTaskRepository:
    """Concrete implementation of TaskRepository using an in-memory list.

    Chapter 5 (OCP): Adding a PostgresTaskRepository requires zero
    changes to this class or to TaskService.
    """

    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def save(self, task: Task) -> Task:
        """Save a task. If it has no ID, assign one."""
        if task.id == 0:
            task.id = self._next_id
            self._next_id += 1
            self._tasks.append(task)
        else:
            # Update existing
            for i, t in enumerate(self._tasks):
                if t.id == task.id:
                    self._tasks[i] = task
                    return task
            self._tasks.append(task)
        return task

    def find_by_id(self, task_id: int) -> Task | None:
        """Find a task by its ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def find_all(self, status: TaskStatus | None = None) -> list[Task]:
        """Return all tasks, optionally filtered by status."""
        if status is None:
            return list(self._tasks)
        return [t for t in self._tasks if t.status == status]

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if found and deleted."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False


# ── Console Notification (Chapter 5: ISP) ───────────────────────

class ConsoleNotificationService:
    """Sends notifications to the console.

    Chapter 5 (LSP): This can be swapped for EmailNotificationService
    or SlackNotificationService without changing TaskService.
    """

    def __init__(self):
        self.sent: list[dict] = []  # Track for testing

    def notify(self, user: User, message: str) -> None:
        """Print a notification and record it."""
        record = {"user": user.username, "message": message}
        self.sent.append(record)
        print(f"📬 [{user.username}] {message}")


# ── Task Service (Chapter 5: SRP) ──────────────────────────────

class TaskService:
    """Coordinates task operations.

    Chapter 5 (SRP): This service handles task CRUD logic.
    It does NOT handle storage (repository) or notifications (service).

    Chapter 5 (DIP): Depends on abstractions (TaskRepository,
    NotificationService), not concrete implementations.
    """

    def __init__(
        self,
        repo: TaskRepository,
        notifier: NotificationService | None = None,
    ):
        self._repo = repo
        self._notifier = notifier

    def create_task(
        self,
        title: str,
        assignee: User,
        priority: TaskPriority = TaskPriority.NORMAL,
        project_id: int | None = None,
    ) -> Task:
        """Create and save a new task.

        Args:
            title: Task title (1–200 characters).
            assignee: The user responsible.
            priority: Task priority level.
            project_id: Optional project association.

        Returns:
            The saved task.

        Raises:
            ValueError: If title is invalid.
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        if len(title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")

        task = Task(
            id=0,  # Will be assigned by repository
            title=title.strip(),
            assignee=assignee,
            priority=priority,
            status=TaskStatus.TO_DO,
            project_id=project_id,
        )
        saved = self._repo.save(task)

        if self._notifier:
            self._notifier.notify(
                assignee, f"New task assigned: {saved.title}"
            )

        return saved

    def update_status(self, task_id: int, new_status: TaskStatus) -> Task:
        """Update a task's status.

        Raises:
            KeyError: If no task with the given ID exists.
        """
        task = self._repo.find_by_id(task_id)
        if task is None:
            raise KeyError(f"Task with id {task_id} not found")

        task.status = new_status
        return self._repo.save(task)

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve a single task by ID."""
        return self._repo.find_by_id(task_id)

    def list_tasks(self, status: TaskStatus | None = None) -> list[Task]:
        """List all tasks, optionally filtered by status."""
        return self._repo.find_all(status)

    def delete_task(self, task_id: int, requesting_user: User) -> bool:
        """Delete a task if the requesting user has permission.

        Chapter 10: Authorization check before destructive action.

        Raises:
            KeyError: If the task doesn't exist.
            PermissionError: If the user isn't the assignee.
        """
        task = self._repo.find_by_id(task_id)
        if task is None:
            raise KeyError(f"Task with id {task_id} not found")

        if not task.can_be_deleted_by(requesting_user):
            raise PermissionError(
                f"User {requesting_user.username} cannot delete task #{task_id}"
            )

        return self._repo.delete(task_id)
