"""
Task API tests.

Chapter 24 (QA Agent): robust behavioural tests vs. fragile mock-based tests.
"""

import pytest
from tasks.models import Task


@pytest.mark.django_db
class TestTaskCreation:
    """Tests from Chapter 24 sec_03_quality_analysis.tex."""

    def test_create_task_persists_to_database(self, test_user, project):
        Task.objects.create(
            title="Write tests",
            project=project,
            assignee=test_user,
        )
        assert Task.objects.filter(title="Write tests").exists()
        task = Task.objects.get(title="Write tests")
        assert task.status == "to_do"
        assert task.project == project
        assert task.assignee == test_user

    def test_complete_task(self, task):
        task.complete()
        task.refresh_from_db()
        assert task.status == "done"


@pytest.mark.django_db
class TestTaskAPI:

    def test_list_tasks_requires_auth(self, api_client):
        response = api_client.get("/api/tasks/")
        assert response.status_code == 401

    def test_list_tasks(self, auth_client, task):
        response = auth_client.get("/api/tasks/")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_create_task(self, auth_client, project):
        response = auth_client.post("/api/tasks/", {
            "title": "New task",
            "project": project.id,
        })
        assert response.status_code == 201
        assert Task.objects.filter(title="New task").exists()

    def test_filter_by_status(self, auth_client, task):
        response = auth_client.get("/api/tasks/?status=to_do")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_filter_by_assignee(self, auth_client, task, test_user):
        response = auth_client.get(f"/api/tasks/?assignee={test_user.id}")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
