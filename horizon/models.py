"""
Chapters 4–5: Clean Code & Design Principles — Domain Models

SOLID-compliant domain models for Horizon.
Each class has a single responsibility and depends on abstractions.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Protocol


# ── Enums ───────────────────────────────────────────────────────

class TaskStatus(Enum):
    """Valid task states. Chapter 4: Use enums instead of magic strings."""
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


# ── Domain Models ───────────────────────────────────────────────

@dataclass
class User:
    """A Horizon user.

    Chapter 5 (SRP): User only holds identity data.
    Authentication is handled by auth.py (separate responsibility).
    """
    id: int
    username: str
    email: str
    full_name: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def display_name(self) -> str:
        """Return the best available display name."""
        return self.full_name if self.full_name else self.username


@dataclass
class Task:
    """A Horizon task.

    Chapter 5 (SRP): Task holds task data.
    Persistence is handled by database.py (separate responsibility).
    Notifications are handled by services.py (separate responsibility).
    """
    id: int
    title: str
    assignee: User
    status: TaskStatus = TaskStatus.TO_DO
    priority: TaskPriority = TaskPriority.NORMAL
    project_id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def is_overdue(self, deadline: datetime) -> bool:
        """Check if the task is past its deadline and not complete."""
        return (
            self.status != TaskStatus.COMPLETE
            and datetime.now() > deadline
        )

    def can_be_deleted_by(self, user: User) -> bool:
        """Only the assignee can delete a task.

        Chapter 10: Authorization logic belongs on the domain model.
        """
        return user.id == self.assignee.id


@dataclass
class Project:
    """A Horizon project — a collection of tasks."""
    id: int
    name: str
    description: str = ""
    owner: User | None = None
    created_at: datetime = field(default_factory=datetime.now)


# ── Protocols (Chapter 5: Dependency Inversion) ─────────────────

class TaskRepository(Protocol):
    """Abstract interface for task storage.

    Chapter 5 (DIP): High-level services depend on this protocol,
    not on a concrete database implementation.
    """
    def save(self, task: Task) -> Task: ...
    def find_by_id(self, task_id: int) -> Task | None: ...
    def find_all(self, status: TaskStatus | None = None) -> list[Task]: ...
    def delete(self, task_id: int) -> bool: ...


class NotificationService(Protocol):
    """Abstract interface for notifications.

    Chapter 5 (ISP): Small, focused interface — just one method.
    """
    def notify(self, user: User, message: str) -> None: ...
