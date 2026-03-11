"""
Tasks app — Django ORM models.

Matches the SQL schema from Chapter 6 (sec_02_relational_databases.tex)
and the serializer field list from Chapter 18 (bridge section).
"""

from django.conf import settings
from django.db import models


class Task(models.Model):
    """A unit of work within a project."""

    class Status(models.TextChoices):
        TO_DO = "to_do", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TO_DO,
    )
    priority = models.IntegerField(default=0)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-priority", "created_at"]

    def __str__(self):
        return self.title

    def complete(self):
        """Mark this task as done (mirrors stdlib Task.complete)."""
        self.status = self.Status.DONE
        self.save()
