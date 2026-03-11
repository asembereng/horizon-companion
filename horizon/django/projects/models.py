"""
Projects app — Django ORM models.

Matches the SQL schema from Chapter 6 (projects table referenced via FK).
"""

from django.conf import settings
from django.db import models


class Project(models.Model):
    """A project that groups related tasks."""

    name = models.CharField(max_length=200)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="administered_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def open_tasks(self):
        """Return tasks that are not yet done (mirrors stdlib Project.open_tasks)."""
        return self.tasks.exclude(status="done")
