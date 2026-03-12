import structlog
import logging
import sys

def configure_logging():
    """Configure structlog for JSON logging to stdout."""
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(*args):
    """Get a structlog logger instance."""
    return structlog.get_logger(*args)
