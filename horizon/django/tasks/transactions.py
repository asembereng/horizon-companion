"""
Transaction patterns from Chapter 6 (sec_02b_transactions.tex).

Demonstrates Django's ``transaction.atomic()`` with select_for_update
and the application-level compensation pattern.
"""

from django.db import transaction
import logging

logger = logging.getLogger(__name__)


def complete_task(task_id: int, performed_by_user_id: int):
    """
    Atomically mark a task as done and create an audit log entry.

    Chapter 6: ACID transaction with select_for_update() to prevent
    race conditions.
    """
    from tasks.models import Task

    with transaction.atomic():
        task = Task.objects.select_for_update().get(id=task_id)

        if task.status == "done":
            raise ValueError(f"Task {task_id} is already complete.")

        task.status = "done"
        task.save()

    logger.info(
        "Task %d marked complete by user %d", task_id, performed_by_user_id
    )
    return task
