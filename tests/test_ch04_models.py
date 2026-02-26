"""Tests for Chapters 4–5: Domain Models"""
import pytest
from datetime import datetime, timedelta
from horizon.models import User, Task, TaskStatus, TaskPriority


@pytest.fixture
def amara():
    return User(id=1, username="amara", email="amara@horizon.app", full_name="Amara Osei")


@pytest.fixture
def ben():
    return User(id=2, username="ben", email="ben@horizon.app")


@pytest.fixture
def sample_task(amara):
    return Task(id=1, title="Fix login bug", assignee=amara)


class TestUser:
    def test_display_name_uses_full_name(self, amara):
        assert amara.display_name() == "Amara Osei"

    def test_display_name_falls_back_to_username(self, ben):
        assert ben.display_name() == "ben"


class TestTask:
    def test_default_status_is_to_do(self, sample_task):
        assert sample_task.status == TaskStatus.TO_DO

    def test_default_priority_is_normal(self, sample_task):
        assert sample_task.priority == TaskPriority.NORMAL

    def test_is_overdue_when_past_deadline(self, sample_task):
        past = datetime.now() - timedelta(days=1)
        assert sample_task.is_overdue(past) is True

    def test_not_overdue_when_complete(self, sample_task):
        sample_task.status = TaskStatus.COMPLETE
        past = datetime.now() - timedelta(days=1)
        assert sample_task.is_overdue(past) is False

    def test_not_overdue_when_future_deadline(self, sample_task):
        future = datetime.now() + timedelta(days=1)
        assert sample_task.is_overdue(future) is False

    def test_can_be_deleted_by_assignee(self, sample_task, amara):
        assert sample_task.can_be_deleted_by(amara) is True

    def test_cannot_be_deleted_by_other_user(self, sample_task, ben):
        assert sample_task.can_be_deleted_by(ben) is False


class TestTaskStatus:
    def test_all_statuses_exist(self):
        assert TaskStatus.TO_DO.value == "to_do"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETE.value == "complete"
