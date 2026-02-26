"""
Chapter 11: Error Handling — Structured Logging Configuration

JSON-formatted logging for Horizon. Structured logs are machine-readable
and enable observability tools (Datadog, Grafana, ELK) to parse them.
"""

import logging
import json
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for machine consumption.

    Chapter 11: Structured logging replaces `print()` debugging.
    Every log entry has: timestamp, level, message, and context.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Include exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }

        # Include extra fields if provided
        for key in ("user_id", "task_id", "action", "request_id"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        return json.dumps(log_entry)


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure structured JSON logging for Horizon.

    Usage:
        logger = setup_logging("DEBUG")
        logger.info("Task created", extra={"task_id": 42, "action": "create"})

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("horizon")
    logger.setLevel(getattr(logging, level.upper()))

    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger
