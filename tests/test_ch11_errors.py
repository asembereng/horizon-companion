"""Tests for Chapter 11: Error Handling"""
import json
import pytest
from horizon.exceptions import (
    HorizonError, ValidationError, NotFoundError,
    AuthenticationError, AuthorizationError,
)
from horizon.logging_config import setup_logging, JSONFormatter


class TestExceptionHierarchy:
    def test_all_exceptions_inherit_from_horizon_error(self):
        assert issubclass(ValidationError, HorizonError)
        assert issubclass(NotFoundError, HorizonError)
        assert issubclass(AuthenticationError, HorizonError)
        assert issubclass(AuthorizationError, HorizonError)

    def test_validation_error_includes_field(self):
        err = ValidationError("title", "cannot be empty")
        assert err.field == "title"
        assert "title" in str(err)
        assert err.code == "VALIDATION_ERROR"

    def test_not_found_error(self):
        err = NotFoundError("Task", 42)
        assert err.resource == "Task"
        assert err.identifier == 42
        assert "42" in str(err)

    def test_auth_error(self):
        err = AuthenticationError("Bad credentials")
        assert err.code == "AUTH_ERROR"

    def test_authorization_error(self):
        err = AuthorizationError("delete", "Task #5")
        assert "delete" in str(err)
        assert err.code == "FORBIDDEN"

    def test_catch_all_horizon_errors(self):
        """Verify that catching HorizonError catches all subtypes."""
        errors = [
            ValidationError("f", "m"),
            NotFoundError("T", 1),
            AuthenticationError(),
            AuthorizationError("a", "r"),
        ]
        for err in errors:
            with pytest.raises(HorizonError):
                raise err


class TestJSONLogging:
    def test_logger_produces_json(self, capsys):
        logger = setup_logging("DEBUG")
        # Clear handlers to avoid duplicates
        logger.handlers.clear()
        import logging
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

        logger.info("Task created", extra={"task_id": 42, "action": "create"})
        output = capsys.readouterr().err
        log_entry = json.loads(output.strip())
        assert log_entry["message"] == "Task created"
        assert log_entry["task_id"] == 42
        assert log_entry["level"] == "INFO"
