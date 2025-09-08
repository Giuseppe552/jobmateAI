"""
Structured logging setup using structlog for FastAPI.
Logs in JSON format and includes request_id, path, method, status_code.
"""
import structlog
from typing import Any


def get_logger() -> structlog.BoundLogger:
    """Returns a structlog logger instance."""
    logger = structlog.get_logger()
    return logger


def setup_logging():
    import logging
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(level=logging.INFO)
