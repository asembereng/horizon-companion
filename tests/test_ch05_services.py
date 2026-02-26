"""Tests for Chapter 5: Service Layer"""
import pytest
from horizon.models import User, TaskStatus, TaskPriority
from horizon.services import TaskService, InMemoryTaskRepository, ConsoleNotificationService


@pytest.fixture
def amara():
    return User(id=1, username="amara", email="amara@horizon.app")


@pytest.fixture
def ben():
    return User(id=2, username="ben", email="ben@horizon.app")


@pytest.fixture
def repo():
    return InMemoryTaskRepository()


@pytest.fixture
def notifier():
    return ConsoleNotificationService()


@pytest.fixture
def service(repo, notifier):
    return TaskService(repo=repo, notifier=notifier)


class TestTaskService:
    def test_create_task(self, service, amara):
        task = service.create_task("Fix bug", amara)
        assert task.id == 1
        assert task.title == "Fix bug"
        assert task.assignee.username == "amara"

    def test_create_task_sends_notification(self, service, amara, notifier):
        service.create_task("Fix bug", amara)
        assert len(notifier.sent) == 1
        assert "Fix bug" in notifier.sent[0]["message"]

    def test_create_task_rejects_empty_title(self, service, amara):
        with pytest.raises(ValueError):
            service.create_task("", amara)

    def test_create_task_rejects_long_title(self, service, amara):
        with pytest.raises(ValueError):
            service.create_task("x" * 201, amara)

    def test_list_tasks_returns_all(self, service, amara):
        service.create_task("Task A", amara)
        service.create_task("Task B", amara)
        assert len(service.list_tasks()) == 2

    def test_list_tasks_filters_by_status(self, service, amara):
        service.create_task("Task A", amara)
        t2 = service.create_task("Task B", amara)
        service.update_status(t2.id, TaskStatus.COMPLETE)
        assert len(service.list_tasks(status=TaskStatus.TO_DO)) == 1
        assert len(service.list_tasks(status=TaskStatus.COMPLETE)) == 1

    def test_update_status(self, service, amara):
        task = service.create_task("Task", amara)
        updated = service.update_status(task.id, TaskStatus.IN_PROGRESS)
        assert updated.status == TaskStatus.IN_PROGRESS

    def test_update_status_missing_task(self, service):
        with pytest.raises(KeyError):
            service.update_status(999, TaskStatus.COMPLETE)

    def test_delete_task_by_assignee(self, service, amara):
        task = service.create_task("Task", amara)
        assert service.delete_task(task.id, amara) is True

    def test_delete_task_unauthorized(self, service, amara, ben):
        task = service.create_task("Task", amara)
        with pytest.raises(PermissionError):
            service.delete_task(task.id, ben)

    def test_delete_missing_task(self, service, amara):
        with pytest.raises(KeyError):
            service.delete_task(999, amara)

    def test_get_task(self, service, amara):
        task = service.create_task("Task", amara)
        found = service.get_task(task.id)
        assert found is not None
        assert found.title == "Task"

    def test_get_missing_task_returns_none(self, service):
        assert service.get_task(999) is None
