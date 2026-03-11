"""
Enterprise Celery tasks.

Chapter 6 (sec_02b_transactions.tex): async notification pattern —
the notification is enqueued OUTSIDE the database transaction.
"""

from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_task_notification(task_id: int, notify_user_id: int) -> None:
    """Send a notification when a task is completed."""
    logger.info(
        "Sending notification for task %d to user %d",
        task_id,
        notify_user_id,
    )


@shared_task
def generate_project_report(project_id: int) -> dict:
    """Generate an async project status report."""
    logger.info("Generating report for project %d", project_id)
    return {"project_id": project_id, "status": "generated"}
