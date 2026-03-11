"""
Django test configuration.

Chapter 24 (QA Agent): pytest-django test setup.
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="amara",
        email="amara@horizon.dev",
        password="testpass123",
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@horizon.dev",
        password="adminpass123",
    )


@pytest.fixture
def project(db, test_user):
    from projects.models import Project
    return Project.objects.create(name="Horizon v1", admin=test_user)


@pytest.fixture
def task(db, test_user, project):
    from tasks.models import Task
    return Task.objects.create(
        title="Fix login bug",
        assignee=test_user,
        project=project,
    )


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client
